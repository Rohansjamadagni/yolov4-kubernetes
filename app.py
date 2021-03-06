import cv2
import numpy as np
import pymongo
import uvicorn
import yaml
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel

net = cv2.dnn_DetectionModel("cfg/yolov4.cfg", "yolov4.weights")
net.setInputSize(704, 704)
net.setInputScale(1.0 / 255)
net.setInputSwapRB(True)

with open("cfg/names.txt", "r") as f:
    names = [line.strip() for line in f.readlines()]
with open("mongo-config/config.yaml", "r") as stream:
    config = yaml.safe_load(stream)

myclient = pymongo.MongoClient(config["app"]["mongo-uri"])
mydb = myclient[config["app"]["db-name"]]
mydb = myclient[config["app"]["db-name"]]
mycol = mydb[config["app"]["col-name"]]

# Creating FastAPI instance
app = FastAPI()

# Creating class to define the request body
# and the type hints of each attribute


class request_body(BaseModel):
    text: str


@app.post("/files/")
async def create_file(file: bytes = File(...)):
    nparr = np.fromstring(file, np.uint8)
    frame = cv2.imdecode(nparr, flags=1)

    # Making the data in a form suitable for prediction
    result_string = {}

    classes, confidences, boxes = net.detect(frame, confThreshold=0.1, nmsThreshold=0.4)

    for classId, confidence, box in zip(classes, confidences, boxes):
        label = "%.2f" % confidence
        label = "%s: %s" % (names[classId], label)
        labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        left, top, width, height = box
        top = max(top, labelSize[1])
        result_string[names[classId]] = str(confidence)

    result = {"result": result_string}
    x = mycol.insert_one(result)
    return str(result)
