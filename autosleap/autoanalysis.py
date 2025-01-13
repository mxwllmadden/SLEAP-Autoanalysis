# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 16:17:32 2024

@author: mbmad
"""

import time
import os
from dataclasses import dataclass
from autosleap.process import TranscodeJob, TrackJob, ConvertJob, FramerateAdjustJob

from autosleap.metadata import __default_setting_keys__, __accepted_video_extensions__
from autosleap.files import extract_filetoken, get_files_in

class Joblist():
    def __init__(self):
        self.list = []
    
    def add(self, job_object):
        self.list.append(job_object)
        
    def joblengths(self):
        lengths = {}
        for job in self.list:
            num, jobtype = job.job_type()
            if num not in lengths:
                lengths[num] = 0
            lengths[num] += 1
        return lengths
        
    def run_next(self, output_function):
        if not self.list:
            print('No jobs available, checking for new jobs...')
            return None
        success = self.list[0].run()
        report = (success, self.list[0].token, self.list[0].job_type()[1])
        self.list.pop(0)
        return report
    
    def sort(self):
        self.list = sorted(self.list, key= lambda x : x.job_type()[0])
        
    def clear(self):
        self.list = []
        

@dataclass
class Reporter():
    job_print = print
    analysis_print = print
    state_update = print
    jobs_remaining = print


class AutoAnalysis():
    def __init__(self, reporter = Reporter(), **settings):
        # Create the joblist, settings, and reporter
        self.joblist = Joblist()
        self.settings = settings
        self.reporter = reporter
        
        # Check to ensure all required settings have been provided
        for setting in __default_setting_keys__:
            if setting not  in settings:
                raise KeyError(f'Missing setting {setting}')
        
        # Grab the name of the current environment (for ffmpeg)
        self.settings['THIS_CONDA'] = os.environ.get('CONDA_DEFAULT_ENV')
        if self.settings['THIS_CONDA'] is None:
            raise RuntimeError('This project must be run inside a Conda environment')
    
    def update_joblist(self, purge = False):
        if purge is True:
            self.joblist.clear()
        # Create the jobsqueue
        jobsqueue = {TranscodeJob: (self.settings['VIDEO_SOURCE'],
                                   self.settings['VIDEO_TRANSCODED'],
                                   __accepted_video_extensions__,
                                   ['.mp4']),
                     TrackJob: (self.settings['VIDEO_TRANSCODED'],
                                     self.settings['PREDICTIONS'],
                                     ['.mp4'],
                                     ['.prediction.slp']),
                     ConvertJob: (self.settings['PREDICTIONS'],
                                               self.settings['H5'],
                                               ['.prediction.slp'],
                                               ['.h5'])}
        if self.settings['FR_ADJUST_ENABLED']:
            jobsqueue[FramerateAdjustJob] = (self.settings['H5'],
                                                 self.settings['FR_ADJUSTED'],
                                                 ['.h5'],
                                                 ['.h5'])
        
        # Iterate through each job type
        for job, (source, dest, srcextensions, dstextensions) in jobsqueue.items():
            # get all files in source
            source_files = get_files_in(source, srcextensions)
            dest_files_tokens = [extract_filetoken(file) for file in
                                 get_files_in(dest, dstextensions)]
            
            # Find jobs that have not already been executed
            pending_processing = [file for file in source_files
                                  if extract_filetoken(file) not in dest_files_tokens]
            
            # Construct each job and add it to the Joblist
            for file in pending_processing:
                self.joblist.add(
                    job(file,
                        os.path.join(dest, extract_filetoken(file) + dstextensions[0]),
                        extract_filetoken(file),
                        self.settings,
                        self.reporter
                        )
                )
    def job_estimate(self):
        lengths = self.joblist.joblengths()
        if self.settings['FR_ADJUST_ENABLED'] is True:
            last_job = 5
        else:
            last_job = 4
        num = 0
        for jobcode, number in lengths.items():
            num += (last_job - jobcode) * number
        return num
        
    
    def run(self, idlewait = 61, quit_on_idle = False):
        self.update_joblist()
        self.loopstate = 'Active'
        while True:
            self.reporter.state_update(self.loopstate)
            jobs_estimate = self.job_estimate()
            self.reporter.jobs_remaining(f'Estimated {jobs_estimate} jobs remain')
            
            if self.loopstate == 'Active':
                report = self.joblist.run_next(self.reporter)
                if report is None:
                    self.loopstate = 'Idle'
                    continue
                if report[0]:
                    self.reporter.analysis_print(
                        f'{report[2]} completed for file {report[1]}')
                else:
                    self.reporter.analysis_print(
                        f'{report[2]} FAILED for file {report[1]}')
            if self.loopstate == 'Idle':
                self.update_joblist()
                if len(self.joblist.list) != 0:
                    self.loopstate = 'Active'
                    continue
                if quit_on_idle:
                    self.reporter.analysis_print('Quitting Analysis')
                    break
                self.reporter.state_update(self.loopstate)
                self.reporter.jobs_remaining('Analysis Done. Waiting for jobs to appear...')
                time.sleep(idlewait)
            if self.loopstate == 'Inactive':
                break
                                                 