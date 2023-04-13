from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QPushButton, QHBoxLayout, QMessageBox, QTableView, QTextEdit
from PyQt5.QtCore import QTimer, QObject, Qt

import sys
import mysql.connector

from Login_Window import Ui_Login_Window
from Employee_Window import Ui_Employee
from Instruction_Window import Ui_InstructionWindow
from Admin_Window import Ui_Admin_Window
from virtual_keyboard import *

# sys.path.append('/home/eced4901/Desktop/SNYProject/UI_design/LoginUI_Design/db_program')
sys.path.append('/Users/jiahaochen/Desktop/SNYProject/UI_design/LoginUI_Design/db_program')

from db_program.check_user import *
from db_program.mysql_statement_gen import *
from db_program.user import *
from db_program.config import *
from db_program.device_class import *

class MyWindow(QMainWindow, Ui_Login_Window, VirtualKeyboard):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setupUi(self)
        self.Login_Button.clicked.connect(self.go_to_inter)
        self.result = None
        self.admin_login = False
        self.admin = None
        
        self.UserID.mousePressEvent = self.create_line_edit_mouse_event_handler(self.UserID)
        self.Password.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Password)
        self.virtual_keyboard = None

    
    def create_line_edit_mouse_event_handler(self, line_edit):
        def line_edit_mouse_event_handler(event):
            nonlocal self, line_edit
            self.virtual_keyboard = self.line_edit_clicked(line_edit, self.virtual_keyboard)
        return line_edit_mouse_event_handler

    
    def go_to_inter(self):
        account = self.UserID.text()
        password = self.Password.text()

        self.myclass = databaseAPI(database_manager.mydb, "employee_table")
        self.result = check_user(account, password, self.myclass)
        # print(f'result check: {self.result[-2]}')

        if self.result is None:
            QMessageBox.information(self,"ErroNoner Message","Invalid User/Password")
        elif self.result[-2] == False:
            QMessageBox.information(self,"Error Message","User not activated")    
        else:
            self.admin = Admin(user_id= self.result[0],
                        user_name= self.result[1],
                        user_email= self.result[2],
                        db_class= database_manager.mydb)

            if self.result[len(self.result)-1] == 1:
                dialog.exec_()
                self.admin_login = True
            else:
                self.hide()
                userWindow.showFullScreen()

        self.virtual_keyboard = None
     
            
class MyDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Set title of dialog
        self.setWindowTitle("Admin Window")

        # build two pushbutton
        self.btn1 = QPushButton("Employee")
        self.btn2 = QPushButton("Product")

        # add event to two pushbutton
        self.btn1.clicked.connect(self.edit_employee_info)
        self.btn2.clicked.connect(self.edit_product_info)

        # build a horizontal layer
        layout = QHBoxLayout()
        layout.addWidget(self.btn1)
        layout.addWidget(self.btn2)

        # set horizontal layer for all the window
        self.setLayout(layout)

        # set window size to 512*300
        self.resize(512, 300)

    def edit_employee_info(self):
        self.hide()
        myWindow.hide()
        admin_window.stackedWidget.setCurrentWidget(admin_window.User_System_UI)
        admin_window.showFullScreen()
        
    def edit_product_info(self):
        self.hide()
        myWindow.hide()
        admin_window.stackedWidget.setCurrentWidget(admin_window.Product_System_UI)
        admin_window.showFullScreen()
        
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Confirmation', 'Do you confirm to close window', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        # depends on user choice to close the window or not
        if reply == QMessageBox.Yes:
            self.hide()
            myWindow.showFullScreen()
        else:
            event.ignore()


