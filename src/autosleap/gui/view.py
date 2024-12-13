# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 17:47:12 2024

@author: mbmad
"""

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from dataclasses import dataclass
from autosleap.metadata import __version__, __default_setting_keys__, \
    __default_setting_names__, __default_setting_values__,\
        __setting_types__, __project_structure__
from autosleap.files import resource_path
from autosleap.gui.widgets import ConsoleOutput
import os
import json
from PIL import Image, ImageTk

@dataclass
class GuiState:
    wizard_state = 'Inactive'
    wizard_state_update = None
    project_path = None
    project_strvar = None
    settings_strvars = {}
    settings_values = {}
    old_vals = {}
    run_button = None
    console_top = None
    console_bot = None
    
    def reset_settings(self, *event):
        for setting in __default_setting_keys__:
            self.settings_strvars[setting].set(__default_setting_values__[setting])
        self.sync()
            
    def sync(self, *event):
        for setting in __default_setting_keys__:
            if setting not in self.settings_values:
                self.settings_values[setting] = None
            if setting not in self.old_vals:
                self.old_vals[setting] = self.settings_values[setting]
        for setting, strvar in self.settings_strvars.items():
            value = strvar.get()
            if value != self.settings_values[setting]:
                if value == self.old_vals[setting]:
                    strvar.set(str(self.settings_values[setting]))
                else:
                    self.settings_values[setting] = value
                self.old_vals[setting] = self.settings_values[setting]
        if self.settings_values['FINAL_OUTPUT_FILE'] is None:
            return
        proj_path = os.path.dirname(self.settings_values['FINAL_OUTPUT_FILE'])
        paths_match = all([os.path.dirname(dir_path) == proj_path 
                           for setting, dir_path in self.settings_values.items()
                           if __setting_types__[setting] == 'projectpath'])
        if paths_match:
            self.project_path = proj_path
        else:
            self.project_path = None
        if self.project_strvar is not None:
            if self.project_path is None:
                self.project_strvar.set(
                    str('Custom Configuration (see Settings)'))
            else: 
                self.project_strvar.set(str(self.project_path))

class NoneBoolVar(tk.BooleanVar):
    def set(self, value):
        if value not in ['True','False', True, False]:
            value = False
        super().set(value)

class View:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f'SLEAP Wizard v{__version__} - SLEAP analysis wizard created by Maxwell Madden')
        self.root.geometry("1000x600")
        self.root.resizable(True, True)
        self.root.minsize(1000, 500)
        self.root.protocol('WM_DELTE_WINDOW',self._on_close)
        
        # Create GuiState to bundle everything i want access to from outside
        self.gui = GuiState()
        self.gui.wizard_state_update = self.update_state
        
        self._setup_view()
    
    def _on_close(self):
        os._exit(0)
    
    def mainloop(self):
        self.root.mainloop()
        
    def update_state(self, img_state, job_text):
        state_image_dict = {'Inactive' : 'icon128',
                            'Idle' : 'icon_idle128',
                            'Active' : 'icon_active128'}
        self.set_wizard_img(state_image_dict[img_state])
        self.status_strvar.set(job_text)
        self.gui.sync()
    
    def set_wizard_img(self, asset):
        """Set the wizard image dynamically."""
        self._wiz_img = self.load_asset(asset)
        self.wizard_label.config(image=self._wiz_img)
        self.wizard_label.image = self._wiz_img
    
    @staticmethod
    def load_asset(png):
        """Load an asset (image) from the assets folder."""
        try:
            # Open the image using Pillow
            image_path = resource_path(f"assets/{png}.png")
            img = Image.open(image_path)
            
            # Resize the image to 2 inches across, maintaining aspect ratio
            dpi = 96  # Assuming standard screen DPI
            width_in_pixels = int(2 * dpi)
            aspect_ratio = img.height / img.width
            height_in_pixels = int(width_in_pixels * aspect_ratio)
            
            resized_img = img.resize((width_in_pixels, height_in_pixels), Image.Resampling.LANCZOS)
            
            return ImageTk.PhotoImage(resized_img)
        except Exception as e:
            print(f"Error loading asset '{png}': {e}")
            return tk.PhotoImage()  # Placeholder if image fails
    
    @property
    def save_location(self):
        try:
            # Get the Local AppData folder
            local_appdata = os.getenv('LOCALAPPDATA')
            if not local_appdata:
                raise EnvironmentError("LOCALAPPDATA environment variable not found.")
            autosleap_folder = os.path.join(local_appdata, "AutoSLEAP")
            os.makedirs(autosleap_folder, exist_ok=True)
            file_path = os.path.join(autosleap_folder, 'wizard_settings.json')
            return file_path
    
        except Exception as e:
            print(f"Settings file unavailable! Error: {e}")
            return None
        
    def _create_project_paths(self):
        projdir = filedialog.askdirectory()
        if projdir is None:
            return
        def create_path(key, path):
            new_path = os.path.join(projdir,path)
            os.makedirs(new_path, exist_ok=True)
            self.settings_strvar[key].set(new_path)
        for key, value in __project_structure__.items():
            create_path(key, value)
        self.gui.sync()
        
    def _save_settings(self):
        print('Saving parameters...')
        self.gui.sync()
        try:
            with open(self.save_location, 'w') as json_file:
                json.dump(self.gui.settings_values, json_file, indent=4)
        except:
            print('Yikes! Something went wrong and I was unable to save!')
        print('Goodbye!')
        self.root.destroy()
    
    def _load_settings(self):
        print('Loading parameters...')
        try:
            with open(self.save_location, 'r') as json_file:
                data = json.load(json_file)
        except Exception as e:
            print(f"Settings file invalid! Error: {e}")
            return None
        for setting, value in data.items():
            if setting in __default_setting_keys__:
                self.gui.settings_strvars[setting].set(value)
    
    def _setsleapmodel_fdiag(self):
        file = filedialog.askopenfilename(
            title='Select a trained SLEAP model',
            filetypes=[('JSON files', '*.json')])
        if file is not None:
            self.settings_strvar['MODEL'].set(file)
            self.gui.sync()
    
    def _setup_view(self):
        # Set icon
        self.root.iconphoto(False, self.load_asset('icon64'))

        # Style
        style = ttk.Style(self.root)
        style.theme_use('clam')

        # Panel organization
        leftpanel = ttk.Notebook(self.root)
        rightpanel = ttk.Frame(self.root)
        leftpanel.pack(side='left', fill='both', expand=False)
        rightpanel.pack(side='right', fill='both', expand=True)

        # Notebook tabs
        fronttab = ttk.Frame(leftpanel)
        settingstab = ttk.Frame(leftpanel)
        leftpanel.add(fronttab, text='Wizard')
        leftpanel.add(settingstab, text='Settings')
        
        # Settings Setup
        self.gui.project_strvar = tk.StringVar()
        self.settings_strvar = {}
        row_offset = 1
        for ind, setting in enumerate(__default_setting_keys__):
            ind += row_offset
            ttk.Label(settingstab, text=__default_setting_names__[setting]
                      ).grid(column=0, row=ind * 2, sticky="w", padx=5)
            if isinstance(__default_setting_values__[setting], bool):
                self.settings_strvar[setting] = NoneBoolVar(
                    value=__default_setting_values__[setting])
                ttk.Checkbutton(settingstab, variable=self.settings_strvar[setting]
                                ).grid(column=0, row=ind * 2 + 1, sticky="w", padx=10)
            else:
                self.settings_strvar[setting] = tk.StringVar(
                    value=__default_setting_values__[setting])
                ttk.Entry(
                    settingstab, textvariable=self.settings_strvar[setting], width=50
                ).grid(column=0, row=ind * 2 + 1, sticky="w", padx=10)
        ttk.Button(settingstab, text = 'Reset Settings to Examples', command = self.gui.reset_settings
                   ).grid(row = 0, column = 0, sticky = 'w')
        self.gui.settings_strvars = self.settings_strvar

        # Wizard Tab setup
        for i in range(2):  
            fronttab.columnconfigure(i, weight=1)  
        self.wizard_label = ttk.Label(fronttab, anchor = 'center')
        self.wizard_label.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=2)
        self.set_wizard_img('icon128')
        self.status_strvar = tk.StringVar(value="Wizard is Sleeping (Inactive)")
        self.gui.status_strvar = self.status_strvar
        ttk.Label(fronttab, textvariable=self.status_strvar, anchor="center"
                  ).grid(row=1, column=0, columnspan=2, sticky="nsew", pady=2)
        ttk.Separator(fronttab, orient = 'horizontal'
                      ).grid(row = 2, column = 0, columnspan = 2, pady=5, sticky = 'nsew')
        ttk.Label(fronttab, anchor = 'center', text = 'SLEAP Wizard',
                  font=("Arial", 12, "bold")
                  ).grid(row = 3, column = 0, columnspan=2, sticky="nsew", pady=2)
        ttk.Label(fronttab, anchor = 'w', text = 'Current selected SLEAP model',
                  font = ('Arial', 10, 'underline')
                  ).grid(row = 4, column = 0, sticky = 'w', pady = 5)
        ttk.Label(fronttab, anchor = 'w', textvariable = self.settings_strvar['MODEL'],
                  wraplength=300
                  ).grid(row = 5, column = 0, sticky = 'w', pady = 5)
        ttk.Button(fronttab, text = 'Select Model', command = self._setsleapmodel_fdiag
                   ).grid(row = 5, column = 1, sticky = 'e', pady = 5)
        ttk.Label(fronttab, anchor = 'w', text = 'Current AutoSLEAP Wizard Project Folder',
                  font = ('Arial', 10, 'underline')
                  ).grid(row = 6, column = 0, sticky = 'w', pady = 5)
        ttk.Label(fronttab, anchor = 'w', textvariable = self.gui.project_strvar,
                  wraplength=300
                  ).grid(row = 7, column = 0, sticky = 'w', pady = 5)
        ttk.Button(fronttab, text = 'Select/Create Project', 
                   command= self._create_project_paths
                   ).grid(row = 7, column = 1, sticky = 'e', pady = 5)
        ttk.Separator(fronttab, orient = 'horizontal'
                      ).grid(row = 8, column = 0, columnspan = 2, pady=5, sticky = 'nsew')
        self.run_button = ttk.Button(fronttab, text='BEGIN PROCESSING')
        self.run_button.grid(row=9, column=0, columnspan = 2, sticky='nsew', pady=5)
        self.gui.run_button = self.run_button
        
        console_top = ConsoleOutput(rightpanel)
        console_bot = ConsoleOutput(rightpanel, textcolor = '#FFA500')
        console_top.pack(side = 'top', fill = 'both', expand = True)
        console_bot.pack(side = 'bottom', fill = 'both', expand = True)
        console_top.write("This is the job feed. You will see the output from the current job here")
        console_bot.write("This is the wizard feed. You will see less verbose logging in this window.")
        self.gui.console_top = console_top
        self.gui.console_bot = console_bot
        
        # Misc Bindings
        leftpanel.bind('<<NotebookTabChanged>>', self.gui.sync)
        self.root.protocol("WM_DELETE_WINDOW", self._save_settings)
        
        # Sync before running
        self._load_settings()
        self.gui.sync()

    


if __name__ == '__main__':
    View().mainloop()
