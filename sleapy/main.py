# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 14:27:34 2024

@author: mbmad
"""

def start():
    parser = argparse.ArgumentParser(description="A utility for ongoing automated SLEAP analysis")
    
class Wizard():
    def __init__(self, settings : dict):
        self.jobqueue = []
        self.job_counts = []
        self.job_count_total = 0
    
    def updatejobs(self):
        pass
    
    def execute_job(self):
        pass
    
    