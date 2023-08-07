from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWebEngineWidgets import *

class WebView(QWebEngineView):
    # 重载一个QWebEngineView类
    def __init__(self, parent=None) -> None:
        super(WebView, self).__init__(parent)
    
    # def mousePressEvent(self, event) -> None:
    #     print(event.buttons())
