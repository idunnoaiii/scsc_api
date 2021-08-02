from typing import List
import cv2
import numpy as np
import base64

def base64_to_image(base64_img):
    try:
        base64_img = np.fromstring(base64.b64decode(base64_img), dtype=np.uint8)
        base64_img = cv2.imdecode(base64_img, cv2.IMREAD_ANYCOLOR)
    except:
        return None
    return base64_img
    

def get_output_layers(net):
    layer_names = net.getLayerNames()

    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers



def predict(base64_img):
    try:
        classes_fname: str = "classes.txt"
        weight_fname: str = "yolov3.backup"
        config_fname: str = "yolov3.cfg"
        img = base64.b64decode(base64_img); 
        npimg = np.fromstring(img, dtype=np.uint8); 
        image = cv2.imdecode(npimg, 1)

        Width = image.shape[1]
        Height = image.shape[0]
        print(Width, Height)
        scale = 0.00392

        classes = None

        with open(classes_fname, 'r') as f:
            classes = [line.strip() for line in f.readlines()]

        COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

        net = cv2.dnn.readNet(weight_fname, config_fname)

        net = cv2.dnn.readNetFromDarknet(config_fname, weight_fname)

        blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)

        net.setInput(blob)

        outs = net.forward(get_output_layers(net))

        class_ids = []
        confidences = []
        boxes = []
        positions = []
        boxes_positions = []
        conf_threshold = 0.35
        nms_threshold = 0.4


        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.35:
                    center_x = int(detection[0] * Width)
                    center_y = int(detection[1] * Height)
                    w = int(detection[2] * Width)
                    h = int(detection[3] * Height)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])
                    boxes_positions.append([detection[0] , detection[1] , detection[2], detection[3]])

        indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

        ret_classes = []

        for i in indices:
            i = i[0]
            box = boxes_positions[i]
            positions.append([int(class_ids[i]+1), float(box[0]), float(box[1]), float(box[2]), float(box[3]), float(confidences[i])])
            ret_classes.append(int(class_ids[i]+1))
            # draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x + w), round(y + h))
            
        return ret_classes, positions
    except:
        return None, None


def predict_2(base64_img):
    try:
        img = base64.b64decode(base64_img); 
        npimg = np.fromstring(img, dtype=np.uint8); 
        image = cv2.imdecode(npimg, 1)

        width = image.shape[1]
        height = image.shape[0]

        Conf_threshold = 0.5
        NMS_threshold = 0.5

        class_name = []
        with open('classes.txt', 'r') as f:
            class_name = [cname.strip() for cname in f.readlines()]

        net = cv2.dnn.readNet('yolov4-custom_last.weights', 'yolov4-custom.cfg')

        model = cv2.dnn_DetectionModel(net)
        model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)

        classes, scores, boxes = model.detect(image, Conf_threshold, NMS_threshold)

        ret_classes = []
        positions = []

        for (classid, score, box) in zip(classes, scores, boxes):
            ret_classes.append(int(class_name[classid[0]]))
            positions.append([int(class_name[classid[0]]), float((box[0]+box[2]/2)/width), float((box[1]+box[3]/2)/height), float(box[2]/width), float(box[3]/height), float(score)])


        return ret_classes, positions

    except Exception as e:
        return None, None