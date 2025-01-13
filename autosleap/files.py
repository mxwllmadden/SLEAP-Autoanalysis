# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 19:50:50 2024

@author: mbmad
"""

import os
import shutil
import h5py
import numpy as np

def h5_to_dict(filename):
    """
    Convert an HDF5 file into a nested Python dictionary, decoding bytes in arrays if necessary.

    Args:
        filename (str): Path to the HDF5 file.

    Returns:
        dict: Nested Python dictionary with data from the HDF5 file.
    """
    def process_value(value):
        if isinstance(value, np.ndarray) and value.dtype.type is np.bytes_:
            # Decode bytes in NumPy arrays
            return np.array([v.decode() for v in value])
        elif isinstance(value, bytes):
            # Decode scalar bytes
            return value.decode()
        return value

    def recurse(group):
        obj = {}
        for key, item in group.items():
            if isinstance(item, h5py.Dataset):
                data = item[()]
                obj[key] = process_value(data)
            elif isinstance(item, h5py.Group):
                obj[key] = recurse(item)
        return obj

    with h5py.File(filename, 'r') as f:
        return recurse(f)

def dict_to_h5(data, filename):
    """
    Save a nested Python dictionary to an HDF5 file, encoding strings as bytes where needed.

    Parameters
    ----------
    data : dict
        Nested python dictionary of arrays.
    filename : pathlike
        Location to save h5 file.

    Raises
    ------
    ValueError
        Raised when an unsupported datatype is passed.
    """
    def process_value(value):
        if isinstance(value, np.ndarray) and value.dtype.kind in {'U', 'O'}:
            # Convert string arrays to byte arrays
            return np.array([v.encode() if isinstance(v, str) else v for v in value], dtype='S')
        elif isinstance(value, (np.integer, np.floating)):
            # Convert NumPy scalars to Python scalars
            return value.item()
        elif isinstance(value, str):
            # Convert strings to bytes
            return value.encode()
        return value

    def recurse(group, data):
        for key, value in data.items():
            if isinstance(value, dict):
                # Create a subgroup for nested dictionaries
                subgroup = group.create_group(key)
                recurse(subgroup, value)
            elif isinstance(value, np.ndarray):
                # Encode strings in NumPy arrays if necessary
                processed_value = process_value(value)
                group.create_dataset(key, data=processed_value)
            elif isinstance(value, (int, float, str, bytes, np.integer, np.floating)):
                # Encode strings and handle NumPy scalars
                group.create_dataset(key, data=process_value(value))
            else:
                raise ValueError(f"Unsupported data type: {type(value)} for key: {key}")

    with h5py.File(filename, 'w') as f:
        recurse(f, data)

def get_files_in(directory: str, extensions: list):
    files = [
        os.path.join(directory, file) for file in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, file)) and file.lower().endswith(tuple(extensions))
    ]
    return files

def extract_filetoken(path):
    token = os.path.splitext(os.path.basename(path))[0]
    if '.' not in token:
        return token
    return extract_filetoken(token)

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
    