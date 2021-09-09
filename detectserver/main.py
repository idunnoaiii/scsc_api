import asyncio
from logging import log
import os
import cv2
import json
import multiprocessing

from av import VideoFrame

#from imageai.Detection import VideoObjectDetection

from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription, RTCDataChannel
from aiortc.contrib.media import MediaPlayer, MediaRelay, MediaBlackhole

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from src.schemas import Offer

from model import yolov5

ROOT = os.path.dirname(__file__)

app = FastAPI()


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class VideoTransformTrack(MediaStreamTrack):
    """
    A video stream track that transforms frames from an another track.
    """

    kind = "video"

    def __init__(self, track, channel):
        super().__init__()
        self.track = track
        self.channel = channel
        self.counters = 0

    async def recv(self):
        frame = await self.track.recv()
        # perform edge detection
        img = frame.to_ndarray(format="bgr24")
        # img = cv2.cvtColor(cv2.Canny(img, 100, 200), cv2.COLOR_GRAY2BGR)
        img, classes = yolov5(img)
        # if self.channel.readyState == 'open':
        #     print(self.channel.label)
        #     self.channel.send("HELLO FROM SERVER")
        # rebuild a VideoFrame, preserving timing information
        print("CLASSSSSSSSSSSSSSSSSSS", classes)
        print("PROCESSSSSSSSSSSSSSSSSS", multiprocessing.current_process())
        if self.channel is not None and self.channel != []:
            self.channel[0].send(json.dumps({"classes": classes}))
        new_frame = VideoFrame.from_ndarray(img, format="bgr24")
        new_frame.pts = frame.pts
        new_frame.time_base = frame.time_base
        return new_frame
    


@app.post("/offer_cv")
async def offer(params: Offer):


    offer = RTCSessionDescription(sdp=params.sdp, type=params.type)

    pc = RTCPeerConnection()
    print(pc)
    pcs.add(pc)

    relay = MediaRelay()

    ch = []

    @pc.on('datachannel')
    def on_datachannel(channel):

        ch.append(channel)
        
        @channel.on('message')
        def on_message(message):
            channel.send('pong')

    
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
                VideoTransformTrack(relay.subscribe(track), channel=ch)
            )
        
        @track.on("ended")
        async def on_ended():
            pass

    # handle offer
    await pc.setRemoteDescription(offer)

    # send answer
    answer = await pc.createAnswer()
    # await pc.setRemoteDescription(offer)
    await pc.setLocalDescription(answer)

    return {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}


pcs = set()
args = ''


@app.on_event("shutdown")
async def on_shutdown():
    # close peer connections
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()
