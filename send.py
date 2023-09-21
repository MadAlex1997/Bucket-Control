# This module is for sending data from the edge device to the s3 bucket
#TODO figure out S3 bucket putting try to get access early to test before range test
import os
import json
from datetime import datetime
from pathlib import Path
import shlex, subprocess



with open("./sensor_info.json","r") as si:
    sidict = json.load(si)
    data_path = sidict["data_path"]
    meta_path = sidict["meta_path"]

def get_files_waiting():
    """
    Compare files in data_path to files in meta_path
    """
    data_waiting = os.listdir("./Data")
    data_waiting = [i for i in data_waiting if ".wav" in i]
    data_waiting = [i.replace(".wav","") for i in data_waiting]
    meta_done = os.listdir("./Meta")
    meta_done = [i for i in meta_done if ".json" in i]
    meta_done = [i.replace(".json","") for i in meta_done]
    files_wating = [data for data in data_waiting if data in meta_done]
    return files_wating

def make_local_storage():
    """
    Create the storage for the files locally
    """
    now = datetime.now()
    year, month, day, hrs = now.year, now.month, now.day, now.hour
    storage_path = f"./sent/{year}/{month}/{day}/{hrs}"
    Path(storage_path).mkdir(parents=True, exist_ok=True)
    return storage_path

def move_local(files_waiting,storage_path):
    """
    Move the files to the local storage
    """
    for file in files_waiting:
        Path(f"./Data/{file}.wav").rename(f"{storage_path}/{file}.wav")
        Path(f"./Meta/{file}.json").rename(f"{storage_path}/{file}.json")

def send_to_bucket(files_waiting,storage_path):
    for file in sorted(files_waiting):
        # meta = shlex.split(f"aws s3 cp ./Meta/{file}.json s3://aftac-test-ore2-temp/PRE testfolder/")
        meta= ["aws","s3","cp",f"./Meta/{file}.json", "s3://aftac-test-ore2-temp/PRE testfolder/"]
        # data = shlex.split(f"aws s3 cp ./Data/{file}.wav s3://aftac-test-ore2-temp/PRE testfolder/")
        data= ["aws","s3","cp",f"./Data/{file}.wav", "s3://aftac-test-ore2-temp/PRE testfolder/"]
        subprocess.Popen(meta)
        subprocess.Popen(data)
        # s3.put_object(
        #     Body = open(f"./Meta/{file}.json","rb").read(),
        #     Bucket = '''aftac-test-ore2-temp''',
        #     key = f"{storage_path}/{file}.json"
            
        # )

        # s3.put_object(
        #     Body = open(f"./Data/{file}.wav","rb").read(),
        #     Bucket = '''aftac-test-ore2-temp''',
        #     key= f"{storage_path}/{file}.wav"
            
        # )

def send():
    
    while True:
        files_waiting = get_files_waiting()
        if files_waiting:
            storage_path = make_local_storage()
            send_to_bucket(files_waiting=files_waiting,storage_path=storage_path)
            
            move_local(files_waiting,storage_path)
            


if __name__ == "__main__":
    send()