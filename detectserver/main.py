import asyncio
from logging import log
import os
import json
from av import VideoFrame
import redis
from fastapi_utils.tasks import repeat_every
from datetime import datetime

#from imageai.Detection import VideoObjectDetection

from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription, RTCDataChannel
from aiortc.contrib.media import MediaPlayer, MediaRelay

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from src.schemas import Offer
from model import yolov5

# ROOT = os.path.dirname(__file__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class VideoTransformTrack(MediaStreamTrack):
    """
    A video stream track that transforms frames from an another track.
    """

    kind = "video"

    def __init__(self, track, channel, status):
        super().__init__()
        self.track = track
        self.channel = channel
        self.status = status

    async def recv(self):
        frame = await self.track.recv()
        img = frame.to_ndarray(format="bgr24")
        classes = None
        if self.status[0] == True:
            img, classes = yolov5(img)

        # rebuild a VideoFrame, preserving timing information
        if self.channel is not None and self.channel != [] and classes is not None:
            self.channel[0].send(json.dumps({"classes": classes}))
        new_frame = VideoFrame.from_ndarray(img, format="bgr24")
        new_frame.pts = frame.pts
        new_frame.time_base = frame.time_base
        return new_frame


@app.get("/check")
async def check():
    for pc in pcs:
        print(pc.connectionState)
    return []


@app.post("/offer_cv")
async def offer(params: Offer):

    offer = RTCSessionDescription(sdp=params.sdp, type=params.type)

    pc = RTCPeerConnection()

    print(pc)
    pcs.add(pc)

    relay = MediaRelay()

    ch = []
    status = [False]

    @pc.on('datachannel')
    def on_datachannel(channel):

        ch.append(channel)

        @channel.on('message')
        def on_message(message):
            status[0] = True if message == "True" else False
            # channel.send('pong')

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        print("Connection state is %s" % pc.connectionState)
        if pc.connectionState == "failed":
            await pc.close()
            pcs.discard(pc)

    @pc.on("track")
    def on_track(track):
        if track.kind == "video":
            pc.addTrack(
                VideoTransformTrack(relay.subscribe(
                    track), channel=ch, status=status)
            )

        @track.on("ended")
        async def on_ended():
            pass

    # handle offer
    await pc.setRemoteDescription(offer)

    # send answer
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)
    return {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}


pcs = set()


@app.on_event("startup")
async def on_start():
    # redis_client = redis.Redis(host='redis-10572.c292.ap-southeast-1-1.ec2.cloud.redislabs.com', port=10572, db=0, password='U8TgyN1jfInisvHn1P3d7LEYaKqZM5cg')
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    if redis_client.ping() == True:
        keys = [int(k) for k in redis_client.scan_iter() if k != b'users']
        keys.sort()
        vals = redis_client.execute_command('JSON.MGET', *keys, '.')
        items = [json.loads(val) for val in vals]
        with open('yolo/classes.txt', 'w+') as file:
            for item in items:
                file.writelines(f"{item['name']}: {item['price']}\n")
            file.writelines("Strange object: NaN")


@app.on_event("shutdown")
async def on_shutdown():
    # close peer connections
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()


@app.on_event("startup")
@repeat_every(seconds=3600, wait_first=True)
async def sync_update_label():
    now = datetime.now()
    if now.hour == 0:
        redis_client = redis.Redis(host='localhost', port=6379, db=0)
        if redis_client.ping() == True:
            keys = [int(k) for k in redis_client.scan_iter() if k != b'users']
            keys.sort()
            vals = redis_client.execute_command('JSON.MGET', *keys, '.')
            items = [json.loads(val) for val in vals]
            with open('yolo/classes.txt', 'w+') as file:
                for item in items:
                    file.writelines(f"{item['name']}: {item['price']}\n")
                file.writelines("Strange object: NaN")
