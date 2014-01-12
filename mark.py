#! /bin/python3

import sys
import os
import random
import subprocess
import codecs
from multiprocessing import Pool, Process, JoinableQueue
#parallelization
import threading
from helper import *

def start_threads(num_threads):
    #parallelize
    thread_queue = JoinableQueue()
    threads = []

    #spawn a pool of threads, and pass them queue instance
    print('\nStarting to make threads...')
    for i in range(num_threads):
        t = Command(i, thread_queue)
        t.start()
        threads.append(t)

    print('Created ' + str(len(threads)) + ' threads')
    return (thread_queue, threads)
    

def fixFile(name):
    print("Fixing: " + filename)
    f = codecs.open(name, "r", "utf-8")
    g = codecs.open(name + ".bak", "w", "utf-8")
    #for line in f:
    #    g.write(line.replace("isConsecutive", "IsConsecutive"))
        
    f.close()
    g.close()
    
    f = codecs.open(name, "w", "utf-8")
    g = codecs.open(name + ".bak", "r", "utf-8")
    for line in g:
        f.write(line)
        
    f.close()
    g.close()

    
def do_command(command_line, parallelize=False):
    if not parallelize:
        subprocess.call(command_line, shell=True)
    else:
        thread_queue.put((command_line))

if __name__ == '__main__':
    print("Beginning marking...")

    #set flags
    reset_mode = False
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        print("Setting reset mode. Files directory will be deleted if found.")
        reset_mode = True
    
    #=============================
    # Initial safety checks and extracting main zip
    #=============================
    
    print("Looking for main zip file and for files directory in this directory...")
    fileList = os.listdir(".")
    zip_file = None
    for f in fileList:
        if f.endswith(".zip") and "Download" in f:
            zip_file = f
        elif f == "files":
            if not reset_mode:
                sys.exit("Error: 'files' directory already created. Please remove it before running this script again.")
            elif reset_mode:
                do_command("rm -rf ./files")
    
    if zip_file == None:
        sys.exit("Error: Main zip file not found")
        
    print("Extracting main zip file to files directory...")
    
    do_command("mkdir files")
    
    command_line = "unzip -q \"" + zip_file + "\" -d ./files/"
    do_command(command_line)
    
    do_command("rm ./files/index.html")
    
    #=============================
    # Extracting zip files into individual folders
    #=============================
    
    dir_name = "./files"
    dirList = os.listdir(dir_name)
    dirList.sort()
        
    #p = Pool()
    #num_threads = 1
    #(thread_queue, threads) = start_threads(num_threads)
    

    print("Fixing up student's files")
    
    print("Creating student directories")
    #move each file to student's directory
    for f in dirList:
        hyphen_count = f.count("-")
        if hyphen_count < 2:
            print("Error: " + f + " is not a proper file")
            continue
            
        #deal with hyphens to get student's name 
        
        student_name_split = f.split("-")
        student_name = student_name_split[0]
        for i in range(1, len(student_name_split)):
            if ", 20" in student_name_split[i]:
                break #TODO: Fix hack
                
            student_name += " " + student_name_split[i]
            
        student_name = student_name.strip()
    
        first_name = student_name.split(" ")[0]
        last_name = student_name.split(" ")[1]
        for i in range(2, len(student_name.split(" "))):
            last_name += " " + student_name.split(" ")[i]
        full_name = last_name + " " + first_name
        full_name = full_name.strip()
        
        new_dir = dir_name + "/" + full_name
        
        do_command("mkdir -p \"" + new_dir + "\"")
        do_command("mv \"" + dir_name + "/" + f + "\" \"" + new_dir +  "/" + f + "\"")
        
        
    files_to_copy = ["template.txt", "compile_and_run.py"]
    compile_and_run_script = "compile_and_run.py"
    
    print("Extracting student files")
    #check each file in each student directory, and decide what to do
    dirList = os.listdir(dir_name)
    dirList.sort()
    for d in dirList:
        d_with_dir = dir_name + "/" + d
        if not os.path.isdir(d_with_dir):
            print("Error: " + d + " is not a directory.")
            continue
            
        #sort student files by modification time
        subdirList = os.listdir(d_with_dir)
        subdirList.sort(key=lambda x: os.path.getmtime( d_with_dir + "/" + x))
        
        zip_warning = "STUDENT_SHOULD_USE_ZIP"
        class_warning = "STUDENT_SHOULD_REMOVE_CLASS_FILES"
        for f in subdirList:
            #save file name with directory prepended. Note the escaped quotations.
            f_with_dir = "\"" + d_with_dir + "/" + f + "\""
            if f.endswith(".zip"):
                #print("Unzipping file: " + f)
                command_line = "unzip -j -q -o " + f_with_dir + " -d \"" + d_with_dir + "\""
                do_command(command_line)
                do_command("rm " + f_with_dir)
            elif f.endswith(".rar"):
                #print("Unraring file: " + f)
                command_line = "unrar e -o+ -inul "  + f_with_dir + " \"" + d_with_dir + "/\" "
                do_command(command_line)
                do_command("rm " + f_with_dir)
                do_command("touch \"" + d_with_dir + "/" + zip_warning + "\"")
            elif f.endswith(".tar.gz"):
                #print("Untaring file: " + f)
                command_line = "tar -C \"" + d_with_dir + "/\" -xf " + f_with_dir
                do_command(command_line)
                do_command("rm " + f_with_dir)
                do_command("touch \"" + d_with_dir + "/" + zip_warning + "\"")
            #elif f.endswith(".class"): TODO: Fix this case
            #    print("Found class file: " + f)
            #    do_command("touch \"" + d_with_dir + "/" + class_warning + "\"")
            else:
                #as we are sorting by modified, by moving the files we should only be keeping the newest files
                #print("Other file: " + f)
                split_filename = f.split("-")
                filename = split_filename[-1]
                for i in range(1, len(split_filename)):
                    if ", 201" in split_filename[i]: #TODO: Same hack
                        break
                    filename = split_filename[i] + "-" + filename
                filename = filename.strip()
                do_command("mv " + f_with_dir + " \"" + d_with_dir + "/" + filename + "\"")
                
        
        #copy the script to compile files, as well as the marking template
        for copy_file in files_to_copy:
            command_line = "cp ./" +  copy_file + " \"" + d_with_dir + "/" + copy_file + "\""
            do_command(command_line)
            
        #run the compiling/running script
        saved_working_path = os.getcwd()
        print(d_with_dir + "/")
        os.chdir(d_with_dir + "/")
        command_line = "python3 " + compile_and_run_script
        do_command(command_line)
        os.chdir(saved_working_path)


