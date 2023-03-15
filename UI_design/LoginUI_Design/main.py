from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QPushButton, QHBoxLayout, QMessageBox
import sys, time
import mysql.connector

from login import *
from Normal_user import *
from Instruction_Window import *
from Admin_WIndow3 import *

sys.path.append('D:/Desktop/sny/SNY/SNYProject/UI_design/LoginUI_Design/db_program')

from db_program.check_user import *
from db_program.mysql_statement_gen import *
from db_program.user import *
from db_program.config import *


### Login Main Window ###
class MyWindow(QMainWindow, Ui_Login_Window):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setupUi(self)
        self.Login_Button.clicked.connect(self.go_to_inter)
        
        self.admin_login = False
        
    def go_to_inter(self):
        account = self.UserID.text()
        password = self.Password.text()
        
        myclass = databaseAPI(mydb, "employee_table")
        result = check_user(account, password, myclass)
        print(result)
        
        if result is False:
            QMessageBox.information(self,"Error Message","Invalid User/Password")
            
        elif result[len(result)-1] == 1:
            dialog = MyDialog()
            dialog.setModal(True)  # 设置对话框为弹窗模式
            dialog.exec_()
            self.admin_login = True
            
        else:
            self.hide()
            userWindow.showFullScreen()
            pass
        
            
class MyDialog(QDialog):
    def __init__(self):
        super().__init__()

        # 设置对话框的标题
        self.setWindowTitle("Admin Window")

        # 创建两个按钮
        self.btn1 = QPushButton("Employee")
        self.btn2 = QPushButton("Product")

        # 给按钮添加点击事件
        self.btn1.clicked.connect(self.edit_employee_info)
        self.btn2.clicked.connect(self.edit_product_info)

        # 创建一个水平布局，并将按钮添加到布局中
        layout = QHBoxLayout()
        layout.addWidget(self.btn1)
        layout.addWidget(self.btn2)

        # 将整个布局设置为对话框的主布局
        self.setLayout(layout)

        # 设置对话框的大小为512*300
        self.resize(512, 300)
        
    def edit_employee_info(self):
        self.hide()
        myWindow.hide()
        admin_window.show()
        
    def edit_product_info(self):
        self.hide()
        myWindow.hide()
        admin_window.show()
        
class Administrator_Window(QMainWindow, Ui_Frame):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setupUi(self)
    
            
class User_Window(QMainWindow, Ui_User_WIndow):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setupUi(self)
        self.Countinue_pushButton.clicked.connect(self.workflow_event)
        
    def workflow_event(self):
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
        self.DicePiezoWaferintoSubwafers0_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(5))
        self.DicePiezoWaferintoSubwafers1_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(6))
        self.DicePiezoWaferintoSubwafers2_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(7))
        self.DicePiezoWaferintoSubwafers3_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(8))
        self.Dice_Framing_Piezo_1_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(9))
        self.Dice_Framing_Piezo_2_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(10))
        self.Dice_Framing_Piezo_3_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(11))
        self.Premount_Clean_and_Measure_Subwafer_1_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(12))
        self.Premount_Clean_and_Measure_Subwafer_2_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(13))
        self.Mount_Subwafers_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(14))
        self.Dice_First_Pillars_1_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(15))
        self.Dice_First_Pillars_2_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(16))
        self.Dice_First_Pillars_3_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(17))
        self.Fill_First_Pillars_1_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(18))
        self.Fill_First_Pillars_2_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(19))
        self.Fill_First_Pillars_3_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(20))
        self.Fill_First_Pillars_4_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(21))
        self.PreLap_First_Epoxy_Fill_1_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(22))
        self.PreLap_First_Epoxy_Fill_2_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(23))
        self.PreLap_First_Epoxy_Fill_3_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(24))
        self.Lap_First_Epoxy_Fill_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(25))
        self.Dice_Framing_Trench_Pattern_1_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(26))
        self.Dice_Framing_Trench_Pattern_2_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(27))
        self.Dice_Framing_Trench_Pattern_3_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(28))
        self.Fill_Second_Pillars_and_Frame_1_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(29))
        self.Fill_Second_Pillars_and_Frame_2_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(30))
        self.Fill_Second_Pillars_and_Frame_3_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(31))
        self.Fill_Second_Pillars_and_Frame_4_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(32))
        self.pre_Lap_Second_Epoxy_Fill_1_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(33))
        self.pre_Lap_Second_Epoxy_Fill_2_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(34))
        self.pre_Lap_Second_Epoxy_Fill_3_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(35))
        self.LapSecondEpoxyFill_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(36))
        self.DepositFirstElectrode1_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(37))
        self.DepositFirstElectrode2_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(38))
        self.DepositFirstElectrode3_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(39))
        self.ScratchDiceElements1_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(40))
        self.ScratchDiceElements2_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(41))
        self.ScratchDiceElements3_Finish.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(42))
        
        # Back to UserWIndow
        self.HomePage_Back.clicked.connect(self.returnToUserWindow)
        self.Mount_Piezo_Wafer_1_Back.clicked.connect(self.returnToUserWindow)
        self.Mount_Piezo_Wafer_2_Back.clicked.connect(self.returnToUserWindow)
        self.Mount_Piezo_Wafer_3_Back.clicked.connect(self.returnToUserWindow)
        self.DicePiezoWaferintoSubwafers0_Back.clicked.connect(self.returnToUserWindow)
        self.DicePiezoWaferintoSubwafers1_Back.clicked.connect(self.returnToUserWindow)
        self.DicePiezoWaferintoSubwafers2_Back.clicked.connect(self.returnToUserWindow)
        self.DicePiezoWaferintoSubwafers3_Back.clicked.connect(self.returnToUserWindow)
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
        self.pre_Lap_Second_Epoxy_Fill_1_Back.clicked.connect(self.returnToUserWindow)
        self.pre_Lap_Second_Epoxy_Fill_2_Back.clicked.connect(self.returnToUserWindow)
        self.pre_Lap_Second_Epoxy_Fill_3_Back.clicked.connect(self.returnToUserWindow)
        self.LapSecondEpoxyFill_Back.clicked.connect(self.returnToUserWindow)
        self.DepositFirstElectrode1_Back.clicked.connect(self.returnToUserWindow)
        self.DepositFirstElectrode2_Back.clicked.connect(self.returnToUserWindow)
        self.DepositFirstElectrode3_Back.clicked.connect(self.returnToUserWindow)
        self.ScratchDiceElements1_Back.clicked.connect(self.returnToUserWindow)
        self.ScratchDiceElements2_Back.clicked.connect(self.returnToUserWindow)
        self.ScratchDiceElements3_Back.clicked.connect(self.returnToUserWindow)
        
        
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
    mydb = mysql.connector.connect(
        host="134.190.203.63",
        user="dslink",
        password="dstestpass123",
        database="test_db"
    )

    # admin = Admin(user_id=result[0],
    #                        user_name=result[1],
    #                        user_email=result[2],
    #                        db_class=mydb)
    # admin.register_user(user_name="Jiahao Chen",
    #                         user_job="Computer Engineering",
    #                         user_email="jiahao@gmail.com",
    #                         account_number="jh123455",
    #                         password="123456")
    
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    admin_window = Administrator_Window()
    userWindow = User_Window()
    instructionWindow = Workflow_Window()
    myWindow.show()
    sys.exit(app.exec_())
