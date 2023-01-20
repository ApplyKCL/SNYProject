# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Admin_Window.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Admin_WIndow(object):
    def setupUi(self, Admin_WIndow):
        Admin_WIndow.setObjectName("Admin_WIndow")
        Admin_WIndow.resize(1562, 1008)
        Admin_WIndow.setMinimumSize(QtCore.QSize(980, 0))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        Admin_WIndow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/icon/首页.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Admin_WIndow.setWindowIcon(icon)
        Admin_WIndow.setStyleSheet("QPushButton#close_pushButton{\n"
" background-color: #ce5137;\n"
" border-radius:10px;\n"
"}\n"
"\n"
"QPushButton#close_pushButton:hover{\n"
" background-size: cover;\n"
" background-image: url(:/icon/icon/close.svg);\n"
"}\n"
"\n"
"QPushButton#min_pushButton{\n"
" background-color: #a1c661;\n"
" border-radius:10px;\n"
"}\n"
"\n"
"QPushButton#min_pushButton:hover{\n"
" background-size: cover;\n"
" background-image: url(:/icon/icon/minimize.svg);\n"
"}\n"
"\n"
"QWidget#widget{\n"
"background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0.0284091 rgba(129, 255, 251, 255), stop:0.9375 rgba(255, 255, 255, 255));\n"
"\n"
"border-radius: 14;\n"
"}\n"
"\n"
"QTableWidget, QTableView\n"
"{\n"
"    gridline-color: #999999;    /*表格中的网格线条颜色*/\n"
"    background: #FDFDFD;\n"
"    /*设置交替颜色，需要在函数属性中设置:tableWidget->setAlternatingRowColors(true)*/\n"
"    alternate-background-color: #EEEEEF;\n"
"    /*selection-color:#FDFDFD;    鼠标选中时前景色：文字颜色*/\n"
"    selection-background-color:#8BF;   /*鼠标选中时背景色*/\n"
"    border:1px solid #999999;  /*边框线的宽度、颜色*/\n"
"    /*border:none;    去除边界线*/\n"
"    /*border-radius:5px;*/\n"
"    /*padding:10px 10px;*/  /*表格与边框的间距*/\n"
"}\n"
"QTableView::item, QTabWidget::item{\n"
"    background: transparent;\n"
"    outline-style: none;\n"
"    border: none;\n"
"}\n"
"\n"
"QTableView::item:hover {\n"
"    background: #8BF;\n"
"    border: 1px solid #EA2;\n"
"}\n"
"\n"
"QTableView::item:selected {\n"
"    background: #8BF;\n"
"    color: #EEEEEF;\n"
"}\n"
"\n"
"QTableView::item:selected:active {\n"
"    background: #59F;\n"
"    color: #EEEEEF;\n"
"}\n"
"\n"
"QTableWidget QComboBox{\n"
"    margin: 2px;\n"
"    border: none;\n"
"}\n"
"\n"
"\n"
"QGroupBox {\n"
"border: 2px solid #999999;\n"
"border-radius: 4px;\n"
"margin-top: 0.5em;\n"
"}\n"
"QGroupBox::title {\n"
"subcontrol-origin: margin;\n"
"subcontrol-position: top left;\n"
"left: 1em;\n"
"top: 0.1em;\n"
"}\n"
"")
        self.horizontalLayout = QtWidgets.QHBoxLayout(Admin_WIndow)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(Admin_WIndow)
        self.widget.setMinimumSize(QtCore.QSize(950, 550))
        self.widget.setObjectName("widget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.groupBox_4 = QtWidgets.QGroupBox(self.widget)
        self.groupBox_4.setMinimumSize(QtCore.QSize(240, 110))
        self.groupBox_4.setMaximumSize(QtCore.QSize(240, 16777215))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setStyleSheet("QGroupBox {\n"
"                background-color:rgb(rgb(98, 93, 255));\n"
"\n"
"}")
        self.groupBox_4.setObjectName("groupBox_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.admin_login_of_user_name_lineEdit = QtWidgets.QLineEdit(self.groupBox_4)
        self.admin_login_of_user_name_lineEdit.setMinimumSize(QtCore.QSize(90, 30))
        self.admin_login_of_user_name_lineEdit.setMaximumSize(QtCore.QSize(90, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.admin_login_of_user_name_lineEdit.setFont(font)
        self.admin_login_of_user_name_lineEdit.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(46,82,101,200);\n"
"color:rgba(0,0,0,240);\n"
"padding-bottom:2px;")
        self.admin_login_of_user_name_lineEdit.setObjectName("admin_login_of_user_name_lineEdit")
        self.verticalLayout_3.addWidget(self.admin_login_of_user_name_lineEdit)
        self.admin_login_of_password_lineEdit = QtWidgets.QLineEdit(self.groupBox_4)
        self.admin_login_of_password_lineEdit.setMinimumSize(QtCore.QSize(90, 30))
        self.admin_login_of_password_lineEdit.setMaximumSize(QtCore.QSize(90, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.admin_login_of_password_lineEdit.setFont(font)
        self.admin_login_of_password_lineEdit.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(rgb(146, 73, 255));\n"
"color:rgba(0,0,0,240);\n"
"padding-bottom:2px;")
        self.admin_login_of_password_lineEdit.setObjectName("admin_login_of_password_lineEdit")
        self.verticalLayout_3.addWidget(self.admin_login_of_password_lineEdit)
        self.horizontalLayout_4.addLayout(self.verticalLayout_3)
        self.admin_login_pushButton = QtWidgets.QPushButton(self.groupBox_4)
        self.admin_login_pushButton.setMinimumSize(QtCore.QSize(90, 30))
        self.admin_login_pushButton.setMaximumSize(QtCore.QSize(90, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.admin_login_pushButton.setFont(font)
        self.admin_login_pushButton.setObjectName("admin_login_pushButton")
        self.horizontalLayout_4.addWidget(self.admin_login_pushButton)
        self.horizontalLayout_6.addWidget(self.groupBox_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(10)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setEnabled(True)
        self.label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_5.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.fresh_pushButton = QtWidgets.QPushButton(self.widget)
        self.fresh_pushButton.setMinimumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.fresh_pushButton.setFont(font)
        self.fresh_pushButton.setObjectName("fresh_pushButton")
        self.horizontalLayout_5.addWidget(self.fresh_pushButton)
        spacerItem1 = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.min_pushButton = QtWidgets.QPushButton(self.widget)
        self.min_pushButton.setEnabled(True)
        self.min_pushButton.setMinimumSize(QtCore.QSize(20, 20))
        self.min_pushButton.setMaximumSize(QtCore.QSize(20, 20))
        self.min_pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.min_pushButton.setText("")
        self.min_pushButton.setObjectName("min_pushButton")
        self.horizontalLayout_5.addWidget(self.min_pushButton)
        self.close_pushButton = QtWidgets.QPushButton(self.widget)
        self.close_pushButton.setMinimumSize(QtCore.QSize(20, 20))
        self.close_pushButton.setMaximumSize(QtCore.QSize(20, 20))
        self.close_pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.close_pushButton.setText("")
        self.close_pushButton.setObjectName("close_pushButton")
        self.horizontalLayout_5.addWidget(self.close_pushButton)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_5)
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setObjectName("formLayout_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox_2 = QtWidgets.QGroupBox(self.widget)
        self.groupBox_2.setMinimumSize(QtCore.QSize(240, 110))
        self.groupBox_2.setMaximumSize(QtCore.QSize(240, 16777215))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(8)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.add_user_of_user_name_lineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.add_user_of_user_name_lineEdit.setMinimumSize(QtCore.QSize(90, 30))
        self.add_user_of_user_name_lineEdit.setMaximumSize(QtCore.QSize(90, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.add_user_of_user_name_lineEdit.setFont(font)
        self.add_user_of_user_name_lineEdit.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(46,82,101,200);\n"
"color:rgba(0,0,0,240);\n"
"padding-bottom:2px;")
        self.add_user_of_user_name_lineEdit.setObjectName("add_user_of_user_name_lineEdit")
        self.verticalLayout_2.addWidget(self.add_user_of_user_name_lineEdit)
        self.add_user_of_password_lineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.add_user_of_password_lineEdit.setMinimumSize(QtCore.QSize(90, 30))
        self.add_user_of_password_lineEdit.setMaximumSize(QtCore.QSize(90, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.add_user_of_password_lineEdit.setFont(font)
        self.add_user_of_password_lineEdit.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(46,82,101,200);\n"
"color:rgba(0,0,0,240);\n"
"padding-bottom:2px;")
        self.add_user_of_password_lineEdit.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.add_user_of_password_lineEdit.setObjectName("add_user_of_password_lineEdit")
        self.verticalLayout_2.addWidget(self.add_user_of_password_lineEdit)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.add_user_pushButton = QtWidgets.QPushButton(self.groupBox_2)
        self.add_user_pushButton.setMinimumSize(QtCore.QSize(90, 30))
        self.add_user_pushButton.setMaximumSize(QtCore.QSize(90, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.add_user_pushButton.setFont(font)
        self.add_user_pushButton.setObjectName("add_user_pushButton")
        self.horizontalLayout_3.addWidget(self.add_user_pushButton)
        self.verticalLayout_4.addWidget(self.groupBox_2)
        self.groupBox = QtWidgets.QGroupBox(self.widget)
        self.groupBox.setMinimumSize(QtCore.QSize(240, 80))
        self.groupBox.setMaximumSize(QtCore.QSize(240, 16777215))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setContentsMargins(11, -1, 11, 11)
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.delete_user_of_id_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.delete_user_of_id_lineEdit.setMinimumSize(QtCore.QSize(90, 30))
        self.delete_user_of_id_lineEdit.setMaximumSize(QtCore.QSize(90, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.delete_user_of_id_lineEdit.setFont(font)
        self.delete_user_of_id_lineEdit.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(46,82,101,200);\n"
"color:rgba(0,0,0,240);\n"
"padding-bottom:2px;")
        self.delete_user_of_id_lineEdit.setText("")
        self.delete_user_of_id_lineEdit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.delete_user_of_id_lineEdit.setObjectName("delete_user_of_id_lineEdit")
        self.horizontalLayout_2.addWidget(self.delete_user_of_id_lineEdit)
        self.delete_user_pushButton = QtWidgets.QPushButton(self.groupBox)
        self.delete_user_pushButton.setMinimumSize(QtCore.QSize(90, 30))
        self.delete_user_pushButton.setMaximumSize(QtCore.QSize(90, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        self.delete_user_pushButton.setFont(font)
        self.delete_user_pushButton.setObjectName("delete_user_pushButton")
        self.horizontalLayout_2.addWidget(self.delete_user_pushButton)
        self.verticalLayout_4.addWidget(self.groupBox)
        self.groupBox_3 = QtWidgets.QGroupBox(self.widget)
        self.groupBox_3.setMinimumSize(QtCore.QSize(240, 160))
        self.groupBox_3.setMaximumSize(QtCore.QSize(240, 16777215))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setLabelAlignment(QtCore.Qt.AlignCenter)
        self.formLayout_2.setFormAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.formLayout_2.setObjectName("formLayout_2")
        self.change_user_of_id_lineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.change_user_of_id_lineEdit.setMinimumSize(QtCore.QSize(90, 30))
        self.change_user_of_id_lineEdit.setMaximumSize(QtCore.QSize(90, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.change_user_of_id_lineEdit.setFont(font)
        self.change_user_of_id_lineEdit.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(46,82,101,200);\n"
"color:rgba(0,0,0,240);\n"
"padding-bottom:2px;")
        self.change_user_of_id_lineEdit.setCursorPosition(0)
        self.change_user_of_id_lineEdit.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.change_user_of_id_lineEdit.setObjectName("change_user_of_id_lineEdit")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.change_user_of_id_lineEdit)
        self.change_user_pushButton = QtWidgets.QPushButton(self.groupBox_3)
        self.change_user_pushButton.setMinimumSize(QtCore.QSize(100, 30))
        self.change_user_pushButton.setMaximumSize(QtCore.QSize(90, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(9)
        self.change_user_pushButton.setFont(font)
        self.change_user_pushButton.setObjectName("change_user_pushButton")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.change_user_pushButton)
        self.verticalLayout.addLayout(self.formLayout_2)
        self.change_user_of_user_name_lineEdit_2 = QtWidgets.QLineEdit(self.groupBox_3)
        self.change_user_of_user_name_lineEdit_2.setEnabled(False)
        self.change_user_of_user_name_lineEdit_2.setMaximumSize(QtCore.QSize(16777215, 5))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.change_user_of_user_name_lineEdit_2.setFont(font)
        self.change_user_of_user_name_lineEdit_2.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"border:none;\n"
"border-bottom:1px dashed rgba(46,82,101,200);\n"
"color:rgba(0,0,0,240);\n"
"padding-bottom:1px;")
        self.change_user_of_user_name_lineEdit_2.setReadOnly(True)
        self.change_user_of_user_name_lineEdit_2.setPlaceholderText("")
        self.change_user_of_user_name_lineEdit_2.setObjectName("change_user_of_user_name_lineEdit_2")
        self.verticalLayout.addWidget(self.change_user_of_user_name_lineEdit_2)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignCenter)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.formLayout.setObjectName("formLayout")
        self.change_user_of_user_name_lineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.change_user_of_user_name_lineEdit.setMinimumSize(QtCore.QSize(90, 30))
        self.change_user_of_user_name_lineEdit.setMaximumSize(QtCore.QSize(90, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.change_user_of_user_name_lineEdit.setFont(font)
        self.change_user_of_user_name_lineEdit.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(46,82,101,200);\n"
"color:rgba(0,0,0,240);\n"
"padding-bottom:1px;")
        self.change_user_of_user_name_lineEdit.setObjectName("change_user_of_user_name_lineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.change_user_of_user_name_lineEdit)
        self.change_user_of_phone_lineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.change_user_of_phone_lineEdit.setMinimumSize(QtCore.QSize(90, 30))
        self.change_user_of_phone_lineEdit.setMaximumSize(QtCore.QSize(90, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(8)
        self.change_user_of_phone_lineEdit.setFont(font)
        self.change_user_of_phone_lineEdit.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(46,82,101,200);\n"
"color:rgba(0,0,0,240);\n"
"padding-bottom:2px;")
        self.change_user_of_phone_lineEdit.setReadOnly(False)
        self.change_user_of_phone_lineEdit.setObjectName("change_user_of_phone_lineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.change_user_of_phone_lineEdit)
        self.change_user_of_email_lineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.change_user_of_email_lineEdit.setMinimumSize(QtCore.QSize(90, 30))
        self.change_user_of_email_lineEdit.setMaximumSize(QtCore.QSize(90, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.change_user_of_email_lineEdit.setFont(font)
        self.change_user_of_email_lineEdit.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(46,82,101,200);\n"
"color:rgba(0,0,0,240);\n"
"padding-bottom:2px;")
        self.change_user_of_email_lineEdit.setObjectName("change_user_of_email_lineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.change_user_of_email_lineEdit)
        self.change_user_of_password_lineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.change_user_of_password_lineEdit.setMinimumSize(QtCore.QSize(90, 30))
        self.change_user_of_password_lineEdit.setMaximumSize(QtCore.QSize(90, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.change_user_of_password_lineEdit.setFont(font)
        self.change_user_of_password_lineEdit.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(46,82,101,200);\n"
"color:rgba(0,0,0,240);\n"
"padding-bottom:2px;")
        self.change_user_of_password_lineEdit.setObjectName("change_user_of_password_lineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.change_user_of_password_lineEdit)
        self.verticalLayout.addLayout(self.formLayout)
        self.verticalLayout_4.addWidget(self.groupBox_3)
        self.formLayout_3.setLayout(0, QtWidgets.QFormLayout.LabelRole, self.verticalLayout_4)
        self.tableWidget = QtWidgets.QTableWidget(self.widget)
        self.tableWidget.setMinimumSize(QtCore.QSize(600, 400))
        self.tableWidget.setAutoFillBackground(False)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.tableWidget)
        self.verticalLayout_5.addLayout(self.formLayout_3)
        self.horizontalLayout.addWidget(self.widget)

        self.retranslateUi(Admin_WIndow)
        QtCore.QMetaObject.connectSlotsByName(Admin_WIndow)

    def retranslateUi(self, Admin_WIndow):
        _translate = QtCore.QCoreApplication.translate
        Admin_WIndow.setWindowTitle(_translate("Admin_WIndow", "Database System"))
        self.groupBox_4.setTitle(_translate("Admin_WIndow", "Administrator"))
        self.admin_login_of_user_name_lineEdit.setPlaceholderText(_translate("Admin_WIndow", "ID"))
        self.admin_login_of_password_lineEdit.setPlaceholderText(_translate("Admin_WIndow", "Password"))
        self.admin_login_pushButton.setText(_translate("Admin_WIndow", "Log in"))
        self.label.setText(_translate("Admin_WIndow", "Database System"))
        self.fresh_pushButton.setText(_translate("Admin_WIndow", "The Information of Employees"))
        self.groupBox_2.setTitle(_translate("Admin_WIndow", "Add User"))
        self.add_user_of_user_name_lineEdit.setPlaceholderText(_translate("Admin_WIndow", "ID"))
        self.add_user_of_password_lineEdit.setPlaceholderText(_translate("Admin_WIndow", "Password"))
        self.add_user_pushButton.setText(_translate("Admin_WIndow", "Add"))
        self.groupBox.setTitle(_translate("Admin_WIndow", "Delete User"))
        self.delete_user_of_id_lineEdit.setPlaceholderText(_translate("Admin_WIndow", "User ID"))
        self.delete_user_pushButton.setText(_translate("Admin_WIndow", "Delete"))
        self.groupBox_3.setTitle(_translate("Admin_WIndow", "Edit User"))
        self.change_user_of_id_lineEdit.setPlaceholderText(_translate("Admin_WIndow", "User ID"))
        self.change_user_pushButton.setText(_translate("Admin_WIndow", "Comfirm Edit"))
        self.change_user_of_user_name_lineEdit.setPlaceholderText(_translate("Admin_WIndow", "User Name"))
        self.change_user_of_phone_lineEdit.setPlaceholderText(_translate("Admin_WIndow", "Phone Number"))
        self.change_user_of_email_lineEdit.setPlaceholderText(_translate("Admin_WIndow", "Email"))
        self.change_user_of_password_lineEdit.setPlaceholderText(_translate("Admin_WIndow", "Password"))
import app_rc
