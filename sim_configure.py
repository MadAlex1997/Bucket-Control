from serial import Serial
from time import sleep
from gps import get_gps
stream = Serial("/dev/ttyUSB3",115200, timeout=3)
stream.write("at+clanmode=1\r\n".encode())
sleep(5)
if stream.inWaiting():
    rec_buff = stream.read(stream.inWaiting()).decode()
    print(rec_buff)
    
    stream.write("at+cenablelan=1\r\n".encode())
    sleep(5)
    if stream.inWaiting():
        rec_buff = stream.read(stream.inWaiting()).decode()
        print(rec_buff)
        stream.write("AT+CUSBPIDSWITCH=9011,1,1\r\n".encode())
        sleep(60)
        if stream.inWaiting():
            rec_buff = stream.read(stream.inWaiting()).decode()
            print(rec_buff)
            stream.write("at+gpsauto=1\r\n".encode())
            sleep(5)
            if stream.inWaiting():
                rec_buff = stream.read(stream.inWaiting()).decode()
                print(rec_buff)
stream.close()
sleep(5)
import os
for i in range(500):
    gps = get_gps()
    if gps["gps_valid"]:
        print("GPS functional")
        gps()
        os.system("ping -I usb0 -w 5 8.8.8.8")
        break

