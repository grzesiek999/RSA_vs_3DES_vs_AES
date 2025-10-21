import time
import sys

def convert_time(time: float) -> str:
    temp = int(time)
    h, rem = divmod(temp, 3600)
    m, s = divmod(rem, 60)
    formatted = f"{h:02}:{m:02}:{s:02}"
    return formatted

def blinking_dots(start_message: str, end_message: str, stop_event=None):
    start_time = time.time()
    sys.stdout.write(start_message)
    sys.stdout.flush()
    dots = ["", ".", "..", "..."]
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r{start_message}{dots[i % len(dots)]}    {convert_time(time.time()-start_time)}   ")
        sys.stdout.flush()
        i += 1
        time.sleep(1)
    sys.stdout.write(f"\r{end_message}\n⏳ Working time: {convert_time(time.time()-start_time)}\n")
    sys.stdout.flush()