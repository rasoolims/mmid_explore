import datetime
import errno
import os
import signal
import sys
import time
import urllib.parse as urlparse
import urllib.request
from functools import wraps


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
alread_downloaded = 0
with open(input_file) as reader:
    for line in reader:
        spl = line.strip().split("\t")
        n, url = spl[0].strip(), spl[1].strip()
        extension = url[:url.rfind(".")]
        file_name = n+"."+extension
        img_file_path = os.path.join(output_folder, file_name)
        if os.path.exists(img_file_path):
            alread_downloaded += 1
            continue

        parsed_link = urlparse.urlsplit(url)
        parsed_link = parsed_link._replace(path=urllib.parse.quote(parsed_link.path))
        fixed_url = parsed_link.geturl()

        url_count += 1

        total_tries = 2
        for t in range(total_tries):
            try:
                download_one_file(fixed_url, img_file_path)
                file_number += 1
                break
            except:
                if t == total_tries - 1:
                    print(spl, extension, n, url, fixed_url)
                    print("unable to download\t" + file_name + "\t" + fixed_url)
                time.sleep(5)
                pass

        if url_count % 100 == 0:
            print(datetime.datetime.now(), url_count, file_number, time.time() - start_time, "already_downloaded:",
                  alread_downloaded)
            start_time = time.time()
            time.sleep(10)  # more respect to wiki servers

    sys.stdout.write(str(url_count) + "\n")

print("Written files", file_number)
