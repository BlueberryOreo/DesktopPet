from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebChannel import QWebChannel

from ctypes.wintypes import MSG
from win32 import win32api
from win32.lib import win32con
from time import sleep
import os
import sys
from random import randint

# memory analyze
from memory_profiler import profile

from utils import *
from utils import config, g_construct_path, g_move, g_timer, g_poses, g_probability_map, g_gravity

window_size = config['window']['size']
pady = config['window']['pady']
padx = config['window']['padx']

# 主桌宠类
class DesktopPet(QMainWindow):
    def __init__(self, parent=None, **kwargs) -> None:
        super(DesktopPet, self).__init__(parent)

        # 获取屏幕分辨率
        self.screen_size = QGuiApplication.primaryScreen().geometry().getRect()
        # print(type(self.screen_size))

        self.BORDER_WIDTH = 5 # 设置边框宽度
        self.windowEffect = WindowEffect() # 窗口效果器

        self.dragging = False
        self.pass_time = 0 # 自由落体时计时器

        self.init()
        self.initPall()
        self.initPetImage()
    
    def init(self):
        """初始化无边框窗口

        """
        # 设置窗口属性:窗口无标题栏且固定在最前面
        # FrameWindowHint:无边框窗口
        # WindowStaysOnTopHint: 窗口总显示在最上面
        # SubWindow: 新窗口部件是一个子窗口，而无论窗口部件是否有父窗口部件
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        # self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setGeometry(padx, self.screen_size[3] - window_size[1] - pady, window_size[0], window_size[1])
        self.repaint()

        # 设置窗口移动工具，用于控制窗口的水平移动
        g_move.trigger.connect(self.windowMove)
        g_move.start()

    def initPall(self):
        """初始化小图标

        """
        # 设置图标
        icons = os.path.join("./app_icon.ico")

        # 设置右键显示的菜单项
        quit_action = QAction("退出", self, triggered=self.quit)
        quit_action.setIcon(QIcon(icons))
        showing = QAction(u"显示", self, triggered=self.showwin)

        # 新建菜单项控件
        self.tray_icon_menu = QMenu(self)
        self.tray_icon_menu.addAction(quit_action)
        self.tray_icon_menu.addAction(showing)

        # 为应用程序在系统托盘上提供一个图标
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(icons))
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        self.tray_icon.show()
    
    def initPetImage(self):
        """建立一个网页嵌入窗口中，作为角色模型的平台
        
        """
        # 嵌入一个html作为模型的显示平台
        self.browser = WebView(self)
        self.model_menu = WebMenu()
        self.is_resizing = False
        self.browser.setContextMenuPolicy(Qt.CustomContextMenu)
        self.browser.customContextMenuRequested.connect(self.modelConfigMenu)

        # 设置计时器，用于随机变换动作
        g_timer.trigger.connect(self.randomChangeModel)
        g_timer.start()
        self.current_pose = config["model"]["pose-index"]["default"]

        self.channel = QWebChannel()
        # 实例化QWebChannel的前端处理对象
        self.handler = CallHandler(self.browser, window=self)
        self.handler.trigger.connect(self.setDragging)
        # 将前端处理对象在前端页面中注册为名PyHandler对象，此对象在前端访问时名称即为PyHandler'
        self.channel.registerObject('PyHandler', self.handler)
        # 挂载前端处理对象
        self.browser.page().setWebChannel(self.channel) 
        # print("file:///" + os.getcwd().replace('\\', '/') + "/index.html")
        self.browser.load(QUrl("file:///" + os.getcwd().replace('\\', '/') + "/web/index.html"))
        # 设置网页背景为透明
        self.browser.page().setBackgroundColor(Qt.transparent)

        self.browser.setGeometry(QRect(-window_size[0] / 4.5, -window_size[1] / 4.5, window_size[0] + padx, window_size[1]))
        # self.setCentralWidget(self.browser)
    
    # @memory_analyze
    def randomChangeModel(self):
        """随机选择模型
            配合g_timer

            疑似该方法出现问题：内存泄露，需要进行内存分析
            20230808 该方法没有问题，主要问题出现在前端，并且主要在于pyinstaller打包之后才会出现内存泄露问题
        """
        # print("change")
        poses = list(config["model"]["pose-index"].keys()) # 模型序号
        # print(poses)
        # 注：随机选择动作需要优化，改成概率形式，并建图
        next_pose = get_next_pose(self.current_pose)
        if next_pose == self.current_pose:
            return
        self.current_pose = next_pose
        selected_pose = g_poses[next_pose]
        pose_path = g_construct_path(config["model"]["path"], selected_pose)
        selected_pose = poses[self.current_pose]
        print(selected_pose, pose_path)

        direct = None
        # direct = 1
        if selected_pose == "move":
            # 注：移动方向的随机选择需要优化，改成概率形式，靠边时向反方向的概率要增大
            direct = 1 if randint(0, 100) > ((self.x() + self.width() / 2) / self.screen_size[2] * 100) else -1 # 限制角色只有在移动的时候才会选择方向
            # print(f"now position: {(self.x() + self.width() / 2) / self.screen_size[2] * 100}")
            g_move.set_direct(direct)
        else:
            g_move.set_direct(0)
        self.handler.change_pose(pose_path, selected_pose, direct)
    
    def windowMove(self, direct):
        """窗口移动
            配合g_move
        """
        # print("moving")
        # 自由落体
        if not self.is_resizing:
            if self.y() + window_size[1] < self.screen_size[3] - pady:
                if not self.dragging:
                    # self.move(self.x(), self.y() + g_gravity * self.pass_time)
                    max_dy = 5 # 纵向一次最大移动距离
                    dy = g_gravity * self.pass_time
                    if dy > max_dy:
                        for _ in range(g_gravity * self.pass_time // max_dy):
                            self.move(self.x(), self.y() + max_dy)
                    else:
                        self.move(self.x(), self.y() + dy)
                    self.pass_time += 1
            else:
                self.move(self.x(), self.screen_size[3] - pady - window_size[1])
                self.pass_time = 0

        # 走路动作
        if direct and (self.x() <= 0 or (self.x() + self.width()) >= self.screen_size[2]):
            # 角色碰到墙上，停下移动，并改动作为默认状态
            last_direct = g_move.direct
            g_move.set_direct(0)
            self.handler.reverse_to_default()
            self.move(self.x() + last_direct * -1, self.y())
        else:
            self.move(self.x() + direct, self.y())

    def nativeEvent(self, eventType, message):
        """无边框窗口伸缩方法
            参考: https://www.cnblogs.com/zhiyiYo/p/14644099.html
        """
        if not self.is_resizing:
            return super().nativeEvent(eventType, message)
        msg = MSG.from_address(message.__int__())
        if msg.message == win32con.WM_NCHITTEST:
            # 处理鼠标拖拽消息
            xPos = win32api.LOWORD(msg.lParam) - self.frameGeometry().x()
            yPos = win32api.HIWORD(msg.lParam) - self.frameGeometry().y()
            w, h = self.width(), self.height()
            lx = xPos < self.BORDER_WIDTH
            rx = xPos + 9 > w - self.BORDER_WIDTH
            ty = yPos < self.BORDER_WIDTH
            by = yPos > h - self.BORDER_WIDTH
            # 顶部
            if ty:
                return True, win32con.HTTOP
            # 底部
            elif by:
                return True, win32con.HTBOTTOM
            # 左边
            elif lx:
                return True, win32con.HTLEFT
            # 右边
            elif rx:
                return True, win32con.HTRIGHT
        return super().nativeEvent(eventType, message)
    
    def modelConfigMenu(self, pos):
        # 呼出菜单时，暂停计时器，停止移动
        g_timer.block(True)
        self.handler.reverse_to_default()
        g_move.set_direct(0)
        # 
        action = self.model_menu.exec_(self.browser.mapToGlobal(pos))
        if action == self.model_menu.show_adjust:
            print("调整窗口位置及大小")
            self.model_menu.adjust_mode()
            self.is_resizing = True
            self.windowEffect.setAeroEffect(self.winId())
        if action == self.model_menu.finish_adjust:
            print("调整完成")
            self.model_menu.normal_mode()
            self.windowEffect.resetEffect(self.winId())
            # 更新参数
            global pady, window_size
            window_size = [self.size().width(), self.size().height()]
            pady = self.screen_size[3] - (self.y() + window_size[1])
            print(window_size, pady)
            self.is_resizing = False
        g_timer.block(False)

        # if action == self.model_menu.quit_app:
        #     # 问题：通过网页关闭后程序没有关闭
        #     self.quit()

    def quit(self):
        # self.browser.page().profile().clearHttpCache()
        self.clearHttpCache()
        self.browser.stop()
        g_move.terminate()
        g_timer.terminate()
        self.close()
        sys.exit()
    
    def clearHttpCache(self):
        self.browser.page().profile().clearHttpCache()
    
    def showwin(self):
        self.setWindowOpacity(1)
    
    def setDragging(self, dragging):
        self.dragging = dragging


"""根据概率图获取下一个动作

"""
def get_next_pose(current_pose) -> int:
    rnd = randint(1, 100)
    print(rnd)
    for i in range(len(g_probability_map[0])):
        if rnd <= g_probability_map[current_pose][i]:
            return i
