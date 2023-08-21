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

        - Program now remembers last cheevo active after restart
        - Settings dialog

        ------
        Log window 
        ------
        Ability to remember viewport last size and position
        Ability to fine tune viewport position and size from config.txt and preferences dialog
        Ability to preview size and position when tweaking values @ preferences menu
        Added preferences -> output -> style personalization tab placeholders
        Ability to open each stylesheet related to each output html file @ preferences
        ------------
        Perspective Personalization for widgets
        Progressbar personalization
"""
try: 
    from classes.ramon       import Ramon
    import os, sys
except ImportError:
    os.system('pip install requests beautifulsoup4 dearpygui pynput')
    os.system(f'pause')
    exit()

Ramon.start()
if Ramon.restart:
    import sys
    cmdline = " ".join(sys.argv)
    os.system(f'start {cmdline}')
