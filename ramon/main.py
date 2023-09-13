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
---------------------
28-8-23
- Added ORM (pewee) to keep better tracking of which cheevos have been notified (planning doing a splash to display as OBS overlay)
- Turned Cheevo class into Model Class to interface the DB, added Game class
- Auto game data scraping ( name, picture and game_id )
- Now each cheevo has its own unique id, taken directly from RA id data
- Made a field in Game table to store which achievement is selected, so that attribute is 
    saved for next sessions, and if game changes it changes automatically :)
---------------------
30-8-23
- Ramon.collectNotifications() 
- Ramon.dumpNotifications() -> Dumps Js + HTML + CSS to a auto updating, show only once notification queue
- We may have to subdivide this into subclass
- But hell it will be cool to be able to show em in overlay instead of 
    being forced to use the embedded blocky Retroarch notifications, at expense of 
    having to manually update or waiting for autoupdate, delaying the realtime notification 
    when one achievement gets unlocked.
.........................
31-8-23 
- RetroAchievements.org status live monitorization in order to avoid useless unlocking, by handling failing request / bad parsing scenarios
- Plugin subsystem
- Plugin composite overlay output (all plugins are linked to a single file through iframes, allowing to keep sound playback permissions upon reloading)
- Plugin autodiscovery 
- Autogenerable compile script aimed to collect all plugins and make a trustable, monolithic app locally 
- Improved action feedback by using the title bar to report current status and avoid clearing the achievement list too early.
---------------------------
01-9-23
- Recent cheevos plugin
- Auto-updatable css styles in runtime, so any change made in preferences is reflected on plugins ( on recent only ftm )
- Preferences plugins tab
- Ability to enable / disable plugins (all disabled by default)
- Moved plugin settings (debug mode) to preferences dialog
- Ability for plugins to store and retrieve any setting seamlessly
- Offline mode, for debugging purposes, avoiding excesive queries to retroachievements at boot and faking some data 
- Plugin configuration auto generated tab per each plugin ( spartan but functional )
---------------------------
- Plugin configuration auto generated tab per each plugin, now fancier :P
- Fixed bug causing an error per plugin loaded if plugin.cfg didnt exist

"""
try: 
    import os, sys
    from classes.ramon          import Ramon
    from classes.plugin         import Plugin
    from classes.preferences    import Preferences
    from pathlib                import Path
except ImportError:
    os.system('pip install requests requests_toolbelt beautifulsoup4 dearpygui pynput peewee pyinstaller')
    os.system(f'pause')
    exit()

if Ramon.start():
    # load plugins
    Path('plugins.cfg').touch() # avoid error messages if file does not exist...
    for plugin in Ramon.plugins:
        Plugin.load( plugin )
    Preferences.populatePluginsTab()
    Preferences.updatePluginLists()
    # build plugin overlay, if any loaded
    if Preferences.settings['debug']:
        from dearpygui import dearpygui as D
        Preferences.show()
        D.set_value('preferences-tabs', 'tab_database')
        Plugin.debug = Preferences.settings['debug']    
    # enter main loop
    Ramon.render()
if Ramon.restart:
    import sys
    cmdline = " ".join(sys.argv)
    os.system(f'start {cmdline}')
