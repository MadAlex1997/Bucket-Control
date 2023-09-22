import multiprocessing
from record import record
from metadata import metadata
from send import send
from video import video

# record = record_dummy

# List of processes
if __name__ == "__main__":
    process_list =[
        multiprocessing.Process(target=record),
        multiprocessing.Process(target=metadata),
        multiprocessing.Process(target=send),
        multiprocessing.Process(target=video)
    ]

    for process in process_list:
        process.start()
    # for process in process_list:
    #     process.join()
