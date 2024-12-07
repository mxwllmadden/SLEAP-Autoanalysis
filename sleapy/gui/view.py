# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 17:47:12 2024

@author: mbmad
"""

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from sleapy import __version__, __default_setting_keys__, \
    __default_setting_names__, __default_setting_values__
from sleapy.utils import resource_path
from sleapy.gui.widgets import ConsoleOutput
import os

class View:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f'SLEAPy Wizard v{__version__} - SLEAP analysis wizard created by Maxwell Madden')
        self.root.geometry("1000x500")
        self.root.resizable(True, True)
        self.root.minsize(1000, 500)

        # Set icon
        self.root.iconphoto(False, self.load_asset('icon64'))

        # Style
        style = ttk.Style(self.root)
        style.theme_use('clam')

        # Panel organization
        leftpanel = ttk.Notebook(self.root)
        rightpanel = ttk.Frame(self.root)
        leftpanel.pack(side='left', fill='both', expand=True)
        rightpanel.pack(side='right', fill='both', expand=True)

        # Notebook tabs
        fronttab = ttk.Frame(leftpanel)
        settingstab = ttk.Frame(leftpanel)
        leftpanel.add(fronttab, text='Wizard')
        leftpanel.add(settingstab, text='Detailed Settings')
        
        # Settings Setup
        self.proj_path = None
        self.proj_path_strvar = tk.StringVar()
        self.settings_strvar = {}
        for ind, setting in enumerate(__default_setting_keys__):
            ttk.Label(settingstab, text=__default_setting_names__[setting]
                      ).grid(column=0, row=ind * 2, sticky="w", padx=5)
            if isinstance(__default_setting_values__[setting], bool):
                self.settings_strvar[setting] = tk.BooleanVar(
                    value=__default_setting_values__[setting])
                ttk.Checkbutton(settingstab, variable=self.settings_strvar[setting]
                                ).grid(column=0, row=ind * 2 + 1, sticky="w", padx=10)
            else:
                self.settings_strvar[setting] = tk.StringVar(
                    value=__default_setting_values__[setting])
                ttk.Entry(
                    settingstab, textvariable=self.settings_strvar[setting], width=50
                ).grid(column=0, row=ind * 2 + 1, sticky="w", padx=10)

        # Wizard Tab setup
        for i in range(2):  
            fronttab.columnconfigure(i, weight=1)  
        self.wizard_label = ttk.Label(fronttab, anchor = 'center')
        self.wizard_label.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=2)
        self.set_wizard_img('icon128')
        self.status_strvar = tk.StringVar(value="Wizard is Sleeping (Inactive)")
        ttk.Label(fronttab, textvariable=self.status_strvar, anchor="center"
                  ).grid(row=1, column=0, columnspan=2, sticky="nsew", pady=2)
        ttk.Separator(fronttab, orient = 'horizontal'
                      ).grid(row = 2, column = 0, columnspan = 2, pady=5, sticky = 'nsew')
        ttk.Label(fronttab, anchor = 'center', text = 'SLEAPy Wizard',
                  font=("Arial", 12, "bold")
                  ).grid(row = 3, column = 0, columnspan=2, sticky="nsew", pady=2)
        ttk.Label(fronttab, anchor = 'w', text = 'Current selected SLEAP model',
                  font = ('Arial', 10, 'underline')
                  ).grid(row = 4, column = 0, sticky = 'w', pady = 5)
        ttk.Label(fronttab, anchor = 'w', textvariable = self.settings_strvar['SLEAP']
                  ).grid(row = 5, column = 0, sticky = 'w', pady = 5)
        ttk.Button(fronttab, text = 'Select Model', command = self._setsleapmodel_fdiag
                   ).grid(row = 5, column = 1, sticky = 'e', pady = 5)
        ttk.Label(fronttab, anchor = 'w', text = 'Current SLEAPy Automated Project Folder',
                  font = ('Arial', 10, 'underline')
                  ).grid(row = 6, column = 0, sticky = 'w', pady = 5)
        ttk.Label(fronttab, anchor = 'w', textvariable = self.proj_path_strvar
                  ).grid(row = 7, column = 0, sticky = 'w', pady = 5)
        ttk.Button(fronttab, text = 'Select/Create Project', 
                   command= self._create_project_paths
                   ).grid(row = 7, column = 1, sticky = 'e', pady = 5)
    
    def _create_project_paths(self):
        projdir = filedialog.askdirectory()
        if projdir is None:
            return
        def create_path(key, path):
            new_path = os.path.join(projdir,path)
            os.makedirs(new_path, exist_ok=True)
            self.settings_strvar[key].set(new_path)
        create_path('VIDEO_SOURCE', 'untranscoded_video')
        create_path('VIDEO_TRANSCODED', 'transcoded_video')
        create_path('PREDICTIONS', 'predictionfiles')
        create_path('H5', 'h5_files')
        create_path('FR_ADJUSTED', 'framerate_adjusted_trajectories')
    
    def _save_settings(self):
        pass
    
    def _load_settings(self):
        pass
    
    def _setsleapmodel_fdiag(self):
        filedialog.askopenfilename(
            title='Select a trained SLEAP model',
            filetypes=[('JSON files', '*.json')])

    def set_wizard_img(self, asset):
        """Set the wizard image dynamically."""
        self._wiz_img = self.load_asset(asset)
        self.wizard_label.config(image=self._wiz_img)

    @staticmethod
    def load_asset(png):
        """Load an asset (image) from the assets folder."""
        try:
            return tk.PhotoImage(file=resource_path(f"assets/{png}.png"))
        except tk.TclError as e:
            print(f"Error loading asset '{png}': {e}")
            return tk.PhotoImage()  # Placeholder if image fails

    def mainloop(self):
        self.root.mainloop()


if __name__ == '__main__':
    View().mainloop()
