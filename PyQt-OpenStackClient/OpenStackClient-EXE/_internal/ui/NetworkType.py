# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\NetworkType.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NetworkType(object):
    def setupUi(self, NetworkType):
        NetworkType.setObjectName("NetworkType")
        NetworkType.resize(426, 190)
        NetworkType.setStyleSheet("QDialog {background-color: white;}")
        self.label_addnetworktypetitle = QtWidgets.QLabel(NetworkType)
        self.label_addnetworktypetitle.setGeometry(QtCore.QRect(130, 10, 161, 41))
        self.label_addnetworktypetitle.setStyleSheet("QLabel {\n"
"    color: #C32E24;\n"
"    font: 57 9pt \"HarmonyOS Sans SC\";\n"
"    font-size: 25px;\n"
"}")
        self.label_addnetworktypetitle.setObjectName("label_addnetworktypetitle")
        self.label_add_networktype = QtWidgets.QLabel(NetworkType)
        self.label_add_networktype.setGeometry(QtCore.QRect(50, 70, 101, 31))
        self.label_add_networktype.setStyleSheet("QLabel {\n"
"    color: #C32E24;\n"
"    font: 57 9pt \"HarmonyOS Sans SC\";\n"
"    font-size: 20px;\n"
"}")
        self.label_add_networktype.setObjectName("label_add_networktype")
        self.lineEdit_add_networktype = QtWidgets.QLineEdit(NetworkType)
        self.lineEdit_add_networktype.setGeometry(QtCore.QRect(160, 70, 201, 31))
        self.lineEdit_add_networktype.setStyleSheet("QLineEdit {\n"
"    font: 57 9pt \"HarmonyOS Sans SC\";\n"
"    border: 1px solid #ddd;\n"
"    box-shadow: none;\n"
"    color: #333;\n"
"    font-size: 15px;\n"
"    border-radius: 10px;\n"
"}\n"
"                        ")
        self.lineEdit_add_networktype.setObjectName("lineEdit_add_networktype")
        self.pushButton_add_addunetworktype = QtWidgets.QPushButton(NetworkType)
        self.pushButton_add_addunetworktype.setGeometry(QtCore.QRect(150, 120, 121, 41))
        self.pushButton_add_addunetworktype.setStyleSheet("QPushButton{\n"
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
        self.pushButton_add_addunetworktype.setObjectName("pushButton_add_addunetworktype")

        self.retranslateUi(NetworkType)
        QtCore.QMetaObject.connectSlotsByName(NetworkType)

    def retranslateUi(self, NetworkType):
        _translate = QtCore.QCoreApplication.translate
        NetworkType.setWindowTitle(_translate("NetworkType", "Dialog"))
        self.label_addnetworktypetitle.setText(_translate("NetworkType", "<html><head/><body><p align=\"center\"><br/></p></body></html>"))
        self.label_add_networktype.setText(_translate("NetworkType", "物理网络:"))
        self.pushButton_add_addunetworktype.setText(_translate("NetworkType", "选择"))