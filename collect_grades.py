#! /bin/python3

import subprocess
import os
import sys

dir_name = "./files"
dirList = os.listdir(dir_name)
dirList.sort()

command_line = "rm -f grades.txt"
subprocess.call(command_line, shell=True)

print("Collecting grades from each template.txt")

for d in dirList:
    student_name = d
    command_line = "echo \"\n==========================\n" + student_name + "\n\" >> grades.txt"
    subprocess.call(command_line, shell=True)
    
    command_line = "cat \"./files/" + d + "/template.txt\" >> grades.txt"
    subprocess.call(command_line, shell=True)
