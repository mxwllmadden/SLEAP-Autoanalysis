# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 17:15:22 2024

@author: mbmad
"""
from autosleap.utils import job_batchfile_create
from datetime import datetime
import subprocess
import threading

def now_str():
    return datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

class JobInterface():
    def __init__(self, sourcefile, destfile, token, *args, **kwargs):
        self.sourcefile = sourcefile
        self.destfile = destfile
        self.settings = kwargs
        self.args = args
        
        self.batch_fpath = job_batchfile_create(
            '_'.join(now_str(),self.job_type(), token,'.bat'))
        
        self.require
    
    def run(self, outputfunction):
        """
        create batch file then run it using the run_batch function
        """
        with open(self.batch_fpath,'w') as file:
            file.write(self.job_construct_batch_contents())
        run_batch(self.batch_fpath, outputfunction = outputfunction)
            
    def job_construct_batch_contents(self):
        raise NotImplementedError('method job_batch_contents not implemented')
    
    def job_type(self):
        raise NotImplementedError('method job_type not implemented')
        
def read_output_subprocess(pipe):
    try:
        for line in iter(pipe.readline, ''):
            print(line, end='', flush=True)
    finally:
        pipe.close()

def run_batch(bat_file_path, outputfunction = read_output_subprocess):
    try:
        process = subprocess.Popen(
            ['cmd.exe', '/c', bat_file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True
        )

        # Create threads to read stdout and stderr
        stdout_thread = threading.Thread(target=outputfunction, args=(process.stdout,))
        stderr_thread = threading.Thread(target=outputfunction, args=(process.stderr,))

        # Start the threads
        stdout_thread.start()
        stderr_thread.start()

        # Wait for the threads to finish
        stdout_thread.join()
        stderr_thread.join()

        process.wait()

        if process.returncode == 0:
            print("\nBatch file executed successfully.")
        else:
            print("\nError occurred while executing the batch file.")
            
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")