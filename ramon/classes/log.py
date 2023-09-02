from dearpygui import dearpygui as dpg
import traceback, time

class Log:
    verbose = False
    parent  = None
    stdout  = True
    BR      = '\n'
    width   = 800
    height  = 600
    
    
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

    
    def show():
        dpg.show_item('log_window')         
         
    
    def hide():
        dpg.hide_item('log_window')

    
    def print(text):
        if Log.stdout:
            print(text, end=Log.BR)
        else:
            dpg.set_value('log', dpg.get_value('log')+text+'\n')

    
    def warning(text):
        Log.print("WARNING:\n\t"+text+"\n")

    
    def info(text):
        Log.print(f'{text}')
        if not Log.stdout:
            dpg.set_viewport_title(f'RAMon - {text}')
            # if dpg.is_dearpygui_running(): 
            #     dpg.render_dearpygui_frame()

    
    def time( finish=False ):
        if not finish:
            Log.when = time.time_ns()
        else:
            Log.info(f"\tFinished in { int((time.time_ns() - Log.when)/10000) } msec")

    
    def error(text, exception=None):
        if not Log.stdout:
            dpg.show_item('log_window')
        Log.print("\t"+('-'*80)+"\n")
        Log.print("\t"+f'ERROR: {text}'+(('\n\t'+str(exception)) if exception else '')+"\n")
        if Log.verbose: 
            Log.print("\t"+(traceback.format_exc() if exception else 'Sorry!')+"\n")
        Log.print('\t'+('-'*80)+"\n")