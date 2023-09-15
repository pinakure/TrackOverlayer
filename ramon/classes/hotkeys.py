from pynput                 import keyboard

class HotKeys: 
    ctrl        = False
    shift       = False
    alt         = False
    listener    = False

    
    def keydown(key):
        from classes.ramon import Ramon
        if key in [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r] :
            HotKeys.ctrl = True
            return 
        if key in [keyboard.Key.alt_l, keyboard.Key.alt_r] :
            HotKeys.alt = True
            return 
        if key in [keyboard.Key.shift_l, keyboard.Key.shift_r] :
            HotKeys.shift = True
            return 
        if key == keyboard.Key.f5 and HotKeys.ctrl:
            if Ramon.timer:
                Ramon.timer.cancel()
                Ramon.timer = None
                Ramon.refresh()

    
    def keyup(key):
        if key in [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r] :
            HotKeys.ctrl = False
            return 
        if key in [keyboard.Key.alt_l, keyboard.Key.alt_r] :
            HotKeys.alt = False
            return 
        if key in [keyboard.Key.shift_l, keyboard.Key.shift_r] :
            HotKeys.shift = False
            return 

    
    def install():
        HotKeys.listener = keyboard.Listener(
            on_press=HotKeys.keydown,
            on_release=HotKeys.keyup
        )
        #HotKeys.listener.start()
