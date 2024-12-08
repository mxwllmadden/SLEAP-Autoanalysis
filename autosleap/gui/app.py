# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 17:48:39 2024

@author: mbmad
"""

from sleapy.gui.view import View

class App():
    def __init__(self):
        self.view = View()
        
    def run(self):
        self.view.mainloop()