from PyQt5.QtWidgets import QMenu, QAction

class WebMenu(QMenu):
    def __init__(self, parent=None):
        super(WebMenu, self).__init__(parent)
        
        self.show_adjust = QAction("调整窗口大小", parent)
        self.finish_adjust = QAction("完成调整", parent)
        # self.quit_app = QAction("退出", parent)
        self.normal_mode()

    def normal_mode(self):
        self.addAction(self.show_adjust)
        self.removeAction(self.finish_adjust)
        # self.addAction(self.quit_app)
    
    def adjust_mode(self):
        self.addAction(self.finish_adjust)
        self.removeAction(self.show_adjust)
