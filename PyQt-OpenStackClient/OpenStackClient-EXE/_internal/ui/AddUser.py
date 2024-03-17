# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\AddUser.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AddUser(object):
    def setupUi(self, AddUser):
        AddUser.setObjectName("AddUser")
        AddUser.resize(380, 439)
        AddUser.setMinimumSize(QtCore.QSize(380, 439))
        AddUser.setMaximumSize(QtCore.QSize(380, 439))
        AddUser.setStyleSheet("QDialog {background-color: white;}")
        self.label_adduser_title = QtWidgets.QLabel(AddUser)
        self.label_adduser_title.setGeometry(QtCore.QRect(120, 20, 131, 41))
        self.label_adduser_title.setStyleSheet("QLabel {\n"
"    color: #C32E24;\n"
"    font: 57 9pt \"HarmonyOS Sans SC\";\n"
"    font-size: 25px;\n"
"}")
        self.label_adduser_title.setObjectName("label_adduser_title")
        self.label_add_username = QtWidgets.QLabel(AddUser)
        self.label_add_username.setGeometry(QtCore.QRect(50, 90, 81, 31))
        self.label_add_username.setStyleSheet("QLabel {\n"
"    color: #C32E24;\n"
"    font: 57 9pt \"HarmonyOS Sans SC\";\n"
"    font-size: 20px;\n"
"}")
        self.label_add_username.setObjectName("label_add_username")
        self.lineEdit_add_username = QtWidgets.QLineEdit(AddUser)
        self.lineEdit_add_username.setGeometry(QtCore.QRect(140, 90, 201, 31))
        self.lineEdit_add_username.setStyleSheet("QLineEdit {\n"
"    font: 57 9pt \"HarmonyOS Sans SC\";\n"
"    border: 1px solid #ddd;\n"
"    box-shadow: none;\n"
"    color: #333;\n"
"    font-size: 15px;\n"
"    border-radius: 10px;\n"
"}\n"
"                        ")
        self.lineEdit_add_username.setObjectName("lineEdit_add_username")
        self.label_add_password = QtWidgets.QLabel(AddUser)
        self.label_add_password.setGeometry(QtCore.QRect(50, 140, 81, 31))
        self.label_add_password.setStyleSheet("QLabel {\n"
"    color: #C32E24;\n"
"    font: 57 9pt \"HarmonyOS Sans SC\";\n"
"    font-size: 20px;\n"
"}")
        self.label_add_password.setObjectName("label_add_password")
        self.lineEdit_add_password = QtWidgets.QLineEdit(AddUser)
        self.lineEdit_add_password.setGeometry(QtCore.QRect(140, 140, 201, 31))
        self.lineEdit_add_password.setStyleSheet("QLineEdit {\n"
"    font: 57 9pt \"HarmonyOS Sans SC\";\n"
"    border: 1px solid #ddd;\n"
"    box-shadow: none;\n"
"    color: #333;\n"
"    font-size: 15px;\n"
"    border-radius: 10px;\n"
"}\n"
"                        ")
        self.lineEdit_add_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_add_password.setObjectName("lineEdit_add_password")
        self.label_add_desc = QtWidgets.QLabel(AddUser)
        self.label_add_desc.setGeometry(QtCore.QRect(50, 290, 81, 31))
        self.label_add_desc.setStyleSheet("QLabel {\n"
"    color: #C32E24;\n"
"    font: 57 9pt \"HarmonyOS Sans SC\";\n"
"    font-size: 20px;\n"
"}")
        self.label_add_desc.setObjectName("label_add_desc")
        self.lineEdit_add_desc = QtWidgets.QLineEdit(AddUser)
        self.lineEdit_add_desc.setGeometry(QtCore.QRect(140, 290, 201, 31))
        self.lineEdit_add_desc.setStyleSheet("QLineEdit {\n"
"    font: 57 9pt \"HarmonyOS Sans SC\";\n"
"    border: 1px solid #ddd;\n"
"    box-shadow: none;\n"
"    color: #333;\n"
"    font-size: 15px;\n"
"    border-radius: 10px;\n"
"}\n"
"                        ")
        self.lineEdit_add_desc.setObjectName("lineEdit_add_desc")
        self.label_add_domain = QtWidgets.QLabel(AddUser)
        self.label_add_domain.setGeometry(QtCore.QRect(50, 190, 81, 31))
        self.label_add_domain.setStyleSheet("QLabel {\n"
"    color: #C32E24;\n"
"    font: 57 9pt \"HarmonyOS Sans SC\";\n"
"    font-size: 20px;\n"
"}")
        self.label_add_domain.setObjectName("label_add_domain")
        self.label_add_project = QtWidgets.QLabel(AddUser)
        self.label_add_project.setGeometry(QtCore.QRect(50, 240, 81, 31))
        self.label_add_project.setStyleSheet("QLabel {\n"
"    color: #C32E24;\n"
"    font: 57 9pt \"HarmonyOS Sans SC\";\n"
"    font-size: 20px;\n"
"}")
        self.label_add_project.setObjectName("label_add_project")
        self.comboBox_add_domain = QtWidgets.QComboBox(AddUser)
        self.comboBox_add_domain.setGeometry(QtCore.QRect(140, 190, 201, 31))
        self.comboBox_add_domain.setStyleSheet("QComboBox {\n"
"font: 57 9pt \"HarmonyOS Sans SC\";\n"
"    border: 1px solid #ddd;\n"
"    box-shadow: none;\n"
"    color: #333;    \n"
"    font-size: 15px;\n"
"    border-radius: 10px;\n"
"    background-color: white;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(\'resources/img/down-arrow.png\'); \n"
"    width: 15px;\n"
"    height: 15px\n"
"}\n"
"\n"
"QComboBox::drop-down{\n"
"    border:0;           \n"
"    min-width: 40px; \n"
"}\n"
"                        ")
        self.comboBox_add_domain.setObjectName("comboBox_add_domain")
        self.comboBox_add_project = QtWidgets.QComboBox(AddUser)
        self.comboBox_add_project.setGeometry(QtCore.QRect(140, 240, 201, 31))
        self.comboBox_add_project.setStyleSheet("QComboBox {\n"
"font: 57 9pt \"HarmonyOS Sans SC\";\n"
"    border: 1px solid #ddd;\n"
"    box-shadow: none;\n"
"    color: #333;    \n"
"    font-size: 15px;\n"
"    border-radius: 10px;\n"
"    background-color: white;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(\'resources/img/down-arrow.png\'); \n"
"    width: 15px;\n"
"    height: 15px\n"
"}\n"
"\n"
"QComboBox::drop-down{\n"
"    border:0;           \n"
"    min-width: 40px; \n"
"}\n"
"                        ")
        self.comboBox_add_project.setObjectName("comboBox_add_project")
        self.pushButton_add_adduer = QtWidgets.QPushButton(AddUser)
        self.pushButton_add_adduer.setGeometry(QtCore.QRect(50, 360, 121, 41))
        self.pushButton_add_adduer.setStyleSheet("QPushButton{\n"
"    font: 57 9pt \"HarmonyOS Sans SC\";\n"
"    background-color: #C32E24;\n"
"    color: white;\n"
"    border: none;\n"
"    border-radius: 10px;\n"
"\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: white;\n"
"    color: #C32E24;\n"
"}")
        self.pushButton_add_adduer.setObjectName("pushButton_add_adduer")
        self.pushButton_add_cancel = QtWidgets.QPushButton(AddUser)
        self.pushButton_add_cancel.setGeometry(QtCore.QRect(220, 360, 121, 41))
        self.pushButton_add_cancel.setStyleSheet("QPushButton{\n"
"    font: 57 9pt \"HarmonyOS Sans SC\";\n"
"    background-color: #C32E24;\n"
"    color: white;\n"
"    border: none;\n"
"    border-radius: 10px;\n"
"\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: white;\n"
"    color: #C32E24;\n"
"}")
        self.pushButton_add_cancel.setObjectName("pushButton_add_cancel")

        self.retranslateUi(AddUser)
        QtCore.QMetaObject.connectSlotsByName(AddUser)

    def retranslateUi(self, AddUser):
        _translate = QtCore.QCoreApplication.translate
        AddUser.setWindowTitle(_translate("AddUser", "Dialog"))
        self.label_adduser_title.setText(_translate("AddUser", "<html><head/><body><p align=\"center\">添加用户</p></body></html>"))
        self.label_add_username.setText(_translate("AddUser", "用户名:"))
        self.label_add_password.setText(_translate("AddUser", "密码:"))
        self.label_add_desc.setText(_translate("AddUser", "描述:"))
        self.label_add_domain.setText(_translate("AddUser", "域名:"))
        self.label_add_project.setText(_translate("AddUser", "项目:"))
        self.pushButton_add_adduer.setText(_translate("AddUser", "添加"))
        self.pushButton_add_cancel.setText(_translate("AddUser", "取消"))