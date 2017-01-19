
#! /bin/python3

import sys
import os
import random
import subprocess
import codecs

import configparser


import unicodedata

from PlagarismDetector import PlagarismDetector


def handle_encoding(s):
    return str(unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('utf-8', 'ignore'))
    
def do_command(command_line, debug=False):
    if debug:
        print(command_line)
    subprocess.call(command_line, shell=True)

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
    zip_files = []
    for f in fileList:
        if f.endswith(".zip") and "Download" in f:
            print("Zip: " + f)
            zip_files.append(f)
        elif f == "files":
            if not reset_mode:
                sys.exit("Error: 'files' directory already created. Please remove it before running this script again.")
            elif reset_mode:
                do_command("rm -rf ./files")
    
    if zip_files is []:
        sys.exit("Error: No zip files were found")
        
    config_file = "config/config.cfg"
    print("Loading config file: " + config_file)
    config = configparser.ConfigParser()
    config.read(config_file)

    # get the information from the config file
    files_to_copy = config['default']["files_to_copy"].split(",")
    files_to_copy = [f.strip().replace("\"", "") for f in files_to_copy]

    print("Files to copy to each student directory")
    print(files_to_copy)

    #=============================
    print("Extracting main zip file to files directory...")
    
    do_command("mkdir files")

    for z in zip_files:
        command_line = "unzip -q \"" + z + "\" -d ./files/"
        do_command(command_line)
    
    do_command("rm ./files/index.html")
    
    #=============================
    # Extracting zip files into individual folders
    #=============================
    
    dir_name = "./files"
    dirList = os.listdir(dir_name)
    dirList.sort()

    print("Fixing up student's files")
    #primarily to remove non-utf-8 encoded names

    for f in dirList:
        new_f = handle_encoding(f)

        if new_f != f:
            print("Moving " + str(f) + " to " + str(new_f))
            do_command("mv \"" + dir_name + "/" + f + "\" \"" + dir_name + "/" + new_f + "\"")

    dirList = os.listdir(dir_name)
    dirList.sort()

    print("Creating student directories")
    #move each file to student's directory
    for f in dirList:

        #print("File: " + f)
        
        hyphen_count = f.count("-")
        if hyphen_count < 4:
            print("Error: " + f + " is not a proper file")
            continue
            
        #deal with hyphens to get student's name 
        
        student_name_split = f.split(" - ")
        student_name = student_name_split[1]
        #print(student_name)

        student_name = student_name.strip()
    
        first_name = student_name.split(" ")[0]
        last_name = student_name.split(" ")[1]
        for i in range(2, len(student_name.split(" "))):
            last_name += " " + student_name.split(" ")[i]
        full_name = last_name + " " + first_name
        full_name = full_name.strip()
        
        full_name = handle_encoding(full_name)
        new_dir = dir_name + "/" + full_name
        
        do_command("mkdir -p \"" + new_dir + "\"")
        
        new_name = handle_encoding(f)
        do_command("mv \"" + dir_name + "/" + f + "\" \"" + new_dir +  "/" + new_name + "\"")
        

    plag_detect = PlagarismDetector()
    sigs = []
    
    compile_and_run_script = "compile_and_run.py"

    print("\nExtracting student files")
    #check each file in each student directory, and decide what to do
    dirList = os.listdir(dir_name)
    dirList.sort()
    for d in dirList:
        d_with_dir = dir_name + "/" + d
        if not os.path.isdir(d_with_dir):
            print("Error: " + d + " is not a directory.")
            continue

        student_sig = [d]

        #sort student files by modification time
        subdirList = os.listdir(d_with_dir)
        subdirList.sort(key=lambda x: os.path.getmtime( d_with_dir + "/" + x))

        #create files if submission wasn't to specifications
        #so TAs can easily add comments/remove marks
        zip_warning = "STUDENT_SHOULD_USE_ZIP"
        class_warning = "STUDENT_SHOULD_REMOVE_CLASS_FILES"

        for f in subdirList:
            #f = handle_encoding(f)
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
            elif f.endswith(".class"):
                #print("Found class file: " + f)
                do_command("touch \"" + d_with_dir + "/" + class_warning + "\"")
            else:
                #as we are sorting by modified, by moving the files we should only be keeping the newest files
                #should be avoided if myCourses only keeps newest submission

                #print("Other file: " + f)
                split_filename = f.split("-")
                filename = split_filename[-1]

                for i in range(len(split_filename), 1):
                    if ", 201" in split_filename[i]: #TODO: Same hack
                        break
                    filename = split_filename[i] + "-" + filename
                filename = filename.strip()
                #print("Moving to filename: " + filename)
                do_command("mv " + f_with_dir + " \"" + d_with_dir + "/" + filename + "\"")

        command_line = "cp ./compile_and_run.py \"" + d_with_dir + "/compile_and_run.py\""
        do_command(command_line)

        # copy the script to compile files, as well as the marking template
        for copy_file in files_to_copy:
            #print("copy file: " + copy_file)
            command_line = "cp ./config/" +  copy_file + " \"" + d_with_dir + "/" + copy_file + "\""
            do_command(command_line)


        #=====================
        #look for similar files amongst students by generating signatures for each file
        #======================
        subdirList = os.listdir(d_with_dir)
        dirList.sort()
        for f in subdirList:
            if f.endswith(".java") and not f.startswith("."):
                genned_sig = plag_detect.generate_sig(d_with_dir, f)
                student_sig.append([f, genned_sig])

        sigs.append(student_sig)


        #================================
        #run the compiling/running script in each directory
        #================================
        saved_working_path = os.getcwd()
        print(d_with_dir + "/")
        os.chdir(d_with_dir + "/")
        command_line = "python " + compile_and_run_script
        do_command(command_line)
        os.chdir(saved_working_path)



    plag_detect.compare_sigs(sigs)



