import json
import socket
config_dict = json.load(open("sensor_info.json","r"))
config_dict["sensor_name"]= socket.gethostname()
json.dump(config_dict,open("sensor_info.json","w"))