from window import *
from PyQt5.QtWidgets import QApplication
from threading import Thread
import sys
import ctypes
from time import sleep

from utils import config, StartWindow

def start():
    app = QApplication(sys.argv)

    start_win = StartWindow()
    start_win.show()

    pet = DesktopPet()
    pet.show()
    
    sleep(1)
    start_win.close()
    sys.exit(app.exec_())

def hide_command():
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd, 0)
        ctypes.windll.kernel32.CloseHandle(whnd)

if __name__ == "__main__":
    hide_command_thread = Thread(target=hide_command)
    hide_command_thread.start()
    start()
    hide_command_thread.join()
