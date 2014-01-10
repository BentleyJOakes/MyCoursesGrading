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

    
def do_command(command_line):
    #subprocess.call(command_line, shell=True)
    thread_queue.put((command_line))

if __name__ == '__main__':
    print("Beginning marking")

    dir_name = "./files"
    dirList = os.listdir(dir_name)
    dirList.sort()
        
    p = Pool()
    num_threads = 1
    (thread_queue, threads) = start_threads(num_threads)
    

    #extract zip files into directories
    for f in dirList:
        f_with_dir = "\"" + dir_name + "/" + f + "\""     
        if f.endswith(".zip"):
            print("Unzipping zip file: " + f)
            command_line = "unzip " + f_with_dir + " -d " + f_with_dir.replace(".zip", "")
            do_command(command_line)
            
        else:
            print("Can't extract file: " + f)
        #elif f.endswith(".rar"):
        #    print("Unraring zip file: " + f)
        #    command_line = "file-roller -e " + f_with_dir.replace(".rar", "") + " --force " + f_with_dir
        #    print(command_line)
            #do_command(command_line)
        
    thread_queue.join()
    
    #remove zip files
    for f in dirList:
        f_with_dir = "\"" + dir_name + "/" + f + "\""
        if f.endswith(".zip"):
            print("Removing zip file: " + f)
            
            command_line = "rm " + f_with_dir
            do_command(command_line)
            
    thread_queue.join()
    
    dirList = os.listdir(dir_name)
    dirList.sort()
    
    #remove duplicate submissions
    student_names = {}
    for d in dirList:
        d_with_dir = dir_name + "/" + d
        
        if os.path.isdir(d_with_dir) and " - " in d:
            student_name = d.split("-")[0].strip()
            #print(student_name)
            if not student_names.get(student_name) == None:
                print(student_name + " is duplicate")
                old_folder = student_names[student_name]
                print(old_folder)
                command_line = "rm -rf \"" + old_folder + "\""
                do_command(command_line)
            
            student_names[student_name] = d_with_dir
            
    thread_queue.join()
    
    #rename folders to be lastname firstname
    student_names = {}
    for d in dirList:
        d_with_dir = dir_name + "/" + d
        if os.path.isdir(d_with_dir) and " - " in d:
            student_name = d.split(" - ")[0].strip()
            print(student_name)
            name_split=student_name.split(" ")
            first = name_split[0]
            rest = name_split[-1]
                
            command_line = "mv \"" + d_with_dir + "\" \"" + dir_name + "/" + rest + " " + first + "\""
            do_command(command_line)
            
    thread_queue.join()
            
            
    dirList = os.listdir(dir_name)
    dirList.sort()
    #make sure there are no subfolders
    for d in dirList:
        d_with_dir = dir_name + "/" + d
        if os.path.isdir(d_with_dir):
            subdirList = os.listdir(d_with_dir)
            subdirList.sort()
            print(d_with_dir)
            
            for subdir in subdirList:
                subdir_path = d_with_dir + "/" + subdir
                if os.path.isdir(subdir_path):
                    print("Is subdir: " + subdir_path)
                    if subdir.endswith("__MACOSX"):
                        print("Removing Mac folder")
                        command_line = "rm -rf \"" + subdir_path + "\""
                        do_command(command_line)
                    else:
                        subsubdirList = os.listdir(subdir_path)
                        subsubdirList.sort()
                        for sub_file in subsubdirList:
                            sub_file_path = subdir_path + "/" + sub_file
                            print(sub_file_path)
                            new_loc = d_with_dir + "/" + sub_file
                            command_line = "mv \"" + sub_file_path + "\" \"" + new_loc + "\""
                            do_command(command_line)
            
    thread_queue.join()
    
    
    files_to_compile = ["Agent.java", "WordList.java", "DiscussionDirector.java"]
    files_to_run = ["Agent.java", "WordList.java", "DiscussionDirector.java"]
    files_to_copy = ["template.txt", "run.py"]
    
    dirList = os.listdir(dir_name)
    dirList.sort()
    for d in dirList:
        d_with_dir = "\"" + dir_name + "/" + d 
        
        for copy_file in files_to_copy:
            command_line = "cp ./" +  copy_file + " " + d_with_dir + "/" + copy_file + "\""
            thread_queue.put((command_line))
            
        if "." in d:
            print("Skipping " + d_with_dir)
            continue
            
        for compile_file in files_to_compile:
            command_line = "javac -cp " +  d_with_dir + "\" " + d_with_dir + "/" + compile_file + "\""
            thread_queue.put((command_line))
            
            
        #TODO: Fix running
        for run_file in files_to_run:
            command_line = "java -cp " +  d_with_dir + "\" " + d_with_dir + "/" + run_file + "\" &> "  + d_with_dir + "/" + run_file.replace(".java", "") + ".txt\""
            subprocess.call(command_line, shell=True)
            
            
     #TODO: Fix ending       
    #thread_queue.join()
    #p.close()
        


