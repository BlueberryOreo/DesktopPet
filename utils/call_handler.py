from PyQt5.QtCore import QObject, pyqtSlot

from .global_attributes import g_construct_path, g_move, g_timer
from .config import config

from memory_profiler import profile

# 通讯接口类，用于与前端进行通信
class CallHandler(QObject):
    def __init__(self, view, **args) -> None:
        super(CallHandler, self).__init__()
        self.view = view
        self.args = args  # dict

        self.mouse = [0, 0]
    
    @pyqtSlot(str, result=str)
    def init_home(self, str_args):
        print('call received')
        print('resolving......init home..')
        print(str_args)  # 查看参数
        # #####
        # 这里写对应的处理逻辑比如：
        # msg = '收到来自python的消息'
        # view.page().runJavaScript("alert('%s')" % msg)
        # view.page().runJavaScript("window.say_hello('%s')" % msg)
        # self.view.page().runJavaScript(f"window.init_pet_source('{self.args['default_pose_path']}')")
        self.change_pose(g_construct_path(config["model"]["path"], config["model"]["default-pose-name"]), "relax")
    
    @pyqtSlot(int, int, result=str)
    def drag_start(self, x, y):
        self.mouse[0], self.mouse[1] = x, y # 记录鼠标初始位置

    @pyqtSlot(int, int, result=str)
    def dragging(self, x, y):
        # print(x, y)
        if self.args.get("window"):
            win = self.args.get("window") # 窗口对象
            # 计算鼠标位置差
            dx = x - self.mouse[0]
            dy = y - self.mouse[1]
            self.mouse[0], self.mouse[1] = x, y
            # print(dx, dy)
            win.move(win.x() + dx, win.y() + dy) # 移动窗口
        else:
            Exception("MainWindow not found in CallHandler")
    
    # @profile
    @pyqtSlot()
    def change_pose(self, pose_path, pose=None, direct=1):
        self.view.page().runJavaScript(f"window.change_pose('{pose_path}', '{pose}', '{direct}');")

    @pyqtSlot(int)
    def tapped(self, direct):
        g_move.set_direct(0) # 停止移动
        g_timer.block(True) # 阻止计时器的循环，并让其睡3s（见random_timer.py）
        self.change_pose(g_construct_path(config["model"]["path"], config["model"]["poses"]["interact"]), "interact", direct)
    
    @pyqtSlot(int)
    def tap_stop(self, direct):
        g_timer.block(False)
        self.reverse_to_default(direct)

    @pyqtSlot()
    def reverse_to_default(self, direct=1):
        self.change_pose(g_construct_path(config["model"]["path"], config["model"]["default-pose-name"]), "relax", direct)
    