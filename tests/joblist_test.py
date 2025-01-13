# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 16:32:13 2024

@author: mbmad
"""
import json

from autosleap import AutoAnalysis

with open('K:/SLEAP-Autoanalysis/tests/settings.json','r') as file:
    settings = json.load(file)
    
settings['FR_ADJUST_ENABLED'] = False
asleap = AutoAnalysis(**settings)

asleap.update_joblist()

print(asleap.joblist.list)