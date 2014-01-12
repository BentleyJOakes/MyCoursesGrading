#! /bin/python3

import subprocess
import os
import sys

files_to_compile = ["Agent.java", "WordList.java", "DiscussionDirector.java"]

#=============================
# Compile and run assignments
#=============================

command_line = "rm -f COMPILE_ERRORS.txt"
subprocess.call(command_line, shell=True)

for compile_file in files_to_compile:
    command_line = "javac " + compile_file + " 2>> COMPILE_ERRORS.txt"
    subprocess.call(command_line, shell=True)

size_of_error_file = os.stat("COMPILE_ERRORS.txt").st_size
if size_of_error_file == 0:
    #No error!
    command_line = "rm -f COMPILE_ERRORS.txt"
    subprocess.call(command_line, shell=True)
else:
    sys.exit("Compile errors for " + os.getcwd())
      
command_line = "rm -f output.txt"
subprocess.call(command_line, shell=True)

command_line = "rm -f RUN_ERRORS.txt"

files_to_run = ["Agent", "Agent", "WordList", "DiscussionDirector", "DiscussionDirector"] 
params_to_files = ["", "", "", "", ""]

for i in range(len(files_to_run)):
    command_line = "java " + files_to_run[i] + " " + params_to_files[i] + " >> output.txt 2>> RUN_ERRORS.txt"
    subprocess.call(command_line, shell=True)
        

