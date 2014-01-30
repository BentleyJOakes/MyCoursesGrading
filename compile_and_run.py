#! /bin/python3

import subprocess
import os
import sys
from datetime import datetime


files_to_compile = [[".", "Question2.java"]]

#package, compile, run, not right output
error_package = "-5"
error_compile = "-5"
error_runtime = "-5"
error_output  = "-5"


def do_command(command_line):
    print(command_line)
    subprocess.call(command_line, shell=True)



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

command_line = "rm -f PACKAGE_ERRORS.txt"
subprocess.call(command_line, shell=True)


#start log file
command_line = "echo \"" + str(datetime.now()) + "\n\"" + " >> LOG_FILE.txt"
subprocess.call(command_line, shell=True)


for compile_package, compile_file in files_to_compile:

    if compile_package != ".":

        #check for package errors
        saw_a_package = False
        saw_right_package = False
        package_name = ""
        f = open(compile_package + "/" + compile_file)
        
        for line in f:
            if "package" in line: #TODO: Could be wrong
                saw_a_package = True
                package_name = line.split(" ")[1].strip().replace(";", "")
                if package_name == compile_package:
                    saw_right_package = True
        f.close()
        
        if saw_right_package == False:
            print("Did not see package: " + compile_package)
            if saw_a_package:
                print("Saw package: " + package_name)
                
            command_line = "echo \"" + error_package + ": Wrong package. Should be: " + compile_package +".\"" + " | tee -a LOG_FILE.txt > PACKAGE_ERRORS.txt"
            subprocess.call(command_line, shell=True)
        
        
            g = open(compile_package + "/temp.file", "w")
            f = open(compile_package + "/" + compile_file)
            
            #Now fix the package
            if package_name == "":
                #means we saw no other package
                g.write("package " + compile_package + ";\n")
                
            for line in f:
                if "package " in line and package_name in line:
                    line = line.replace(package_name, compile_package)
                g.write(line)
                
            f.close()
            g.close()
            
            command_line = "mv \"" + compile_package + "/temp.file\" " + "\"" + compile_package + "/" + compile_file + "\""
            subprocess.call(command_line, shell=True)

    file_path = compile_file
    if compile_package != ".":
        file_path = compile_package + "/" + compile_file

    do_command("javac " + file_path + " 2>&1 >/dev/null | tee -a LOG_FILE.txt > COMPILE_ERRORS.txt")
    
    #command_line = "javac " + compile_package + "/" + compile_file + " 2>> LOG_FILE.txt"
    #subprocess.call(command_line, shell=True)

size_of_error_file = os.stat("COMPILE_ERRORS.txt").st_size
if size_of_error_file == 0:
    #No error
    command_line = "rm -f COMPILE_ERRORS.txt"
    subprocess.call(command_line, shell=True)
else:
    sys.exit("Compile errors for " + os.getcwd())
      
command_line = "rm -f output.txt"
subprocess.call(command_line, shell=True)

command_line = "rm -f RUN_ERRORS.txt"
subprocess.call(command_line, shell=True)

files_to_run = [[".", "Question2"]]
params_to_files = ["", "", "", "", ""]

for i in range(len(files_to_run)):

    file_path = files_to_run[i][1]
    if compile_package != ".":
        file_path = files_to_run[i][0] + "/" + file_path

    do_command("java " + file_path + " " + params_to_files[i] + " >> output.txt 2>> RUN_ERRORS.txt")
    
    do_command("cat RUN_ERRORS.txt >> LOG_FILE.txt")

size_of_error_file = os.stat("RUN_ERRORS.txt").st_size
if size_of_error_file == 0:
    #No error
    command_line = "rm -f RUN_ERRORS.txt"
    subprocess.call(command_line, shell=True)
else:
    sys.exit("Run errors for " + os.getcwd())
    
#===========================
#Check output vs correct answer

f = open("correct_answer.txt", "r")
correct_answer = []
for line in f:
	correct_answer.append(line)
f.close()

g = open("output.txt", "r")
output = []
for line in g:
	output.append(line)
g.close()

for i in range(len(correct_answer)):
	if correct_answer[i] != output[i]:
		print(correct_answer[i] + " is not " + output[i])
		break



        

