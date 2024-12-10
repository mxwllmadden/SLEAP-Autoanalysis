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
        
    def run_next(self, output_function):
        if not self.list:
            print('No jobs available')
            return None
        report = self.list[0].run(output_function)
        return report
    
    def sort(self):
        pass
    

class AutoAnalysis():
    def __init__(self, output_function = print):
        self.joblist = Joblist()
    
    def update_joblist(self):
        pass
    
    def run(self):
        self.update_joblist()
        loopstate = 'Active'
        while True:
            if loopstate == 'Active':
                report = self.joblist.run_next(output_function)