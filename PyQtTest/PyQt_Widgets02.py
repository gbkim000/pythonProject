#%% 위젯 활용(1) : Layout 중첩하기(1) - 클래스 생성 없이 직접 구현
# addLayout() 메소드의 인자로는, groupbox, 

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGroupBox

app = QApplication([])
app.setStyle('Fusion')
window = QWidget()
window.setGeometry(800, 200, 400, 100)
     
groupBox1 = QGroupBox("Group1")
layout1 = QVBoxLayout()
layout1.addWidget(QPushButton('1'))
layout1.addWidget(QPushButton('2'))
layout1.addWidget(QPushButton('3'))
groupBox1.setLayout(layout1)

groupBox2 = QGroupBox("Group2")
layout2 = QHBoxLayout()
layout2.addWidget(QPushButton('A'))
layout2.addWidget(QPushButton('B'))
layout2.addWidget(QPushButton('C'))
groupBox2.setLayout(layout2)

layout = QHBoxLayout()
layout.addWidget(groupBox1)
layout.addWidget(groupBox2)
# layout.addLayout(layout1)
# layout.addLayout(layout2)

window.setLayout(layout)
window.show()
app.exec_()

#%% 위젯 활용(2) : Layout 중첩하기(2) - 클래스 사용

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGroupBox

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(800, 200, 200, 50)
        
        groupBox1 = QGroupBox("Group1")
        layout1 = QVBoxLayout()
        layout1.addWidget(QPushButton('1'))
        layout1.addWidget(QPushButton('2'))
        layout1.addWidget(QPushButton('3'))
        groupBox1.setLayout(layout1)
        
        groupBox2 = QGroupBox("Group2")
        layout2 = QHBoxLayout()
        layout2.addWidget(QPushButton('A'))
        layout2.addWidget(QPushButton('B'))
        layout2.addWidget(QPushButton('C'))
        groupBox2.setLayout(layout2)
        
        layout = QVBoxLayout()
        layout.addWidget(groupBox1)
        layout.addWidget(groupBox2)
        # layout.addLayout(layout1)
        # layout.addLayout(layout2)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.setPalette(app.style().standardPalette())   # default Palette
    app.exec_() 

#%% 위젯 활용(3) : 위젯 종합
    
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Widgets App")

        layout = QVBoxLayout()
        widgets = [
            QCheckBox,
            QComboBox,
            QDateEdit,
            QDateTimeEdit,
            QDial,
            QDoubleSpinBox,
            QFontComboBox,
            QLCDNumber,
            QLabel,
            QLineEdit,
            QProgressBar,
            QPushButton,
            QRadioButton,
            QSlider,
            QSpinBox,
            QTimeEdit, ]

        for w in widgets:
            layout.addWidget(w())

        widget = QWidget()
        widget.setLayout(layout)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)

app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()

