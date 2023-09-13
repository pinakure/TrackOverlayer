from dearpygui import dearpygui as dpg
import traceback, time

class Log:
    verbose = False
    parent  = None
    stdout  = True
    BR      = '\n'
    width   = 800
    height  = 0
    
    
    def create(parent):
        Log.parent = parent 
        Log.height = parent.log_height
        Log.width  = parent.inner_width-(parent.padding*2)
        with dpg.child_window(
                label       =  "Log",
                tag         = "log-window", 
                width       = Log.width, 
                height      = Log.height, 
                no_scrollbar= True, 
                pos         = [
                    0, 
                    parent.inner_height-(Log.height+parent.statusbar_height),
                ]):
                    dpg.add_input_text(
                        track_offset = 1.0,
                        tracked      = True, 
                        readonly     = True, 
                        pos          = (0,0), 
                        multiline    = True, 
                        tag          = 'log', 
                        width        = Log.width-8, 
                        height       = Log.height,
                    )
        Log.stdout = False


    def show():
        dpg.show_item('log_window')         
         
    
    def hide():
        dpg.hide_item('log_window')

    
    def print(text):
        if Log.stdout:
            print(text, end=Log.BR)
        else:
            dpg.set_value(
                'log', 
                "\n".join(
                    (
                        dpg.get_value('log')+text+'\n'
                    ).split('\n')[-(Log.parent.log_line_count+3):]
                ),
            )
            
    
    def warning(text):
        Log.print("WARNING:\n\t"+text+"\n")

    
    def info(text, force_redraw=False):
        Log.print(f'{text}')
        if not Log.stdout:
            dpg.set_viewport_title(f'tRAckOverlayer - {text}')            
            #if force_redraw: dpg.render_dearpygui_frame()
    
    def time( finish=False ):
        if not finish:
            Log.when = time.time_ns()
        else:
            pass
            #Log.info(f"\tFinished in { int((time.time_ns() - Log.when)/10000) } msec")

    
    def error(text, exception=None):
        # if not Log.stdout:
        #     dpg.show_item('log_window')
        Log.print("\t"+('-'*80)+"\n")
        Log.print("\t"+f'ERROR: {text}'+(('\n\t'+str(exception)) if exception else '')+"\n")
        if Log.verbose: 
            Log.print("\t"+(traceback.format_exc() if exception else 'Sorry!')+"\n")
        Log.print('\t'+('-'*80)+"\n")