#%% Window 활용(1) : QMainWindow - setCentralWidget

import sys
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("My App...")
        
        # button=QPushButton("Press Me!", parent=self)
        button=QPushButton("Press Me!")
        button.move(50, 30)
        self.setCentralWidget(button)
        self.setFixedSize(QSize(300, 200))
        #self.setFixedSize(300, 200)
        
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()


#%% Window 활용(2) : QWidget / QDialog / QMainWindow

import sys 
from PyQt5.QtWidgets import * 

class MyWidget(QWidget): 
    def __init__(self): 
        super().__init__() 
        btn1 = QPushButton('1') 
        btn2 = QPushButton('2') 
        layout = QHBoxLayout() 
        layout.addWidget(btn1) 
        layout.addWidget(btn2) 
        self.setLayout(layout) 
        self.setGeometry(300, 100, 350, 150)  # x, y, width, height 
        self.setWindowTitle("QWidget") 
        self.show() 
  
class MyDialog(QDialog): 
    def __init__(self): 
        super().__init__() 
        btn1 = QPushButton('1') 
        btn2 = QPushButton('2') 
        layout = QHBoxLayout() 
        layout.addWidget(btn1) 
        layout.addWidget(btn2) 
        self.setLayout(layout) 
        self.setGeometry(300, 300, 350, 150) 
        self.setWindowTitle("QDialog") 
        self.show() 
        
class MyMainWindow(QMainWindow): 
    """ 
    옳은 방법... 
    QWidget, QDialog 와 달리 QMainWindow 는 자체적으로 layout 가지고 있다. 
    central widget 을 반드시 필요로함. 
    """ 
    def __init__(self): 
        super().__init__() 
        wg = MyWidget()            # placeholder -- QWidget 상속하여 만든것으로 추후 교체하면 됨. 
        self.setCentralWidget(wg)   # 반드시 필요함. 
        self.setGeometry(300, 500, 350, 150) 
        self.setWindowTitle("QWidget") 
        self.show() 

class MyMainWindow2(QMainWindow): 
    """ 
    틀린방법... 
    ** QWidget, QDialog 처럼 layout 사용 못함. 
    """ 
    def __init__(self): 
        super().__init__() 
        btn1 = QPushButton('1') 
        btn2 = QPushButton('2') 
        layout = QHBoxLayout() 
        layout.addWidget(btn1) 
        layout.addWidget(btn2) 
        self.setLayout(layout) 
        self.setGeometry(300, 700, 350, 150) 
        self.setWindowTitle("QMainWindow 틀린 방법") 
        self.show() 
        
if __name__ == '__main__': 
    app = QApplication(sys.argv)
    
    ex1 = MyWidget() 
    ex2 = MyDialog() 
    ex3 = MyMainWindow() 
    ex4 = MyMainWindow2() 
    
    sys.exit(app.exec_())


