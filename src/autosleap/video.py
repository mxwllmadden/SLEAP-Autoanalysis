# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 17:07:37 2024

@author: mbmad
"""
import numpy as np
import cv2
import json
from matplotlib import pyplot as plt

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


if __name__ == '__main__':
    file = 'D:/Kiwi_Backup_10_27_24/Kiwi/Maxwell_PsiloObjRewApproach_Test/Media Files/Trial  4505.mpg'
    f2 = 'C:/Users/Maxwell/Documents/GitHub/SLEAP-Autoanalysis/final_cfr_output.mp4'
    t = get_all_frame_times(file)
    t2 = get_all_frame_times(f2)
    
    
    plt.figure()
    plt.plot(t-t2)
    plt.show()
    
    
"""

ffmpeg -i "D:/Kiwi_Backup_10_27_24/Kiwi/Maxwell_PsiloObjRewApproach_Test/Media Files/Trial  4505.mpg" -vsync vfr -c:v libx264 -pix_fmt yuv420p -preset superfast -crf 23 output.mp4

sleap-track cfr_header_output.mp4 -m D:/Kiwi_Backup_10_27_24/Kiwi/SECOND_TRACKING_PICK_ME/sleapmodel/attempt_at_final_model240827_222524.single_instance.n=992/training_config.json --tracking.tracker none -o trajpred --verbosity json --no-empty-frames


ffmpeg -i "D:/Kiwi_Backup_10_27_24/Kiwi/Maxwell_PsiloObjRewApproach_Test/Media Files/Trial  4505.mpg" -vsync 0 frames/frame_%04d.png

ffmpeg -framerate 25 -i frames/frame_%04d.png -vf "fps=25" -c:v libx264 -crf 23 -pix_fmt yuv420p exact_cfr_output.mp4

sleap-track new_cfr_output.mp4 -m D:/Kiwi_Backup_10_27_24/Kiwi/SECOND_TRACKING_PICK_ME/sleapmodel/attempt_at_final_model240827_222524.single_instance.n=992/training_config.json --tracking.tracker none -o trajpred --verbosity json --no-empty-frames



ffmpeg -i "D:/Kiwi_Backup_10_27_24/Kiwi/Maxwell_PsiloObjRewApproach_Test/Media Files/Trial  4505.mpg" -vf "fps=25" -c:v libx264 -crf 23 -pix_fmt yuv420p new_cfr_output.mp4




THIS IS THE FINAL FFMPEG COMMAND => FULL FRAME PRESERVATION
ffmpeg -i "D:/Kiwi_Backup_10_27_24/Kiwi/Maxwell_PsiloObjRewApproach_Test/Media Files/Trial  4505.mpg" -vsync 0 -f image2pipe -vcodec ppm - | ffmpeg -f image2pipe -framerate 25 -i - -c:v libx264 -crf 23 -pix_fmt yuv420p final_cfr_output.mp4


"""