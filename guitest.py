# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 15:43:18 2024

@author: mbmad
"""

import json

from autosleap.gui.app import App

with open('K:/SLEAP-Autoanalysis/tests/settings.json','r') as file:
    settings = json.load(file)

settings['FR_ADJUST_ENABLED'] = False
app = App()
app.gui.settings_values = settings
app.gui.sync()
app.run()