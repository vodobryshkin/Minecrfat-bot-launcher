# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'changebot.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ChangeForm(object):
    def setupUi(self, ChangeForm):
        ChangeForm.setObjectName("ChangeForm")
        ChangeForm.resize(390, 165)
        ChangeForm.setMinimumSize(QtCore.QSize(390, 165))
        ChangeForm.setMaximumSize(QtCore.QSize(390, 165))
        font = QtGui.QFont()
        font.setFamily("MS Serif")
        font.setPointSize(11)
        ChangeForm.setFont(font)
        self.formLayoutWidget = QtWidgets.QWidget(ChangeForm)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 20, 371, 100))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.name_lineedit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.name_lineedit.setObjectName("name_lineedit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.name_lineedit)
        self.label_4 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.version_lineedit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.version_lineedit.setObjectName("version_lineedit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.version_lineedit)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.server_lineedit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.server_lineedit.setObjectName("server_lineedit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.server_lineedit)
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.create_bot_button = QtWidgets.QPushButton(ChangeForm)
        self.create_bot_button.setGeometry(QtCore.QRect(262, 130, 121, 31))
        self.create_bot_button.setObjectName("create_bot_button")
        self.error_label = QtWidgets.QLabel(ChangeForm)
        self.error_label.setGeometry(QtCore.QRect(10, 130, 251, 31))
        self.error_label.setText("")
        self.error_label.setObjectName("error_label")

        self.retranslateUi(ChangeForm)
        QtCore.QMetaObject.connectSlotsByName(ChangeForm)

    def retranslateUi(self, ChangeForm):
        _translate = QtCore.QCoreApplication.translate
        ChangeForm.setWindowTitle(_translate("ChangeForm", "Изменение бота"))
        self.label_4.setText(_translate("ChangeForm", "Версия:"))
        self.label_2.setText(_translate("ChangeForm", "Сервер:"))
        self.label.setText(_translate("ChangeForm", "Имя бота:"))
        self.create_bot_button.setText(_translate("ChangeForm", "Подтвердить"))
