import os
import time
import json
from os import O_WRONLY, O_NONBLOCK, O_RDONLY
FIFO2BACK = "anti-LOL-to-back"
FIFO2FRONT = "anti-LOL-to-front"

PATH_TO_SETTINGS = "jielu.conf"
HEARTBEAT_TIME = 2
BUF_SIZE = 512
settings = {}

def encoder(ss):
    return (ss+' ').encode()

def update_setting():
    settings_file = open(PATH_TO_SETTINGS, 'r')
    settings.update(json.load(settings_file))
    settings_file.close()

def exe():
    update_setting()
    to_front = os.open(FIFO2FRONT, O_WRONLY)
    os.mkfifo(FIFO2BACK)
    from_front = os.open(FIFO2BACK, O_RDONLY | O_NONBLOCK)
    print(to_front, from_front)
    os.write(to_front, encoder("BACK_START_SUCCESSFULLY"))
    last_heartbeat = time.time()
    last_heartbeat2 = time.time()
    is_time_to_check = False
    running = True
    while running:
        # data processor
        try:
            sss = os.read(from_front, BUF_SIZE).decode()
            for ss in sss.split():
                print(ss) # TODO DEBUG
                if ss == "HEART_BEAT":
                    last_heartbeat = time.time()
                elif ss == "EXIT":
                    running = False
                    last_heartbeat = time.time()
                elif ss == "SETTING_MODIFIED":
                    update_setting()
                else:
                    pass # TODO
            if not running:
                break
        except BlockingIOError:     # no data read
            current_time = time.time()
            # HEARTBEAT TIMEOUT
            if current_time - last_heartbeat > 4 * HEARTBEAT_TIME:
                print("TIMEOUT!!! EXITTING") # TODO DEBUG
                running = False
                break
            else:
                time.sleep(HEARTBEAT_TIME/2)
        finally:
            pass    # TODO

        # message sender
        try:
            current_time = time.time()
            if current_time - last_heartbeat2 > HEARTBEAT_TIME:
                os.write(to_front, encoder("HEART_BEAT"))
                if is_time_to_check and check_a
dult_content():
                    os.write(to_front, encoder("PORN_DETECTED"))
                last_heartbeat2 = current_time
                is_time_to_check = not is_time_to_check
        except BrokenPipeError:
            print("Parent brokes down. Exiting")
            exit()


def check_adult_content():
    print("checking")
    if True:
        db = open("debug.conf", "r")
        if json.load(db):
            return True
    return False

if __name__ == "__main__":
    exe()