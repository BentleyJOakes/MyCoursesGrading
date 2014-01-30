#! /bin/python3

import subprocess
import os
import sys
from datetime import datetime
import ConfigParser

files_to_compile = [[".", "Question2.java"]]

#package, compile, run, not right output
error_package = "-5"
error_compile = "-5"
error_runtime = "-5"
error_output  = "-5"


def do_command(command_line, debug=False):

    if(debug == True):
        print(command_line)
    subprocess.call(command_line, shell=True)

config_file = "config.cfg"
config = ConfigParser.ConfigParser()
config.read(config_file)

files_to_compile = config.get("default", "files_to_compile").split(",")

compile_file_packages = []
compile_file_names = []

#TODO: very hacky
for i in range(0, len(files_to_compile)):
    files_to_compile[i] = files_to_compile[i].strip().replace("\"", "")

    compile_file_parts = files_to_compile[i].split(".")
    if len(compile_file_parts) == 3:
        compile_file_packages.append(compile_file_parts[0])
        compile_file_names.append(compile_file_parts[1] + "." + compile_file_parts[2])
    else:
        compile_file_packages.append("")
        compile_file_names.append(compile_file_parts[0] + "." + compile_file_parts[1])


#Move assignments to right folder for packages

fileList = os.listdir(".")
fileList.sort()

for i in range(len(files_to_compile)):
    if (compile_file_packages[i] != ""):
        for f in fileList:
            if (f == compile_file_names[i]):
                do_command("mkdir -p " + compile_file_packages[i])
                do_command("mv " + f + " " + compile_file_packages[i] + "/" + compile_file_names[i])

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


for i in range(len(files_to_compile)):

    if compile_file_packages[i] != "":
        compile_package = compile_file_packages[i]
        compile_file = compile_file_names[i]
        #check for package errors
        saw_a_package = False
        saw_right_package = False
        package_name = ""
        f = open(compile_package + "/" + compile_file)
        
        for line in f:
            if "package" in line: #TODO: Could be wrong
                saw_a_package = True
                package_name = line.split(" ")[1].split("//")[0].strip().replace(";", "")
                if package_name == compile_package:
                    saw_right_package = True
        f.close()
        
        if saw_right_package == False:
            print("Did not see package: " + compile_package)
            if saw_a_package:
                print("Saw package: " + package_name)
                
            do_command("echo \"" + error_package + ": Wrong package. Should be: " + compile_package +".\"" + " | tee -a LOG_FILE.txt > PACKAGE_ERRORS.txt")
        
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
            
            do_command("mv \"" + compile_package + "/temp.file\" " + "\"" + compile_package + "/" + compile_file + "\"")

    file_path = compile_file_names[i]
    if compile_file_packages[i] != "":
        file_path = compile_file_packages[i] + "/" + file_path

    do_command("javac " + file_path + " 2>&1 >/dev/null | tee -a LOG_FILE.txt > COMPILE_ERRORS.txt")
    

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



#===============================
# Start running



files_to_run = config.get("default", "files_to_run").split(",")

run_file_packages = []
run_file_names = []
run_file_params = []

#TODO: very hacky
for i in range(0, len(files_to_run)):
    files_to_run[i] = files_to_run[i].strip().replace("\"", "")

    run_file_parts = files_to_run[i].split(".")
    if len(run_file_parts) == 3:
        run_file_packages.append(run_file_parts[0])
        run_file_names.append(run_file_parts[1] + "." + run_file_parts[2])
    else:
        run_file_packages.append("")
        run_file_names.append(run_file_parts[0] + "." + run_file_parts[1])
    run_file_params.append("")

for i in range(len(run_file_names)):

    file_path = run_file_names[i]
    if run_file_packages[i] != "":
        file_path = run_file_packages[i] + "/" + file_path

    do_command("java " + file_path + " " + run_file_params[i] + " >> output.txt 2>> RUN_ERRORS.txt")
    
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



        

