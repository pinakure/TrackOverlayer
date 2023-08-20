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
