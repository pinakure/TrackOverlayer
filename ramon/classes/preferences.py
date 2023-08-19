from dearpygui import dearpygui as dpg

class Preferences:

    width = 800
    height = 600

    @staticmethod
    def create():
        with dpg.window(
            tag='main',
            label="RAMon", 
            width=Preferences.width, 
            height=Preferences.height, 
            no_close=True, 
            no_collapse=True, 
            no_resize=True, 
            no_title_bar=True, 
            no_bring_to_front_on_focus=True, 
            no_move=True
        ):
            row = 23
            row_height = 23
            dpg.add_text(
                color=(220,255,0),
                default_value="RA Username", 
                pos=(8, row),
            )
            dpg.add_input_text(
                tag='username', 
                default_value="",
                pos=(96, row),
                width=110,
                callback=Preferences.updateSettings,
                on_enter=True,
            )
            dpg.add_text(
                default_value="Last connection", 
                pos=(230,row),
                color=(220,255,0),                
            )
            dpg.add_input_text(
                tag='date', 
                pos=(346, row),    
                width=200,            
                readonly=True,  
            )
            dpg.add_text(
                default_value="Score", 
                pos=(566, row),
                color=(220,255,0),                
            )
            dpg.add_input_text(
                tag='score', 
                pos=(610, row),    
                width=80,          
                readonly=True,  
            )
            dpg.add_text(
                default_value="Rank", 
                pos=(708, row),
                color=(220,255,0),                
            )
            dpg.add_input_text(
                tag='rank', 
                pos=(746, row),    
                width=132,          
                readonly=True,  
            )
            row+=row_height
        

    @staticmethod
    def show():
        dpg.show_item('preferences_main')

    @staticmethod
    def hide():
        dpg.hide_item('preferences_main')