class Administrator_Window(QMainWindow, Ui_Admin_Window, VirtualKeyboard):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setupUi(self)
        self.id_list = None
        self.current_input = "" 
        self.into_workflow = False
        
        self.inactivity_timeout = InactivityTimeout(1, self.logout)
        
        # Employee System
        self.pushButton_close_employee.clicked.connect(self.back_to_dialog) # type: ignore
        self.pushButton_close_workflow.clicked.connect(self.back_to_dialog) # type: ignore
        self.add_user_pushButton_2.clicked.connect(self.add_user)
        self.fresh_pushButton_2.clicked.connect(self.update_table)  
        self.disable_user_pushButton_2.clicked.connect(self.disable_user)
        
        self.enable_user_pushButton_2.clicked.connect(self.enable_user)
        self.tableView_employee.setSelectionBehavior(QTableView.SelectItems)
        self.tableView_employee.clicked.connect(self.show_virtual_keyboard)
        
        # Product System
        self.pushButton_enter.clicked.connect(self.generate_workflow)
        self.pushButton_refresh_workflow.clicked.connect(self.generate_workflow)
        
        # Virtual Keyboard
        self.disable_user_name.mousePressEvent = self.create_line_edit_mouse_event_handler(self.disable_user_name)
        self.disable_password.mousePressEvent = self.create_line_edit_mouse_event_handler(self.disable_password)
        self.add_user_of_user_name_lineEdit_2.mousePressEvent = self.create_line_edit_mouse_event_handler(self.add_user_of_user_name_lineEdit_2)
        self.add_job.mousePressEvent = self.create_line_edit_mouse_event_handler(self.add_job)
        self.add_email.mousePressEvent = self.create_line_edit_mouse_event_handler(self.add_email)
        self.add_useraccount.mousePressEvent = self.create_line_edit_mouse_event_handler(self.add_useraccount)
        self.add_user_of_password_lineEdit_2.mousePressEvent = self.create_line_edit_mouse_event_handler(self.add_user_of_password_lineEdit_2)
        self.virtual_keyboard = None
        
    def generate_workflow(self):
        barcode = self.barcode_number.text()
        print(f'barcode: {barcode}')
        data = myWindow.admin.display_work_flow(barcode)
        new_data = [(tup[0], *tup[4:]) for tup in data]
        print(f'data: {new_data}')
        title = ('Data ID', 'Data Value', 'Comment', 'Initial')
        new_data = [title] + new_data
        self.model = TableModel(new_data)
        self.tableView_workflow.setModel(self.model)
        self.into_workflow = True
        
    
    def create_line_edit_mouse_event_handler(self, line_edit):
        def line_edit_mouse_event_handler(event):
            nonlocal self, line_edit
            self.virtual_keyboard = self.line_edit_clicked(line_edit, self.virtual_keyboard)
        return line_edit_mouse_event_handler
        
    def enable_user(self):
        account = self.disable_user_name.text()
        password = self.disable_password.text()
        if account and password:
            result = myWindow.admin.query_user(constrain=("account_number", "password"), constrain_value=(account,password))
            if result is False:
                QMessageBox.information(self,"Error Message","Account Number or Password is invalid")
            else:
                old_result = result[0]
                new_result = old_result[:6] + (True,) + old_result[7:]
                myWindow.admin.update_table(new_result, old_result, table_name=config.table_name[config.employee_position])
        else:
            QMessageBox.information(self,"Error Message","Account Number or Password Missed")
        
    def disable_user(self):
        account = self.disable_user_name.text()
        password = self.disable_password.text()
        if account and password:
            result = myWindow.admin.query_user(constrain=("account_number", "password"), constrain_value=(account,password))
            if result is False:
                QMessageBox.information(self,"Error Message","Account Number or Password is invalid")
            else:
                old_result = result[0]
                new_result = old_result[:6] + (False,) + old_result[7:]
                myWindow.admin.update_table(new_result, old_result, table_name=config.table_name[config.employee_position])
        else:
            QMessageBox.information(self,"Error Message","Account Number or Password Missed")
        
        
    def update_table(self):
        user_info = myWindow.admin.query_user()
        empolyee_table_title = tuple(config.table_elements_name_dict[config.table_name[config.employee_position]])
        self.id_list = [tup[0] for tup in user_info]
        user_info.insert(0, empolyee_table_title)
        user_info = [t[1:] for t in user_info]
        self.model = TableModel(user_info)
        self.tableView_employee.setModel(self.model)
        # self.tableView_employee.clicked.connect(self.show_virtual_keyboard)
        
    def show_virtual_keyboard(self, index):
        if index.isValid():
            virtual_keyboard = VirtualKeyboard(self)
            virtual_keyboard.set_focused_tableview(self.tableView_employee) 
            virtual_keyboard.keyPressed.connect(lambda key: self.key_pressed(key, index))
            virtual_keyboard.move(self.pos().x() + 300, self.pos().y())
            virtual_keyboard.show()

    def key_pressed(self, key, index):
        if key == " ":
            self.model.setData(index, self.current_input, Qt.EditRole)
            self.current_input = ""
        else:
            self.current_input += key

    def add_user(self):
        user_name_admin = self.add_user_of_user_name_lineEdit_2.text()
        user_job_admin = self.add_job.text()
        email_admin = self.add_email.text()
        user_account_admin = self.add_useraccount.text()
        password_admin = self.add_user_of_password_lineEdit_2.text()
        
        if user_name_admin and user_job_admin and email_admin and user_account_admin and password_admin:
            myWindow.admin.register_user(user_name= user_name_admin,
                                user_job= user_job_admin,
                                user_email= email_admin,
                                account_number= user_account_admin,
                                password= password_admin)
            if myWindow.admin.accout_number_status is False:
                QMessageBox.information(self,"Error Message","Account Number is existed")
                myWindow.admin.accout_number_status=True
        else:
            QMessageBox.information(self, "Error Message", "Registration is not completed")

    def back_to_dialog(self):
        self.hide()
        dialog.exec_()

    def logout(self):
        self.hide()
        myWindow.showFullScreen()
        
     
