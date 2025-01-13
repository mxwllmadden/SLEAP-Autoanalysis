# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 17:31:08 2024

@author: mbmad
"""

import os
import cv2
from autosleap.files import h5_to_dict

def label_video(orig_video_path : str,
                h5_traj_filepath : str,
                labeled_video_output : str,
                label_radius = 10,
                label_thickness = 2):
    if not os.path.exists(orig_video_path) and \
        not os.path.exists(h5_traj_filepath):
            raise FileExistsError(f'Either {orig_video_path} or {h5_traj_filepath} does not exist')
    traj_data = h5_to_dict(h5_traj_filepath)
    
    capture = cv2.VideoCapture(orig_video_path)
    if not capture.isOpened():
        raise TypeError(f'Issue with opening video file {orig_video_path}')
    
    frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(capture.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4 output
    
    # Define the VideoWriter object
    vidwrite = cv2.VideoWriter(labeled_video_output, fourcc, fps, (frame_width, frame_height))
        
    while True:
        ret, frame = capture.read()
        if not ret:  # Break the loop if no frames are left
            break
    
        # Draw a circle on the frame
        cv2.circle(frame, circle_center, label_radius, circle_color, label_thickness)
    
        # Write the edited frame to the output video
        vidwrite.write(frame)
    
    capture.release()
    vidwrite.release()
    return True
    """
Desired capabilities (KISS)

Draw tracking data over top of a video
Draw tracking data over top of an image

Should be enough...
"""