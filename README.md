MyCoursesGrading
================
A set of Python scripts to aid MyCoursesGrading. Note that these scripts are built to run on Linux systems.

This script also runs a custom plagarism checker on the submitted files. More information is found at the bottom of this document. 

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

Plagarism Detector
================

This repository also contains a plagarism detector, which is a custom algorithm to detect Java source code files which are very similar in two different students submissions.

During the execution of the marking script, a signature is made for each .java file. This signature is a list of numbers, where each entry is the count of how many "words" appear on that line.

At the end of the marking script, the plagarism detector is then invoked. Each signature for each file is compared with every other student. As these sequences are a list of numbers, the intuition is to find lists that are "most similar". This is performed using Python's difflib.SequenceMatcher. This gives a numeric score to the signature's similarity.

Finally, the similarities are measured against a plagarism threshold defined in the top of the PlagarismDetector. All similarities above this threshold are reported, along with the student's names. The marker is then able to examine the files in question and alert the course supervisor as needed.