#%% Window 활용(3) : QWidget
    
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(431, 241)
        self.addBtn = QtWidgets.QPushButton(Form)
        self.addBtn.setGeometry(QtCore.QRect(350, 10, 75, 23))
        self.addBtn.setObjectName("addBtn")
        self.textBox = QtWidgets.QLineEdit(Form)
        self.textBox.setGeometry(QtCore.QRect(10, 10, 331, 20))
        self.textBox.setObjectName("textBox")
        self.textList = QtWidgets.QListView(Form)
        self.textList.setGeometry(QtCore.QRect(10, 40, 331, 192))
        self.textList.setObjectName("textList")
        self.exitBtn = QtWidgets.QPushButton(Form)
        self.exitBtn.setGeometry(QtCore.QRect(350, 40, 75, 191))
        self.exitBtn.setObjectName("exitBtn")
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "This is Widget"))
        self.addBtn.setText(_translate("Form", "ADD"))
        self.exitBtn.setText(_translate("Form", "EXIT"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
    
#%% Window 활용(4) : QDialog

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(429, 241)
        self.addBtn = QtWidgets.QPushButton(Dialog)
        self.addBtn.setGeometry(QtCore.QRect(350, 10, 75, 23))
        self.addBtn.setObjectName("addBtn")
        self.textBox = QtWidgets.QLineEdit(Dialog)
        self.textBox.setGeometry(QtCore.QRect(10, 10, 331, 20))
        self.textBox.setObjectName("textBox")
        self.testList = QtWidgets.QListView(Dialog)
        self.testList.setGeometry(QtCore.QRect(10, 40, 331, 192))
        self.testList.setObjectName("testList")
        self.exitBtn = QtWidgets.QPushButton(Dialog)
        self.exitBtn.setGeometry(QtCore.QRect(350, 40, 75, 191))
        self.exitBtn.setObjectName("exitBtn")
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.addBtn.setText(_translate("Dialog", "ADD"))
        self.exitBtn.setText(_translate("Dialog", "EXIT"))
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

#%% Window 활용(5) : QMainWindow
    
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(430, 244)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.addBtn = QtWidgets.QPushButton(self.centralwidget)
        self.addBtn.setGeometry(QtCore.QRect(350, 10, 75, 23))
        self.addBtn.setObjectName("addBtn")
        self.textBox = QtWidgets.QLineEdit(self.centralwidget)
        self.textBox.setGeometry(QtCore.QRect(10, 10, 331, 20))
        self.textBox.setObjectName("textBox")
        self.textList = QtWidgets.QListView(self.centralwidget)
        self.textList.setGeometry(QtCore.QRect(10, 40, 331, 192))
        self.textList.setObjectName("textList")
        self.exitBtn = QtWidgets.QPushButton(self.centralwidget)
        self.exitBtn.setGeometry(QtCore.QRect(350, 40, 75, 191))
        self.exitBtn.setObjectName("exitBtn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.addBtn.setText(_translate("MainWindow", "ADD"))
        self.exitBtn.setText(_translate("MainWindow", "EXIT"))
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

#%% Window 활용(6) : 창 띄우기

import sys
import random
from PyQt5 import QtCore, QtWidgets, QtGui

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World", alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

    def magic(self):
        self.text.setText(random.choice(self.hello))
        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
    
#%% Window 활용(7) : 버튼 클릭 이벤트

import sys
from PyQt5.QtWidgets import *

class MyTest(QMainWindow):
    def __init__(self):
        super().__init__()

        btn1 = QPushButton("Button 1", self)
        btn1.move(30, 50)

        btn2 = QPushButton("Button 2", self)
        btn2.move(150, 50)

        btn1.clicked.connect(self.button_clicked)
        btn2.clicked.connect(self.button_clicked)

        self.statusbar = self.statusBar()

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Event sender')
        self.show()

    def button_clicked(self):  # 사용자 정의 slot -- @pyqtSlot() decorator 사용하면 가독성 좋을듯.
        sender = self.sender()
        self.statusbar.showMessage(sender.text() + ' was pressed')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyTest()
    sys.exit(app.exec_())

#%% Window 활용(8) : 화면 중앙에 표시하기

import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QDesktopWidget, \
     QMessageBox, QDialog, QMainWindow

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Hello Bryan')
        self.resize(500, 200)   # 창 크기(default : 640*480)
        self.center()           # 화면 중앙 정렬해주는 함수 호출
        # self.move(100,100)    # 창 위치 이동   
        # self.statusBar().showMessage('이 줄은 상태바~~') # MainWindow를 사용 시
        # 버튼 정의 : 보통 'self.btnRun'과 같이 사용하지만, 지역변수로 'btnRun'과 같이 사용도 가능
        btnRun = QPushButton("Run Button", self)	# 버튼 텍스트
        btnRun.move(20, 20)	# 버튼 위치
        btnRun.clicked.connect(self.btnRun_clicked)	# 클릭 시 실행할 function

    def btnRun_clicked(self):
        QMessageBox.about(self, "message", "Button clicked !")

    # 화면의 가운데로 띄우기
    def center(self):
        qr = self.frameGeometry()   # 변수 qr앞에 self.을 생략하면 함수 내부 지역변수임.
        # QtCore.QRect(0, 0, 500, 200) - 창의 위치와 크기 정보

        cp = QDesktopWidget().availableGeometry().center() 
        # QtCore.QPoint(959, 539) - 사용자 모니터 화면의 중심 위치를 가져옴

        qr.moveCenter(cp) #(QPoint(500,500))
        # 표시할 창(직사각형)의 중심 위치를 화면의 중심 위치로 이동.

        self.move(qr.topLeft())
        # 현재 창을, 화면의 중심에 위치한 직사각형(qr) 위치로 이동.
        # 결과적으로 현재 창의 중심이 화면의 중심과 일치하게 돼서 창이 가운데 위치

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = App()
   ex.show()
   app.exec_()


#%% Window 활용(9) : 버튼 클릭하기

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtGui

class Window(QWidget):
    
    def __init__(self):
        super().__init__()
        self.count = 0
        self.initialize()
 
    def initialize(self):
        self.setGeometry(300, 300, 400, 300)
        layout = QVBoxLayout()      # 변수 layout은 함수 내부에서만 사용하므로 self.가 없어도 됨.
        self.setLayout(layout)
 
        self.label = QLabel("PyQt5 Ex!")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QtGui.QFont('Hack', 15))
        layout.addWidget(self.label)
 
        button = QPushButton("Press Button!")   # 변수 button은 함수 내부에서만 사용하므로 self.가 없어도 됨.
        button.clicked.connect(self.button_clicked)
        button.setFont(QtGui.QFont('Hack', 15))
        layout.addWidget(button)
 
    def button_clicked(self):
        print("Button Clicked", self.count)
        #QMessageBox.about(self, "Alert", "Clicked!")
        self.count += 1
        self.label.setText("Count " + str(self.count))
 
app = QApplication(sys.argv)
screen = Window()
print(screen.label.text())
screen.show()
sys.exit(app.exec_())


#%% Window 활용(10) : 람다식 적용

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMainWindow

class Form(QWidget):
#class Form(QMainWindow):

    def __init__(self):
        
        super().__init__()
        self.setWindowTitle("Appia Qt GUI")
        self.resize(400, 300)
        self.move(50,50)
        self.intialL1 = 'First Label'
        self.intialL2 = 'Second Label'
        
        self.label1 = QLabel(self.intialL1, self)   # label1은 print_label()에서 사용하므로 self.로 선언
        self.label1.move(10,10)
        label2 = QLabel(self.intialL2, self)        # label2는 __init()__에서만 사용하므로 self. 없어도 됨.
        label2.move(10, 50)
        
        self.button1 = QPushButton('Button1', self)
        self.button1.move(50, 110)
        self.button1.clicked.connect(lambda: self.print_label(self.button1, self.label1))
        button2 = QPushButton('Button2', self)
        button2.move(50, 140)
        button2.clicked.connect(lambda: self.print_label(button2, label2))
        self.setWindowTitle("Appia Qt GUI")
        self.show()
        print(label2.text())
        
    def print_label(self, vbutton, vlabel):
        vlabel.setText(vbutton.text())
        print(self.label1.text())
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Form()
    app.exec_()


#%% Window 활용(11) : QHBoxLayout, QVBoxLayout, addStretch

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
 
class QtGUI(QWidget):
 
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Appia Qt GUI")
        self.resize(300, 300)
        self.intialL1 = 'First Label'
        self.intialL2 = 'Two Label'
 
        label1 = QLabel(self.intialL1, self)
        label2 = QLabel(self.intialL2, self)
        
        button1 = QPushButton('Button1', self)
        button1.clicked.connect(lambda: self.print_label(button1,label1))
        button2 = QPushButton('Button2', self)
        button2.clicked.connect(lambda: self.print_label(button2,label2))
        
        qhbox1 = QHBoxLayout()
        qhbox1.addStretch(20)
        qhbox1.addWidget(label1)
        qhbox1.addWidget(button1)
        qhbox1.addStretch(10)
        
        qhbox2 = QHBoxLayout()
        qhbox2.addStretch(1)
        qhbox2.addWidget(label2)
        qhbox2.addWidget(button2)
        qhbox2.addStretch(2)
        
        qvbox = QVBoxLayout()
        qvbox.addStretch(1)
        qvbox.addLayout(qhbox1)
        qvbox.addLayout(qhbox2)
        qvbox.addStretch(2)
        self.setLayout(qvbox)
        self.show()
 
    def print_label(self, vbutton,vlabel):
        vlabel.setText(vbutton.text())
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = QtGUI()
    app.exec_()    


#%% Window 활용(12) : QGridLayout

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGridLayout
 
class QtGUI(QWidget):
 
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Appia Qt GUI")
        self.resize(300, 300)
        self.intialL1 = 'First Label'
        self.intialL2 = 'Two Label'
 
       # 그리드 레이아웃 생성 및 현재 윈도우 창에 적용
        Lgrid = QGridLayout()
        self.setLayout(Lgrid)
        
        label1 = QLabel(self.intialL1, self)
        label2 = QLabel(self.intialL2, self)
        
        button1 = QPushButton('Button1', self)
        button1.clicked.connect(lambda: self.print_label(button1,label1))
        button2 = QPushButton('Button2', self)
        button2.clicked.connect(lambda: self.print_label(button2,label2))
        label3 = QLabel("aa", self)
        label4 = QLabel("bb", self)
        label5 = QLabel("cc", self)
        label6 = QLabel("dd", self)
        label7 = QLabel("ee", self)
        

        label1.setStyleSheet("background-color: yellow")
        label2.setStyleSheet("background-color: red")
        label3.setText("Label 3")
        label4.setText("Label 4")
        
        
        Lgrid.addWidget(label1, 0, 0, alignment=Qt.AlignLeft)
        Lgrid.addWidget(label2, 1, 0, alignment=Qt.AlignRight)
        Lgrid.addWidget(label3, 2, 0)
        Lgrid.addWidget(button1, 0, 1)
        Lgrid.addWidget(button2, 1, 1)
        Lgrid.addWidget(label4, 2, 1)
        Lgrid.addWidget(label5, 0, 2)
        Lgrid.addWidget(label6, 1, 2)
        Lgrid.addWidget(label7, 2, 2)
 
        self.show()
 
    def print_label(self, vbutton,vlabel):
        vlabel.setText(vbutton.text())
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = QtGUI()
    app.exec_()

#%% Window 활용(13) : Grid Layout 적용하기(1)

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui  import QColor, QPalette

from PyQt5.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QGridLayout,
    QWidget
)

class Color(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")

        layout = QGridLayout()

        layout.addWidget(Color("red"), 0, 0)
        layout.addWidget(Color("pink"), 1, 0)
        layout.addWidget(Color("blue"), 1, 1)
        layout.addWidget(Color("skyblue"), 2, 1)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()

#%% Window 활용(14) : Grid Layout 적용하기(2)
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui  import QColor, QPalette

from PyQt5.QtWidgets import (
    QApplication, 
    QMainWindow,
    QHBoxLayout, 
    QVBoxLayout,
    QGridLayout,
    QWidget
)

class Color(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")

        layout1 = QHBoxLayout()
        layout2 = QVBoxLayout()
        layout3 = QVBoxLayout()

        layout2.addWidget(Color("red"))
        layout2.addWidget(Color("yellow"))
        layout2.addWidget(Color("purple"))

        layout1.addLayout(layout2)
        layout1.addWidget(Color("green"))
        
        layout3.addWidget(Color("red"))
        layout3.addWidget(Color("purple"))

        layout1.addLayout(layout3)

        widget = QWidget()
        widget.setLayout(layout1)

        self.setCentralWidget(widget)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()

# %% Windows flags 제어하기

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt
 
class MyApp(QWidget):
 
    def __init__(self):
        super().__init__()
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle('test')
        # flags = Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint
        flags = Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint | Qt.WindowCloseButtonHint
        self.setWindowFlags(flags)             
        self.move(400, 400)
        self.resize(200, 200)
        self.show()
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    app.setStyleSheet('')                           # style 미적용
    app.setStyle(QStyleFactory.create('Fusion'))    # Windows/Fusion/...
    app.setPalette(app.style().standardPalette())   # default Palette
    sys.exit(app.exec_())

