from PyQt5.QtCore import QObject, pyqtSlot


class CallHandler(QObject):
    def __init__(self, view, **args) -> None:
        super(CallHandler, self).__init__()
        self.view = view
        self.args = args  # dict
    
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
        self.view.page().runJavaScript(f"window.init_pet_source('{self.args['default_pose_path']}')")

    @pyqtSlot(int, int, result=str)
    def dragging(self, x, y):
        print(x, y)
        if self.args.get("window"):
            win = self.args.get("window")
            last_pos = win.geometry()
            print(last_pos)
        else:
            Exception("MainWindow not found in CallHandler")
