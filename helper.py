
#!/usr/bin/env python
import subprocess
import re
import sys
import time

from subprocess import Popen,PIPE

class Timeout(Exception):
    pass

def run_with_timeout(command, timeout=10):
    proc = subprocess.Popen(command, bufsize=100000000, stdout=PIPE, stderr=PIPE,shell=True)
    poll_seconds = .10
    deadline = time.time()+timeout
    while time.time() < deadline and proc.poll() == None:
        print("Now polling proc")
        time.sleep(poll_seconds)
    print("Program completed, now checking if it succeeded")

    if proc.poll() == None:
        if float(sys.version[:3]) >= 2.6:
            proc.terminate()
        raise Timeout()
    else:
        print("Program completed successfully!")
    stdout = proc.stdout.readlines()
    stderr = proc.stderr.readlines()
    return stdout, stderr, proc.returncode

import threading

class Command(threading.Thread):
    def __init__(self, num, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.process = None
        self.stdout = ""
        self.stderr = ""
        self.timeout = 100
        self.num = num

    def run(self):
        #def target():

        print_details = False
        #time.sleep(0.3)
        while True:
            #grabs host from queue

            #if print_details == True:
            #    print('Thread ' + str(self.num) + ': Waiting for job')

            from_queue =self.queue.get()

            if from_queue == None:
                if print_details == True:
                    print('Thread ' + str(self.num) + ': Exiting')
                return

            (self.cmd) = from_queue

            if print_details == True:
                print('Running: '+ self.cmd)

            #time.sleep((self.num + 1) * 0.4)

            valid = False

            count = 0

            self.process = subprocess.Popen(self.cmd, bufsize=100000000, stdout=PIPE, stderr=PIPE,shell=True)
            (self.stdout,self.stderr) = self.process.communicate()

            self.returncode = self.process.returncode

            if self.returncode != 0:
                print("ERROR for " + self.cmd)
                for line in self.stdout.splitlines():
                    print(line)
                for line in self.stderr.splitlines():
                    print(line)
                    
            if print_details == True:
                print('Thread ' + str(self.num) + ': Finished a job with returncode: ' + str(self.returncode))

            self.queue.task_done()
