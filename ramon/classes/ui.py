from dearpygui import dearpygui as WM
from classes.tools import Color, elegant




class Layout:

    def __init__(self, columns):
        from classes.ramon import Ramon
        self.fields         = []
        self.labels         = []
        self.columns        = []
        self.column_count   = columns
        self.column_width   = int(Ramon.inner_width / self.column_count)
        self.current_column = 0
        ix = 8
        for i in range(0, self.column_count):
            self.columns.append( ix )
            ix += self.column_width
            self.fields.append([])
            self.labels.append([])

    def add(self, field):
        label = UI.last_label
        self.fields.append(field)
        self.labels.append(label)
        self.current_column += 1
        self.current_column %= self.column_count
        
    def resize(self):
        from classes.ramon import Ramon
        self.column_width   = int(Ramon.inner_width / self.column_count)
        from dearpygui import dearpygui as dpg
        for i in range(0, len(self.columns)):
            # Move labels
            labels = self.fields[i]
            for label in labels:
                x = self.columns[i]
                y = dpg.get_item_pos(label)[1]
                dpg.configure_item(label, pos=(x,y))
            # Move fields
            fields = self.fields[i]
            for field in fields:
                x = self.columns[i] + int(self.column_width / 2)
                y = dpg.get_item_pos(field)[1]
                dpg.configure_item(field, pos=(x,y))
            

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
    last_label      = None
    layouts         = []
    layout          = None

    def nop(sender, value, user_data):
        print( "NOP", sender, value, user_data )

    def label( text="A label", color=(255,255,0), x=None, y=None, left_align=False):
        
        UI.last_label = WM.add_text(
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
    
    def resize():
        for layout in UI.layouts:
            layout.resize()

    def setColumns(count, width):
        column.label = 0
        column.input = 0
        last_width = UI.setColumnWidth(width)
        last_count = UI.setColumnCount(count)
        return last_width,last_count

    def setColumnCount(c):
        last_count = len(UI.columns)
        UI.columns = [ 8+(x*UI.column_width) for x in range(0,c) ]
        return last_count
        
    def setColumnWidth(w):
        last_width = UI.column_width
        UI.column_width = int(w)
        UI.label_len = int((UI.column_width)/16)
        return last_width

    def setCursor(x,y):
        column.set( x )
        row.set( y )

    def jump():
        UI.setCursor(0, row.input+1)
    
    def updateCursor(x,y, varname):
        if UI.layout:
            UI.layout.add(varname)        
        column.input += 1 if x is None else 0
        row.input    += 1 if y is None and x is not None else 0
        if column.input >= len(UI.columns): UI.jump()

    def textfield( text="A label", varname='a_var_name', x=None, y=None, callback=None, password=False, user_data=None, settings=None, on_enter=False, readonly=False):
        from classes.preferences    import Preferences
        from classes.config         import help
        UI.label(text, Color.banana)
        settings = Preferences.settings if settings is None else settings
        id = WM.add_input_text(
            tag             = varname, 
            pos             = pos(x,y),
            default_value   = settings[ varname ] if varname in settings.keys() else '', 
            width           = UI.column_width>>1,
            password        = password,
            user_data       = user_data,
            callback        = Preferences.updateSetting if callback is None else callback,
            on_enter        = on_enter,
            readonly        = readonly,
        )
        if varname in help.keys():
            with WM.tooltip(varname):
                WM.add_text( help[ varname ] )
        UI.updateCursor(x,y, varname)
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
        UI.updateCursor(x,y, varname)
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
                [ min, max ] = [-100.0,  100.0 ] if not varname in ranges.keys() else range[varname]
                id = WM.add_slider_float(
                    tag             = varname, 
                    pos             = pos(x,y),
                    default_value   = settings[varname],
                    width           = UI.column_width>>1,
                    min_value       = min,
                    max_value       = max,
                    user_data       = user_data,
                    callback        = Preferences.updateSetting if callback is None else callback,
                )
            elif isinstance( settings[ varname ], int):
                [ min, max ] = [-1444,  1444 ] if not varname in ranges.keys() else ranges[varname]
                id = WM.add_slider_int(
                    tag             = varname, 
                    pos             = pos(x,y),
                    default_value   = settings[varname],
                    width           = UI.column_width>>1,
                    min_value       = min,
                    max_value       = max,
                    user_data       = user_data,
                    callback        = Preferences.updateSetting if callback is None else callback,
                )
            with WM.tooltip(varname):
                if varname in help.keys():
                    WM.add_text( help[ varname ] )            
                else:
                    WM.add_text( "Click + Ctrl to type a value" )

            UI.updateCursor(x,y, varname)
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
        UI.updateCursor(x,y, varname)
        return id
    