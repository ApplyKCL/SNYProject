from PyQt5.QtWidgets import QApplication, QMainWindow
import sys, time
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
            userWindow.showFullScreen()
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
        instructionWindow.showFullScreen()
            
class Workflow_Window(QMainWindow, Ui_InstructionWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setupUi(self)
        # Initialize the HomePage
        self.stackedWidget.setCurrentWidget(self.HomePage)
        
        # Move to Next Page
        self.HomePage_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.Mount_Piezo_Wafer_1_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.Mount_Piezo_Wafer_2_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.Mount_Piezo_Wafer_3_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4))
        self.Dice_Framing_Piezo_1_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(5))
        self.Dice_Framing_Piezo_2_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(6))
        self.Dice_Framing_Piezo_3_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(7))
        self.Premount_Clean_and_Measure_Subwafer_1_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(8))
        self.Premount_Clean_and_Measure_Subwafer_2_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(9))
        self.Mount_Subwafers_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(10))
        self.Dice_First_Pillars_1_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(11))
        self.Dice_First_Pillars_2_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(12))
        self.Dice_First_Pillars_3_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(13))
        self.Fill_First_Pillars_1_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(14))
        self.Fill_First_Pillars_2_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(15))
        self.Fill_First_Pillars_3_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(16))
        self.Fill_First_Pillars_4_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(17))
        self.PreLap_First_Epoxy_Fill_1_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(18))
        self.PreLap_First_Epoxy_Fill_2_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(19))
        self.PreLap_First_Epoxy_Fill_3_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(20))
        self.Lap_First_Epoxy_Fill_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(21))
        self.Dice_Framing_Trench_Pattern_1_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(22))
        self.Dice_Framing_Trench_Pattern_2_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(23))
        self.Dice_Framing_Trench_Pattern_3_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(24))
        self.Fill_Second_Pillars_and_Frame_1_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(25))
        self.Fill_Second_Pillars_and_Frame_2_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(26))
        self.Fill_Second_Pillars_and_Frame_3_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(27))
        # self.Fill_Second_Pillars_and_Frame_4_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(27))
        
        # Back to UserWIndow
        self.HomePage_Back.clicked.connect(self.returnToUserWindow)
        self.Mount_Piezo_Wafer_1_Back.clicked.connect(self.returnToUserWindow)
        self.Mount_Piezo_Wafer_2_Back.clicked.connect(self.returnToUserWindow)
        self.Mount_Piezo_Wafer_3_Back.clicked.connect(self.returnToUserWindow)
        self.Dice_Framing_Piezo_1_Back.clicked.connect(self.returnToUserWindow)
        self.Dice_Framing_Piezo_2_Back.clicked.connect(self.returnToUserWindow)
        self.Dice_Framing_Piezo_3_Back.clicked.connect(self.returnToUserWindow)
        self.Premount_Clean_and_Measure_Subwafer_1_Back.clicked.connect(self.returnToUserWindow)
        self.Premount_Clean_and_Measure_Subwafer_2_Back.clicked.connect(self.returnToUserWindow)
        self.Mount_Subwafers_Back.clicked.connect(self.returnToUserWindow)
        self.Dice_First_Pillars_1_Back.clicked.connect(self.returnToUserWindow)
        self.Dice_First_Pillars_2_Back.clicked.connect(self.returnToUserWindow)
        self.Dice_First_Pillars_3_Back.clicked.connect(self.returnToUserWindow)
        self.Fill_First_Pillars_1_Back.clicked.connect(self.returnToUserWindow)
        self.Fill_First_Pillars_2_Back.clicked.connect(self.returnToUserWindow)
        self.Fill_First_Pillars_3_Back.clicked.connect(self.returnToUserWindow)
        self.Fill_First_Pillars_4_Back.clicked.connect(self.returnToUserWindow)
        self.PreLap_First_Epoxy_Fill_1_Back.clicked.connect(self.returnToUserWindow)
        self.PreLap_First_Epoxy_Fill_2_Back.clicked.connect(self.returnToUserWindow)
        self.PreLap_First_Epoxy_Fill_3_Back.clicked.connect(self.returnToUserWindow)
        self.Lap_First_Epoxy_Fill_Back.clicked.connect(self.returnToUserWindow)
        self.Dice_First_Pillars_1_Back.clicked.connect(self.returnToUserWindow)
        self.Dice_First_Pillars_2_Back.clicked.connect(self.returnToUserWindow)
        self.Dice_First_Pillars_3_Back.clicked.connect(self.returnToUserWindow)
        self.Fill_Second_Pillars_and_Frame_1_Back.clicked.connect(self.returnToUserWindow)
        self.Fill_Second_Pillars_and_Frame_2_Back.clicked.connect(self.returnToUserWindow)
        self.Fill_Second_Pillars_and_Frame_3_Back.clicked.connect(self.returnToUserWindow)
        self.Fill_Second_Pillars_and_Frame_4_Back.clicked.connect(self.returnToUserWindow)
        
        
    def returnToUserWindow(self):
        self.hide()
        self.stackedWidget.setCurrentWidget(self.HomePage)
        userWindow.showFullScreen()
        
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

# Timer for 15 minutes
def countdown_timer(duration):
    start_time = time.monotonic()  # 记录开始时间
    end_time = start_time + duration  # 计算结束时间

    while time.monotonic() < end_time:
        remaining_time = end_time - time.monotonic()  # 计算剩余时间
        minutes, seconds = divmod(remaining_time, 60)  # 将剩余时间转换为分钟和秒钟
        time_string = f"{int(minutes):02d}:{int(seconds):02d}"  # 格式化时间字符串
        print(time_string, end="\r")  # 输出时间字符串，覆盖当前行
        time.sleep(0.1)  # 暂停一段时间，以免程序占用过多CPU资源


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    # admin_window = Administrator_Window()
    userWindow = User_Window()
    instructionWindow = Workflow_Window()
    myWindow.show()
    sys.exit(app.exec_())