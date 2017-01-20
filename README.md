MyCoursesGrading
================
A set of Python scripts to aid MyCoursesGrading. Note that these script are built to run on Unix systems.

Overview
================
These scripts will take the main zip file containing all of the student's submissions and un-zip it.
Each student submission will then be unzipped into its own directory. This also handles rars and tar.gz compression.

A set of files will be copied into each student directory, such as a marking template and any code to automate marking.

The files in each student directory will be compiled. Errors are reported to a log file.

Then, based on the config file, the Java programs can be run. As mentioned before, each file can be given input arguments or standard input

Once marking is done, the collect_grade script will output the comments in each template file in the student directories to a master file, making it easy to look through this file and provide the marks on myCourses.

Steps
================
Place the zip file containing all student's submissions in the main MyCoursesGrading directory

Change config.cfg for each assignment
  - files_to_copy: these files are copied to each student directory from the config folder. This may include a testing class that calls methods in the student's programs
  - files_to_compile: the filenames for the programs to compile, in which order
  
  - files_to_run: the file names of the programs to run. Must be of same dimension as the files_arguments and files_input configs
  - files_arguments: a list of arguments to provide to the program
  - files_input: strings to provide as standard in to the running programs. Note that currently multiple scanner calls are not supported
  
Run 'python mark.py' to begin marking

In each student directory, you will find LOG_FILE, which contains compile or runtime errors. As well, the presence of files such as 'STUDENT_SHOULD_REMOVE_CLASS_FILES' alerts you to non-fatal errors with the submission.

If you need to re-compile or re-run the student's code, navigate to the student folder and execute 'python compile_and_run.py'. This is designed to facilitate the fixing of compile-time or run-time errors.

Place student grades and comments in template.txt

At end of grading, run 'python collect_grades.py'. This will create a grade.txt file which contains all the text from the templates.txt contained in each student folder. This is designed such that you can easily enter grades and comments on MyCourses.


