from window import *
from PyQt5.QtWidgets import QApplication
import sys, os
import ctypes

from utils import config

def start():
    app = QApplication(sys.argv)
    # default_pose_path = "." + config['model']['path'] + "/" + config['model']['default-pose-name']
    # print(g_construct_path(config['model']['path'], config['model']['default-pose-name']))
    # print(default_pose_path)
    pet = DesktopPet()
    pet.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd, 0)
        ctypes.windll.kernel32.CloseHandle(whnd)
    start()
