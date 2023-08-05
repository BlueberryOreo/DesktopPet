from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebChannel import QWebChannel
import os
import sys
from time import sleep

from utils import *
from config import config

window_size = config['window']['size']
pady = config['window']['pady']
padx = config['window']['padx']


class DesktopPet(QMainWindow):
    def __init__(self, default_pose_path, parent=None, **kwargs) -> None:
        super(DesktopPet, self).__init__(parent)

        # 获取屏幕分辨率
        self.screen_size = QGuiApplication.primaryScreen().geometry().getRect()
        # print(self.screen_size)

        self.init()
        self.initPall()
        self.initPetImage(default_pose_path)
    
    def init(self):
        # 设置窗口属性:窗口无标题栏且固定在最前面
        # FrameWindowHint:无边框窗口
        # WindowStaysOnTopHint: 窗口总显示在最上面
        # SubWindow: 新窗口部件是一个子窗口，而无论窗口部件是否有父窗口部件
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setGeometry(padx, self.screen_size[3] - window_size[1] - pady, window_size[0], window_size[1])
        self.repaint()

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
    
    def initPetImage(self, default_pose_path):
        # 嵌入一个html作为webm的显示平台
        self.browser = WebView(self)
        self.model_menu = WebMenu()
        self.browser.setContextMenuPolicy(Qt.CustomContextMenu)
        self.browser.customContextMenuRequested.connect(self.modelConfigMenu)

        self.channel = QWebChannel()
        # 实例化QWebChannel的前端处理对象
        self.handler = CallHandler(self.browser, default_pose_path=default_pose_path, window=self)
        # 将前端处理对象在前端页面中注册为名PyHandler对象，此对象在前端访问时名称即为PyHandler'
        self.channel.registerObject('PyHandler', self.handler)
        # 挂载前端处理对象
        self.browser.page().setWebChannel(self.channel) 
        # print("file:///" + os.getcwd().replace('\\', '/') + "/index.html")
        self.browser.load(QUrl("file:///" + os.getcwd().replace('\\', '/') + "/web/index.html"))
        # 设置网页背景为透明
        self.browser.page().setBackgroundColor(Qt.transparent)
        
        self.setCentralWidget(self.browser)
    
    def modelConfigMenu(self, pos):
        action = self.model_menu.exec_(self.browser.mapToGlobal(pos))
        if action == self.model_menu.show_conf:
            print("显示设置")
        if action == self.model_menu.quit_app:
            # 问题：通过网页关闭后程序没有关闭
            self.quit()

    def quit(self):
        self.browser.page().profile().clearHttpCache()
        self.browser.stop()
        self.close()
        sys.exit()
    
    def showwin(self):
        self.setWindowOpacity(1)
    
    def runJavaScript(self, cmd):
        self.browser.page().runJavaScript(cmd)
