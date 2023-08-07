from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebChannel import QWebChannel

from ctypes.wintypes import HWND, MSG, POINT
from win32 import win32api, win32gui
from win32.lib import win32con
import os
import sys
from random import choice

from utils import *
from utils import config, g_construct_path, g_move, g_timer

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
        self.windowEffect = WindowEffect()

        self.init()
        self.initPall()
        self.initPetImage()
    
    def init(self):
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
        # 嵌入一个html作为webm的显示平台
        self.browser = WebView(self)
        self.model_menu = WebMenu()
        self.browser.setContextMenuPolicy(Qt.CustomContextMenu)
        self.browser.customContextMenuRequested.connect(self.modelConfigMenu)

        # 设置计时器，用于随机变换动作
        g_timer.trigger.connect(self.randomChangeModel)
        g_timer.start()
        self.last_pose = None

        self.channel = QWebChannel()
        # 实例化QWebChannel的前端处理对象
        self.handler = CallHandler(self.browser, window=self)
        # 将前端处理对象在前端页面中注册为名PyHandler对象，此对象在前端访问时名称即为PyHandler'
        self.channel.registerObject('PyHandler', self.handler)
        # 挂载前端处理对象
        self.browser.page().setWebChannel(self.channel) 
        # print("file:///" + os.getcwd().replace('\\', '/') + "/index.html")
        self.browser.load(QUrl("file:///" + os.getcwd().replace('\\', '/') + "/web/index.html"))
        # 设置网页背景为透明
        self.browser.page().setBackgroundColor(Qt.transparent)
        
        self.setCentralWidget(self.browser)
    
    def randomChangeModel(self):
        # print("change")
        poses = list(filter(lambda x: x != "interact", config["model"]["poses"].keys()))
        # print(poses)
        selected_pose = choice(poses)
        if(selected_pose == self.last_pose):
            return
        self.last_pose = selected_pose
        pose_path = g_construct_path(config["model"]["path"], config["model"]["poses"][selected_pose])
        print(selected_pose, pose_path)

        direct = None
        # direct = 1
        if selected_pose == "move":
            direct = choice([-1, 1]) # 限制角色只有在移动的时候才会选择方向
            g_move.set_direct(direct)
        else:
            g_move.set_direct(0)
        self.handler.change_pose(pose_path, selected_pose, direct)
    
    def windowMove(self, direct):
        # print("moving")
        if(self.x() <= 0 or (self.x() + self.width()) >= self.screen_size[2]):
            # 角色碰到墙上，停下移动，并改动作为默认状态
            last_direct = g_move.direct
            g_move.set_direct(0)
            self.handler.reverse_to_default()
            self.move(self.x() + last_direct * -1, self.y())
        else:
            self.move(self.x() + direct, self.y())

    def nativeEvent(self, eventType, message):
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
            # 左上角
            if (lx and ty):
                return True, win32con.HTTOPLEFT
            # 右下角
            elif (rx and by):
                return True, win32con.HTBOTTOMRIGHT
            # 右上角
            elif (rx and ty):
                return True, win32con.HTTOPRIGHT
            # 左下角
            elif (lx and by):
                return True, win32con.HTBOTTOMLEFT
            # 顶部
            elif ty:
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
        g_move.set_direct(0)
        # 
        action = self.model_menu.exec_(self.browser.mapToGlobal(pos))
        if action == self.model_menu.show_adjust:
            print("调整窗口大小")
            self.model_menu.adjust_mode()
            self.windowEffect.setAeroEffect(self.winId())
        if action == self.model_menu.finish_adjust:
            print("调整完成")
            self.model_menu.normal_mode()
            self.windowEffect.resetEffect(self.winId())
        g_timer.block(False)

        # if action == self.model_menu.quit_app:
        #     # 问题：通过网页关闭后程序没有关闭
        #     self.quit()

    def quit(self):
        self.browser.page().profile().clearHttpCache()
        self.browser.stop()
        g_move.terminate()
        g_timer.terminate()
        self.close()
        sys.exit()
    
    def showwin(self):
        self.setWindowOpacity(1)
    
    def runJavaScript(self, cmd):
        self.browser.page().runJavaScript(cmd)
