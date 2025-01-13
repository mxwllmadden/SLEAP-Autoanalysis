# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 17:14:41 2024

@author: mbmad
"""

from autosleap.process.common import JobInterface
from autosleap.files import extract_filetoken, get_files_in, h5_to_dict, dict_to_h5
from autosleap.metadata import __accepted_video_extensions__
from autosleap.video import get_all_frame_times
from autosleap.trajectory import downsample_trajectory
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
        """
        identify source video
        extract all the frame timings from the video
        adjust the frame timings with the old function logic
        save the old, new trajectories and the frame timinings in h5
        """
        try:
            h5dataset = h5_to_dict(self.sourcefile)
            origfile = self._get_original_file()
            self.reporter.job_print(f'Found original videofile {origfile}')
            frametimes = get_all_frame_times(origfile)
            self.reporter.job_print(f'{frametimes.size} frames extracted')
            ds_frametimes, ds_tracks = downsample_trajectory(frametimes,
                                                             h5dataset,
                                                             int(self.settings['TARGET_FRAMERATE']),
                                                             mode = 'closest')
            self.reporter.job_print(f'Downsampling to {ds_frametimes.size} samples at {self.settings["TARGET_FRAMERATE"]} fps completed')
            h5dataset['downsampled_tracks'] = ds_tracks
            h5dataset['downsample_framerate'] = int(self.settings['TARGET_FRAMERATE'])
            h5dataset['downsampled_frametimes'] = ds_frametimes
            h5dataset['original_frametimes'] = frametimes
            self.reporter.job_print(f'Saving to {self.destfile}')
            dict_to_h5(h5dataset, self.destfile)
            return True
        except Exception as e:
            self.reporter.job_print(e)
        return False
        
    def _get_original_file(self):
        src_token = extract_filetoken(self.sourcefile)
        orig_file = self._get_file_from_token(src_token,
                                              self.settings['VIDEO_SOURCE'],
                                              __accepted_video_extensions__)
        if orig_file is None:
            orig_file = self._get_file_from_token(src_token,
                                                  self.settings['VIDEO_TRANSCODED'],
                                                  ['.mp4'])
        return orig_file
    
    @staticmethod
    def _get_file_from_token(token, path, extensions):
        files = get_files_in(path, extensions)
        fileandtoken = {extract_filetoken(file) : file for file in files}
        if token in fileandtoken:
            return fileandtoken[token]
        return None

    def job_type(self):
        return (4, 'framerate-adjustment')


