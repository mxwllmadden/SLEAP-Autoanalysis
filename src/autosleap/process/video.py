# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 17:07:37 2024

@author: mbmad
"""
import numpy as np
import cv2

def video_aware_downsample(vid_name, tracks : dict, override = False):
    videopath = f'videotransfer_MM_LFE/{vid_name}.mp4'
    cap = cv2.VideoCapture(videopath)
    frames = checkforconstantframerate(cap)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print('Original FPS:',fps)
    cap.release()
    downsampled_video = {}
    if frames is None or override is True:
        for node, track in tracks.items():
            try:
                downsampled_video[node] = downsampleto10hz(fps,track)
            except:
                raise Exception(vid_name)
        return downsampled_video
    for node,track in tracks.items():
        txy = np.concatenate((frames, track), axis=1)
        downsampled_video[node] =downsample_to_constant_fps(txy,10)
    return downsampled_video
    
def downsample_to_constant_fps(data, target_fps):
    print('Variable framerate converted to ', end='')
    # Calculate the target time interval in seconds (1 / target_fps)
    target_interval = 1.0 / target_fps
    
    # Initialize the list to store the downsampled data
    downsampled_data = []
    
    # Start the time for the first window
    current_time = data[0, 0]
    end_time = data[-1, 0]
    
    while current_time <= end_time:
        # Find all rows within the current time window (current_time to current_time + target_interval)
        window = data[(data[:, 0] >= current_time) & (data[:, 0] < current_time + target_interval)]
        
        if len(window) > 0:
            # Average the x and y values over the window
            avg_time = current_time + target_interval / 2  # Use the middle of the interval for time
            avg_x = np.mean(window[:, 1])
            avg_y = np.mean(window[:, 2])
            
            # Append the averaged point to the downsampled data
            downsampled_data.append([avg_x, avg_y])
        
        # Move to the next time window
        current_time += target_interval
    ds_arr = np.array(downsampled_data)
    print(f'{ds_arr.shape}')
    return ds_arr

def downsampleto10hz(original_fps : int,track : np.ndarray):
    print('Constant framerate converted to ', end='')
    assert track.shape[1] == 2
    ratio = original_fps / 10
    
    # Calculate the number of original frames that correspond to one target frame
    window_size = int(np.ceil(ratio))
    assert window_size >= 2
    
    # List to store downsampled data
    downsampled_data = []
    
    for i in range(0, len(track), window_size):
        # Average the x and y data over the current window
        window_data = track[i:i + window_size]
        avg_x = np.mean(window_data[:, 0])
        avg_y = np.mean(window_data[:, 1])
        
        # Append the averaged point to the downsampled data
        downsampled_data.append([avg_x, avg_y])
    
    ds_arr = np.array(downsampled_data)
    print(f'{ds_arr.shape}')
    return ds_arr


    
def checkforconstantframerate(capture):
    frame_times = []
    frame_T = []
    prev_frame_time = None
    
    while True:
        ret, frame = capture.read()
        if not ret:
            break
    
        # Get the timestamp of the current frame in milliseconds
        frame_time = capture.get(cv2.CAP_PROP_POS_MSEC)
        frame_T.append(frame_time)
    
        if prev_frame_time is not None:
            frame_times.append(frame_time - prev_frame_time)
    
        prev_frame_time = frame_time
    if len(frame_times) > 0 and round( min(frame_times) - max(frame_times),4) != 0 :
        frame_T = np.array(frame_T)
        frame_T = frame_T[:, np.newaxis] 
        return frame_T/1000
    return None

        
def get_traces(lateralitymap, photometry_traces, run, trial, animal):
    global traces___check
    
    traces = photometry_traces['regressed_traces_by_run_signal_trial'][run]
    if any(trial > trace.shape[1]-1 for trace in traces.values()):
        raise KeyError('Requested photom trial does not exist')
    traces = {t_label: trace[:,trial] for t_label, trace in traces.items()}
    
    signals = {}
    if lateralitymap[animal]['plpfc'] == 'R':
        signals['plpfc'] = traces['RCL_ch1']
        signals['pta'] = traces['LCL_ch1'] 
    elif lateralitymap[animal]['plpfc'] == 'L':
        signals['plpfc'] = traces['LCL_ch1']
        signals['pta'] = traces['RCL_ch1']
    else:
        raise Exception('Laterality Error in {run}')
    return signals
    
def loadphotom(path):
    with open(path, 'rb') as file:
        photometry_traces = pickle.load(file)
    return photometry_traces

def jsonload(path):
    with open(path, 'r') as file:
        content = json.load(file)
    return content

class Cached_Data_Get:
    def __init__(self):
        try:
            with open('cached_data.json', 'r') as file:
                self.cdata = json.load(file)
        except FileNotFoundError:
            self.cdata = {}

    @staticmethod
    def hash_func(func):
        bytecode = func.__code__.co_code
        return hashlib.md5(bytecode).hexdigest()

    def do(self, func, *args):
        func_hash = self.hash_func(func)
        if func_hash not in self.cdata:
            self.cdata[func_hash] = {}

        if str(args) in self.cdata[func_hash]:
            return self.cdata[func_hash][str(args)]

        result = func(*args)
        self.cdata[func_hash][str(args)] = result

        return result

    def save(self):
        with open('cached_data.json', 'w') as file:
            json.dump(self.cdata, file)

def find_traj_file(trial_int : str):
    fnames = glob.glob(f'Traj/H5/*l{trial_int}.mp4.predictions.slp.h5')
    fnames2 = glob.glob(f'Traj/H5/* {trial_int}.mp4.predictions.slp.h5')
    fnames3 = glob.glob(f'Traj/H5/*_{trial_int}.mp4.predictions.slp.h5')
    fnames = fnames + fnames2 + fnames3
    if len(fnames) != 1:
        print('found', len(fnames), 'trajectory for', trial_int)
        print('choosing the original')
        fnames = sorted(fnames, key = lambda x : x.count('_'))
    if len(fnames) == 0:
        print('notfound!')
        raise Exception(fnames)
    return fnames
    
def load_trajectories(runs_info):
    traj = {}
    data_cache = Cached_Data_Get()
    for ind, (vid_nm, vid_info) in enumerate(runs_info.items()):
        global fnames
        if ind%50 == 0:
            print(ind*100//len(runs_info),'% found')
        trial_int = vid_info['trial_int'].replace('_',' ')
        fnames = data_cache.do(find_traj_file, trial_int)
        if len(fnames) != 1:
            print('found', len(fnames), 'trajectory for', trial_int)
            print('choosing the original')
            fnames = sorted(fnames, key = lambda x : x.count('_'))
        if len(fnames) == 0:
            print('notfound!')
            raise Exception(fnames)
    
        with h5py.File(fnames[0], 'r') as file:
            node_names = [item.decode() for item in file['node_names'][:]]
            tracks = file['tracks'][:][0].T
    
        # Unpack Tracks into 'RUN'x'BODYPART' nested dicts
        traj[vid_nm] = {}
        for ind, node in enumerate(node_names):
            traj[vid_nm][node] = tracks[:, ind, :]
    data_cache.save()
    return traj, node_names