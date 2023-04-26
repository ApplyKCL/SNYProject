"""
Author: Jiahao Chen
Description: This is the main program for all the UI design, the database connection, 
virtual keyboard and 15min counter timer. All the connection between the UI, the database,
virtual keyboard and timer are in this file. The different UI are in the UI_design folder.
Virtual keyboard is in the virtual_keyboard.py file. Timer function is in this file already.
"""

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QPushButton, QHBoxLayout, QMessageBox, QTableView
from PyQt5.QtCore import QTimer, QObject, Qt

import sys
import mysql.connector

# Based on different IDE, the path should be changed
# All the UI files are loaded here
# sys.path.append('/home/eced4901/Desktop/SNYProject/UI_design/LoginUI_Design/UI_files')
sys.path.append('/Users/jiahaochen/Downloads/SNYProject/Daxsonics_Ultrasound_Transducer_Build_Tracker/UI_files')
from Login_Window import Ui_Login_Window
from Employee_Window import Ui_Employee
from Instruction_Window import Ui_InstructionWindow
from Admin_Window import Ui_Admin_Window
from virtual_keyboard import *

# Based on different IDE, the path should be changed
# All the database files are loaded here
# sys.path.append('/home/eced4901/Desktop/SNYProject/UI_design/LoginUI_Design/db_program')
sys.path.append('/Users/jiahaochen/Downloads/SNYProject/Daxsonics_Ultrasound_Transducer_Build_Tracker/db_program')
from db_program.check_user import *
from db_program.mysql_statement_gen import *
from db_program.user import *
from db_program.config import *
from db_program.device_class import *

"""
The flow of the program is:
Login -> User -> Instruction 
      -> Admin -> Employee/Product
The guidenice of the program can be found in report/ PPT/ Demostration video.
If you had further question, you can reach one of us.
"""

class MyWindow(QMainWindow, Ui_Login_Window, VirtualKeyboard):
    """
    This is the main window of the program, Login window
    The program should start from here
    The virtual keyboard includes in this class
    Args:
        QMainWindow (Qwidget): The main window of the program
        Ui_Login_Window (object): The UI of the login window
        VirtualKeyboard (QDialog): The virtual keyboard
    """
    def __init__(self):
        super().__init__()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setupUi(self)
        self.Login_Button.clicked.connect(self.go_to_inter)
        self.result = None
        self.admin_login = False
        self.admin = None
        
        # The virtual keyboard event connection
        self.UserID.mousePressEvent = self.create_line_edit_mouse_event_handler(self.UserID)
        self.Password.mousePressEvent = self.create_line_edit_mouse_event_handler(self.Password)
        self.virtual_keyboard = None

    # The event handler function for virtual keyboard
    # It will be called when the line edit is clicked
    # Virtual keyboard will be shown and wait for user input
    def create_line_edit_mouse_event_handler(self, line_edit):
        def line_edit_mouse_event_handler(event):
            nonlocal self, line_edit
            self.virtual_keyboard = self.line_edit_clicked(line_edit, self.virtual_keyboard)
        return line_edit_mouse_event_handler

    # function for the login button
    def go_to_inter(self):
        """
        This function is for the login button, it will check the user input
        after the button is clicked. If the user input is correct, it will
        hide the login window and show the user window. If the user is admin,
        it will show the admin window. If the user input is incorrect, it will
        show the error message.
        """
        account = self.UserID.text()
        password = self.Password.text()
        
        # The database connection and get the user information
        self.myclass = databaseAPI(database_manager.mydb, "employee_table")
        self.result = check_user(account, password, self.myclass)

        if self.result is None:
            QMessageBox.information(self,"ErroNoner Message","Invalid User/Password")
        elif self.result[-2] == False:
            QMessageBox.information(self,"Error Message","User not activated")    
        else:
            # Initialize the admin class for the further use
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
    """
    This is the dialog window for the admin to choose the function.
    There are two function for the admin, employee information and
    product information.
    """
    def __init__(self):
        # Initialize the dialog window with two pushbutton Employee and Product
        # Employee and product window are in the Admin_Window.py file
        # Used stackedWidget(you can google or chatgpt, if you don't have idea on it)
        # to switch between the two window
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

    # The event handler for employee button
    def edit_employee_info(self):
        self.hide()
        myWindow.hide()
        admin_window.stackedWidget.setCurrentWidget(admin_window.User_System_UI)
        admin_window.showFullScreen()
    
    # The event handler for product button    
    def edit_product_info(self):
        self.hide()
        myWindow.hide()
        admin_window.stackedWidget.setCurrentWidget(admin_window.Product_System_UI)
        admin_window.showFullScreen()
    
    # The event handler for close button, it will close the dialog window
    # and back to the login window
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Confirmation', 'Do you confirm to close window', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        # depends on user choice to close the window or not
        if reply == QMessageBox.Yes:
            self.hide()
            myWindow.showFullScreen()
        else:
            event.ignore()


