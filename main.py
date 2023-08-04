from window import *
from PyQt5.QtWidgets import QApplication
import sys, os

from config import *

def start():
    app = QApplication(sys.argv)
    pet = DesktopPet()
    pet.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    start()
