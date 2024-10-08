#from classes.collections    import Collections
from dearpygui              import dearpygui as D
from classes.tools          import elegant

#HACK:not-proud-of-this-class 

class Attribute:
    groupname   = ''
    group       = ''
    groupname   = ''  
    types       = {}  
    sizes       = {}  
    heights     = {}  
    italics     = {}  
    bolds       = {}  
    shadows     = {}  
    posxs       = {}  
    posys       = {}  
    blurs       = {}
    plugin      = {}
    bcolors     = {}
    bwidths     = {}
    sposxs      = {}
    sposys      = {}
    bradius     = {}
    sizexs      = {}
    sizeys      = {}

    def setup( groupname, group, types, name, sizes, heights, italics, bolds, shadows, posxs, posys, blurs,  bcolors, bwidths, sposxs, sposys, bradius, sizexs, sizeys ):
        Attribute.name          = name
        Attribute.group         = group
        Attribute.groupname     = groupname
        Attribute.types         = types
        Attribute.sizes         = sizes
        Attribute.heights       = heights
        Attribute.italics       = italics
        Attribute.bolds         = bolds
        Attribute.shadows       = shadows
        Attribute.posxs         = posxs
        Attribute.posys         = posys
        Attribute.blurs         = blurs
        Attribute.bcolors       = bcolors
        Attribute.bwidths       = bwidths
        Attribute.sposxs        = sposxs
        Attribute.sposys        = sposys
        Attribute.bradius       = bradius
        Attribute.sizexs        = sizexs
        Attribute.sizeys        = sizeys

    def label( x=0, y=0, text="A label", color=(255,255,0), parent=None):
        D.add_text(
            text,
            pos     = (x, y),
            color   = color,
            parent  = parent if parent is not None else Attribute.parent
        )

    def color( x, y, color, callback=None):
        D.add_color_picker(
            tag             = f'{Attribute.group}-color', 
            default_value   = (0, 0, 0, 255),
            callback        = callback, 
            user_data       = Attribute.name, 
            width           = 200, 
            height          = 32, 
            no_side_preview = True, 
            no_small_preview= True, 
            no_inputs       = True, 
            alpha_bar       = True, 
            picker_mode     = D.mvColorPicker_wheel,
            display_type    = D.mvColorEdit_uint8,
            pos             = (x,y),
        )
        D.set_value(f'{Attribute.group}-color', color)

    def boolean( x, y, name, value, callback=None):
        from classes.ui import UI
        varname = f'plugin-setting-{Attribute.plugin}-{name}'
        UI.checkbox(
            text            = name, 
            varname         = varname,
            callback        = callback,
            user_data       = name,
            settings        = { varname : value },
        )

    #
    # Class defined combo, to use this define a static dictionary in your plugin class, then 
    # define the value of the field as 'dict_name:dic_key', so when rendering it will turn into 
    # a combo. 
    #     
    # Obviously, its forbidden to enter this char in any text field to avoid data corruption
    # 
    def combo( x, y, name, value, parent=None, callback=None):
        from classes.ui     import UI
        exec(f'from plugins.{Attribute.plugin} import plugin as {Attribute.plugin}')
        items = eval(f'{Attribute.plugin}.plugin.{value.split("|")[0]}.keys()')
        varname = f'plugin-setting-{Attribute.plugin}-{name}'
        UI.combo(
            text            = name, 
            varname         = varname,
            callback        = callback,
            user_data       = f'{value.split("|")[0]}|{name}',
            settings        = { varname : value },
            items           = list(items),
        )

    def filename( x, y, name, value, parent=None, callback=None):
        from classes.ui     import UI, row as UI_row, column as UI_column
        from classes.tools  import Color
        exec(f'from plugins.{Attribute.plugin} import plugin as {Attribute.plugin}')
        varname = f'plugin-setting-{Attribute.plugin}-{name}'
        UI.label(elegant(name), Color.banana)
        D.add_button(
            tag             = varname,
            label           = value,
            callback        = callback,
            user_data       = varname,
            width           = UI.column_width/2,
            pos             = (
                (UI.column_width/2)+UI.columns[UI_column.input], 
                8+(UI_row.input*UI.row_height)
            ),
        )
        UI.updateCursor(None, None)
        
    def integer( x, y, name, value, parent=None, negative=False, max_value=128, callback=None):
        from classes.ui import UI
        varname = f'plugin-setting-{Attribute.plugin}-{name}'
        UI.numeric(
            text            = name, 
            varname         = varname,
            callback        = callback,
            user_data       = name,
            settings        = { varname : value },
        )
    
    def text( x, y, name, value, callback=None):
        from classes.ui import UI
        varname = f'plugin-setting-{Attribute.plugin}-{name}'
        UI.textfield(
            text            = name, 
            varname         = varname,
            callback        = callback,
            user_data       = name,
            settings        = { varname : value },
        )

    def font( x, y,callback=None):
        from classes.ui     import UI
        from classes.fonts  import fonts
        if not f'{Attribute.groupname}-font' in Attribute.types.keys(): return
        varname = f'{Attribute.group}-font'
        D.add_combo(
            tag             = varname,
            items           = list(fonts.keys()), 
            callback        = callback, 
            user_data       = f'{Attribute.groupname}-font', 
            default_value   = Attribute.types[f'{Attribute.groupname}-font'],
            pos             = (x,y),
            width           = 95,
        )

    def font_size( x, y ,callback=None):
        if not f'{Attribute.groupname}-font-size' in Attribute.sizes.keys(): return
        D.add_combo(
            tag             = f'{Attribute.group}-font-size',
            items           = list(range(1, 256)), 
            callback        = callback, 
            user_data       = f'{Attribute.groupname}-font-size', 
            default_value   = Attribute.sizes[f'{Attribute.groupname}-font-size'],
            pos             = (x, y),
            width           = 40,
        )
        with D.tooltip(f'{Attribute.group}-font-size'): 
            D.add_text("Font Size")

    def line_height( x, y ,callback=None):
        if not f'{Attribute.groupname}-line-height' in Attribute.heights.keys(): return
        D.add_combo(
            tag             = f'{Attribute.group}-line-height',
            items           = list(range(0, 256)),
            callback        = callback,
            user_data       = f'{Attribute.groupname}-line-height', 
            default_value   = Attribute.heights[f'{Attribute.groupname}-line-height'],
            pos             = (x, y),
            width           = 40,
        )
        with D.tooltip(f'{Attribute.group}-line-height'): 
            D.add_text("Line Height")

    def italic( x, y ,callback=None):
        if not f'{Attribute.groupname}-font-italic' in Attribute.italics.keys(): return
        D.add_checkbox(
            tag             = f'{Attribute.group}-font-italic',
            callback        = callback,
            user_data       = f'{Attribute.groupname}-font-italic', 
            default_value   = Attribute.italics[f'{Attribute.groupname}-font-italic'],
            pos             = (x, y),                                                    
        )
        with D.tooltip(f'{Attribute.group}-font-italic'):
            D.add_text("Italic")

    def bold( x, y ,callback=None):
        if not f'{Attribute.groupname}-font-bold' in Attribute.bolds.keys(): return
        D.add_checkbox(
            tag             = f'{Attribute.group}-font-bold',
            callback        = callback,
            user_data       = f'{Attribute.groupname}-font-bold', 
            default_value   = Attribute.bolds[f'{Attribute.groupname}-font-bold'],
            pos             = (x, y),                                                    
        )
        with D.tooltip(f'{Attribute.group}-font-bold'):
            D.add_text("Bold")
    def shadow( x, y ,callback=None):
        if not f'{Attribute.groupname}-shadow-color' in Attribute.shadows.keys(): return
        D.add_color_picker(
            tag             = f'{Attribute.group}-shadow-color', 
            default_value   = (0, 0, 0, 255),
            callback        = callback, 
            user_data       = f'{Attribute.groupname}-shadow-color', 
            width           = 140, 
            height          = 140, 
            no_side_preview = True, 
            no_small_preview= True, 
            no_inputs       = True, 
            alpha_bar       = True, 
            picker_mode     = D.mvColorPicker_bar,
            display_type    = D.mvColorEdit_uint8,
            pos             = (x, y),
        )
        with D.tooltip(f'{Attribute.group}-shadow-color'): 
            D.add_text("Shadow Color")
        D.set_value(f'{Attribute.group}-shadow-color', Attribute.shadows[f'{Attribute.groupname}-shadow-color'])
    
    def pos_x( x, y ,callback=None):
        if not f'{Attribute.groupname}-pos-x' in Attribute.posxs.keys(): return
        D.add_slider_int(
            tag             = f'{Attribute.group}-pos-x',
            callback        = callback,
            user_data       = f'{Attribute.groupname}-pos-x', 
            default_value   = Attribute.posxs[f'{Attribute.groupname}-pos-x'],
            pos             = (x, y),
            max_value       = 2048,
            min_value       = -2048,
            width           = 172,
        )
        with D.tooltip(f'{Attribute.group}-pos-x'): 
            D.add_text("Horizontal Position\n( Ctrl + Click to edit value )")
    
    def size_x( x, y ,callback=None):
        if not f'{Attribute.groupname}-size-x' in Attribute.sizexs.keys(): return
        D.add_slider_int(
            tag             = f'{Attribute.group}-size-x',
            callback        = callback,
            user_data       = f'{Attribute.groupname}-size-x', 
            default_value   = Attribute.sizexs[f'{Attribute.groupname}-size-x'],
            pos             = (x, y),
            max_value       = 2048,
            min_value       = -2048,
            width           = 172,
        )
        with D.tooltip(f'{Attribute.group}-size-x'):
            D.add_text("Horizontal Size\n( Ctrl + Click to edit value )")
    
    def pos_y( x, y ,callback=None):
        if not f'{Attribute.groupname}-pos-y' in Attribute.posys.keys(): return
        D.add_slider_int(
            tag             = f'{Attribute.group}-pos-y',
            callback        = callback,
            user_data       = f'{Attribute.groupname}-pos-y', 
            default_value   = Attribute.posys[f'{Attribute.groupname}-pos-y'],
            pos             = (x, y),
            max_value       = 2048,
            min_value       = -2048,
            width           = 172,            
        )
        with D.tooltip(f'{Attribute.group}-pos-y'): 
            D.add_text("Vertical Position\n( Ctrl + Click to edit value )")
    
    def size_y( x, y ,callback=None):
        if not f'{Attribute.groupname}-size-y' in Attribute.sizeys.keys(): return
        D.add_slider_int(
            tag             = f'{Attribute.group}-size-y',
            callback        = callback,
            user_data       = f'{Attribute.groupname}-size-y', 
            default_value   = Attribute.sizeys[f'{Attribute.groupname}-size-y'],
            pos             = (x, y),
            max_value       = 2048,
            min_value       = -2048,
            width           = 172,
        )
        with D.tooltip(f'{Attribute.group}-size-y'):
            D.add_text("Vertical Size\n( Ctrl + Click to edit value )")
    
    def shadow_pos_x( x, y ,callback=None):
        if not f'{Attribute.groupname}-shadow-pos-x' in Attribute.sposxs.keys(): return
        D.add_combo(
            tag             = f'{Attribute.group}-shadow-pos-x',
            items           = list(range(-32, 32)),
            callback        = callback,
            user_data       = f'{Attribute.groupname}-shadow-pos-x', 
            default_value   = Attribute.sposxs[f'{Attribute.groupname}-shadow-pos-x'],
            pos             = (x, y),
            width           = 64,
        )
        with D.tooltip(f'{Attribute.group}-shadow-pos-x'): 
            D.add_text("Shadow X Position")
    
    def shadow_pos_y( x, y ,callback=None):
        if not f'{Attribute.groupname}-shadow-pos-y' in Attribute.sposys.keys(): return
        D.add_combo(
            tag             = f'{Attribute.group}-shadow-pos-y',
            items           = list(range(-32, 32)),
            callback        = callback,
            user_data       = f'{Attribute.groupname}-shadow-pos-y', 
            default_value   = Attribute.sposys[f'{Attribute.groupname}-shadow-pos-y'],
            pos             = (x, y),
            width           = 64,
        )
        with D.tooltip(f'{Attribute.group}-shadow-pos-y'): 
            D.add_text("Shadow Y Offset")
    
    def shadow_blur( x, y ,callback=None):
        if not f'{Attribute.groupname}-shadow-blur' in Attribute.blurs.keys(): return
        D.add_combo(
            tag             = f'{Attribute.group}-shadow-blur',
            items           = list(range(0, 80)),
            callback        = callback,
            user_data       = f'{Attribute.groupname}-shadow-blur', 
            default_value   = Attribute.blurs[f'{Attribute.groupname}-shadow-blur'],
            pos             = (x, y),
            width           = 64,
        )
        with D.tooltip(f'{Attribute.group}-shadow-blur'): 
            D.add_text("Shadow Blur")
    
    def border_width( x, y ,callback=None):
        if not f'{Attribute.groupname}-border-width' in Attribute.bwidths.keys(): return
        D.add_combo(
            tag             = f'{Attribute.group}-border-width',
            items           = list(range(0, 80)),
            callback        = callback,
            user_data       = f'{Attribute.groupname}-border-width', 
            default_value   = Attribute.bwidths[f'{Attribute.groupname}-border-width'],
            pos             = (x, y),
            width           = 64,
        )
        with D.tooltip(f'{Attribute.group}-border-width'): 
            D.add_text("Border Width")

    def border_radius( x, y ,callback=None):
        if not f'{Attribute.groupname}-border-radius' in Attribute.bradius.keys(): return
        D.add_combo(
            tag             = f'{Attribute.group}-border-radius',
            items           = list(range(0, 128)),
            callback        = callback,
            user_data       = f'{Attribute.groupname}-border-radius', 
            default_value   = Attribute.bradius[f'{Attribute.groupname}-border-radius'],
            pos             = (x, y),
            width           = 64,
        )
        with D.tooltip(f'{Attribute.group}-border-radius'): 
            D.add_text("Border Radius")
    
    def border_color( x, y ,callback=None):
        if not f'{Attribute.groupname}-border-color' in Attribute.bcolors.keys(): return
        D.add_color_picker(
            tag             = f'{Attribute.group}-border-color', 
            default_value   = (0, 0, 0, 255),
            callback        = callback, 
            user_data       = f'{Attribute.groupname}-border-color', 
            width           = 140, 
            height          = 140, 
            no_side_preview = True, 
            no_small_preview= True, 
            no_inputs       = True, 
            alpha_bar       = True, 
            picker_mode     = D.mvColorPicker_bar,
            display_type    = D.mvColorEdit_uint8,
            pos             = (x, y),
        )
        with D.tooltip(f'{Attribute.group}-border-color'): 
            D.add_text("Border Color")
        D.set_value(f'{Attribute.group}-border-color', Attribute.bcolors[f'{Attribute.groupname}-border-color'])
    
