from dearpygui import dearpygui as dpg
from colorama  import Fore
import traceback, time

class Log:
    verbose = False
    parent  = None
    stdout  = True
    BR      = '\n'
    width   = 800
    height  = 0
    buffer  = []    
    
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
        if Log.parent.text_only:
            Log.parent.log.print(text)
            Log.parent.activity = True
        else:
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
            
        Log.buffer.append(text+"\n")            
        if len(Log.buffer) > 256:
            with open('trackoverlayer.log', 'a') as file:
                  file.write( Log.BR.join( Log.buffer ) )
            Log.buffer = []
    
    def open(parent=None):
        Log.parent = parent
        with open('trackoverlayer.log', 'w') as file:
            pass

    def close():
        with open('trackoverlayer.log', 'a') as file:
            file.write( "\n".join( Log.buffer ) )
        
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

    def dump(tdu):
        from classes.tdu import Tdu
        tdu.restore()
        try: Log.buffer.remove('\n')
        except: pass
        try: Log.buffer.remove(' ')
        except: pass
        try: Log.buffer.remove('')
        except: pass
        for line in Log.buffer[-tdu.height:]:
            tdu.print(line, wrap=False)
                
    
    def error(text, exception=None):
        if Log.parent.text_only:
            Log.print(f'{Fore.RED}{text}')
            Log.print("\t"+Fore.RED+(traceback.format_exc() if exception else 'Sorry!')+"\n"+Fore.BLUE)
            return
        Log.print("\t"+('-'*80)+"\n")
        Log.print("\t"+f'ERROR: {text}'+(('\n\t'+str(exception)) if exception else '')+"\n")
        if Log.verbose: 
            Log.print("\t"+(traceback.format_exc() if exception else 'Sorry!')+"\n")
        Log.print('\t'+('-'*80)+"\n")
