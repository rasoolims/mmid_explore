import os
import subprocess
import sys

# warc_path_prefix = os.path.abspath(sys.argv[1])
warc_info_path = os.path.abspath(sys.argv[1])
warc_json_path = os.path.abspath(sys.argv[2])

path_dir_name = os.path.dirname(os.path.realpath(__file__))
# if not os.path.exists(warc_info_path):
#     os.makedirs(warc_info_path)
if not os.path.exists(warc_json_path):
    os.makedirs(warc_json_path)

# command = "python3 -u "+path_dir_name+"/read_warc_raw.py " + warc_path_prefix +" "+warc_info_path+"/info"
# print(command)
# os.system(command)

num_sim_process = 0
process_counter = 0

dir_list = os.listdir(warc_info_path)
for i, f in enumerate(dir_list):
    process_counter += 1
    command = ["python3", path_dir_name + "/read_warc.py", os.path.join(warc_info_path, f),
               os.path.join(warc_json_path, f + ".pickle.gz")]
    popopen = subprocess.Popen(command)
    # subprocess.call()
    # command = "python3 -u "+path_dir_name+"/read_warc.py " + os.path.join(warc_info_path, f)+" "+os.path.join(warc_json_path, f+".pickle.gz")
    print(os.path.join(warc_info_path, f))
    if process_counter % 40 == 0:
        print("waiting")
        popopen.wait()
    #    command+=" &"
    # print(command)
    # os.system(command)

print("done!")
