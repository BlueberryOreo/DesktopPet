from PyQt5.QtCore import QObject, pyqtSlot


class CallHandler(QObject):
    def __init__(self) -> None:
        super(CallHandler, self).__init__()
    
    @pyqtSlot(str, result=str)
    def init_home(self, str_args):
        print('call received')
        print('resolving......init home..')
        print(str_args)  # 查看参数
        # #####
        # 这里写对应的处理逻辑比如：
        msg = '收到来自python的消息'
        # view.page().runJavaScript("alert('%s')" % msg)
        # view.page().runJavaScript("window.say_hello('%s')" % msg)
        return 'hello, Python'
