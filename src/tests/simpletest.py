# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 14:08:51 2024

@author: mbmad
"""

import autosleap
import json


with open('K:/SLEAP-Autoanalysis/tests/settings.json','r') as file:
    settings = json.load(file)
    
settings['FR_ADJUST_ENABLED'] = False
asleap = autosleap.AutoAnalysis(**settings)

asleap.run(quit_on_idle=True)