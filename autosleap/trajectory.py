# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 13:25:47 2024

@author: mbmad
"""
import h5py
import numpy as np

def downsample_trajectory(frametimes_ms, h5trajdataset, target_samplerate_hz=10, mode='closest'):
    tracks = h5trajdataset['tracks']  # Extract out the tracked positions of each node

    # Determine the target sample window in milliseconds
    target_samplewindow_ms = 1000 / target_samplerate_hz
    frames_start_time = frametimes_ms[0]
    frames_end_time = frametimes_ms[-1]

    # Calculate the number of windows
    numwins = int(np.floor((frames_end_time - frames_start_time) / target_samplewindow_ms)[0])
    ds_tracks_shape = list(tracks.shape)
    ds_tracks_shape[-1] = numwins

    # Initialize the downsampled array with NaNs
    ds_tracks = np.full(ds_tracks_shape, np.nan)

    # Adjust windows to be centered on the start time
    window_centers = frames_start_time + np.arange(numwins) * target_samplewindow_ms

    for win_idx, center_time in enumerate(window_centers):
        # Define the time window centered around the current center time
        window_start = center_time - target_samplewindow_ms / 2
        window_end = center_time + target_samplewindow_ms / 2

        # Get indices of frametimes within the current window
        indices = np.where((frametimes_ms >= window_start) & (frametimes_ms < window_end))[0]

        if len(indices) > 0:
            if mode == 'closest':
                # Use the closest frame to the center time
                closest_idx = indices[np.argmin(np.abs(frametimes_ms[indices] - center_time))]
                ds_tracks[..., win_idx] = tracks[..., closest_idx]
            elif mode == 'mean':
                # Use the mean of all frames in the window
                ds_tracks[..., win_idx] = np.nanmean(tracks[..., indices], axis=-1)
            else:
                raise ValueError(f"Unsupported mode: {mode}")
    ds_frametimes = window_centers
    return ds_frametimes, ds_tracks

    
if __name__ == '__main__':
    from autosleap.video import get_all_frame_times
    from matplotlib import pyplot as plt
    
    file = 'K:/mytestproj/h5_files/Trial3826.h5'
    vfile = 'K:/mytestproj/untranscoded_video/Trial3826.mpg'
    ft = get_all_frame_times(vfile)
    window_centers, ds_tracks, frametimes_ms, tracks = downsample_trajectory(ft, file,
                                                                             mode = 'closest',
                                                                             target_samplerate_hz = 10)
    plt.plot(frametimes_ms, tracks[0,0,0,:])
    plt.plot(window_centers, ds_tracks[0,0,0,:])
    