# This module creates the metadata json files
import json
from datetime import datetime
import numpy as np
import os
from time import sleep
from hashlib import sha256
from gps import get_gps
# from pigps import GPS


# gps = GPS()

def gps_now(num_atempts=50):
    """
    Makes at most 50 attempts to get the Current GPS data
    returns
        gps_dict
            keys: lat[string degrees minutes N/S], lon[string degrees minutes E/W], time[ datetime.datetime(YYY, M, DD, HH, MM, SS)], gps_valid[Bool]
    """
    for i in range(num_atempts):
        gps = get_gps()
        
        if gps["gps_valid"]==False:
            sleep(.1)
            if i == num_atempts-1:
                return False, False
            continue
        elif gps["gps_valid"]==True:
            return gps,datetime.now().timestamp()




def check_waiting(data_path, meta_path):
    """
    Give a list of data files that are waiting for a meta data file to be written
    that list has the file type striped from the end 
    """
    data_waiting = os.listdir(data_path)
    data_waiting = [i for i in data_waiting if ".wav" in i]
    data_waiting = [i.replace(".wav","") for i in data_waiting]
    meta_done = os.listdir(meta_path)
    meta_done = [i for i in meta_done if ".json" in i]
    meta_done = [i.replace(".json","") for i in meta_done]
    data_waiting = [data for data in data_waiting if data not in meta_done]
    return data_waiting



def write_metadata(file,sidict, data_path, meta_path):
    json_dict = sidict
    unix_time = datetime.fromtimestamp(float(file.split("_")[1]))
    gps,_= gps_now()
    # If we can get the current gps data then we will otherwise we use the start
    # times for both gps and the system to get a delta
    if gps:
        json_dict["lat"] = gps["lat"]
        json_dict["lon"] = gps["lon"]
        json_dict["gps_date_time"] =gps["datetime"]
        system_time_now = np.datetime64(datetime.now())
        gps_time_now = np.datetime64(gps["datetime"])
        system_time_diff = system_time_now - np.datetime64(unix_time)
        json_dict["start_time_gps"] = str(gps_time_now - system_time_diff)
        json_dict["start_time_system"] = str(np.datetime64(unix_time))
    else:
        time_delta = np.timedelta64(sidict["delta_T_SysvGPS_ms"], "ms")
        json_dict["start_time_gps"] = str(np.datetime64(unix_time) - time_delta)
        json_dict["start_time_system"] = str(np.datetime64(unix_time))
        

    
    
    # TODO Use numpy time diff to determine start time based on gps time and unix time
    
    
    with open(f"{data_path}{file}.wav","rb") as hash_file:
        checksum = sha256(hash_file.read()).hexdigest()
    
    json_dict["checksum"] =checksum
    
    with open(f"{meta_path}{file}.json","w+") as jfile:
        json.dump(json_dict,jfile)
        
def metadata():
    #replace with while loop in production

    g = gps_now(num_atempts=500)
    gps_at_start =g[0]
    process_start_time = g[1]
    if not gps_at_start:
        #determine behavure if no gps at start depends on operator competency
        print("GPS broken")
        return False
        pass

    with open("./sensor_info.json","r") as si:
        sidict = json.load(si)
        data_path = sidict["data_path"]
        meta_path = sidict["meta_path"]
    
    #get GPS data at start time to fall back on if issues with GPS

    sidict["lat"] = gps_at_start["lat"]
    sidict["lon"] = gps_at_start["lon"]
    sidict["gps_date_time"] =gps_at_start["datetime"]

    system_start_time = np.datetime64(process_start_time)
    gps_start_time = np.datetime64(sidict["gps_date_time"])
    
    sidict["delta_T_SysvGPS_ms"] = (system_start_time-gps_start_time)/np.timedelta64(1,"ms")

    while True:
        data_waiting = check_waiting(data_path=data_path, meta_path=meta_path)
        if data_waiting:
            for file in data_waiting:
                write_metadata(file=file, sidict=sidict, data_path=data_path, meta_path=meta_path)
        else:
            # sleep(10)
            continue
if __name__ == "__main__":
    metadata()
