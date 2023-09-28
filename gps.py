from serial import Serial
# from pynmeagps import NMEAReader
from time import sleep
from datetime import datetime

#stream = Serial('/dev/tty.usbmodem14101', 9600, timeout=3)
def nors(buff1):
    if "N" == buff1:
        return 1
    if "S" == buff1:
        return -1

def eorw(buff3):
    if "E" == buff3:
        return 1
    if "W" == buff3:
        return -1
    
def lat_dec(buff0):
    return float(buff0[:2])+float(buff0[2:])/60

def lon_dec(buff2):
    return float(buff2[:3])+float(buff2[3:])/60

def get_gps():
    stream = Serial("/dev/ttyUSB3",115200, timeout=3)
    # stream.open()
    stream.write("at+cgpsinfo\r\n".encode())
    sleep(0.1)
    gps_dict  = dict()
    rec_buff = stream.read(stream.inWaiting())
    buff = rec_buff.decode().split(":")[1:][0].replace(" ","")
    if not any([i=="N" or i=="S" for i in buff]):
        gps_dict["gps_valid"]=False
        return gps_dict
    buff = buff.split(",")
    gps_dict["lat"] = buff[0]+buff[1]
    gps_dict["lon"] = buff[2]+buff[3]
    gps_dict["lat_deg"] = lat_dec(buff0=buff[0]) * nors(buff1=buff[1])
    gps_dict["lon_deg"] = lon_dec(buff2=buff[2]) * eorw(buff3=buff[3])
    date = buff[4]
    time = buff[5]
    gps_dict["alt"] = buff[6]
    # gps_dict["datetime"] = datetime.strptime(date+str(int(float(time))),"%d%m%y%H%M%S")
    gps_dict["datetime"] = date+str(int(float(time)))
    stream.close()
    gps_dict["gps_valid"]=True
    return gps_dict

if __name__  == "__main__":
    print(get_gps())
	
