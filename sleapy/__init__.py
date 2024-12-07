# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 17:48:47 2024

@author: mbmad
"""

__version__ = '0.1.0'

__default_setting_keys__ = ['SLEAP',
                            'FFMPEG',
                            'MODEL',
                            'VIDEO_SOURCE',
                            'VIDEO_TRANSCODED',
                            'PREDICTIONS',
                            'H5',
                            'FR_ADJUST_ENABLED',
                            'FR_ADJUSTED',
                            'TARGET_FRAMERATE'
                            ]
__default_setting_values__ = {'SLEAP': 'path/to/SLEAP/env',
                              'FFMPEG': '-c:v libx264 -crf 23 -preset fast -c:a aac -b:a 192k',
                              'MODEL': 'path/to/SLEAP/model/training_data.json',
                              'VIDEO_SOURCE': 'path/to/untranscodedvideo',
                              'VIDEO_TRANSCODED': 'path/to/tracoded/videos',
                              'PREDICTIONS': 'path/to/predictions',
                              'H5': 'path/to/H5/files',
                              'FR_ADJUST_ENABLED': True,
                              'FR_ADJUSTED': 'path/to/adjusted_framerate',
                              'TARGET_FRAMERATE': 30
                              }
__default_setting_names__ = {'SLEAP': 'SLEAP conda environment path',
                             'FFMPEG': 'FFMPEG command',
                             'MODEL': 'Trained SLEAP model location',
                             'VIDEO_SOURCE': 'Path to original video files',
                             'VIDEO_TRANSCODED': 'Path to store transcoded files',
                             'PREDICTIONS': 'Path to store prediction files',
                             'H5': 'Path to store H5 files',
                             'FR_ADJUST_ENABLED': 'Adjust prediction framerate?',
                             'FR_ADJUSTED': 'Path to store framerate adjusted data',
                             'TARGET_FRAMERATE': 'Target Framerate'
                             }
