import os
import sys

print(sum([len(os.listdir(os.path.join(os.path.abspath(sys.argv[1]), folder))) for folder in
           os.listdir(os.path.abspath(sys.argv[1]))]))
