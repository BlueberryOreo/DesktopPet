from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget
from time import sleep

frame = 30
sleep_time = 1 / frame

class Move(QThread):
    trigger = pyqtSignal(int) # 触发器，用于在window.py中让窗口移动起来

    def __init__(self) -> None:
        super(Move, self).__init__()
        # self.view = view

        self.direct = 0 # 1 ->, -1 <-, 0 stay
    
    # 设置方向，1表示向右，-1表示向左，为0时表示停止
    def set_direct(self, direct: int):
        self.direct = direct if direct == 0 else 1 if direct > 0 else -1
    
    def run(self):
        while True:
            sleep(sleep_time)
            # print("here")
            if self.direct:
                self.trigger.emit(self.direct)
                # self.view.move(self.view.x() + self.direct, self.view.y())
