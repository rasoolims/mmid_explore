import sys
import urllib.request
import datetime
import time
from functools import wraps
import errno
import os
import signal

class TimeoutError(Exception):
    pass

def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator

@timeout(300, "time out")
def download_one_file(fixed_url, file_path):
    urllib.request.urlretrieve(fixed_url, file_path)

input_file = os.path.abspath(sys.argv[1])
output_folder = os.path.abspath(sys.argv[2])
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


file_number = 0
url_count = 0
start_time = time.time()
file_path = os.path.join(output_folder, "index.txt")
with open(input_file) as reader:
    for line in reader:
        spl = line.strip().split("\t")
        file_name = spl[0]
        fixed_url = spl[2].replace(" ", "_")
        url_count += 1

        html_file_path = os.path.join(output_folder, file_name)

        totol_tries = 3
        for t in range(totol_tries):
            try:
                download_one_file(fixed_url, html_file_path)
                file_number += 1
                break
            except:
                if t==totol_tries-1:
                    print("unable to download " + fixed_url)
                else:
                    time.sleep(5)
                pass

        if url_count%100==0:
            print(datetime.datetime.now(), url_count, file_number, time.time()-start_time)
            start_time = time.time()

    sys.stdout.write(str(url_count)+"\n")

print("Written files", file_number)

