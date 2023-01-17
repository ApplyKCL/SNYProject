from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import resource_rc
from login import *
from Admin_window import *

class MyWindow(QMainWindow, Ui_Login_Window):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setupUi(self)
        self.Login_Button.clicked.connect(self.go_to_inter)
        
    def go_to_inter(self):
        account = self.UserID.text()
        password = self.Password.text()
        if account == "Jiahao" and password == "950321":
            otherwindow = Administrator_Window()
            otherwindow.show()
            self.close()
        else:
            pass
        
    def mousePressEvent(self, event):                                 # +
        self.dragPos = event.globalPos()
        
    def mouseMoveEvent(self, event):                                  # !!!
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()
        
class Administrator_Window(QMainWindow, Ui_Administrator_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    sys.exit(app.exec_())