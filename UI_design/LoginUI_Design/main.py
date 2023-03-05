from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from login import *
# from Admin_Window_1 import *
from Normal_user import *
from Instruction_Window import *

### Login Main Window ###
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
            self.hide()
            # admin_window.show()
        else:
            self.hide()
            user_window.showFullScreen()
            pass
        
    def mousePressEvent(self, event):                                 # +
        self.dragPos = event.globalPos()
        
    def mouseMoveEvent(self, event):                                  # !!!
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()
        
# class Administrator_Window(QMainWindow, Ui_Admin_WIndow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
#         self.setupUi(self)
#         self.close_pushButton.clicked.connect(self.close_event)
    
#     def close_event(self):
#         self.hide()
#         myWindow.show()
        
#     def mousePressEvent(self, event):                                 # +
#         self.dragPos = event.globalPos()
        
#     def mouseMoveEvent(self, event):                                  # !!!
#         if event.buttons() == QtCore.Qt.LeftButton:
#             self.move(self.pos() + event.globalPos() - self.dragPos)
#             self.dragPos = event.globalPos()
#             event.accept()
            
class User_Window(QMainWindow, Ui_User_WIndow):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setupUi(self)
        self.LogOut_User_pushButton.clicked.connect(self.close_event)
        
    def close_event(self):
        self.hide()
        ppt.showFullScreen()
            
class Instruction_Window(QMainWindow, Ui_InstructionWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setupUi(self)
        self.stackedWidget.setCurrentWidget(self.HomePage)
        self.HomePage_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.Mount_Piezo_Wafer_1_Back.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.Mount_Piezo_Wafer_1_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.Mount_Piezo_Wafer_2_Back.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    # admin_window = Administrator_Window()
    user_window = User_Window()
    ppt = Instruction_Window()
    myWindow.show()
    sys.exit(app.exec_())