class User_Window(QMainWindow, Ui_Employee):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setupUi(self)
        self.barcode_result = None
        self.employee_continue.clicked.connect(self.workflow_event)
        self.employee_close.clicked.connect(self.close_window)
        
        self.inactivity_timeout = InactivityTimeout(1, self.logout)
        
    def logout(self):
        self.hide()
        myWindow.showFullScreen()
        
    def close_window(self):
        self.hide()
        myWindow.showFullScreen()
        
    def workflow_event(self):
        self.barcode = self.employee_barcode.text()
        if self.barcode is None or self.barcode == '':
            QMessageBox.information(self, "Error Message", "Barcode is not scanned")
        else:
            self.barcode_result = myWindow.admin.barcode_context(barcode=self.barcode)
            # print(f'self.barcode_result: {self.barcode_result}')
            if self.barcode_result=="NEW":
                self.hide()
                instructionWindow.showFullScreen()
                self.barcode_result = myWindow.admin.create_new_process(barcode=self.barcode)
            else:
                page_number = int((self.barcode_result[0].split(":"))[2])
                self.hide()
                instructionWindow.stackedWidget.setCurrentIndex(page_number)
                instructionWindow.showFullScreen()
            # self.barcode = "next"
        
            
class Workflow_Window(QMainWindow, Ui_InstructionWindow, VirtualKeyboard):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setupUi(self)
        # Initialize the HomePage
        self.stackedWidget.setCurrentWidget(self.HomePage)
        
        self.inactivity_timeout = InactivityTimeout(1, self.logout)
        
        # Move to Next Page
        self.HomePage_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.Mount_Piezo_Wafer_1_Next.clicked.connect(self.store_data_to_next_page_MPW)
        self.DicePiezoWaferintoSubwafers1_Next.clicked.connect(self.store_data_to_next_page_DPWIS)
        self.Dice_Framing_Piezo_3_Next.clicked.connect(self.store_data_to_next_page_DFP)
        self.Premount_Clean_and_Measure_Subwafer_1_Next.clicked.connect(self.store_data_to_next_page_PCMS)
        self.Mount_Subwafers_Next.clicked.connect(self.store_data_to_next_page_MSW)
        self.Dice_First_Pillars_2_Next.clicked.connect(self.store_data_to_next_page_DFPR)
        # self.LapSecondEpoxyFill_Next.clicked.connect(self.store_data_to_next_page_LSEF)

        # Back to UserWIndow
        self.HomePage_Back.clicked.connect(self.returnToUserWindow)
        self.Mount_Piezo_Wafer_1_Back.clicked.connect(self.returnToUserWindow)
        self.DicePiezoWaferintoSubwafers1_Back.clicked.connect(self.returnToUserWindow)
        self.Dice_Framing_Piezo_3_Back.clicked.connect(self.returnToUserWindow)
        self.Premount_Clean_and_Measure_Subwafer_1_Back.clicked.connect(self.returnToUserWindow)
        self.Mount_Subwafers_Back.clicked.connect(self.returnToUserWindow)
        self.Dice_First_Pillars_2_Back.clicked.connect(self.returnToUserWindow)
        # self.LapSecondEpoxyFill_Back.clicked.connect(self.returnToUserWindow)
        
        # Virtual Keyboard
        self.HomePage_Name.mousePressEvent = self.create_text_edit_mouse_event_handler(self.HomePage_Name)
        self.Mount_Piezo_Wafer_1_Data.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Mount_Piezo_Wafer_1_Data)
        self.Mount_Piezo_Wafer_1_Comments_3.mousePressEvent = self.create_text_edit_mouse_event_handler(self.Mount_Piezo_Wafer_1_Comments_3)
        self.Mount_Piezo_Wafer_1_Initial.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Mount_Piezo_Wafer_1_Initial)
        self.Mount_Piezo_Wafer_1_Dates.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Mount_Piezo_Wafer_1_Dates)
        self.DicePiezoWaferintoSubwafers1_Data.mousePressEvent = self.create_line_edit_mouse_event_handler(self.DicePiezoWaferintoSubwafers1_Data)
        self.DicePiezoWaferintoSubwafers1_comments.mousePressEvent = self.create_text_edit_mouse_event_handler(self.DicePiezoWaferintoSubwafers1_comments)
        self.DicePiezoWaferintoSubwafers1_Dates.mousePressEvent = self.create_line_edit_mouse_event_handler(self.DicePiezoWaferintoSubwafers1_Dates)
        self.DicePiezoWaferintoSubwafers1_Initals.mousePressEvent = self.create_line_edit_mouse_event_handler(self.DicePiezoWaferintoSubwafers1_Initals)
        self.Dice_Framing_Piezo_3_Data.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Dice_Framing_Piezo_3_Data)
        self.Dice_Framing_Piezo_3_Comments.mousePressEvent = self.create_text_edit_mouse_event_handler(self.Dice_Framing_Piezo_3_Comments)
        self.Dice_Framing_Piezo_3_Dates.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Dice_Framing_Piezo_3_Dates)
        self.Dice_Framing_Piezo_3_Initial.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Dice_Framing_Piezo_3_Initial)
        self.Premount_Clean_and_Measure_Subwafer_1_Data0.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Premount_Clean_and_Measure_Subwafer_1_Data0)
        self.Premount_Clean_and_Measure_Subwafer_1_Data1.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Premount_Clean_and_Measure_Subwafer_1_Data1)
        self.Premount_Clean_and_Measure_Subwafer_1_Data2.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Premount_Clean_and_Measure_Subwafer_1_Data2)
        self.Premount_Clean_and_Measure_Subwafer_1_Data3.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Premount_Clean_and_Measure_Subwafer_1_Data3)
        self.Premount_Clean_and_Measure_Subwafer_1_Data4.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Premount_Clean_and_Measure_Subwafer_1_Data4)
        self.Premount_Clean_and_Measure_Subwafer_1_Data5.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Premount_Clean_and_Measure_Subwafer_1_Data5)
        self.Premount_Clean_and_Measure_Subwafer_1_Data6.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Premount_Clean_and_Measure_Subwafer_1_Data6)
        self.Premount_Clean_and_Measure_Subwafer_1_Data7.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Premount_Clean_and_Measure_Subwafer_1_Data7)
        self.Premount_Clean_and_Measure_Subwafer_1_Data8.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Premount_Clean_and_Measure_Subwafer_1_Data8)
        self.Premount_Clean_and_Measure_Subwafer_1_Data9.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Premount_Clean_and_Measure_Subwafer_1_Data9)
        self.Premount_Clean_and_Measure_Subwafer_1_Data10.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Premount_Clean_and_Measure_Subwafer_1_Data10)
        self.Premount_Clean_and_Measure_Subwafer_1_Data11.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Premount_Clean_and_Measure_Subwafer_1_Data11)
        self.Premount_Clean_and_Measure_Subwafer_1_Comments.mousePressEvent = self.create_text_edit_mouse_event_handler(self.Premount_Clean_and_Measure_Subwafer_1_Comments)
        self.Premount_Clean_and_Measure_Subwafer_1_Dates.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Premount_Clean_and_Measure_Subwafer_1_Dates)
        self.Premount_Clean_and_Measure_Subwafer_1_Initial.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Premount_Clean_and_Measure_Subwafer_1_Initial)
        self.Mount_Subwafers_Data0.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Mount_Subwafers_Data0) 
        self.Mount_Subwafers_Data1.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Mount_Subwafers_Data1)
        self.Mount_Subwafers_Data2.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Mount_Subwafers_Data2)
        self.Mount_Subwafers_Data3.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Mount_Subwafers_Data3)
        self.Mount_Subwafers_Data4.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Mount_Subwafers_Data4)
        self.Mount_Subwafers_Data5.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Mount_Subwafers_Data5)
        self.Mount_Subwafers_Data6.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Mount_Subwafers_Data6)
        self.Mount_Subwafers_Data7.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Mount_Subwafers_Data7)
        self.Mount_Subwafers_Data8.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Mount_Subwafers_Data8)
        self.Mount_Subwafers_Data9.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Mount_Subwafers_Data9)
        self.Mount_Subwafers_Data10.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Mount_Subwafers_Data10)
        self.Mount_Subwafers_Data11.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Mount_Subwafers_Data11)
        self.Mount_Subwafers_Data12.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Mount_Subwafers_Data12)
        self.Mount_Subwafers_Data13.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Mount_Subwafers_Data13)
        self.Mount_Subwafers_Data14.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Mount_Subwafers_Data14)
        self.Mount_Subwafers_Data15.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Mount_Subwafers_Data15)
        self.Mount_Subwafers_Comments.mousePressEvent = self.create_text_edit_mouse_event_handler(self.Mount_Subwafers_Comments)
        self.Mount_Subwafers_Dates.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Mount_Subwafers_Dates)
        self.Mount_Subwafers_Initial.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Mount_Subwafers_Initial)
        self.Dice_First_Pillars_2_Data.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Dice_First_Pillars_2_Data)
        self.Dice_First_Pillars_2_Initial1.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Dice_First_Pillars_2_Initial1)
        self.Dice_First_Pillars_2_Initial2.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Dice_First_Pillars_2_Initial2)
        self.Dice_First_Pillars_2_Comments.mousePressEvent = self.create_text_edit_mouse_event_handler(self.Dice_First_Pillars_2_Comments)
        self.Dice_First_Pillars_2_Dates.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Dice_First_Pillars_2_Dates)
        # self.LapSecondEpoxyFill_Data1.mousePressEvent = self.create_line_edit_mouse_event_handler(self.LapSecondEpoxyFill_Data1)
        # self.LapSecondEpoxyFill_Data2.mousePressEvent = self.create_line_edit_mouse_event_handler(self.LapSecondEpoxyFill_Data2)
        # self.LapSecondEpoxyFill_Data3.mousePressEvent = self.create_line_edit_mouse_event_handler(self.LapSecondEpoxyFill_Data3)
        # self.LapSecondEpoxyFill_Data4.mousePressEvent = self.create_line_edit_mouse_event_handler(self.LapSecondEpoxyFill_Data4)
        # self.LapSecondEpoxyFill_Data5.mousePressEvent = self.create_line_edit_mouse_event_handler(self.LapSecondEpoxyFill_Data5)
        # self.LapSecondEpoxyFill_Data6.mousePressEvent = self.create_line_edit_mouse_event_handler(self.LapSecondEpoxyFill_Data6)
        # self.LapSecondEpoxyFill_Data7.mousePressEvent = self.create_line_edit_mouse_event_handler(self.LapSecondEpoxyFill_Data7)
        # self.LapSecondEpoxyFill_Data8.mousePressEvent = self.create_line_edit_mouse_event_handler(self.LapSecondEpoxyFill_Data8)
        # self.LapSecondEpoxyFill_Data9.mousePressEvent = self.create_line_edit_mouse_event_handler(self.LapSecondEpoxyFill_Data9)
        # self.LapSecondEpoxyFill_Dates.mousePressEvent = self.create_line_edit_mouse_event_handler(self.LapSecondEpoxyFill_Dates)
        # self.LapSecondEpoxyFill_Initials.mousePressEvent = self.create_line_edit_mouse_event_handler(self.LapSecondEpoxyFill_Initials)
        
        self.virtual_keyboard = None
        
    def store_data_to_next_page_MPW(self):
        data=[]
        data = myWindow.admin.barcode_context(userWindow.barcode)[1][0]
        # print(f'data MPW is {data}')
        data[4] = self.Mount_Piezo_Wafer_1_Data.text()
        data[5] = self.Mount_Piezo_Wafer_1_Comments_3.toPlainText()
        data[6] = self.Mount_Piezo_Wafer_1_Initial.text()
        myWindow.admin.input_data([data])
        input_check = myWindow.admin.barcode_context(barcode='next')
        # print(f'input_check MPW is {input_check}')
        if input_check != 'NF':
            self.stackedWidget.setCurrentIndex(2)
        else:
             QMessageBox.about(self, "Error", "Input value is not finished")
                
    def store_data_to_next_page_DPWIS(self):
        data=[]
        data= myWindow.admin.barcode_context(userWindow.barcode)[1][0]
        # print(f'data DPWIS is {data}')
        data[4] = self.DicePiezoWaferintoSubwafers1_Data.text()
        data[5] = self.DicePiezoWaferintoSubwafers1_comments.toPlainText()
        data[6] = self.DicePiezoWaferintoSubwafers1_Initals.text()
        myWindow.admin.input_data([data])
        input_check = myWindow.admin.barcode_context(barcode='next')
        # print(f'input_check DPWIS is {input_check}')
        if input_check != 'NF':
            self.stackedWidget.setCurrentIndex(3)
        else:
             QMessageBox.about(self, "Error", "Input value is not finished")
    
    def store_data_to_next_page_DFP(self):
        data=[]
        data= myWindow.admin.barcode_context(userWindow.barcode)[1][0]
        data[4] = self.Dice_Framing_Piezo_3_Data.text()
        data[5] = self.Dice_Framing_Piezo_3_Comments.toPlainText()
        data[6] = self.Dice_Framing_Piezo_3_Initial.text()
        myWindow.admin.input_data([data])
        input_check = myWindow.admin.barcode_context(barcode='next')
        if input_check != 'NF':
            self.stackedWidget.setCurrentIndex(4)
        else:
             QMessageBox.about(self, "Error", "Input value is not finished")
        
    def store_data_to_next_page_PCMS(self):
        data = []
        barcode_result = myWindow.admin.barcode_context(userWindow.barcode)
        # print(f'barcode_result is : {barcode_result}')
        # print(f'barcode_result length is : {len(barcode_result[1])}')
        for i in range(len(barcode_result[1])):
            # print(f'i is: {i}')
            data.append(barcode_result[1][i])
            if i == 0:
                data[i][4]= getattr(self, f"Premount_Clean_and_Measure_Subwafer_1_Data{i}").text()
                # data[i][4] = self.Mount_Piezo_Wafer_1_Data.text()
                data[i][5] = self.Premount_Clean_and_Measure_Subwafer_1_Comments.toPlainText()
                data[i][6] = self.Premount_Clean_and_Measure_Subwafer_1_Initial.text()
            else:
                data[i][4] = getattr(self, f"Premount_Clean_and_Measure_Subwafer_1_Data{i}").text()
                data[i][5] = None
                data[i][6] = None
        # print(f'data: {data}')
        myWindow.admin.input_data(data)
        input_check = myWindow.admin.barcode_context(barcode='next')
        # print(f'input_check PCMS is {input_check}')
        if input_check != 'NF':
            self.stackedWidget.setCurrentIndex(5)
        else:
             QMessageBox.about(self, "Error", "Input value is not finished")
                
    def store_data_to_next_page_MSW(self):
        data=[]
        barcode_result = myWindow.admin.barcode_context(userWindow.barcode)
        for i in range(len(barcode_result[1])):
            data.append(barcode_result[1][i])
            if i == 0:
                data[i][4]= getattr(self, f"Mount_Subwafers_Data{i}").text()
                # data[i][4] = self.Mount_Piezo_Wafer_1_Data.text()
                data[i][5] = self.Mount_Subwafers_Comments.toPlainText()
                data[i][6] = self.Mount_Subwafers_Initial.text()
            else:
                data[i][4] = getattr(self, f"Mount_Subwafers_Data{i}").text()
                data[i][5] = None
                data[i][6] = None
        myWindow.admin.input_data(data)
        input_check = myWindow.admin.barcode_context(barcode='next')
        if input_check != 'NF':
            self.stackedWidget.setCurrentIndex(6)
        else:
             QMessageBox.about(self, "Error", "Input value is not finished")
                
    def store_data_to_next_page_DFPR(self):
        data=[[],[]]
        data[0]= myWindow.admin.barcode_context(userWindow.barcode)[1][0]
        data[0][4] = self.Dice_First_Pillars_2_Data.text()
        data[0][5] = self.Dice_First_Pillars_2_Comments.toPlainText()
        data[0][6] = self.Dice_First_Pillars_2_Initial2.text()
        data[1]= myWindow.admin.barcode_context(userWindow.barcode)[1][1]
        data[1][4] = self.Dice_First_Pillars_2_Initial1.text()
        data[1][5] = None
        data[1][6] = None
        myWindow.admin.input_data(data)
        input_check = myWindow.admin.barcode_context(barcode='next')
        if input_check != 'NF':
            self.stackedWidget.setCurrentIndex(6)
            QMessageBox.about(self, "Warning", "Workflow is done!")
        else:
             QMessageBox.about(self, "Error", "Input value is not finished")
        
    # def store_data_to_next_page_LSEF(self):
    #     data=[]
    #     barcode_result = myWindow.admin.barcode_context(userWindow.barcode)
    #     for i in range(len(barcode_result[1])):
    #         data[i].append(barcode_result[1][i])
    #         if i == 1:
    #             data[i][4]= getattr(self, f"LapSecondEpoxyFill_Data{i}").text()
    #             data[i][5] = None
    #             data[i][6] = self.LapSecondEpoxyFill_Initials.text()
    #         else:
    #             data[i][4] = getattr(self, f"LapSecondEpoxyFill_Data{i}").text()
    #             data[i][5] = None
    #             data[i][6] = None
    #     myWindow.admin.input_data(data)
    #     input_check = myWindow.admin.barcode_context(barcode='next')
    #     if input_check != 'NF':
    #         self.stackedWidget.setCurrentIndex(7)
    #     else:
    #          QMessageBox.about(self, "Error", "Input value is not finished")
                
    
    def create_line_edit_mouse_event_handler(self, line_edit):
        def line_edit_mouse_event_handler(event):
            nonlocal self, line_edit
            self.virtual_keyboard = self.line_edit_clicked(line_edit, self.virtual_keyboard)
        return line_edit_mouse_event_handler
    
    def create_text_edit_mouse_event_handler(self, text_edit):
        def text_edit_mouse_event_handler(event):
            nonlocal self, text_edit
            self.virtual_keyboard = self.text_edit_clicked(text_edit, self.virtual_keyboard)
        return text_edit_mouse_event_handler


    def logout(self):
        self.hide()
        myWindow.showFullScreen()
        
    def returnToUserWindow(self):
        self.hide()
        self.stackedWidget.setCurrentWidget(self.HomePage)
        userWindow.showFullScreen()   
        
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
            # Remote Connection Configure
            host="134.190.203.146",
            # host="192.168.4.30",
            user="dslink",
            password="dstestpass123",
            
            # Local Connection Configure
            # host="localhost",
            # user="root",
            # password="369300Ab*",
            
            database="DaxsonicsBuildTrackDB"
        )

        if not self.mydb.is_connected():
            print("Failed to connect to database.")
            sys.exit(-1)
            
    
class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data
        
    def get_data(self, index):
        return self._data[index.row()][index.column()]

    def data(self, index, role):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self.get_data(index)
        return None

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0]) if self._data else 0
    
    def setData(self, index, value, role):
        if  role == Qt.EditRole:
            row = index.row()
            column = index.column()
            data_row = list(self._data[row])
            data_row[column] = value
            self._data[row] = tuple(data_row)
            self.dataChanged.emit(index, index)
            if admin_window.into_workflow == False:
                result = myWindow.admin.query_user(constrain=("id",), constrain_value=(admin_window.id_list[row],))
                data_row.insert(0,result[0][0])
                new_result = tuple(data_row)
                myWindow.admin.update_table(new_result, result[0], table_name=config.table_name[config.employee_position])
            return True
        return False
    
    def flags(self,index):
        return Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled
    
if __name__ == '__main__':
    database_manager = DatabaseManager()
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    dialog = MyDialog()
    dialog.setModal(True)
    admin_window = Administrator_Window()
    userWindow = User_Window()
    instructionWindow = Workflow_Window()
    myWindow.showFullScreen()
    sys.exit(app.exec_())
