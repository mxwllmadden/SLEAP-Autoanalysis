# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 17:31:08 2024

@author: mbmad
"""

import os
import cv2
from autosleap.files import h5_to_dict
import numpy as np

def label_video(orig_video_path : str,
                h5_traj_filepath : str,
                labeled_video_output : str,
                label_radius : int = 10 ,
                label_thickness : int = 2,
                color_labels : list = []):
    if not os.path.exists(orig_video_path) and \
        not os.path.exists(h5_traj_filepath):
            raise FileExistsError(f'Either {orig_video_path} or {h5_traj_filepath} does not exist')
    traj_data = h5_to_dict(h5_traj_filepath)
    bodyparts = [str(s) for s in traj_data['node_names']]
    node_colors = {}
    for ind, node in enumerate(bodyparts):
        if ind >= len(color_labels):
            node_colors[node] = (0,0,0)
        else:
            node_colors[node] = color_labels[ind]
    
    capture = cv2.VideoCapture(orig_video_path)
    if not capture.isOpened():
        raise TypeError(f'Issue with opening video file {orig_video_path}')
    
    frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(capture.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4 output
    
    # Define the VideoWriter object
    vidwrite = cv2.VideoWriter(labeled_video_output, fourcc, fps, (frame_width, frame_height))
    
    frame_number = 0
    while True:
        if frame_number % 10 == 0:
            print(f'Labeling frame {frame_number}')
        ret, frame = capture.read()
        if not ret:  # Break the loop if no frames are left
            break
    
        # Draw a circle on the frame
        for ind, node in enumerate(bodyparts):
            color = node_colors[node]
            coordinate = traj_data['tracks'][0,:,ind,frame_number]
            if np.isnan(coordinate).any():
                continue
            coordinate = tuple(int(c) for c in coordinate)
            cv2.circle(frame, coordinate, label_radius, node_colors[node], 
                       label_thickness)
    
        # Write the edited frame to the output video
        vidwrite.write(frame)
        frame_number += 1
    
    capture.release()
    vidwrite.release()
    print(f"Width: {frame_width}, Height: {frame_height}, FPS: {fps}")
    return True
label_video('K:/photometry/video files/Trial1.mp4',
            'K:/photometry/framerate adjusted trajectories/Trial1.h5', 
            'K:/video_label_out.mp4')
"""
Desired capabilities (KISS)

Draw tracking data over top of a video
Draw tracking data over top of an image
 
Should be enough...
"""