import pyHook 
from threading import Timer
import win32gui
import logging

class blockInput():
    def OnKeyboardEvent(self,event):
        return False

    def OnMouseEvent(self,event):
        return False

    def unblock(self):
        logging.info(" -- Unblock!")
        if self.t.is_alive():
            self.t.cancel()
        try: self.hm.UnhookKeyboard()
        except: pass
        try: self.hm.UnhookMouse()
        except: pass

    def block(self, timeout = 10, keyboard = True, mouse = True):
        self.t = Timer(timeout, self.unblock)
        self.t.start()

        logging.info(" -- Block!")
        if mouse:
            self.hm.MouseAll = self.OnMouseEvent
            self.hm.HookMouse()
        if keyboard:
            self.hm.KeyAll = self.OnKeyboardEvent
            self.hm.HookKeyboard()
        win32gui.PumpWaitingMessages()

    def __init__(self):
        self.hm = pyHook.HookManager()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    block = blockInput()
    block.block()

    import time
    t0 = time.time()
    while time.time() - t0 < 5:
        time.sleep(1)
        print(time.time() - t0)

    block.unblock()
    logging.info("Done.")