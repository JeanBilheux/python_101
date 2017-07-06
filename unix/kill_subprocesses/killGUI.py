# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'killGUI.ui'
#
# Created: Tue Oct 25 14:43:21 2016
#      by: PyQt4 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(411, 116)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.runButton = QtGui.QPushButton(self.centralwidget)
        self.runButton.setGeometry(QtCore.QRect(70, 40, 84, 25))
        self.runButton.setObjectName(_fromUtf8("runButton"))
        self.killButton = QtGui.QPushButton(self.centralwidget)
        self.killButton.setGeometry(QtCore.QRect(280, 40, 84, 25))
        self.killButton.setObjectName(_fromUtf8("killButton"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.runButton.setText(_translate("MainWindow", "Run", None))
        self.killButton.setText(_translate("MainWindow", "Kill", None))

