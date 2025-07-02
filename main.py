import sys
import os
from subprocess import call

filename, file_extension = os.path.splitext(sys.argv[1])
if file_extension != ".jm":
    raise Exception("Invalid file extension! Use .jm")

file_path = ""
if "/" in filename:
    file_path = filename[:filename.rfind("/")+1]
    filename = filename[filename.rfind("/")+1:]

call("python3 " + "sintax.py " + f"{file_path}{filename}{file_extension}", shell=True)

error_file_empty = os.stat(f"./logs/erros_{filename}.txt").st_size == 0

if(error_file_empty):
    call("python3 " + f"{filename}.py", shell=True)
else:
    print("WARNING: The parser detected syntax errors in the source code.")
    sys.exit(0)