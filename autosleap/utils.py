# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 19:50:50 2024

@author: mbmad
"""

import os
import shutil

def resource_path(relative_path):
    """ Get the absolute path to a resource, works for packaged apps. """
    base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

def job_batchfile_create(job_name):
    job_batch_folder = job_batchdir_get()
    file_path = os.path.join(job_batch_folder, job_name)
    return file_path

def job_batchfile_cleanup():
    shutil.rmtree(job_batchdir_get(), ignore_errors= True)
    
def job_batchdir_get():
    try:
        # Get the Local AppData folder
        local_appdata = os.getenv('LOCALAPPDATA')
        if not local_appdata:
            raise EnvironmentError("LOCALAPPDATA environment variable not found.")
        job_batch_folder = os.path.join(local_appdata, "AutoSLEAP", 'batchfile_jobs')
        os.makedirs(job_batch_folder, exist_ok=True)
        return job_batch_folder

    except Exception as e:
        print(f"Local Appdata unavailable! Error: {e}")
        return None
    