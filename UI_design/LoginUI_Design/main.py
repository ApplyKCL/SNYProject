from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QPushButton, QHBoxLayout, QMessageBox, QTableView
from PyQt5.QtCore import QTimer, QObject, Qt
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtGui import QFont

import sys
import mysql.connector

from login import Ui_Login_Window
from Employee_Window import Ui_Employee
from Instruction_Window import Ui_InstructionWindow
from Admin_Window import Ui_Admin_Window

sys.path.append('C:/Users/ch243/Desktop/SNYProject/UI_design/LoginUI_Design/db_program')

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
        self.result = None
        self.admin_login = False
        self.admin = None
        
    def go_to_inter(self):
        account = self.UserID.text()
        password = self.Password.text()
        
        myclass = databaseAPI(database_manager.mydb, "employee_table")
        self.result = check_user(account, password, myclass)
        self.admin = Admin(user_id= self.result[0],
                        user_name= self.result[1],
                        user_email= self.result[2],
                        db_class= database_manager.mydb)
        # print(self.result)
        
        if self.result is False:
            QMessageBox.information(self,"Error Message","Invalid User/Password")
            
        elif self.result[len(self.result)-1] == 1:  # 设置对话框为弹窗模式
            dialog.exec_()
            self.admin_login = True
            
        else:
            self.hide()
            userWindow.show()
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
        admin_window.stackedWidget.setCurrentWidget(admin_window.User_System_UI)
        admin_window.show()
        
    def edit_product_info(self):
        self.hide()
        myWindow.hide()
        admin_window.stackedWidget.setCurrentWidget(admin_window.Product_System_UI)
        admin_window.show()
        
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Confirmation', 'Do you confirm to close window？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        # 根据用户的选择，决定是否关闭对话框
        if reply == QMessageBox.Yes:
            self.hide()
            myWindow.show()
        else:
            event.ignore()
        
class Administrator_Window(QMainWindow, Ui_Admin_Window):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setupUi(self)
        self.admin = None
        
        self.inactivity_timeout = InactivityTimeout(0.1, self.logout)
        
        self.pushButton_close_employee.clicked.connect(self.back_to_dialog) # type: ignore
        self.pushButton_close_workflow.clicked.connect(self.back_to_dialog) # type: ignore
        self.add_user_pushButton_2.clicked.connect(self.add_user)
        self.fresh_pushButton_2.clicked.connect(self.update_table)
        
    def update_table(self):
        # model = database_manager.get_table_model()
        # self.tableView_employee.setModel(model)
        user_info = myWindow.admin.query_user()
        
        print(user_info)
        
        self.model = TableModel(user_info)
        self.tableView_employee.setModel(self.model)
        
    def add_user(self):
        user_name_admin = self.add_user_of_user_name_lineEdit_2.text()
        user_job_admin = self.add_job.text()
        email_admin = self.add_email.text()
        user_account_admin = self.add_useraccount.text()
        password_admin = self.add_user_of_password_lineEdit_2.text()
        
        if user_name_admin and user_job_admin and email_admin and user_account_admin and password_admin is not None:
            myWindow.admin.register_user(user_name= user_name_admin,
                                user_job= user_job_admin,
                                user_email= email_admin,
                                account_number= user_account_admin,
                                password= password_admin)
        else:
            QMessageBox.information(self,"Error Message","Registration is not completed")
            
    def back_to_dialog(self):
        self.hide()
        dialog.exec_()
        
    def logout(self):
        self.hide()
        myWindow.show()
        
     
class User_Window(QMainWindow, Ui_Employee):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setupUi(self)
        self.employee_continue.clicked.connect(self.workflow_event)
        self.employee_close.clicked.connect(self.close_window)
        
        self.inactivity_timeout = InactivityTimeout(0.1, self.logout)
        
    def logout(self):
        self.hide()
        myWindow.show()
        
    def close_window(self):
        self.hide()
        myWindow.show()
        
    def workflow_event(self):
        self.hide()
        instructionWindow.show()
        
            
class Workflow_Window(QMainWindow, Ui_InstructionWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setupUi(self)
        # Initialize the HomePage
        self.stackedWidget.setCurrentWidget(self.HomePage)
        
        self.inactivity_timeout = InactivityTimeout(0.1, self.logout)
        
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
     
    def logout(self):
        self.hide()
        myWindow.show()
        
    def returnToUserWindow(self):
        self.hide()
        self.stackedWidget.setCurrentWidget(self.HomePage)
        userWindow.show()   
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

class InactivityTimeout:
    def __init__(self, timeout_minutes, timeout_callback):
        self.timeout = timeout_minutes * 60 * 1000  # Timeout in milliseconds
        self.callback = timeout_callback
        self.timer = QTimer()
        self.mouse_filter = MouseFilter(self.timer)
        
        # Install the mouse filter as an event filter
        app = QApplication.instance()
        app.installEventFilter(self.mouse_filter)

        # Connect the timer timeout signal to the timeout callback
        self.timer.timeout.connect(self.callback)

        # Start the timer
        self.timer.start(self.timeout)

    def __del__(self):
    # Remove the mouse event filter when the object is destroyed
        app = QApplication.instance()
        if app is not None:
            app.removeEventFilter(self.mouse_filter)
            

class MouseFilter(QObject):
    def __init__(self, timer):
        super().__init__()
        self.timer = timer
    
    def eventFilter(self, obj, event):
        if event.type() == event.MouseMove:
            self.timer.start()
        elif event.type() == event.MouseButtonPress:
            self.timer.start()
        return super().eventFilter(obj, event)
    

class DatabaseManager:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="950321",
            database="test_db"
        )
        
        if not self.mydb.is_connected():
            print("Failed to connect to database.")
            sys.exit(-1)
            
    # def get_table_model(self):
    #     # Create a table model that retrieves data from a table
    #     model = QSqlTableModel()
    #     model.setTable('employee_table')
    #     model.setEditStrategy(QSqlTableModel.OnFieldChange)
    #     model.select()
    #     return model
    
class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0]) 
    

if __name__ == '__main__':
    
    # mydb = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     password="950321",
    #     database="test_db"
    # )
    database_manager = DatabaseManager()
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    dialog = MyDialog()
    dialog.setModal(True)
    admin_window = Administrator_Window()
    userWindow = User_Window()
    instructionWindow = Workflow_Window()
    myWindow.show()
    sys.exit(app.exec_())