class Administrator_Window(QMainWindow, Ui_Admin_Window, VirtualKeyboard):
    """
    This is the admin window, it includes two function, edit employee information
    and edit product information. Program include check, add/edit and enable/disable employee information.
    And check/edit product information.
    """
    def __init__(self):
        super().__init__()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setupUi(self)
        self.id_list = None
        self.current_input = "" 
        self.into_workflow = False
        
        # 15 minutes inactivity timeout
        self.inactivity_timeout = InactivityTimeout(15, self.logout)
        
        # Connection for the employee section
        self.pushButton_close_employee.clicked.connect(self.back_to_dialog)
        self.pushButton_close_workflow.clicked.connect(self.back_to_dialog)
        self.add_user_pushButton_2.clicked.connect(self.add_user)
        self.fresh_pushButton_2.clicked.connect(self.update_table)  
        self.disable_user_pushButton_2.clicked.connect(self.disable_user)
        self.enable_user_pushButton_2.clicked.connect(self.enable_user)
        
        # Print the employee information in the table
        # SelectionBehavior is used to select the cells
        self.tableView_employee.setSelectionBehavior(QTableView.SelectItems)
        self.tableView_employee.clicked.connect(self.show_virtual_keyboard)
        
        # Connection for the product section
        self.pushButton_enter.clicked.connect(self.generate_workflow)
        self.pushButton_refresh_workflow.clicked.connect(self.generate_workflow)
        
        # Virtual Keyboard connection
        self.disable_user_name.mousePressEvent = self.create_line_edit_mouse_event_handler(self.disable_user_name)
        self.disable_password.mousePressEvent = self.create_line_edit_mouse_event_handler(self.disable_password)
        self.add_user_of_user_name_lineEdit_2.mousePressEvent = self.create_line_edit_mouse_event_handler(self.add_user_of_user_name_lineEdit_2)
        self.add_job.mousePressEvent = self.create_line_edit_mouse_event_handler(self.add_job)
        self.add_email.mousePressEvent = self.create_line_edit_mouse_event_handler(self.add_email)
        self.add_useraccount.mousePressEvent = self.create_line_edit_mouse_event_handler(self.add_useraccount)
        self.add_user_of_password_lineEdit_2.mousePressEvent = self.create_line_edit_mouse_event_handler(self.add_user_of_password_lineEdit_2)
        self.virtual_keyboard = None
        
    def generate_workflow(self):
        """
        This function is used to generate the workflow table based on 
        the barcode number. The data need to be filled in the TableModel(),
        TableModle() will processing the data and display it by calling setModel().
        """
        barcode = self.barcode_number.text()
        barcode_result = myWindow.admin.barcode_context(barcode)
        if barcode_result=="NEW":
            QMessageBox.warning(self, "Warning", "The barcode is not in the database, please check again")
        else:
            data = myWindow.admin.display_work_flow(barcode)
            new_data = [(tup[0], *tup[4:]) for tup in data]
            title = ('Data ID', 'Data Value', 'Comment', 'Initial')
            new_data = [title] + new_data
            self.model = TableModel(new_data)
            self.tableView_workflow.setModel(self.model)
            self.into_workflow = True
        
    
    def create_line_edit_mouse_event_handler(self, line_edit):
        # This function is used to create a mouse event handler for the line edit
        # It will be used to show the virtual keyboard
        def line_edit_mouse_event_handler(event):
            nonlocal self, line_edit
            self.virtual_keyboard = self.line_edit_clicked(line_edit, self.virtual_keyboard)
        return line_edit_mouse_event_handler
        
    def enable_user(self):
        """
        Based on the account number and password, the function will enable the user.
        query_user() will return the user information if the account number and password
        is exist. Then the function will update the user information to enable the user.
        If not, it will show the error message.
        """
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
        # Same as the enable_user() function
        # The only difference is the user will be disabled
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
        # This function is used to update the employee table
        # It will call the query_user() function to get the user information
        # Processing the data by calling TableModel()
        # Then it will update the table by calling setModel()
        user_info = myWindow.admin.query_user()
        empolyee_table_title = tuple(config.table_elements_name_dict[config.table_name[config.employee_position]])
        self.id_list = [tup[0] for tup in user_info]
        user_info.insert(0, empolyee_table_title)
        user_info = [t[1:] for t in user_info]
        self.model = TableModel(user_info)
        self.tableView_employee.setModel(self.model)
        
    def show_virtual_keyboard(self, index):
        """
        This function is used to call the virtual keyboard in the table view
        The virtual keyboard will be shown when the user click cells in the table view
        """
        if index.isValid():
            virtual_keyboard = VirtualKeyboard(self)
            virtual_keyboard.set_focused_tableview(self.tableView_employee) 
            virtual_keyboard.keyPressed.connect(lambda key: self.key_pressed(key, index))
            virtual_keyboard.move(self.pos().x() + 300, self.pos().y())
            virtual_keyboard.show()

    def key_pressed(self, key, index):
        """
        This function is used to set the virtual keyboard input to the table view
        Space key will be used to check whether the input is finished
        The reason for that is the QTableview can not be edited word by word
        """
        if key == " ":
            self.model.setData(index, self.current_input, Qt.EditRole)
            self.current_input = ""
        else:
            self.current_input += key

    def add_user(self):
        """
        This function is used to add user to the database
        It will generate user information based on the user input
        Then check whether the user information is valid or not
        If it is valid, it will add the user to the database
        If not, it will show the error message
        """
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

    # Back to the dialog window for admin
    def back_to_dialog(self):
        self.hide()
        dialog.exec_()

    # Logout the admin and back to the Login window
    def logout(self):
        self.hide()
        myWindow.showFullScreen()
        
     
