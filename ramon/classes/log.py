from dearpygui import dearpygui as dpg

class Log:
    
    stdout  = True
    BR      = '\n'

    @staticmethod
    def print(text):
        if Log.stdout:
            print(text, end=Log.BR)
        else:
            dpg.set_value('log', dpg.get_value('log')+text)

    @staticmethod
    def warning(text):
        Log.print(f'W: {text}')

    @staticmethod
    def info(text):
        Log.print(f'I: {text}')

    @staticmethod
    def error(text):
        Log.print(f'E: {text}')