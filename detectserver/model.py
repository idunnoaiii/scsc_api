import cv2
import base64
import numpy as np
import logging
import time
import glob
import datetime

# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)


# logger.info("============================LOAD")

CONFIDENCE_THRESHOLD = 0.5
NMS_THRESHOLD = 0.5
COLORS = [(0, 255, 0), (0, 0, 255), (255, 0, 0),
          (255, 255, 0), (255, 0, 255), (0, 255, 255)]

weights = glob.glob("yolo/*.weights")[0]
labels = glob.glob("yolo/*.txt")[0]
cfg = glob.glob("yolo/*.cfg")[0]

class_names = []
with open('yolo/classes.txt', 'r') as f:
    class_names = [cname.strip() for cname in f.readlines()]

net = cv2.dnn.readNet('yolo/yolov4-custom_last.weights', 'yolo/yolov4-custom.cfg')
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)

def yolov5(image):
    try:
        # img = base64.b64decode(base64_img); 
        # npimg = np.fromstring(img, dtype=np.uint8); 
        # image = cv2.imdecode(npimg, 1)
        
        # width = image.shape[1]
        # height = image.shape[0]

        microsecond = datetime.datetime.now()
        start_time = time.time()
        classes, scores, boxes = model.detect(image, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
        end_time = time.time()
        # print("DETECT TIME", end_time-start_time)

        ret_classes = []

        for (classid, score, box) in zip(classes, scores, boxes):
            if int(classid[0]) != 15:
                ret_classes.append(int(classid[0]+1))
            (x, y) = (box[0], box[1])
            (w, h) = (box[2], box[3])
            # color = COLORS[int(classid) % len(COLORS)]
            label = "%s" % (class_names[classid[0]])
            label = label.split(": ")
            if int(classid[0]) != 15:
                color = (255, 0, 0)
            else:
                color = (0, 255, 0)
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            cv2.putText(image, label[0], (box[0]+4, box[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            cv2.putText(image, label[1], (box[0]+4, box[1] + 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        fps_label = "FPS: %.2f" % (1 / (end_time - start_time))
        print(fps_label)
        # cv2.putText(image, "", (0, 25),
        #     cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        return image, ret_classes if microsecond.microsecond >= 750000 else None

    except Exception as e:
        # logger.exception(e)
        return None, None