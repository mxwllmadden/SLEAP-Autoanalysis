# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 17:07:37 2024

@author: mbmad
"""
import numpy as np
import cv2
import json

def get_all_frame_times(videopath):
    capture = cv2.VideoCapture(videopath)
    frame_timings = []
    
    while True:
        ret, frame = capture.read()
        if not ret:
            break

        # Get the timestamp of the current frame in milliseconds
        frame_time = capture.get(cv2.CAP_PROP_POS_MSEC)
        frame_timings.append(frame_time)
    
    # Convert frame timings to a numpy array
    if frame_timings:
        return np.array(frame_timings)[:, np.newaxis]
    return None

def downsample_trajectory(frametimes, trajectories):
    pass