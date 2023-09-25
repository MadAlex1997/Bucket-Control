# This module is for sending data from the edge device to the s3 bucket
#TODO figure out S3 bucket putting try to get access early to test before range test
import os
import json
from datetime import datetime
from pathlib import Path
from subprocess import run
# import shlex, subprocess
import os

def get_files_waiting(waiting_path):
    """
    Get the names of the files that are waiting to be sent
    """

    data_waiting = os.listdir(waiting_path)
    data_waiting = [f for f in data_waiting if ".wav" in f or ".json" in f]
    files_waiting = list(set([".".join(i.split(".")[:-1]) for i in data_waiting]))

    return files_waiting

def make_local_storage(sent_path):
    """
    Create the storage for the files locally
    """
    now = datetime.now()
    year, month, day, hrs = now.year, now.month, now.day, now.hour
    storage_path = f"{year}/{month}/{day}/{hrs}"
    Path({sent_path}+storage_path).mkdir(parents=True, exist_ok=True)
    return storage_path

def move_local(files_waiting,storage_path,waiting_path,sent_path):
    """
    Move the files to the local storage
    """
    for file in files_waiting:
        Path(f"{waiting_path}{file}").rename(f"{sent_path}{storage_path}/{file}")
    # for file in files_waiting:
    #     Path(f"{waiting_path}{file}.wav").rename(f"{sent_path}{storage_path}/{file}.wav")
    #     Path(f"{waiting_path}{file}.json").rename(f"{sent_path}{storage_path}/{file}.json")

def send_to_bucket(waiting_path, storage_path, files_waiting):
    """
    Send the files in the waiting_path folder to the s3 bucket in a folder defined by storage path

    The files that are waiting will be sent

    If files send sucessfully add them to a list for archival

    If files are sent unsucessfully (cuasing an error) don't add them to the list
    """
    done_list = list()
    for file in sorted(files_waiting):
        try:
            run(["aws","s3","cp",f"{waiting_path}{file}.json",f"s3://aftac-test-ore2-temp/{storage_path}/"],check=True)
            done_list.append(f"{file}.json")
        except:
            print(f"{file}.json could not be sent to bucket")
            pass
        try:
            run(["aws","s3","cp",f"{waiting_path}{file}.wav",f"s3://aftac-test-ore2-temp/{storage_path}/"],check=True)
            done_list.append(f"{waiting_path}{file}.wav")
        except:
            print(f"{file}.wav could not be sent to bucket")
            pass

        return done_list
        
    # os.system(f"aws s3 cp {waiting_path} s3://aftac-test-ore2-temp/{storage_path}/ --recursive")
   

def send():
    with open("./sensor_info.json","r") as si:
        sidict = json.load(si)
        data_path = sidict["data_path"]
        meta_path = sidict["meta_path"]
        waiting_path = sidict["waiting_path"]
        sent_path = sidict["sent_path"]
    while True:
        files_waiting = get_files_waiting(waiting_path=waiting_path)
        if files_waiting:
            storage_path = make_local_storage()
            done_list = send_to_bucket(waiting_path=waiting_path ,storage_path=storage_path)
            
            move_local(files_waiting=done_list, storage_path=storage_path,sent_path=sent_path)
            


if __name__ == "__main__":
    send()