from classes.plugin         import Plugin
from dearpygui              import dearpygui as D

def elegant( filthy ):
    # TODO: move to tools
    return filthy.replace('_', ' ').replace('-', ' ').capitalize()

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

    def setup( groupname, group, types, name, sizes, heights, italics, bolds, shadows, posxs, posys, blurs,  bcolors, bwidths, sposxs, sposys, bradius ):
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

    def label( x=0, y=0, text="A label", color=(255,255,0), parent=None):
        D.add_text(
            text,
            pos     = (x, y),
            color   = color,
            parent  = parent if parent is not None else Attribute.parent
        )

    def color( x, y, color):
        D.add_color_picker(
            tag             = f'{Attribute.group}-color', 
            default_value   = (0, 0, 0, 255),
            callback        = Plugin.updateColor, 
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

    def boolean( x, y, name, value):
        D.add_checkbox(
            tag             = f'plugin-setting-{Attribute.plugin}-{name}', 
            default_value   = value, 
            callback        = Plugin.updateSettings, 
            user_data       = name,
            pos             = (x, y),
        )
    
    def integer( x, y, name, value, parent=None, negative=False, max_value=128):
        slider = D.add_slider_int(
            tag             = f'plugin-setting-{Attribute.plugin}-{name}',
            default_value   = value, 
            callback        = Plugin.updateSettings, 
            user_data       = name,
            width           = 180,
            pos             = (x, y), 
            parent          = parent if parent is not None else Attribute.parent,
            min_value       = -max_value if negative else 0,
            max_value       = max_value,
        )
        with D.tooltip(slider): 
            D.add_text("Ctrl + Click to edit value")
        
    
    def text( x, y, name, value):
        D.add_input_text(
            tag             = f'plugin-setting-{Attribute.plugin}-{name}',
            default_value   = value,
            callback        = Plugin.updateSettings,
            user_data       = name,
            width           = 180,
            pos             = (x, y), 
        )

    def font( x, y):
        from classes.dynamic_css import fonts
        if not f'{Attribute.groupname}-font' in Attribute.types.keys(): return
        D.add_combo(
            tag             = f'{Attribute.group}-font',
            items           = list(fonts.keys()), 
            callback        = Plugin.updateSettings, 
            user_data       = f'{Attribute.groupname}-font', 
            default_value   = Attribute.types[f'{Attribute.groupname}-font'],
            pos             = (x,y),
            width           = 95,
        )

    def font_size( x, y):
        if not f'{Attribute.groupname}-font-size' in Attribute.sizes.keys(): return
        D.add_combo(
            tag             = f'{Attribute.group}-font-size',
            items           = list(range(1, 256)), 
            callback        = Plugin.updateSettings, 
            user_data       = f'{Attribute.groupname}-font-size', 
            default_value   = Attribute.sizes[f'{Attribute.groupname}-font-size'],
            pos             = (x, y),
            width           = 40,
        )
        with D.tooltip(f'{Attribute.group}-font-size'): 
            D.add_text("Font Size")

    def line_height( x, y):
        if not f'{Attribute.groupname}-line-height' in Attribute.heights.keys(): return
        D.add_combo(
            tag             = f'{Attribute.group}-line-height',
            items           = list(range(0, 256)),
            callback        = Plugin.updateSettings,
            user_data       = f'{Attribute.groupname}-line-height', 
            default_value   = Attribute.heights[f'{Attribute.groupname}-line-height'],
            pos             = (x, y),
            width           = 40,
        )
        with D.tooltip(f'{Attribute.group}-line-height'): 
            D.add_text("Line Height")

    def italic( x, y ):
        if not f'{Attribute.groupname}-font-italic' in Attribute.italics.keys(): return
        D.add_checkbox(
            tag             = f'{Attribute.group}-font-italic',
            callback        = Plugin.updateSettings,
            user_data       = f'{Attribute.groupname}-font-italic', 
            default_value   = Attribute.italics[f'{Attribute.groupname}-font-italic'],
            pos             = (x, y),                                                    
        )
        with D.tooltip(f'{Attribute.group}-font-italic'):
            D.add_text("Italic")

    def bold( x, y ):
        if not f'{Attribute.groupname}-font-bold' in Attribute.bolds.keys(): return
        D.add_checkbox(
            tag             = f'{Attribute.group}-font-bold',
            callback        = Plugin.updateSettings,
            user_data       = f'{Attribute.groupname}-font-bold', 
            default_value   = Attribute.bolds[f'{Attribute.groupname}-font-bold'],
            pos             = (x, y),                                                    
        )
        with D.tooltip(f'{Attribute.group}-font-bold'):
            D.add_text("Bold")
    def shadow( x, y ):
        if not f'{Attribute.groupname}-shadow' in Attribute.shadows.keys(): return
        D.add_color_picker(
            tag             = f'{Attribute.group}-shadow', 
            default_value   = (0, 0, 0, 255),
            callback        = Plugin.updateColor, 
            user_data       = f'{Attribute.groupname}-shadow', 
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
        with D.tooltip(f'{Attribute.group}-shadow'): 
            D.add_text("Shadow Color")
        D.set_value(f'{Attribute.group}-shadow', Attribute.shadows[f'{Attribute.groupname}-shadow'])
    
    def pos_x( x, y ):
        if not f'{Attribute.groupname}-pos-x' in Attribute.posxs.keys(): return
        D.add_slider_int(
            tag             = f'{Attribute.group}-pos-x',
            callback        = Plugin.updateSettings,
            user_data       = f'{Attribute.groupname}-pos-x', 
            default_value   = Attribute.posxs[f'{Attribute.groupname}-pos-x'],
            pos             = (x, y),
            max_value       = 9999,
            min_value       = -9999,
            width           = 172,
        )
        with D.tooltip(f'{Attribute.group}-pos-x'): 
            D.add_text("Horizontal Position\n( Ctrl + Click to edit value )")
    
    def pos_y( x, y ):
        if not f'{Attribute.groupname}-pos-y' in Attribute.posys.keys(): return
        D.add_slider_int(
            tag             = f'{Attribute.group}-pos-y',
            callback        = Plugin.updateSettings,
            user_data       = f'{Attribute.groupname}-pos-y', 
            default_value   = Attribute.posys[f'{Attribute.groupname}-pos-y'],
            pos             = (x, y),
            max_value       = 9999,
            min_value       = -9999,
            width           = 172,            
        )
        with D.tooltip(f'{Attribute.group}-pos-y'): 
            D.add_text("Vertical Position\n( Ctrl + Click to edit value )")
    
    def shadow_pos_x( x, y ):
        if not f'{Attribute.groupname}-shadow-pos-x' in Attribute.sposxs.keys(): return
        D.add_combo(
            tag             = f'{Attribute.group}-shadow-pos-x',
            items           = list(range(-32, 32)),
            callback        = Plugin.updateSettings,
            user_data       = f'{Attribute.groupname}-shadow-pos-x', 
            default_value   = Attribute.sposxs[f'{Attribute.groupname}-shadow-pos-x'],
            pos             = (x, y),
            width           = 64,
        )
        with D.tooltip(f'{Attribute.group}-shadow-pos-x'): 
            D.add_text("Shadow X Position")
    
    def shadow_pos_y( x, y ):
        if not f'{Attribute.groupname}-shadow-pos-y' in Attribute.sposys.keys(): return
        D.add_combo(
            tag             = f'{Attribute.group}-shadow-pos-y',
            items           = list(range(-32, 32)),
            callback        = Plugin.updateSettings,
            user_data       = f'{Attribute.groupname}-shadow-pos-y', 
            default_value   = Attribute.sposys[f'{Attribute.groupname}-shadow-pos-y'],
            pos             = (x, y),
            width           = 64,
        )
        with D.tooltip(f'{Attribute.group}-shadow-pos-y'): 
            D.add_text("Shadow Y Offset")
    
    def shadow_blur( x, y ):
        if not f'{Attribute.groupname}-shadow-blur' in Attribute.blurs.keys(): return
        D.add_combo(
            tag             = f'{Attribute.group}-shadow-blur',
            items           = list(range(0, 80)),
            callback        = Plugin.updateSettings,
            user_data       = f'{Attribute.groupname}-shadow-blur', 
            default_value   = Attribute.blurs[f'{Attribute.groupname}-shadow-blur'],
            pos             = (x, y),
            width           = 64,
        )
        with D.tooltip(f'{Attribute.group}-shadow-blur'): 
            D.add_text("Shadow Blur")
    
    def border_width( x, y ):
        if not f'{Attribute.groupname}-border-width' in Attribute.bwidths.keys(): return
        D.add_combo(
            tag             = f'{Attribute.group}-border-width',
            items           = list(range(0, 80)),
            callback        = Plugin.updateSettings,
            user_data       = f'{Attribute.groupname}-border-width', 
            default_value   = Attribute.bwidths[f'{Attribute.groupname}-border-width'],
            pos             = (x, y),
            width           = 64,
        )
        with D.tooltip(f'{Attribute.group}-border-width'): 
            D.add_text("Border Width")

    def border_radius( x, y ):
        if not f'{Attribute.groupname}-border-radius' in Attribute.bradius.keys(): return
        D.add_combo(
            tag             = f'{Attribute.group}-border-radius',
            items           = list(range(0, 128)),
            callback        = Plugin.updateSettings,
            user_data       = f'{Attribute.groupname}-border-radius', 
            default_value   = Attribute.bradius[f'{Attribute.groupname}-border-radius'],
            pos             = (x, y),
            width           = 64,
        )
        with D.tooltip(f'{Attribute.group}-border-radius'): 
            D.add_text("Border Radius")
    
    def border_color( x, y ):
        if not f'{Attribute.groupname}-border-color' in Attribute.bcolors.keys(): return
        D.add_color_picker(
            tag             = f'{Attribute.group}-border-color', 
            default_value   = (0, 0, 0, 255),
            callback        = Plugin.updateColor, 
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
    
