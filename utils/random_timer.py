from PyQt5.QtCore import pyqtSignal, QThread
from random import randint
import gc

from .config import config
from .memory_anaylzer import *

# 随机时钟类，用于随机定时选择角色动作
class RandomTimer(QThread):
    trigger = pyqtSignal() # 触发器，用于向外面发送信号，告诉外面哪个函数该调用了

    def __init__(self) -> None:
        super(RandomTimer, self).__init__()
        self._running = False
        self._block = False
    
    # @memory_analyze
    def run(self):
        self._running = True
        while self._running:
            # print(f"[DEBUG] in {__name__}-20 current memory: {get_current_memory()}MB")
            if self._block:
                self.sleep(3)
                continue
            # print(f"[DEBUG] in {__name__}-24 before sleep: {get_current_memory()}MB")
            rnd = randint(config["change-interval"][0], config["change-interval"][1])
            self.sleep(rnd)
            # print(f"[DEBUG] in {__name__}-26 after sleep: {get_current_memory()}MB")
            self.trigger.emit()
            # print(f"[DEBUG] in {__name__}-28 current memory: {get_current_memory()}MB")
    
    def block(self, is_block: bool):
        self._block = is_block

    def terminate(self):
        self._running = False
