import multiprocessing
from record import record
from metadata import metadata
from send import send, move_to_not, get_files_waiting
from video import video
from time import sleep
import json
# record = record_dummy

#TODO Build prestart checking utilities that use indicator lights and stops the process from running if it will not be able to run
def prestart():
    pass
#TODO Rewrite the process handler to be able to monitor whether the processes are still alive
def process_loop():
    func_list = [record, metadata, send, video]
    process_list =[multiprocessing.Process(target=func) for func in func_list]

    for process in process_list:
        process.start()
    
    while True:
        sleep(120)
        for i in range(len(process_list)):
            proc = process_list[i]
            if not proc.is_alive():
                proc.terminate()
                process_list[i] = multiprocessing.Process(target=func_list[i])
                process_list[i].start()
                
# List of processes
if __name__ == "__main__":
    # process_list =[
    #     multiprocessing.Process(target=record),
    #     multiprocessing.Process(target=metadata),
    #     multiprocessing.Process(target=send),
    #     multiprocessing.Process(target=video)
    # ]

    # for process in process_list:
    #     process.start()
    with open("./sensor_info.json","r") as si:
        sidict = json.load(si)
        waiting_path = sidict["waiting_path"]
        sent_path = sidict["sent_path"]
        not_path = sidict["not_sent"]
        aws_bucket = sidict["Bucket_name"]
    waiting_list = get_files_waiting(waiting_path=waiting_path)
    move_to_not(files_waiting=waiting_list,waiting_path=waiting_path,not_path=not_path)
    process_loop()
    # for process in process_list:
    #     process.join()
