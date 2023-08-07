from PyQt5.QtWidgets import QMenu, QAction

class WebMenu(QMenu):
    def __init__(self, parent=None):
        super(WebMenu, self).__init__(parent)
        
        self.show_conf = QAction("调整窗口大小", parent)
        # self.quit_app = QAction("退出", parent)

        self.addAction(self.show_conf)
        # self.addAction(self.quit_app)
