# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 17:14:41 2024

@author: mbmad
"""

from autosleap.process.common import JobInterface
from os import path

def quote_path(path: str) -> str:
    return f'"{path}"'

class TranscodeJob(JobInterface):
    def job_construct_batch_contents(self):
        contents = ' '.join(['call',
                            quote_path(self.settings['CONDA']),
                            self.settings['THIS_CONDA'],
                            '\n'])
        contents += ' '.join(['ffmpeg -y -i',
                              quote_path(self.sourcefile),
                              self.settings['FFMPEG'],
                              quote_path(self.destfile)])
        return contents

    def job_type(self):
        return (1, 'transcode')


class TrackJob(JobInterface):
    def job_construct_batch_contents(self):
        contents = ' '.join(['call',
                            quote_path(self.settings['CONDA']),
                            'sleap',
                            '\n'])
        contents += ' '.join([path.join(self.settings['SLEAP'],
                                        'Scripts',
                                        'sleap-track'),
                             quote_path(self.sourcefile),
                             '-m',
                             quote_path(self.settings['MODEL']),
                             '--tracking.tracker none -o',
                             self.destfile,
                             '--verbosity json --no-empty-frames'])
        return contents

    def job_type(self):
        return (2, 'sleap-track')


class ConvertJob(JobInterface):
    def job_construct_batch_contents(self):
        contents = ' '.join(['call',
                            quote_path(self.settings['CONDA']),
                            'sleap',
                            '\n'])
        contents += ' '.join([path.join(self.settings['SLEAP'],
                                        'Scripts',
                                        'sleap-convert'),
                             '--format analysis -o',
                             quote_path(self.destfile),
                             quote_path(self.sourcefile)
                             ])
        return contents

    def job_type(self):
        return (3, 'predict-to-h5-convert')


class FramerateAdjustJob(JobInterface):
    def run(self):
        pass

    def job_type(self):
        return (4, 'framerate-adjustment')


class FinalOutput(JobInterface):
    def run(self, outputfunction):
        pass

    def job_type(self):
        return (10000, 'final-output')
