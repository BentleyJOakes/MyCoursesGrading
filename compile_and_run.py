#! /bin/python3

files_to_compile = ["Agent.java", "WordList.java", "DiscussionDirector.java"]
files_to_run = ["Agent.java", "WordList.java", "DiscussionDirector.java"]

print("Running!")

#=============================
    # Compile and run assignments
    #=============================
    
    

   
    '''
    dirList = os.listdir(dir_name)
    dirList.sort()
    for d in dirList:
        d_with_dir = "\"" + dir_name + "/" + d 
        
        
            
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
    '''
