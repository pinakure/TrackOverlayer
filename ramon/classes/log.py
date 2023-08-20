from dearpygui import dearpygui as dpg

class Log:
    
    parent  = None
    stdout  = True
    BR      = '\n'
    width   = 800
    height  = 600

    @staticmethod
    def create(parent):
        Log.parent = parent 
        with dpg.window(
                modal=True, 
                label="Log",
                tag="log_window", 
                on_close=Log.hide,
                width=Log.width, 
                height=Log.height, 
                min_size=[Log.width, Log.height], 
                no_scrollbar=True, 
                max_size=[Log.width, Log.height], 
                no_collapse=True, 
                no_resize=True, 
                pos=[(parent.width / 2)-100, 
                (parent.height / 2)-32], 
                show=False
                ):
                    dpg.add_input_text(readonly=True, pos=(0,22), multiline=True, tag='log', width=Log.width - 4, height=Log.height-26)
        Log.stdout = False

    @staticmethod
    def show():
        dpg.show_item('log_window')         
         
    @staticmethod
    def hide():
        dpg.hide_item('log_window')

    @staticmethod
    def print(text):
        if Log.stdout:
            print(text, end=Log.BR)
        else:
            dpg.set_value('log', dpg.get_value('log')+text+'\n')

    @staticmethod
    def warning(text):
        Log.print(f'W: {text}')

    @staticmethod
    def info(text):
        Log.print(f'I: {text}')

    @staticmethod
    def error(text):
        Log.print(f'E: {text}')