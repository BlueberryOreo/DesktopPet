from window import *
from PyQt5.QtWidgets import QApplication
import sys, os

from utils import config

def start():
    app = QApplication(sys.argv)
    # default_pose_path = "." + config['model']['path'] + "/" + config['model']['default-pose-name']
    # print(construct_path(config['model']['path'], config['model']['default-pose-name']))
    # print(default_pose_path)
    pet = DesktopPet()
    pet.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    start()
