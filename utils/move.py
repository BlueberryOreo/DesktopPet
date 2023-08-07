from PyQt5.QtCore import QThread, pyqtSignal
from time import sleep

frame = 30
sleep_time = 1 / frame

# 控制移动类，用于控制角色移动
class Move(QThread):
    trigger = pyqtSignal(int) # 触发器，用于在window.py中让窗口移动起来

    def __init__(self) -> None:
        super(Move, self).__init__()
        self._running = False

        self._direct = 0 # 1 ->, -1 <-, 0 stay
    
    # 设置方向，1表示向右，-1表示向左，为0时表示停止
    def set_direct(self, change_direct: int):
        self._direct = change_direct if change_direct == 0 else 1 if change_direct > 0 else -1

    @property
    def direct(self):
        return self._direct
    
    def run(self):
        self._running = True
        while self._running:
            sleep(sleep_time)
            # print("here")
            if self.direct:
                self.trigger.emit(self.direct)
                # self.view.move(self.view.x() + self.direct, self.view.y())

    def terminate(self):
        self._running = False
