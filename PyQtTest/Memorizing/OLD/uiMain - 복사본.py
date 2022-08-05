# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'main.ui'
# Created by: PyQt5 UI code generator 5.9.2

from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
class Ui_MainWindow(object):
    
    def setupUi(self, MainWindow):
        MainWindow.resize(1231, 868)
        self.centralwidget = QWidget(MainWindow)

        self.frame = QFrame(self.centralwidget)
        self.frame.setGeometry(QRect(10, 0, 1211, 121))
        self.frame.setAutoFillBackground(False)
        self.frame.setStyleSheet("border-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,\
                                 stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));\
                                 background-color: rgba(200, 200, 200, 238);")
        self.frame.setFrameShape(QFrame.Box)
        self.frame.setFrameShadow(QFrame.Raised)

        self.pushButton = QPushButton("검색", self.frame)
        self.pushButton.setGeometry(QRect(90, 40, 101, 41))

        self.radioButton = QRadioButton("암기", self.frame)
        self.radioButton.setGeometry(QRect(240, 50, 90, 16))

        self.checkBox = QCheckBox("한국어", self.frame)
        self.checkBox.setGeometry(QRect(380, 50, 81, 16))

        self.comboBox = QComboBox(self.frame)
        self.comboBox.setGeometry(QRect(610, 50, 181, 22))
        self.comboBox.setStyleSheet("background-color: rgb(170, 255, 255);")

        self.lineEdit = QLineEdit("Path", self.frame)
        self.lineEdit.setGeometry(QRect(820, 40, 201, 41))
        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 200);")
        self.lineEdit.setReadOnly(True)

        view = QTableWidget()
        view.setColumnCount(5)
        view.setColumnWidth(0, 50)
        view.setColumnWidth(1, 500)
        view.setColumnWidth(2, 500)
        view.setColumnWidth(3, 50)
        view.setColumnWidth(4, 50)        
        view.setHorizontalHeaderLabels(["seq", "Korean", "English", "Done", "Point"])
        view.horizontalHeader().setFixedHeight(50)
        view.horizontalHeader().setStretchLastSection(True)    # 마지막 칼럼 확장하기        
        view.verticalHeader().setVisible(False)
        view.verticalHeader().setDefaultSectionSize(50)
        view.verticalHeader().setSectionResizeMode(QHeaderView.Interactive ) #(QHeaderView.Fixed)
        
        view.setAlternatingRowColors(True)
        view.setShowGrid(True)  

        # layout = QVBoxLayout()
        # layout.addWidget(view)
        # self.setLayout(layout)
        
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QRect(10, 130, 1211, 691))

        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 1231, 21))

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)

        MainWindow.setStatusBar(self.statusbar)

        # self.retranslateUi(MainWindow)
        # QMetaObject.connectSlotsByName(MainWindow)
  
    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.radioButton.setText(_translate("", "한국어"))
        self.checkBox.setText(_translate("MainWindow", "CheckBox"))

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