#%% 위젯 활용(4) : %% comboBox / radioButton

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(368, 288)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(90, 80, 51, 31))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(150, 20, 201, 31))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(150, 90, 90, 16))
        self.radioButton.setObjectName("radioButton")
        self.radioButton.setChecked(True)
        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setGeometry(QtCore.QRect(150, 120, 90, 16))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_3 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_3.setGeometry(QtCore.QRect(150, 150, 90, 16))
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton_4 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_4.setGeometry(QtCore.QRect(150, 180, 90, 16))
        self.radioButton_4.setObjectName("radioButton_4")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(280, 210, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.insertButtonClicked)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 368, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Operating System : "))
        self.label_2.setText(_translate("MainWindow", "Phone : "))
        self.comboBox.setItemText(0, _translate("MainWindow", "iOS"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Android"))
        self.radioButton.setText(_translate("MainWindow", "S"))
        self.radioButton_2.setText(_translate("MainWindow", "A"))
        self.radioButton_3.setText(_translate("MainWindow", "W"))
        self.radioButton_4.setText(_translate("MainWindow", "J"))
        self.pushButton.setText(_translate("MainWindow", "Insert"))
        
        # MainWindow.setWindowTitle("MainWindow")
        # self.label.setText("MainWindow")
        # self.label_2.setText("Phone : ")
        # self.comboBox.setItemText(0, "iOS")
        # self.comboBox.setItemText(1, "Android")
        # self.radioButton.setText("S")
        # self.radioButton_2.setText("A")
        # self.radioButton_3.setText("W")
        # self.radioButton_4.setText("J")
        # self.pushButton.setText("Insert")    

    def insertButtonClicked(self):
        os = self.comboBox.currentText()
        phone = ""
        if (self.radioButton.isChecked()):
            phone = "S"
        elif (self.radioButton_2.isChecked()):
            phone = "A"
        elif (self.radioButton_3.isChecked()):
            phone = "W"
        elif (self.radioButton_4.isChecked()):
            phone = "J"
        print(os, phone)

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


#%% 위젯 활용(5) : UI 디자인 - 계산기
    
from PyQt5 import QtCore, QtGui, QtWidgets 

class Ui_Dialog(object): 
  def setupUi(self, Dialog): 
      Dialog.setObjectName("Dialog") 
      Dialog.resize(1074, 661) 

      Dialog.setStyleSheet("background-color: rgb(255, 255, 255);\n") 
      self.num_pushbutton_1 = QtWidgets.QPushButton(Dialog) 
      self.num_pushbutton_1.setGeometry(QtCore.QRect(310, 240, 111, 81)) 
      self.num_pushbutton_1.setStyleSheet("font: 24pt \"고도 B\";\n" 
        "background-color: rgb(255, 170, 255);\n" 
        "color: rgb(255, 255, 255);") 
      self.num_pushbutton_1.setObjectName("num_pushbutton_1") 
      self.num_pushbutton_2 = QtWidgets.QPushButton(Dialog) 
      self.num_pushbutton_2.setGeometry(QtCore.QRect(430, 240, 111, 81)) 
      self.num_pushbutton_2.setStyleSheet("font: 24pt \"고도 B\";\n" 
        "background-color: rgb(255, 140, 234);\n" 
        "color: rgb(255, 255, 255);\n") 
      self.num_pushbutton_2.setObjectName("num_pushbutton_2") 
      self.num_pushbutton_3 = QtWidgets.QPushButton(Dialog) 
      self.num_pushbutton_3.setGeometry(QtCore.QRect(550, 240, 111, 81)) 
      self.num_pushbutton_3.setStyleSheet("font: 24pt \"고도 B\";\n" 
        "background-color: rgb(255, 117, 223);\n" 
        "color: rgb(255, 255, 255);\n") 
      self.num_pushbutton_3.setObjectName("num_pushbutton_3") 
      self.num_pushbutton_4 = QtWidgets.QPushButton(Dialog) 
      self.num_pushbutton_4.setGeometry(QtCore.QRect(310, 330, 111, 81)) 
      self.num_pushbutton_4.setStyleSheet("font: 24pt \"고도 B\";\n" 
        "background-color: rgb(170, 170, 255);\n" 
        "color: rgb(255, 255, 255);") 
      self.num_pushbutton_4.setObjectName("num_pushbutton_4") 
      self.num_pushbutton_6 = QtWidgets.QPushButton(Dialog) 
      self.num_pushbutton_6.setGeometry(QtCore.QRect(550, 330, 111, 81)) 
      self.num_pushbutton_6.setStyleSheet("font: 24pt \"고도 B\";\n" 
        "background-color: rgb(204, 140, 255);\n" 
        "color: rgb(255, 255, 255);") 
      self.num_pushbutton_6.setObjectName("num_pushbutton_6") 
      self.num_pushbutton_5 = QtWidgets.QPushButton(Dialog) 
      self.num_pushbutton_5.setGeometry(QtCore.QRect(430, 330, 111, 81)) 
      self.num_pushbutton_5.setStyleSheet("font: 24pt \"고도 B\";\n" 
        "background-color: rgb(255, 137, 214);\n" 
        "color: rgb(255, 255, 255);\n") 
      self.num_pushbutton_5.setObjectName("num_pushbutton_5") 
      self.num_pushbutton_7 = QtWidgets.QPushButton(Dialog) 
      self.num_pushbutton_7.setGeometry(QtCore.QRect(310, 420, 111, 81)) 
      self.num_pushbutton_7.setStyleSheet("font: 24pt \"고도 B\";\n" 
        "background-color: rgb(214, 89, 255);\n" 
        "color: rgb(255, 255, 255);") 
      self.num_pushbutton_7.setObjectName("num_pushbutton_7") 
      self.num_pushbutton_9 = QtWidgets.QPushButton(Dialog) 
      self.num_pushbutton_9.setGeometry(QtCore.QRect(550, 420, 111, 81)) 
      self.num_pushbutton_9.setStyleSheet("font: 24pt \"고도 B\";\n" 
        "background-color: rgb(241, 83, 255);\n" 
        "color: rgb(255, 255, 255);") 
      self.num_pushbutton_9.setObjectName("num_pushbutton_9") 
      self.num_pushbutton_8 = QtWidgets.QPushButton(Dialog) 
      self.num_pushbutton_8.setGeometry(QtCore.QRect(430, 420, 111, 81)) 
      self.num_pushbutton_8.setStyleSheet("font: 24pt \"고도 B\";\n" 
        "color: rgb(255, 255, 255);\n" 
        "background-color: rgb(205, 21, 221);\n") 
      self.num_pushbutton_8.setObjectName("num_pushbutton_8") 
      self.del_pushbutton = QtWidgets.QPushButton(Dialog) 
      self.del_pushbutton.setGeometry(QtCore.QRect(670, 240, 111, 81)) 
      self.del_pushbutton.setStyleSheet("font: 24pt \"고도 B\";\n" 
        "background-color: rgb(197, 103, 255);\n" 
        "color: rgb(255, 255, 255);") 
      self.del_pushbutton.setObjectName("del_pushbutton") 
      self.num_pushbutton_0 = QtWidgets.QPushButton(Dialog) 
      self.num_pushbutton_0.setGeometry(QtCore.QRect(670, 420, 111, 81)) 
      self.num_pushbutton_0.setStyleSheet("font: 24pt \"고도 B\";\n" 
        "color: rgb(255, 255, 255);\n" 
        "background-color: rgb(255, 123, 249);\n") 
      self.num_pushbutton_0.setObjectName("num_pushbutton_0") 
      self.enter_pushbutton = QtWidgets.QPushButton(Dialog) 
      self.enter_pushbutton.setGeometry(QtCore.QRect(670, 330, 111, 81)) 
      self.enter_pushbutton.setStyleSheet("font: 24pt \"고도 B\";\n" 
        "background-color: rgb(249, 60, 255);\n" 
        "color: rgb(255, 255, 255);") 
      self.enter_pushbutton.setObjectName("enter_pushbutton") 
      self.reset_pushbutton = QtWidgets.QPushButton(Dialog) 
      self.reset_pushbutton.setGeometry(QtCore.QRect(820, 110, 101, 81)) 
      font = QtGui.QFont() 
      font.setFamily("고도B") 
      font.setPointSize(24) 
      font.setBold(False) 
      font.setItalic(False) 
      font.setWeight(9) 
      self.reset_pushbutton.setFont(font) 
      self.reset_pushbutton.setStyleSheet("color: rgb(255, 255, 255);\n" 
        "font: 75 24pt \"고도B\";\n"
        "background-color: rgb(248, 192, 255);") 
      self.reset_pushbutton.setObjectName("reset_pushbutton") 
      self.label = QtWidgets.QLabel(Dialog) 
      self.label.setGeometry(QtCore.QRect(-10, 0, 1081, 71)) 
      self.label.setStyleSheet("background-color: qlineargradient(spread:pad,\
        x1:0, y1:0, x2:1, y2:0, stop:0 rgba(168, 151, 255, 255), stop:1 rgba(255, 126, 200, 255));") 
      self.label.setText("") 
      self.label.setObjectName("label") 
      self.Q_lineEdit = QtWidgets.QLineEdit(Dialog) 
      self.Q_lineEdit.setGeometry(QtCore.QRect(310, 110, 471, 51)) 
      self.Q_lineEdit.setObjectName("Q_lineEdit") 
      self.actionbackspace = QtWidgets.QAction(Dialog) 
      self.actionbackspace.setObjectName("actionbackspace") 
      
      self.Q_lineEdit.raise_() 
      self.retranslateUi(Dialog)

      self.num_pushbutton_1.clicked.connect(lambda: self.Q_lineEdit.insert("1"))
      self.num_pushbutton_2.clicked.connect(lambda: self.Q_lineEdit.insert("2"))
      self.num_pushbutton_3.clicked.connect(lambda: self.Q_lineEdit.insert("3"))
      self.num_pushbutton_4.clicked.connect(lambda: self.Q_lineEdit.insert("4"))
      self.num_pushbutton_5.clicked.connect(lambda: self.Q_lineEdit.insert("5"))
      self.num_pushbutton_6.clicked.connect(lambda: self.Q_lineEdit.insert("6"))
      self.num_pushbutton_7.clicked.connect(lambda: self.Q_lineEdit.insert("7"))
      self.num_pushbutton_8.clicked.connect(lambda: self.Q_lineEdit.insert("8"))
      self.num_pushbutton_9.clicked.connect(lambda: self.Q_lineEdit.insert("9"))
      self.num_pushbutton_0.clicked.connect(lambda: self.Q_lineEdit.insert("0"))

      self.del_pushbutton.clicked.connect(self.Q_lineEdit.backspace)
      self.reset_pushbutton.clicked.connect(self.Q_lineEdit.clear)
      self.enter_pushbutton.clicked.connect(self.enterClicked)

      self.Q_lineEdit.setMaxLength(58)
      
      #self.del_pushbutton.clicked.connect(Dialog.exec) 
      QtCore.QMetaObject.connectSlotsByName(Dialog)

  def enterClicked(self):
      print("Clicked enter!!!", self.Q_lineEdit.text())

  def retranslateUi(self, Dialog): 
      _translate = QtCore.QCoreApplication.translate 
      Dialog.setWindowTitle(_translate("Dialog", "MANLESS DELIVERY")) 
      self.num_pushbutton_1.setText(_translate("Dialog", "1")) 
      self.num_pushbutton_2.setText(_translate("Dialog", "2")) 
      self.num_pushbutton_3.setText(_translate("Dialog", "3")) 
      self.num_pushbutton_4.setText(_translate("Dialog", "4")) 
      self.num_pushbutton_6.setText(_translate("Dialog", "6")) 
      self.num_pushbutton_5.setText(_translate("Dialog", "5")) 
      self.num_pushbutton_7.setText(_translate("Dialog", "7")) 
      self.num_pushbutton_9.setText(_translate("Dialog", "9")) 
      self.num_pushbutton_8.setText(_translate("Dialog", "8")) 
      self.del_pushbutton.setText(_translate("Dialog", "Back")) 
      self.num_pushbutton_0.setText(_translate("Dialog", "0")) 
      self.enter_pushbutton.setText(_translate("Dialog", "Enter")) 
      self.reset_pushbutton.setText(_translate("Dialog", "RESET")) 
      self.actionbackspace.setText(_translate("Dialog", "backspace")) 
      
if __name__ == "__main__": 
  import sys 
  app = QtWidgets.QApplication(sys.argv) 
  Dialog = QtWidgets.QDialog() 
  ui = Ui_Dialog() 
  ui.setupUi(Dialog) 
  Dialog.show() 
  sys.exit(app.exec_()) 
  
#%% 위젯 활용(6) : UI 디자인 - KeyMaker
    
from PyQt5 import QtCore, QtGui, QtWidgets
from random import randint

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(360, 379)
        font=QtGui.QFont()
        font.setFamily("맑은 고딕")
        MainWindow.setFont(font)
        icon=QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/key.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget=QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget=QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 0, 321, 361))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout=QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label=QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.horizontalLayout=QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2=QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.spinBox=QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinBox.setEnabled(True)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(100)
        self.spinBox.setProperty("value", 4)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout.addWidget(self.spinBox)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.verticalLayout=QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton=QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.plainTextEdit=QtWidgets.QPlainTextEdit(self.gridLayoutWidget)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.gridLayout.addLayout(self.verticalLayout, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.ans1="1"
        self.ans2="9"
        self.pushButton.clicked.connect(self.makkey)
        self.spinBox.valueChanged.connect(self.length)

    def retranslateUi(self, MainWindow):
        _translate=QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Keymaker"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:28pt; color:#00aaff;\">Keymaker</span></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">key length:</span></p></body></html>"))
        self.pushButton.setText(_translate("MainWindow", "Get Key"))

    def length(self):
        val = self.spinBox.value()
        for i in range(99):
            if val==i:
                for x in range(i-1):
                    self.ans1+="0"
                for y in range(i-1):
                    self.ans2+="9"

    def makkey(self):
        answer=randint(int(self.ans1),int(self.ans2))
        self.plainTextEdit.setPlainText(str(answer))

if __name__=="__main__":
    import sys
    app=QtWidgets.QApplication(sys.argv)
    MainWindow=QtWidgets.QMainWindow()
    ui=Ui_MainWindow()
    ui.setupUi(MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())
    
# %% font 목록 출력

import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QFont, QFontDatabase

f_db = QFontDatabase()
fonts = f_db.families()
    
for font in fonts:
    print(font)
    
print("total:", len(fonts))

qf_fixed = f_db.systemFont(QFontDatabase.FixedFont)
print( 'Fixed font:',qf_fixed.family() )
qf_general = f_db.systemFont(QFontDatabase.GeneralFont)
print( 'General font:',qf_general.family() )

idx=0
win = QWidget()
btn = QPushButton("abcABC", win)

font = QFont()
font.setFamily(("Times New Roman"))
font.setPointSize(16)
font.setBold(True)
font.setWeight(75)
btn.setFont(font)

def changeFont(coment, x):
    global idx, win, btn
    print(coment, x)
    btn.setFont(QFont(fonts[idx], 15))
    btn.setText("폰트:"+(fonts[idx]))
    idx += 1
    
def main():
    app = QApplication( sys.argv )
    win.resize(500, 300)  
    btn.setFont(QFont(fonts[0], 16))
    btn.resize(300, 60)
    btn.move(100,50)
    x = 10
    btn.clicked.connect(lambda: changeFont('fooData', x))
    win.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
    
#%%
import sys
import PyQt5
from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

css = '''
QDialog{
    background:white;
}

QPushButtonOperation{
    background-color:rgb(80, 188, 223, 0.5);
    color:black;
    border-radius:5px;
}

QPushButtonNumber{
    background-color:rgb(247, 230, 0, 0.5);
    color:black;
    border-radius:5px;
}

QLineEditCustom{
    background-color:white;
    color:black;
}

QLabelCustom{
    color:black;
}

QPushButtonNumber:hover{
    background-color:rgb(247, 230, 0, 1.0);
    color:black;
    border-radius:5px;
}

QPushButtonOperation:hover{
    background-color:rgb(80, 188, 223, 1.0);
    color:black;
    border-radius:5px;
}
'''

class QPushButtonOperation(QPushButton):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        font = QFont("Helvetia", 13)
        font.setBold(True)
        self.setFont(font)

class QPushButtonNumber(QPushButton):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        font = QFont("Helvetia", 13)
        font.setBold(True)
        self.setFont(font)

class QLineEditCustom(QLineEdit):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        font = QFont("Helvetia", 13)
        self.setFont(font)

class QLabelCustom(QLabel):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        font = QFont("Helvetia", 13)
        font.setBold(True)
        self.setFont(font)

class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.set_style()
        self.init_ui()

    def set_style(self):
        # with open("update_style", 'r') as f:
        #     self.setStyleSheet(f.read())
        self.setStyleSheet(css)

    def init_ui(self):
        main_layout = QVBoxLayout()

        layout_operation = QHBoxLayout()
        layout_clear_equal = QHBoxLayout()
        layout_number = QGridLayout()
        layout_equation_solution = QFormLayout()

        label_equation = QLabelCustom("Equation: ")
        label_solution = QLabelCustom("Solution: ")
        self.equation = QLineEditCustom("")
        self.solution = QLineEditCustom("")

        layout_equation_solution.addRow(label_equation, self.equation)
        layout_equation_solution.addRow(label_solution, self.solution)
        group_equation_solution = QGroupBox()
        group_equation_solution.setLayout(layout_equation_solution)

        button_plus = QPushButtonOperation("+")
        button_minus = QPushButtonOperation("-")
        button_product = QPushButtonOperation("x")
        button_division = QPushButtonOperation("/")

        button_plus.clicked.connect(lambda state, operation = "+": self.button_operation_clicked(operation))
        button_minus.clicked.connect(lambda state, operation = "-": self.button_operation_clicked(operation))
        button_product.clicked.connect(lambda state, operation = "*": self.button_operation_clicked(operation))
        button_division.clicked.connect(lambda state, operation = "/": self.button_operation_clicked(operation))

        layout_operation.addWidget(button_plus)
        layout_operation.addWidget(button_minus)
        layout_operation.addWidget(button_product)
        layout_operation.addWidget(button_division)

        button_equal = QPushButtonNumber("=")
        button_clear = QPushButtonNumber("Clear")
        button_backspace = QPushButtonNumber("Backspace")

        button_equal.clicked.connect(self.button_equal_clicked)
        button_clear.clicked.connect(self.button_clear_clicked)
        button_backspace.clicked.connect(self.button_backspace_clicked)

        layout_clear_equal.addWidget(button_clear)
        layout_clear_equal.addWidget(button_backspace)
        layout_clear_equal.addWidget(button_equal)

        number_button_dict = {}
        for number in range(0, 10):
            number_button_dict[number] = QPushButtonNumber(str(number))
            number_button_dict[number].clicked.connect(lambda state, num = number:
                                                       self.number_button_clicked(num))
            if number >0:
                x,y = divmod(number-1, 3)
                layout_number.addWidget(number_button_dict[number], x, y)
            elif number==0:
                layout_number.addWidget(number_button_dict[number], 3, 1)

        button_dot = QPushButtonNumber(".")
        button_dot.clicked.connect(lambda state, num = ".": self.number_button_clicked(num))
        layout_number.addWidget(button_dot, 3, 2)

        button_double_zero = QPushButtonNumber("00")
        button_double_zero.clicked.connect(lambda state, num = "00": self.number_button_clicked(num))
        layout_number.addWidget(button_double_zero, 3, 0)

        main_layout.addWidget(group_equation_solution, stretch=2)
        main_layout.addLayout(layout_operation, stretch=1)
        main_layout.addLayout(layout_clear_equal, stretch=1)
        main_layout.addLayout(layout_number, stretch=3)

        self.setLayout(main_layout)
        self.setWindowTitle("CALCULATOR")
        self.setWindowIcon(QIcon("./icon.png"))
        self.resize(500, 500)
        self.show()

    ### functions ###
    def number_button_clicked(self, num):
        equation = self.equation.text()
        equation += str(num)
        self.equation.setText(equation)

    def button_operation_clicked(self, operation):
        equation = self.equation.text()
        equation += operation
        self.equation.setText(equation)

    def button_equal_clicked(self):
        equation = self.equation.text()
        solution = eval(equation)
        self.solution.setText(str(solution))

    def button_clear_clicked(self):
        self.equation.setText("")
        self.solution.setText("")

    def button_backspace_clicked(self):
        equation = self.equation.text()
        equation = equation[:-1]
        self.equation.setText(equation)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    app.setStyleSheet('')                           # style 미적용
    app.setStyle(QStyleFactory.create('Fusion'))    # Windows/Fusion/...
    app.setPalette(app.style().standardPalette())   # default Palette
    sys.exit(app.exec_())

# %% QLCDNumber, app.primaryScreen(), Size(), QPalette

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLCDNumber, QGridLayout, QWidget, QLabel, qApp

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        grid = QGridLayout()
        self.setLayout(grid)

        # LCD Widgets
        self.lcd1 = QLCDNumber()
        self.lcd2 = QLCDNumber()
        self.lb1  = QLabel("This is Label")

        grid.addWidget(self.lcd1, 0, 0, Qt.AlignTop)
        grid.addWidget(self.lcd2, 0, 1, Qt.AlignTop)
        grid.addWidget(self.lb1,  0, 2, Qt.AlignTop)
        self.setMouseTracking(True)
        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Enter or Qt.Key_E:
            self.lb1.setText(str(self.lcd1.value()) + ' ' + str(self.lcd2.value()))

    def mouseMoveEvent(self, e):
        x = e.x()
        y = e.y()
        self.lcd1.display(x)
        self.lcd2.display(y)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    screen = app.primaryScreen()
    size = screen.size()
    w, h = 300, 300
    ex.setGeometry(int(size.width()/2-w/2), int(size.height()/2-h/2), w, h)
    ex.setWindowTitle('Test Program')
    
    qApp.setStyle("Fusion")
    # dark color 색상 지정
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    
    qApp.setPalette(dark_palette)
    qApp.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")

    sys.exit(app.exec_())
    
    
# %% QLCDNumber, QPalette, QColor

from PyQt5.QtGui import QPalette, QColor

WHITE =     QColor(255, 255, 255)
BLACK =     QColor(0, 0, 0)
RED =       QColor(255, 0, 0)
PRIMARY =   QColor(53, 53, 53)
SECONDARY = QColor(35, 35, 35)
TERTIARY =  QColor(42, 130, 218)

def css_rgb(color, a=False):
    """Get a CSS `rgb` or `rgba` string from a `QtGui.QColor`."""
    return ("rgba({}, {}, {}, {})" if a else "rgb({}, {}, {})").format(*color.getRgb())

class QDarkPalette(QPalette):
    """Dark palette for a Qt application meant to be used with the Fusion theme."""
    def __init__(self, *__args):
        super().__init__(*__args)

        # Set all the colors based on the constants in globals
        self.setColor(QPalette.Window,          PRIMARY)
        self.setColor(QPalette.WindowText,      WHITE)
        self.setColor(QPalette.Base,            SECONDARY)
        self.setColor(QPalette.AlternateBase,   PRIMARY)
        self.setColor(QPalette.ToolTipBase,     WHITE)
        self.setColor(QPalette.ToolTipText,     WHITE)
        self.setColor(QPalette.Text,            WHITE)
        self.setColor(QPalette.Button,          PRIMARY)
        self.setColor(QPalette.ButtonText,      WHITE)
        self.setColor(QPalette.BrightText,      RED)
        self.setColor(QPalette.Link,            TERTIARY)
        self.setColor(QPalette.Highlight,       TERTIARY)
        self.setColor(QPalette.HighlightedText, BLACK)

    @staticmethod
    def set_stylesheet(app):
        """Static method to set the tooltip stylesheet to a `QtWidgets.QApplication`."""
        app.setStyleSheet("QToolTip {{"
                          "color: {white};"
                          "background-color: {tertiary};"
                          "border: 1px solid {white};"
                          "}}".format(white=css_rgb(WHITE), tertiary=css_rgb(TERTIARY)))

    def set_app(self, app):
        """Set the Fusion theme and this palette to a `QtWidgets.QApplication`."""
        app.setStyle("Fusion")
        app.setPalette(self)
        # self.set_stylesheet(app)
        
class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        grid = QGridLayout()
        self.setLayout(grid)

        # LCD Widgets
        self.lcd1 = QLCDNumber()
        self.lcd2 = QLCDNumber()
        self.lb1  = QLabel("This is Label")

        grid.addWidget(self.lcd1, 0, 0, Qt.AlignTop)
        grid.addWidget(self.lcd2, 0, 1, Qt.AlignTop)
        grid.addWidget(self.lb1,  0, 2, Qt.AlignTop)
        self.setMouseTracking(True)
        self.resize(300,300)
        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Enter or Qt.Key_E:
            self.lb1.setText(str(self.lcd1.value()) + ' ' + str(self.lcd2.value()))

    def mouseMoveEvent(self, e):
        x = e.x()
        y = e.y()
        self.lcd1.display(x)
        self.lcd2.display(y) 
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    qdark = QDarkPalette()
    # app.setStyleSheet('')                           # style 미적용
    # app.setStyle(QStyleFactory.create('Fusion'))    # Windows/Fusion/...
    app.setPalette(app.style().standardPalette())   # default Palette    
    qdark.set_app(app)
    # qdark.set_stylesheet(app) # set the tooltip stylesheet to app.

    win = Example()
    sys.exit(app.exec_())
    