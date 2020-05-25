# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Form_user.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Fm_Users(object):
    def setupUi(self, Fm_Users):
        Fm_Users.setObjectName("Fm_Users")
        Fm_Users.resize(335, 254)
        self.Btn_Create = QtWidgets.QPushButton(Fm_Users)
        self.Btn_Create.setGeometry(QtCore.QRect(20, 220, 75, 23))
        self.Btn_Create.setObjectName("Btn_Create")
        self.Btn_Close = QtWidgets.QPushButton(Fm_Users)
        self.Btn_Close.setGeometry(QtCore.QRect(240, 220, 75, 23))
        self.Btn_Close.setObjectName("Btn_Close")
        self.DateCreate = QtWidgets.QDateTimeEdit(Fm_Users)
        self.DateCreate.setGeometry(QtCore.QRect(130, 170, 141, 22))
        self.DateCreate.setCalendarPopup(True)
        self.DateCreate.setObjectName("DateCreate")
        self.Lb_Fecha = QtWidgets.QLabel(Fm_Users)
        self.Lb_Fecha.setGeometry(QtCore.QRect(40, 170, 81, 16))
        self.Lb_Fecha.setObjectName("Lb_Fecha")
        self.listWidget = QtWidgets.QListWidget(Fm_Users)
        self.listWidget.setGeometry(QtCore.QRect(40, 40, 256, 101))
        self.listWidget.setObjectName("listWidget")
        self.Lb_Users = QtWidgets.QLabel(Fm_Users)
        self.Lb_Users.setGeometry(QtCore.QRect(10, 10, 111, 16))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Lb_Users.setFont(font)
        self.Lb_Users.setObjectName("Lb_Users")

        self.retranslateUi(Fm_Users)
        QtCore.QMetaObject.connectSlotsByName(Fm_Users)

    def retranslateUi(self, Fm_Users):
        _translate = QtCore.QCoreApplication.translate
        Fm_Users.setWindowTitle(_translate("Fm_Users", "Creation user"))
        self.Btn_Create.setText(_translate("Fm_Users", "Create"))
        self.Btn_Close.setText(_translate("Fm_Users", "Close"))
        self.DateCreate.setDisplayFormat(_translate("Fm_Users", "MMM/dd/yyyy h:mm AP"))
        self.Lb_Fecha.setText(_translate("Fm_Users", "Fecha actual:"))
        self.Lb_Users.setText(_translate("Fm_Users", "Usuarios creados"))
