# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 19:50:50 2024

@author: mbmad
"""

import os

def resource_path(relative_path):
    """ Get the absolute path to a resource, works for packaged apps. """
    base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)