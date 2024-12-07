


import glob, subprocess, os, json, datetime

video_path = 'REPLACE'
sleap_env_path ='REPLACE'


def main():
    settings = load_json('settings')
    logs = load_json('logs')
    
    transcoded_vids = logs.get('transcode_logs',[])
    tracked_vids = logs.get('tracking_logs', [])
    converted_files = logs.get('h5_convert_logs', [])
    logs_general = logs.get('logs',[])
    
    if len(settings.keys()) == 0:
        assign_setting_defaults()
        return
    if settings['Setup Complete?'] is not True:
        return
    
    video_list = glob.glob(settings['VIDEO_SOURCE'] + '/*.mpg')
    video_list = [vid for vid in video_list if os.path.split(vid)[1] not in transcoded_vids]
    transcode_batch_file = create_transcode_batch(video_list, 
                                                  ffmpeg_exe_path = settings['FFMPEG'],
                                                  target_folder= settings['TRANSCODED_VIDEO'])
    subprocess.run(transcode_batch_file)
    transcoded_vids += [os.path.split(vid)[1] for vid in video_list]
    logs_general.append(f'Processed {video_list} with {transcode_batch_file}')
    
    logs['transcode_logs'] = transcoded_vids
    logs['logs'] = logs_general
    save_json('logs', logs)
    
    video_list = glob.glob(settings['TRANSCODED_VIDEO'] + '/*.mp4')
    video_list = [vid for vid in video_list if os.path.split(vid)[1] not in tracked_vids]
    tracking_batch_file = create_tracking_batch(video_list,
                                                sleap_path = settings['SLEAP'],
                                                model_path = settings['MODEL'],
                                                predictions_path = settings['PREDICTIONS'])
    subprocess.run(tracking_batch_file)
    tracked_vids += [os.path.split(vid)[1] for vid in video_list]
    logs_general.append(f'Tracked {video_list} with {tracking_batch_file}')
    
    logs['tracking_logs'] = tracked_vids
    logs['logs'] = logs_general
    save_json('logs', logs)
    
def create_tracking_batch(videofilelist,
                          conda_activate_bat,
                          sleap_path,
                          model_path,
                          predictions_path):
    batch_file = 'batch/' +  get_datecode() + '_track.bat'
    
    track_script = rf'{sleap_path}\Scripts\sleap-track'
    with open(batch_file, 'w') as file:
        file.write(conda_activate_bat + ' sleap')
        for vid in videofilelist:
            videoname = os.path.split(vid)[1]
            videoname = os.path.splitext(videoname)[0]
            command = e = f'{track_script} "{vid}" -m "{model_path}" --tracking.tracker none -o "{videoname}.predictions.slp" --verbosity json --no-empty-frames/n'
            file.write(command)

def create_transcode_batch(videofilelist, ffmpeg_exe_path = 'ffmpeg.exe',
                           target_folder = ''):
    batch_file = 'batch/' +  get_datecode() + '_transcode.bat'
    with open(batch_file, 'w') as file:
        for vid in videofilelist:
            videoname = os.path.split(vid)[1]
            videoname = os.path.splitext(videoname)[0]
            vid_output = f'{target_folder}/{videoname}.mp4'
            command = f'{ffmpeg_exe_path} -i {vid} -c:v libx264 -crf 23 -preset fast -c:a aac -b:a 192k {vid_output}/n'
            file.write(command)
    return batch_file
        
def get_datecode():
    return datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

def assign_setting_defaults():
    default_settings = {'Setup Complete?' : False,
                        'SLEAP' : 'path/to/SLEAP/env',
                        'CONDA' : 'C:\Users\<YourUsername>\anaconda3\Scripts\activate.bat',
                        'FFMPEG' : 'path/to/FFMPEG.exe',
                        'MODEL' : 'path/to/SLEAP/model/training_data.json',
                        'VIDEO_SOURCE' : 'path/to/untranscodedvideo',
                        'TRANSCODED_VIDEO' : 'path/to/tracoded/videos',
                        'PREDICTIONS' : 'path/to/predictions',
                        'H5' : 'path/to/H5/files'}
    save_json('settings', default_settings)

def load_json(name):
    fname = name + '.json'
    if not os.path.isfile(fname):
        data = {}
        save_json(name, data)
        return data
    with open(fname, 'r') as file:
        return json.load(file)
    
def save_json(name, data):
    fname = name + '.json'
    with open(fname, 'w') as file:
        json.dump(data, file, indent=2)

if __name__ == '__main__':
    main()