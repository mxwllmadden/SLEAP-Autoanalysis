# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 17:14:41 2024

@author: mbmad
"""

from autosleap.process.common import JobInterface

class TranscodeJob(JobInterface):
    def job_construct_batch_contents(self):
        contents = ' '.join('ffmpeg',
                            self.sourcefile,
                            self.settings['FFMPEG'],
                            self.destfile)
        return contents
    
    def job_type(self):
        return (1, 'transcode')

class TrackJob(JobInterface):
    def job_construct_batch_contents(self):
        pass
    
    def job_type(self):
        return (2, 'sleap-track')
    
class ConvertJob(JobInterface):
    def job_construct_batch_contents(self):
        pass
    
    def job_type(self):
        return (3, 'predict-to-h5-convert')
    
class FramerateAdjustJob(JobInterface):
    def run(self, outputfunction):
        pass
    
    def job_type(self):
        return (4, 'framerate-adjustment')
    
class FinalOutput(JobInterface):
    def run(self, outputfunction):
        pass
    
    def job_type(self):
        return (-1, 'final-output')