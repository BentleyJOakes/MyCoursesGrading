#! /bin/python3

import subprocess
import os
import sys
from datetime import datetime
import configparser


#package, compile, run, not right output
error_package = "-5"
error_compile = "-5"
error_runtime = "-5"
error_output  = "-5"


def do_command(command_line, debug=False):

    if debug:
        print(command_line)
        
    try:
        output = subprocess.check_output(command_line, stderr=subprocess.STDOUT, shell=True, timeout=5)
        
    except Exception:
        pass

config_file = "config.cfg"
config = configparser.ConfigParser()
config.read(config_file)

files_to_compile = config["default"]["files_to_compile"].split(",")

compile_file_packages = []
compile_file_names = []

#TODO: very hacky
for i in range(0, len(files_to_compile)):
    files_to_compile[i] = files_to_compile[i].strip().replace("\"", "")

    compile_file_parts = files_to_compile[i].split(".")
    if len(compile_file_parts) == 3:
        compile_file_packages.append(compile_file_parts[0])
        compile_file_names.append(compile_file_parts[1] + "." + compile_file_parts[2])
    elif len(compile_file_parts) == 2:
        compile_file_packages.append("")
        compile_file_names.append(compile_file_parts[0] + "." + compile_file_parts[1])
    else:
        compile_file_packages.append("")
        compile_file_names.append("")

#Move assignments to right folder for packages
fileList = os.listdir(".")
fileList.sort()

for i in range(len(files_to_compile)):
    if compile_file_packages[i] != "":
        for f in fileList:
            if f == compile_file_names[i]:
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

    if files_to_compile[i] == "":
        continue

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
        
        if not saw_right_package:
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
    
try:
    size_of_error_file = os.stat("COMPILE_ERRORS.txt").st_size
    if size_of_error_file == 0:
        #No error
        command_line = "rm -f COMPILE_ERRORS.txt"
        subprocess.call(command_line, shell=True)
    else:
        sys.exit("Compile errors for " + os.getcwd())
except FileNotFoundError:
    pass
      
command_line = "rm -f output.txt"
subprocess.call(command_line, shell=True)

command_line = "rm -f RUN_ERRORS.txt"
subprocess.call(command_line, shell=True)



#===============================
# Start running



files_to_run = config["default"]["files_to_run"].split(",")
files_arguments = config["default"]["files_arguments"].split(",")
files_input = config["default"]["files_input"].split(",")

#print(files_to_run)
#print(files_input)

run_file_packages = []
run_file_names = []
run_file_input = []

#TODO: very hacky
for i in range(0, len(files_to_run)):
    files_to_run[i] = files_to_run[i].strip().replace("\"", "")

    run_file_parts = files_to_run[i].split(".")
    if len(run_file_parts) > 1:
        run_file_packages.append(run_file_parts[0])
        run_file_names.append(run_file_parts[1])
    else:
        run_file_packages.append("")
        run_file_names.append(run_file_parts[0])
    
    run_file_input.append(files_input[i].strip().replace("\"", ""))

for i in range(len(run_file_names)):

    if run_file_names[i] == "":
        continue
        
    file_path = run_file_names[i]
    if run_file_packages[i] != "":
        file_path = run_file_packages[i] + "/" + file_path

    do_command("echo -e \"" + run_file_input[i] + "\" | java " + file_path + " " + files_arguments[i] + " >> output.txt 2>> RUN_ERRORS.txt")
    
    do_command("cat RUN_ERRORS.txt >> LOG_FILE.txt")

try:
    size_of_error_file = os.stat("RUN_ERRORS.txt").st_size
    if size_of_error_file == 0:
        #No error
        command_line = "rm -f RUN_ERRORS.txt"
        subprocess.call(command_line, shell=True)
    else:
        sys.exit("Run errors for " + os.getcwd())
except FileNotFoundError:
    pass
    

