from serial import Serial
# from pynmeagps import NMEAReader
from time import sleep
from datetime import datetime

#stream = Serial('/dev/tty.usbmodem14101', 9600, timeout=3)

def get_gps():
    stream = Serial("/dev/ttyUSB3",115200, timeout=3)
    stream.open()
    stream.write("at+cgpsinfo\r\n".encode())
    sleep(0.1)
    gps_dict  = dict()
    rec_buff = stream.read(stream.inWaiting())
    buff = rec_buff.decode().split(":")[1:][0].replace(" ","")
    if not any([i=="N" or i=="S" for i in buff]):
        gps_dict["gps_valid"]=False
        return False
    buff = buff.split(",")
    gps_dict["lat"] = buff[0]+buff[1]
    gps_dict["lon"] = buff[2]+buff[3]
    date = buff[4]
    time = buff[5]
    gps_dict["alt"] = buff[6]
    gps_dict["datetime"] = datetime.strptime(date+str(int(float(time))),"%d%m%y%H%M%S")
    stream.close()
    gps_dict["gps_valid"]=True
    return gps_dict

if __name__  == "__main__":
    print(get_gps())
	
