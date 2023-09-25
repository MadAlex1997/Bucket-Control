import cv2
import time
from datetime import datetime
import json


def record_video(cam, frames, duration, file_prefix, video_path):
    """
    Record video from camera cam, at frames frames per secon, for duration second
    store it as file_prefix_unixtimestamp.mp4 in the video_path format
    """
    now = datetime.now().timestamp()
    width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    writer = cv2.VideoWriter(f"{video_path}{file_prefix}_{now}.mp4",
                             fourcc=fourcc,
                             fps=frames,
                             frameSize=(width,height))
    
    for _ in range(frames*duration):
        ret, frame = cam.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            writer.write(frame)
            time.sleep(1/frames)
    
def video():
    with open("./sensor_info.json","r") as si:
        sidict = json.load(si)
        sensor_name = sidict["sensor_name"]
        video_path = sidict["video_path"]
        cam =  cv2.VideoCapture(0)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH,640)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH,480)
    while True:
        record_video(cam=cam,
                     frames=20,
                     duration=30,
                     file_prefix=sensor_name,
                     video_path=video_path
                     )
    
    