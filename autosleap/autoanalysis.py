# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 16:17:32 2024

@author: mbmad
"""

import time

class Joblist():
    def __init__(self):
        self.list = []
    
    def add(self, job_object):
        self.list.append(job_object)
        
    def run_next(self, batch_runfunction, output_function):
        if not self.list:
            print('No jobs available')
            return None
        report = self.list[0].run(output_function) #waits for job completion
        return report #returns job report
        
    def sort(self):
        # Sort jobs according to type, then token (execute fast jobs first)
        # Sort occurs at beginning of execution of a new job type
        pass
    

class AutoAnalysis():
    def __init__(self,
                 batch_runfunction = None,
                 output_function = print):
        self.joblist = Joblist()
    
    def update_joblist(self):
        # Search for new jobs then add jobs to joblist
        pass
    
    def run(self):
        pass
    
    def runloop(self):
        pass
    
    def idleloop(self):
        pass