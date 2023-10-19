# This module is for sending data from the edge device to the s3 bucket
#TODO figure out S3 bucket putting try to get access early to test before range test
import os
import json
from datetime import datetime
from pathlib import Path
from subprocess import run
# import shlex, subprocess
import os
from zipfile import ZipFile

def get_files_waiting(waiting_path):
    """
    Get the names of the files that are waiting to be sent
    """

    files_waiting = os.listdir(waiting_path)
    files_waiting = [f for f in files_waiting if ".zip" in f]
    
    return files_waiting

def make_local_storage(sent_path):
    """
    Create the storage for the files locally
    """
    now = datetime.now()
    year, month, day, hrs = now.year, now.month, now.day, now.hour
    storage_path = f"{year}/{month}/{day}/{hrs}"
    Path(sent_path+storage_path).mkdir(parents=True, exist_ok=True)

    return storage_path

def move_local(files_waiting,storage_path,waiting_path,sent_path):
    """
    Move the files to the local storage
    """
    for file in files_waiting:
        try:
            Path(f"{waiting_path}{file}").rename(f"{sent_path}{storage_path}/{file}")
        except(FileNotFoundError):
            continue
        


def few_files(waiting_path, storage_path, files_waiting,aws_bucket):
    """
    Using the aws cli send all data in the waiting folder to the bucket
    """
    done_list = list()
    try:
        run(["aws","s3","cp",f"{waiting_path}",f"{aws_bucket}{storage_path}/","--recursive","--cli-read-timeout","150"],check=True)
        done_list=files_waiting
    except:
        print(f"dump to bucket unsucessful")
    return done_list


def move_to_not(files_waiting, waiting_path,not_path):
    """
    If there are more than 10 zip files waiting the backlog is greater than five minutes
    so the files are moved to the `Not` folder 
    """
    for file in files_waiting:
        try:
            Path(not_path).mkdir(parents=True, exist_ok=True)
            Path(f"{waiting_path}{file}").rename(f"{not_path}{file}")
        except(FileNotFoundError):
            continue

def send_to_bucket(waiting_path, storage_path, files_waiting, not_path,aws_bucket):
    """
    Send the files in the waiting_path folder to the s3 bucket in a folder defined by storage path

    The files that are waiting will be sent

    If files send sucessfully add them to a list for archival

    If files are sent unsucessfully (cuasing an error) don't add them to the list
    """
    if len(files_waiting)>10:
        move_to_not(files_waiting=files_waiting,
                    waiting_path=waiting_path,
                    storage_path=storage_path,
                    not_path=not_path)
        done_list = []

    else:
        done_list = few_files(waiting_path, storage_path, files_waiting,aws_bucket)
    return done_list

def send():
    with open("./sensor_info.json","r") as si:
        sidict = json.load(si)
        waiting_path = sidict["waiting_path"]
        sent_path = sidict["sent_path"]
        not_path = sidict["not_sent"]
        aws_bucket = sidict["Bucket_name"]
    while True:
        files_waiting = get_files_waiting(waiting_path=waiting_path)
        if files_waiting:
            storage_path = make_local_storage(sent_path=sent_path)
            done_list = send_to_bucket(waiting_path=waiting_path,
                                       storage_path=storage_path,
                                       files_waiting=files_waiting,
                                       not_path = not_path,
                                       aws_bucket=aws_bucket)
            if done_list:
                move_local(files_waiting=done_list, storage_path=storage_path,waiting_path=waiting_path,sent_path=sent_path)
            


if __name__ == "__main__":
    send()
