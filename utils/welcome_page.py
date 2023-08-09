import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QMenu, QAction
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt

class StartWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)  # 无边框窗口且不在任务栏显示图标
        self.center_window()  # 将窗口置于屏幕中间
        
        # 设置背景颜色
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(30, 30, 30))
        self.setPalette(palette)
        
        layout = QVBoxLayout()
        
        # 设置艺术字标题
        title_label = QLabel("DesktopPet")
        title_label.setFont(QFont("Arial", 48))
        title_label.setStyleSheet("color: white;")
        layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        # 添加初始化中的文字
        init_label = QLabel("Initializing...")
        init_label.setFont(QFont("Arial", 20))
        init_label.setStyleSheet("color: white;")
        layout.addWidget(init_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        self.setLayout(layout)
        
        # 添加右键菜单
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def center_window(self):
        screen_geometry = QApplication.desktop().screenGeometry()
        window_geometry = self.geometry()
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2
        self.move(x, y)
    
    def show_context_menu(self, pos):
        context_menu = QMenu(self)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.exit_app)
        context_menu.addAction(exit_action)
        context_menu.exec_(self.mapToGlobal(pos))
    
    def exit_app(self):
        # 可以在退出操作中加入资源的释放等处理
        self.close()
        sys.exit()

def show_start_window():
    app = QApplication(sys.argv)
    window = StartWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    show_start_window()
