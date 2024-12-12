# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 17:48:39 2024

@author: mbmad
"""

from dataclasses import dataclass
import threading

from autosleap.gui.view import View
from autosleap import AutoAnalysis

class GuiReporter():
    def __init__(self, gui_object, view):
        self.gui = gui_object
        self.state = 'Inactive'
        self.msg = None
        
    def job_print(self, msg, end = '\n', flush = True):
        self.gui.console_top.write(msg)
    
    def analysis_print(self, msg, end = '\n', flush = True):
        self.gui.console_bot.write(msg)
    
    def state_update(self, msg, end = '\n', flush = True):
        self.gui.wizard_state = msg
        self.state = msg
        self.gui.wizard_state_update(msg, self.msg)
    
    def jobs_remaining(self, msg, end = '\n', flush = True):
        self.gui.wizard_state_update(self.state, msg)


class App():
    def __init__(self):
        self.view = View()
        self.gui = self.view.gui
        self.reporter = GuiReporter(self.gui, self.view)
        self.gui.sync()
        self.autosleap = AutoAnalysis(reporter = self.reporter,
                                      **self.gui.settings_values)
        
        self.gui.run_button.config(command = self.toggle_autosleap)
        
    def run(self):
        self.view.mainloop()
    
    def toggle_autosleap(self):
        if self.gui.wizard_state == 'Inactive':
            autosleap_thread = threading.Thread(target = self.autosleap.run,
                                                daemon = True)
            autosleap_thread.start()
            self.gui.wizard_state == 'Active'
        elif self.gui.wizard_state == 'Active':
            self.autosleap.loopstate = 'Inactive'
            self.gui.wizard_state = 'Idle'

if __name__ == '__main__':
    App().run()