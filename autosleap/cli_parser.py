# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 14:27:34 2024

@author: mbmad
"""

import argparse
import json
import os
from autosleap.gui import App

from autosleap.metadata import __default_setting_values__, \
    __setting_types__
from autosleap import AutoAnalysis 

def main():
    parser = argparse.ArgumentParser(description='AUTOSleap, a mini application for SLEAP analysis')
    subparsers = parser.add_subparsers(dest='commands', required=True, help='commands')
    
    # new command
    new_parser = subparsers.add_parser('new', help='Create a new AutoSLEAP file')
    new_parser.add_argument('-f', '--file', type=str, required=True, help='Path to the file')
    
    # run command
    run_parser = subparsers.add_parser('run', help='Run AutoSLEAP analysis')
    run_parser.add_argument('-f', '--file', type=str, required=True, help='Path to the file')
    
    # wizard command
    wizard_parser = subparsers.add_parser('wizard', help='Open the AutoSLEAP wizard')
    
    args = parser.parse_args()
    
    if args.commands == 'new':
        print(f"Creating a new AutoSLEAP file with path: {args.file}.autosleap_config")
        try:
            with open('.'.join([args.file,'autosleap_config']), 'w') as file:
                json.dump(__default_setting_values__, file, indent = 4)
        except Exception as e:
            print(f'Failed to create AutoSLEAP due to {e}')
    elif args.commands == 'run':
        print(f"Running AutoSLEAP analysis for file: {args.file}.autosleap_config")
        try:
            with open('.'.join([args.file,'autosleap_config']), 'r') as file:
                data = json.load(file)
                check_file(data)
                analysis = AutoAnalysis(**data)
                analysis.run()
        except Exception as e:
            print(f'Failed to process AutoSLEAP due to {e}')
    elif args.commands == 'wizard':
        print("Opening the AutoSLEAP wizard...")
        App().run()
        
        
def check_file(data : dict):
    for setting in __default_setting_values__:
        if setting not in data:
            raise ValueError('Missing some required parameters in the *.autosleap file')
        if 'path' in __setting_types__[setting]:
            if not os.path.exists(data[setting]):
                raise FileNotFoundError(f'{data[setting]} does not exist')

if __name__ == '__main__':
    main()

    