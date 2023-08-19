"""
        CHANGES:
        - Added auto refresh feature on rendered output HTML files
        - Added global hotkey to force data refresh (CTRL+F5)
        - Added custom css files for every HTML generated file ( info will be embedded in the HTML output )

        ------
        - Code refactor
        - Added preferences module
        - Bugfix: Fixed unlocked achievements position calculation, now displays correctly
        ------
        
"""

import os, sys, time
try: 
    from dearpygui import dearpygui as dpg
    from classes.dynamic_css import DynamicCSS
    from classes.preferences import Preferences
    from classes.ramon       import Ramon
    from classes.cheevo      import Cheevo
except ImportError:
    os.system('pip install requests beautifulsoup4 dearpygui pynput cssbeautifier')
    exit()

Ramon.start()
if Ramon.restart:
    import sys
    cmdline = " ".join(sys.argv)
    os.system(f'start {cmdline}')