class User_Window(QMainWindow, Ui_Employee):
    """
    This class is used to create the user window
    The main function is to generate the barcode and 
    open the instruction window properly
    """
    def __init__(self):
        super().__init__()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setupUi(self)
        self.barcode_result = None
        self.employee_continue.clicked.connect(self.workflow_event)
        self.employee_close.clicked.connect(self.close_window)
        
        # 15 minutes timer for logtout the user
        self.inactivity_timeout = InactivityTimeout(15, self.logout)
        
    # Logout the user and back to the Login window    
    def logout(self):
        self.hide()
        myWindow.showFullScreen()
        
    # Close the user window and back to the Login window
    def close_window(self):
        self.hide()
        myWindow.showFullScreen()
        
    def workflow_event(self):
        """
        Generate the barcode and check whether the barcode is valid or not
        If it is a new barcode, it will build workflow window and show the first page
        If barcode is existed, it will show the continue page left from last time
        If barcode is invalid, it will show the error message
        """
        self.barcode = self.employee_barcode.text()
        if self.barcode is None or self.barcode == '':
            QMessageBox.information(self, "Error Message", "Barcode is not scanned")
        else:
            self.barcode_result = myWindow.admin.barcode_context(barcode=self.barcode)
            if self.barcode_result=="NEW":
                self.hide()
                instructionWindow.showFullScreen()
                self.barcode_result = myWindow.admin.create_new_process(barcode=self.barcode)
            else:
                page_number = int((self.barcode_result[0].split(":"))[2])
                self.hide()
                instructionWindow.stackedWidget.setCurrentIndex(page_number)
                instructionWindow.showFullScreen()
        
            
