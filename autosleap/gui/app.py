# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 17:48:39 2024

@author: mbmad
"""

from autosleap.gui.view import View

class App():
    def __init__(self):
        self.view = View()
        self.gui = self.view.gui
        
    def run(self):
        self.view.mainloop()