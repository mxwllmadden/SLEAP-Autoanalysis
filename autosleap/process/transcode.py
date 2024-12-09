# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 17:14:33 2024

@author: mbmad
"""

from autosleap.process.jobs import JobInterface

class TranscodeJob(JobInterface):
    def job_construct_batch_contents(self):
        raise NotImplementedError('method job_batch_contents not implemented')
    
    def job_type(self):
        self.settings['']