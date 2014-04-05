#! /bin/python3

import subprocess
import os
import sys
from datetime import datetime
import configparser

config_file = "config.cfg"
config = configparser.ConfigParser()
config.read(config_file)


#===========================
#Check output vs correct answer

correct_answer_file = config.get("default", "correct_output_file").replace("\"", "")
#print("Correct output file: " + correct_answer_file)

print("Starting compare")
if correct_answer_file != "\"\"":
    f = open(correct_answer_file, "r")
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
	    if not correct_answer[i] in output and not "residualCapacities" in correct_answer[i-1]:
		    print("Line " + str(i) + ": " + correct_answer[i] + " is not in output")




        