class Workflow_Window(QMainWindow, Ui_InstructionWindow, VirtualKeyboard):
    """
    This class is used to create the workflow window
    All the pages are stored in the stackedWidget
    All the data will be generated based on the user input
    And store them in the database
    """
    def __init__(self):
        super().__init__()
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setupUi(self)
        # Initialize the HomePage
        self.stackedWidget.setCurrentWidget(self.HomePage)
        # Initialize the Timer for 15 minutes
        self.inactivity_timeout = InactivityTimeout(15, self.logout)
        
        # Set up the connection with "Next" button, clicked button will generate all the
        # data and move to Next Page
        self.HomePage_Next.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.Mount_Piezo_Wafer_1_Next.clicked.connect(self.store_data_to_next_page_MPW)
        self.DicePiezoWaferintoSubwafers1_Next.clicked.connect(self.store_data_to_next_page_DPWIS)
        self.Dice_Framing_Piezo_3_Next.clicked.connect(self.store_data_to_next_page_DFP)
        self.Premount_Clean_and_Measure_Subwafer_1_Next.clicked.connect(self.store_data_to_next_page_PCMS)
        self.Mount_Subwafers_Next.clicked.connect(self.store_data_to_next_page_MSW)
        self.Dice_First_Pillars_2_Next.clicked.connect(self.store_data_to_next_page_DFPR)

        # Set up the connection with "Back" button, clicked button will back to user window
        self.HomePage_Back.clicked.connect(self.returnToUserWindow)
        self.Mount_Piezo_Wafer_1_Back.clicked.connect(self.returnToUserWindow)
        self.DicePiezoWaferintoSubwafers1_Back.clicked.connect(self.returnToUserWindow)
        self.Dice_Framing_Piezo_3_Back.clicked.connect(self.returnToUserWindow)
        self.Premount_Clean_and_Measure_Subwafer_1_Back.clicked.connect(self.returnToUserWindow)
        self.Mount_Subwafers_Back.clicked.connect(self.returnToUserWindow)
        self.Dice_First_Pillars_2_Back.clicked.connect(self.returnToUserWindow)
        
        # Add event handler for Virtual Keyboard
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
        
        self.virtual_keyboard = None
    
    # Store all the datas need to be collected in the MPW page
    def store_data_to_next_page_MPW(self):
        """
        Based on the data structure from the database, the data is stored in the list
        barcode===>next used for checking if the input is finished and move to the next page
        If any input is missing, the error message will be shown
        """
        data=[]
        # Initialize the data list
        data = myWindow.admin.barcode_context(userWindow.barcode)[1][0]
        print(f'data is {data}')
        data[4] = self.Mount_Piezo_Wafer_1_Data.text()
        data[5] = self.Mount_Piezo_Wafer_1_Comments_3.toPlainText()
        data[6] = self.Mount_Piezo_Wafer_1_Initial.text()
        # Store the data to the database
        myWindow.admin.input_data([data])
        # Check if the input is finished
        input_check = myWindow.admin.barcode_context(barcode='next')
        if input_check != 'NF':
            self.stackedWidget.setCurrentIndex(2)
        else:
             QMessageBox.about(self, "Error", "Input value is not finished")
             
    # Store all the datas need to be collected in the DPWIS page            
    def store_data_to_next_page_DPWIS(self):
        # Function is same as the MPW page
        data=[]
        data= myWindow.admin.barcode_context(userWindow.barcode)[1][0]
        data[4] = self.DicePiezoWaferintoSubwafers1_Data.text()
        data[5] = self.DicePiezoWaferintoSubwafers1_comments.toPlainText()
        data[6] = self.DicePiezoWaferintoSubwafers1_Initals.text()
        myWindow.admin.input_data([data])
        input_check = myWindow.admin.barcode_context(barcode='next')
        if input_check != 'NF':
            self.stackedWidget.setCurrentIndex(3)
        else:
             QMessageBox.about(self, "Error", "Input value is not finished")
    
    # Store all the datas need to be collected in the DFP page
    def store_data_to_next_page_DFP(self):
        # Function is same as the MPW page
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
    
    # Store all the datas need to be collected in the PCMS page    
    def store_data_to_next_page_PCMS(self):
        # Function is same as the MPW page
        # The difference is that the number of input data is more than one
        data = []
        barcode_result = myWindow.admin.barcode_context(userWindow.barcode)
        # Returned data list has all the elements needed to be collected
        for i in range(len(barcode_result[1])):
            data.append(barcode_result[1][i])
            # Based on the structure of the database, the first data need to be collected
            # with the comments and initials
            if i == 0:
                data[i][4]= getattr(self, f"Premount_Clean_and_Measure_Subwafer_1_Data{i}").text()
                data[i][5] = self.Premount_Clean_and_Measure_Subwafer_1_Comments.toPlainText()
                data[i][6] = self.Premount_Clean_and_Measure_Subwafer_1_Initial.text()
                
            # Rest of the data only need to be collected with the data
            else:
                data[i][4] = getattr(self, f"Premount_Clean_and_Measure_Subwafer_1_Data{i}").text()
                data[i][5] = None
                data[i][6] = None
        myWindow.admin.input_data(data)
        input_check = myWindow.admin.barcode_context(barcode='next')
        if input_check != 'NF':
            self.stackedWidget.setCurrentIndex(5)
        else:
             QMessageBox.about(self, "Error", "Input value is not finished")
    
    # Store all the datas need to be collected in the MSW page            
    def store_data_to_next_page_MSW(self):
        # Function is same as the PCMS page
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
    
    # Store all the datas need to be collected in the DFPR page            
    def store_data_to_next_page_DFPR(self):
        # Function is same as the MPW page
        # The difference is the input data need to be collected twice
        data=[[],[]]    # Create a list with two empty lists
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
                
    # Set up the virtual keyboard event handler for line edit
    def create_line_edit_mouse_event_handler(self, line_edit):
        def line_edit_mouse_event_handler(event):
            nonlocal self, line_edit
            self.virtual_keyboard = self.line_edit_clicked(line_edit, self.virtual_keyboard)
        return line_edit_mouse_event_handler
    
    # Set up the virtual keyboard event handler for text edit
    def create_text_edit_mouse_event_handler(self, text_edit):
        def text_edit_mouse_event_handler(event):
            nonlocal self, text_edit
            self.virtual_keyboard = self.text_edit_clicked(text_edit, self.virtual_keyboard)
        return text_edit_mouse_event_handler

    # Log out the user and return to the login page
    def logout(self):
        self.hide()
        myWindow.showFullScreen()
    
    # Return to the user window    
    def returnToUserWindow(self):
        self.hide()
        self.stackedWidget.setCurrentWidget(self.HomePage)
        userWindow.showFullScreen()   
    
    # Catch the key press event for closeing the window   
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()


