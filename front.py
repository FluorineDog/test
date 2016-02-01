import os, fcntl
import time
import json
from os import O_WRONLY, O_NONBLOCK, O_RDONLY
FIFO2BACK = "anti-LOL-to-back"
FIFO2FRONT = "anti-LOL-to-front"
PATH_TO_SETTINGS = "jielu.conf"
default_settings = dict(image_detect=True, text_detect=True,
                        game_type=0, difficulty=0,
                        )



HEARTBEAT_TIME = 2
BUF_SIZE = 512
def run_something_bad():
    pass # TODO porn detected



def start_the_back():
    save_settings()
    try:
        os.unlink(FIFO2BACK)
    except:
        pass
    try:
        os.unlink(FIFO2FRONT)
    except:
        pass
    os.mkfifo(FIFO2FRONT)
    from_back = os.open(FIFO2FRONT, O_RDONLY)
    # TODO start back.py like
    # TODO os.system("python back.py > xxx.log")
    '''
    the back start,
    '''
    ss = ""
    ss = os.read(from_back, BUF_SIZE).decode()
    fcntl.fcntl(from_back, fcntl.F_SETFL, O_NONBLOCK)
    ss = ss.split()[0]
    if ss == "BACK_START_SUCCESSFULLY":
        to_back = os.open(FIFO2BACK, O_WRONLY )
    else:
        print(ss)
        print("WTF")
        exit()
    return from_back, to_back

def warn_the_user():
    print("warnning") # TODO give warning when back is killed
    pass



def todo_no_internet():
    pass    # TODO no INTERNET

def save_settings():
    print(default_settings)
    print("setting saved")
    sfile = open(PATH_TO_SETTINGS, "w")
    json.dump(default_settings, sfile)
    sfile.close()
def encoder(ss):
    return (ss+' ').encode()
def exe():
    from_back, to_back = start_the_back()

    print("server start")
    last_heartbeat = time.time()
    last_heartbeat2 = time.time()
    while True:
        # data processor
        try:
            sss = os.read(from_back, BUF_SIZE).decode()
            for ss in sss.split():
                if ss == "HEART_BEAT":
                    last_heartbeat = time.time()
                    print(last_heartbeat)
                elif ss == "PORN_DETECTED":
                    run_something_bad()
                    last_heartbeat = time.time()
                elif ss == "NO_INTERNET":
                    todo_no_internet()
                    last_heartbeat = time.time()
                else:
                    print("shenmegui")
                    print(ss)
                    pass # TODO (MAY NOT NEED)
        except BlockingIOError:     # no data read
            current_time = time.time()
            # HEARTBEAT TIMEOUT
            if current_time - last_heartbeat > 4 * HEARTBEAT_TIME:
                print(last_heartbeat)
                warn_the_user()
                start_the_back()
                last_heartbeat = current_time
            # TODO need sleep() ?


        # message sender
        try:
            current_time = time.time()
            if current_time - last_heartbeat2 >  HEARTBEAT_TIME:
                print("beating")
                os.write(to_back, encoder("HEART_BEAT"))
                last_heartbeat2 = time.time()

            is_time_to_exit = False         # TODO
            is_settings_modified = False    # TODO
            if is_time_to_exit:
                os.write(to_back, "EXIT".encode())
                is_time_to_exit = False
                break
            if is_settings_modified:
                save_settings()
                os.write(to_back, encoder("SETTING_MODIFIED"))
                is_settings_modified = False
        except BrokenPipeError:
            warn_the_user()
            os.close(to_back)
            os.close(from_back)
            from_back, to_back = start_the_back()


    os.unlink(FIFO2BACK)
    os.unlink(FIFO2FRONT)
if __name__ == "__main__":
    exe()