from dearpygui import dearpygui as WM
from classes.tools import Color, elegant

class row:
    label = 0
    input = 0

    def set(v):
        row.label = v
        row.input = v

class column:
    label = 0
    input = 0
    
    def set(v):
        column.label = v
        column.input = v

def pos(x,y):
    return (
        ( UI.column_width>>1) + (x if x is not None else (UI.columns[ column.input ])), 
        8 + (y if y is not None else (row.input * UI.row_height)),
    )

class UI:
    

    simple          = False
    column_width    = 300
    label_len       = int((column_width)/16)
    columns         = [ 8, 8+column_width, 8+(column_width*2) ]
    row_height      = 24

    def nop(sender, value, user_data):
        print( "NOP", sender, value, user_data )

   
    def label( text="A label", color=(255,255,0), x=None, y=None, left_align=False):
        
        WM.add_text(
            elegant(text).rjust(UI.label_len) if not left_align else text,
            pos     = (
                8 + (x if x is not None else UI.columns[ column.label ]), 
                8 + (y if y is not None else row.label * UI.row_height )
            ),
            color   = color,
        )
        column.label += 1 if x is None else 0
        row.label += 1 if y is None and x is not None else 0
        if column.label >= len(UI.columns):
            row.label += 1 
            column.label = 0
        return id
    
    def setColumnWidth(w):
        UI.column_width = w
        UI.label_len = int((UI.column_width)/16)

    def setCursor(x,y):
        column.set( x )
        row.set( y )

    def jump():
        UI.setCursor(0, row.input+1)
    
    def updateCursor(x,y):
        column.input += 1 if x is None else 0
        row.input    += 1 if y is None and x is not None else 0
        if column.input >= len(UI.columns): UI.jump()

    def textfield( text="A label", varname='a_var_name', x=None, y=None, callback=None, password=False, user_data=None, settings=None):
        from classes.preferences    import Preferences
        from classes.config         import help
        UI.label(text, Color.banana)
        id = WM.add_input_text(
            tag             = varname, 
            pos             = pos(x,y),
            default_value   = Preferences.settings[ varname ] if settings is None else settings[ varname ], 
            width           = UI.column_width>>1,
            password        = password,
            user_data       = user_data,
            callback        = Preferences.updateSetting if callback is None else callback,
        )
        if varname in help.keys():
            with WM.tooltip(varname):
                WM.add_text( help[ varname ] )
        UI.updateCursor(x,y)
        return id
    
    def combo( text="A label", varname='a_var_name', x=None, y=None, callback=None, password=False, user_data=None, items=[], settings=None):
        from classes.preferences    import Preferences
        from classes.config         import help
        settings = settings if settings is not None else Preferences.settings
        UI.label(text, Color.banana)
        
        default_value = settings[ varname ]
        
        # If value is separated by class combo separator, modify the value to match its corresponding valid items[] entry
        if isinstance( default_value, str ): 
            default_value = default_value if '|' not in default_value else default_value.split('|')[1]

        id = WM.add_combo(
                tag             = varname, 
                pos             = pos(x,y),
                default_value   = default_value,
                items           = list(items),
                width           = UI.column_width>>1,
                user_data       = user_data,
                callback        = Preferences.updateSetting if callback is None else callback,
            )            
        if varname in help.keys():
            with WM.tooltip(varname):
                WM.add_text( help[ varname ] )
        UI.updateCursor(x,y)
        return id

    def numeric( text="A label", varname='a_var_name', x=None, y=None, callback=None, user_data=None, settings=None):
        from classes.preferences    import Preferences
        from classes.config         import combos, ranges, help
        settings = settings if settings is not None else Preferences.settings
        if varname in combos:
            id = UI.combo(
                text            = text,
                varname         = varname,
                x               = x,
                y               = y,
                callback        = callback,
                user_data       = user_data,
                settings        = settings,
                items           = range( 
                    ranges[varname][0], 
                    ranges[varname][1]+1, 
                ),
            )
        else:
            UI.label(text, Color.banana)
            if isinstance( settings[ varname ], float ):
                id = WM.add_slider_float(
                    tag             = varname, 
                    pos             = pos(x,y),
                    default_value   = settings[varname],
                    width           = UI.column_width>>1,
                    min_value       = -100.0,
                    max_value       = 100.0,
                    user_data       = user_data,
                    callback        = Preferences.updateSetting if callback is None else callback,
                )
            elif isinstance( settings[ varname ], int):
                id = WM.add_slider_int(
                    tag             = varname, 
                    pos             = pos(x,y),
                    default_value   = settings[varname],
                    width           = UI.column_width>>1,
                    min_value       = -1444,
                    max_value       = 1444,
                    user_data       = user_data,
                    callback        = Preferences.updateSetting if callback is None else callback,
                )
            with WM.tooltip(varname):
                if varname in help.keys():
                    WM.add_text( help[ varname ] )            
                else:
                    WM.add_text( "Click + Ctrl to type a value" )

            UI.updateCursor(x,y)
        if varname.endswith('-size-y'): UI.jump()
        if varname.endswith('-perspective'): UI.jump()
        return id
    
    def checkbox( text="A label", varname='a_var_name', x=None, y=None, callback=None, enabled=True, user_data=None, settings=None):
        from classes.preferences    import Preferences
        from classes.config         import help
        UI.label(text, Color.banana)
        id = WM.add_checkbox(
            tag             = varname, 
            pos             = pos(x,y),
            default_value   = Preferences.settings[ varname ] if settings is None else settings[ varname ], 
            user_data       = user_data,
            callback        = Preferences.updateSetting if callback is None else callback,
        )
        if varname in help.keys():
            with WM.tooltip(varname):
                WM.add_text( help[ varname ] )
        if not enabled:
            WM.configure_item( varname, enabled=False )
        UI.updateCursor(x,y)
        return id
    