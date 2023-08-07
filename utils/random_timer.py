from PyQt5.QtCore import pyqtSignal, QThread
from random import randint

from .global_attributes import config

# 随机时钟类，用于随机定时选择角色动作
class RandomTimer(QThread):
    trigger = pyqtSignal() # 触发器，用于向外面发送信号，告诉外面哪个函数该调用了

    def __init__(self) -> None:
        super(RandomTimer, self).__init__()
    
    def run(self):
        while True:
            rnd = randint(config["change-interval"][0], config["change-interval"][1])
            self.sleep(rnd)
            self.trigger.emit()
