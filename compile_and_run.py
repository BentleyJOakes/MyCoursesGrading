#! /bin/python3

import subprocess
import os
import sys

files_to_compile = [["a1posted", "IndexedHeap.java"], ["a1posted", "TestIndexedHeap.java"]]

#Move assignments to right folder for packages

fileList = os.listdir(".")
fileList.sort()
for f in fileList:

	for compile_package, compile_file in files_to_compile:
		if (f == compile_file):
			command_line = "mkdir -p " + compile_package
			subprocess.call(command_line, shell=True)

			command_line = "mv " + f + " " + compile_package + "/" + compile_file
			subprocess.call(command_line, shell=True)

		#print(f)

#=============================
# Compile and run assignments
#=============================

command_line = "rm -f COMPILE_ERRORS.txt"
subprocess.call(command_line, shell=True)

for compile_package, compile_file in files_to_compile:
    command_line = "javac " + compile_package + "/" + compile_file + " 2>> COMPILE_ERRORS.txt"
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
subprocess.call(command_line, shell=True)

files_to_run = [["a1posted", "TestIndexedHeap"]]
params_to_files = ["", "", "", "", ""]

for i in range(len(files_to_run)):
    command_line = "java " + files_to_run[i][0] + "/" + files_to_run[i][1] + " " + params_to_files[i] + " >> output.txt 2>> RUN_ERRORS.txt"
    #print(command_line)
    subprocess.call(command_line, shell=True)

#===========================
#Check output vs correct answer

f = open("correct_answer.txt", "r")
correct_answer = []
for line in f:
	correct_answer.append(line)

g = open("output.txt", "r")
output = []
for line in g:
	output.append(line)

for i in range(len(correct_answer)):
	if correct_answer[i] != output[i]:
		print(correct_answer[i] + " is not " + output[i])
		break



        

