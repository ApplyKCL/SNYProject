# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Normal_user.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_User_WIndow(object):
    def setupUi(self, User_WIndow):
        User_WIndow.setObjectName("User_WIndow")
        User_WIndow.resize(980, 586)
        User_WIndow.setMinimumSize(QtCore.QSize(980, 0))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/icon/首页.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        User_WIndow.setWindowIcon(icon)
        User_WIndow.setStyleSheet("")
        self.horizontalLayout = QtWidgets.QHBoxLayout(User_WIndow)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(User_WIndow)
        self.widget.setMinimumSize(QtCore.QSize(950, 550))
        self.widget.setStyleSheet("QFrame {\n"
"        background-color :rgb(255, 255, 255)\n"
"}")
        self.widget.setObjectName("widget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setText("")
        self.label.setObjectName("label")
        self.horizontalLayout_5.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(88, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.fresh_pushButton = QtWidgets.QPushButton(self.widget)
        self.fresh_pushButton.setMinimumSize(QtCore.QSize(130, 45))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.fresh_pushButton.setFont(font)
        self.fresh_pushButton.setObjectName("fresh_pushButton")
        self.horizontalLayout_5.addWidget(self.fresh_pushButton)
        spacerItem1 = QtWidgets.QSpacerItem(138, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
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
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout.setContentsMargins(13, -1, 13, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.Barcode_Scan_pushButton = QtWidgets.QPushButton(self.groupBox_2)
        self.Barcode_Scan_pushButton.setMinimumSize(QtCore.QSize(90, 30))
        self.Barcode_Scan_pushButton.setMaximumSize(QtCore.QSize(130, 50))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.Barcode_Scan_pushButton.setFont(font)
        self.Barcode_Scan_pushButton.setStyleSheet("")
        self.Barcode_Scan_pushButton.setObjectName("Barcode_Scan_pushButton")
        self.gridLayout.addWidget(self.Barcode_Scan_pushButton, 0, 0, 1, 1)
        self.Countinue_pushButton = QtWidgets.QPushButton(self.groupBox_2)
        self.Countinue_pushButton.setMinimumSize(QtCore.QSize(90, 30))
        self.Countinue_pushButton.setMaximumSize(QtCore.QSize(130, 50))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.Countinue_pushButton.setFont(font)
        self.Countinue_pushButton.setIconSize(QtCore.QSize(28, 24))
        self.Countinue_pushButton.setObjectName("Countinue_pushButton")
        self.gridLayout.addWidget(self.Countinue_pushButton, 1, 0, 1, 1)
        self.LogOut_User_pushButton = QtWidgets.QPushButton(self.groupBox_2)
        self.LogOut_User_pushButton.setMinimumSize(QtCore.QSize(90, 30))
        self.LogOut_User_pushButton.setMaximumSize(QtCore.QSize(130, 50))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.LogOut_User_pushButton.setFont(font)
        self.LogOut_User_pushButton.setObjectName("LogOut_User_pushButton")
        self.gridLayout.addWidget(self.LogOut_User_pushButton, 2, 0, 1, 1)
        self.verticalLayout_4.addWidget(self.groupBox_2)
        self.formLayout_3.setLayout(1, QtWidgets.QFormLayout.LabelRole, self.verticalLayout_4)
        self.tableWidget = QtWidgets.QTableWidget(self.widget)
        self.tableWidget.setMinimumSize(QtCore.QSize(600, 400))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.tableWidget)
        self.verticalLayout_5.addLayout(self.formLayout_3)
        self.horizontalLayout.addWidget(self.widget)

        self.retranslateUi(User_WIndow)
        QtCore.QMetaObject.connectSlotsByName(User_WIndow)

    def retranslateUi(self, User_WIndow):
        _translate = QtCore.QCoreApplication.translate
        User_WIndow.setWindowTitle(_translate("User_WIndow", "Welcome! Normal User"))
        self.fresh_pushButton.setText(_translate("User_WIndow", "Work Selection"))
        self.groupBox_2.setTitle(_translate("User_WIndow", "Current Status"))
        self.Barcode_Scan_pushButton.setText(_translate("User_WIndow", "Barcode Scan"))
        self.Countinue_pushButton.setText(_translate("User_WIndow", "Countinue "))
        self.LogOut_User_pushButton.setText(_translate("User_WIndow", "LogOut"))