class InactivityTimeout:
    """
    There are two ways to reset the timer:
    1. Function to detect any mouse or keyboard activity
        When there is no activity for a certain amount of time,
        the timeout callback function will be called
    2. The timer will be reset when there is any mouse or keyboard activity
    """
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
    """
    Function used to handle the mouse event
    Based on our hardware setup, the mouse event is the only way
    to detect the user activity
    """
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
    """
    The class used to connect to the database
    There are two ways to connect to the database:
    1. Remote connection - connect to the database on a remote server
        this is for client's requirement
    2. Local connection - connect to the database on your local machine
        this is for testing purpose
    Address of host, username, password, and database name need to be changed
    """
    def __init__(self):
        self.mydb = mysql.connector.connect(
            # Remote Connection Configure
            # host="134.190.203.146",
            # user="dslink",
            # password="dstestpass123",
            
            # Local Connection Configure
            host="localhost",
            user="root",
            password="369300Ab*",
            
            database="DaxsonicsBuildTrackDB"
        )
        # Check if the connection is successful
        if not self.mydb.is_connected():
            print("Failed to connect to database.")
            sys.exit(-1)
            
    
class TableModel(QtCore.QAbstractTableModel):
    """
    The class used to create a table model for the QTableView
    it will generate the length of the row and column based on the data structure
    setData function is used to set the data through the cell
    :param data: list of lists containing the data
    """
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
        # In this function, we will update the data in both table
        # employee table and product table
        # For current work, employee table can be edited
        # Product table is still under development
        if  role == Qt.EditRole:
            row = index.row()
            column = index.column()
            data_row = list(self._data[row])
            data_row[column] = value
            self._data[row] = tuple(data_row)
            self.dataChanged.emit(index, index)
            if admin_window.into_workflow == False:
                # Update the employee table
                result = myWindow.admin.query_user(constrain=("id",), constrain_value=(admin_window.id_list[row-1],))
                data_row.insert(0,result[0][0])
                new_result = tuple(data_row)
                myWindow.admin.update_table(new_result, result[0], table_name=config.table_name[config.employee_position])
            else:
                # Update the product table
                admin_window.into_workflow = False
            return True
        return False
    
    def flags(self,index):
        return Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled

# Main function intialize all the windows and dialog
# and start the application
# Represent first window as the login page
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
