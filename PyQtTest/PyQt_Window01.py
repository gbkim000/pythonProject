#%% Window 활용(1) : geometry /frameGeometry /QIcon

import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        super(MyApp, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('My First Application')
        self.move(100, 300)
        self.resize(400, 200)
        self.setWindowIcon(QIcon('./images/icon23.png'))
        # self.setGeometry(100, 300, 400, 200)
        print(self.size(), self.rect())         # QSize(400, 200)  QRect(0, 0, 400, 200)
        print(self.width(), self.height())              # 400 200        
        print(self.pos().y(),self.pos().x())            # 300 100     
        print(self.geometry().y(),self.geometry().x())  # 300 100
        print(self.geometry().width(),self.geometry().height())             # 400 200
        print(self.frameGeometry().width(),self.frameGeometry().height())   # 400 200 
        self.showMaximized()
        # self.showFullScreen()  # 우측상단 최소/최대창 아이콘 표시 안됨.
        # self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    app.setPalette(app.style().standardPalette())   # default Palette
    sys.exit(app.exec_())

#%% Window 활용(2) : 함수나 클래스 생성없이 직접 실행
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget

if not QApplication.instance():
    app = QApplication(sys.argv)
else:
    app = QApplication.instance()  
    
win = QWidget()
win.setWindowTitle('My First Application')
win.move(100, 300)
win.resize(400, 200)
win.setWindowIcon(QIcon('./images/icon23.png'))
win.setGeometry(100, 300, 400, 200)
win.show()
print(win.width(), win.height())
print(win.size())
print(win.rect())
sys.exit(app.exec_())

#%% Window 활용(3) : 창 크기(QSizePolicy), 창 닫기

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QSizePolicy, QVBoxLayout

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        btn = QPushButton('   Quit   ', self)
        btn.move(50, 50)
        btn.setStyleSheet('color: blue; font-weight: bold; font-size: 30px; background: yellow;')
        btn.clicked.connect(QApplication.instance().quit)
        #btn.clicked.connect(self.close)
                
        # 버튼 박스 사이즈 변경(1) : 박스 레이아웃의 크기에 맞게 확장하기
        # QSizePolicy.Fixed # /Minimum /Maximum /Preferred /Expanding /Ignored
        # btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed) 
        btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding) 
        vbox = QVBoxLayout()
        vbox.addWidget(btn)
        self.setLayout(vbox)
        
        # 버튼 박스 사이즈 변경(2) : 임의로 변경하기
        #btn.resize(150,50)
        # 버튼 박스 사이즈 변경(3) : sizeHint() 메서드로 자동 조절하기        
        btn.resize(btn.sizeHint())
        print('--------------------------------------')
        print(btn.size())
        print(btn.sizeHint())
        print(btn.minimumSizeHint())
        
        self.setWindowTitle('Quit Button')
        # self.resize(500, 200)
        self.setGeometry(300, 300, 500, 200)
        self.printPosition()        
        self.show()
        
        #self.close()
        #self.destroy()
        #sys.exit(0)
        
    def printPosition(self):
        print(self.pos().x(), self.pos().y())                               # 292 269
        print(self.geometry().x(), self.geometry().y())                     # 300 300
        print(self.width(), self.height())                                  # 500 200        
        print(self.geometry().width(), self.geometry().height())            # 500 200
        print(self.frameGeometry().width(), self.frameGeometry().height())  # 516 239
        print(self.size(), self.rect())
        
def main():
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
    
#%% Window 활용(4) : sizeHint(), sezePolicy()

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, \
    QVBoxLayout, QHBoxLayout, QSizePolicy

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Quit Button')
        self.setGeometry(300, 300, 500, 200)        
        btn = QPushButton('   Quit   ', self)
        btn.move(50, 50)
        btn.setStyleSheet('color: blue; font-weight: bold; font-size: 30px; background: yellow;')
        
        # 버튼 박스 사이즈 변경(1) : 박스 레이아웃의 크기에 맞게 확장하기
        # QSizePolicy.Fixed # /Minimum /Maximum /Preferred /Expanding /Ignored
        print(btn.size())
        print(btn.sizeHint())
        
        btn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum) 
        btn.resize(200,100)
        
        print(btn.size())
        print(btn.sizeHint())

        vbox = QHBoxLayout()
        vbox.addWidget(btn)
        self.setLayout(vbox)
        
        # 버튼 박스 사이즈 변경(2) : 임의로 변경하기
        #btn.resize(150,50)

        # 버튼 박스 사이즈 변경(3) : sizeHint() 메서드로 자동 조절하기        
        # btn.resize(btn.sizeHint())
        # print(btn.size())
        
        self.show()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())    

#%% Window 활용(5) : 버튼 박스 크기 조정하기
# (https://blog.naver.com/PostView.nhn?isHttpsRedirect=true&blogId=sagala_soske&logNo=221732045935)

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QSizePolicy
from PyQt5 import QtGui
import sys

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        ok_button = QPushButton("OK in hbox")
        ok_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        can_button = QPushButton("Cancel in h box")
        can_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # QSizePolicy.Fixed # /Minimum /Maximum /Preferred /Expanding /Ignored
        
        hbox = QHBoxLayout()

        vbox1 = QVBoxLayout()
        vbox1.addWidget(ok_button)

        vbox2 = QVBoxLayout()
        vbox2.addWidget(can_button)

        hbox.addLayout(vbox1)
        hbox.addLayout(vbox2)

        self.setLayout(hbox)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    screen = app.primaryScreen()
    size = screen.size()
    # print(size)
    w, h = 500, 500
    ex.setGeometry(int(size.width()/2-w/2),  int(size.height()/2-h/2), w, h)
    ex.setWindowTitle('Test Program')
    sys.exit(app.exec_())

#%% Window 활용(6) : addStretch() 적용하기

import sys
from PyQt5.QtWidgets import QApplication, QWidget ,QMainWindow, QAction, \
     QPushButton, QHBoxLayout, QVBoxLayout

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        ok_button = QPushButton("OK")
        can_button = QPushButton("Cancel")

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(ok_button)
        hbox.addStretch(2)
        hbox.addWidget(can_button)
        hbox.addStretch(1)
        
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addStretch(1)
        vbox.addStretch(0)
        
        self.setLayout(vbox)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    screen = app.primaryScreen()
    size = screen.size()
    w, h = 400, 400
    ex.setGeometry(int(size.width()/2-w/2), int(size.height()/2-h/2), w, h)
    ex.setWindowTitle('Test Program')
    sys.exit(app.exec_())
    
#%% Window 활용(7) : Grid 와 Box 를 합체해서 버튼 배치하기
# https://blog.naver.com/PostView.nhn?isHttpsRedirect=true&blogId=sagala_soske&logNo=221732045935

import sys
from PyQt5.QtWidgets import QGridLayout, QApplication, QWidget, QPushButton, \
     QHBoxLayout, QVBoxLayout, QSizePolicy

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        grid = QGridLayout()
        self.setLayout(grid)

        names = range(1, 11)
        coords = [(i, j) for i in range(5) for j in range(2)]
        for name, coord in zip(names, coords):
            if name=='':
                continue
            button = QPushButton(str(name))
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            grid.addWidget(button, *coord)

        hbox = QHBoxLayout()
        for i in range(4):
            i = QPushButton(str(i))
            i.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            hbox.addWidget(i)
        grid.addLayout(hbox, 0, 2)

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    screen = app.primaryScreen()
    size = screen.size()
    w, h = 500, 500
    ex.setGeometry(int((size.width()-w)/2), int((size.height()-h)/2), w, h)
    ex.setWindowTitle('Test Program')
    sys.exit(app.exec_())

#%% Window 활용(8) : 창을 화면의 가운데로.
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Centering')
        self.resize(500, 350)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()  # 모니터 중심 좌표
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())    
    
#%% Window 활용(9) : Multiple Screen 스위칭하기
# switch screens without opening a new window.

import sys, os
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QLabel, QStackedWidget

class Screen1(QDialog):
    def __init__(self, ret_msg = None):

        #super(Screen1, self).__init__()
        super().__init__()
        print(os.getcwd())
        os.chdir("C:\\Users\\Administrator\\PyQtTest")      # 현재 디렉토리 변경        
        
        loadUi('screen1.ui', self)
        self.button.clicked.connect(self.gotoScreen2)
        self.message="(Here is Screen2) Hello, Did you get my message?"
        lbl_msg = QLabel(self)
        lbl_msg.move(60,230)
        
        if ret_msg == None:
            lbl_msg.setText("")
        else:
            lbl_msg.setText(ret_msg)
        
    def gotoScreen2(self):
        screen2 = Screen2(self.message)
        widget.addWidget(screen2)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
class Screen2(QDialog):
    def __init__(self, message = None):
        #super(Screen2, self).__init__() 
        super().__init__() 
        
        loadUi('Screen2.ui', self)
        self.lbl_message = QLabel(self)
        self.lbl_message.move(60, 230)
        self.lbl_message.setText(message)
        #self.label.setText(message)
        
        self.button.clicked.connect(self.gotoScreen1)
    
    def gotoScreen1(self):
        sendMsg="(Here is Screen1) Yes, I received your message~"
        screen1 = Screen1(sendMsg)
        widget.addWidget(screen1)
        widget.setCurrentIndex(widget.currentIndex()+1)


app = QApplication(sys.argv) # sys.argv : 실행 프로그램의 절대경로롤 넘겨줌

widget = QStackedWidget() 
widget.setFixedWidth(500)
widget.setFixedHeight(300)

screen1 = Screen1()
widget.addWidget(screen1)
# screen2= Screen2()
# widget.addWidget(screen2)

widget.show()

try:
    # sys.exit(app.exec_())
    # PyQt5에서 위 문장은 다음과 같이 사용해도 됨
    sys.exit(app.exec())
    # 방법(1) : app.exec() or app.exec_() // 즉, sys.exit를 생략해도 무관
    # 방법(2) : raise SystemExit(app.exec())
except:
    print('Exit!')

#%% Window 활용(10) : LoginWindow(1) - Ui_Form 상속

import sys
from PyQt5.QtSql import *
from login_box import Ui_Form
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

# 사용자가 만든 Ui_Form을 상속받아서 구현
class LoginWindow(qtw.QWidget, Ui_Form):

    def __init__(self):  
        super().__init__()
        self.setupUi(self)
        self.submit_btn.clicked.connect(self.authenticate)

    def authenticate(self):
        username = self.username_edit.text()
        password = self.password_edit.text()

        if username == 'user' and password == 'pass':
            qtw.QMessageBox.information(self, 'Success','You are logged in')
        else:
            qtw.QMessageBox.critical(self, 'Fail', 'You did not log in')        
        
if __name__ == '__main__':
    app = qtw.QApplication([])
    widget = LoginWindow()
    widget.show()
    sys.exit(app.exec())
    # raise SystemExit(app.exec())
    
#%% Window 활용(11) : LoginWindow(2) - Ui_Form 상속, 인수전달

import sys
from PyQt5.QtSql import *
from login_box import Ui_Form
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

# 사용자가 만든 Ui_Form을 상속받아서 구현
class LoginWindow(qtw.QWidget, Ui_Form):

    def __init__(self, *args, **kwargs):    # 인수(튜플, 딕셔너리) 전달
        print(args, kwargs)        
        super().__init__()
        self.setupUi(self)
        self.submit_btn.clicked.connect(self.authenticate)
        
    def authenticate(self):
        username = self.username_edit.text()
        password = self.password_edit.text()

        if username == 'user' and password == 'pass':
            qtw.QMessageBox.information(self, 'Success','You are logged in')
        else:
            qtw.QMessageBox.critical(self, 'Fail', 'You did not log in')        
        
if __name__ == '__main__':
    app = qtw.QApplication([])
    widget = LoginWindow(10, 'flag', {'key':30})
    widget.show()
    sys.exit(app.exec())
    
#%% Window 활용(12) : LoginWindow(3) - Ui_Form 객체 생성

import sys
from PyQt5.QtSql import *
from login_box import Ui_Form
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

# Ui_Form을 상속받지 않고 초기화 함수에서 Ui_Form 객체를 생성
class LoginWindow(qtw.QWidget):    
         
    def __init__(self):        
        super().__init__()
        self.ui = Ui_Form()     # Ui_Form()는 클래스임
        self.ui.setupUi(self)   # setupUi()는 클래스에 정의된 함수임.
        self.ui.submit_btn.clicked.connect(self.authenticate)
        
    def authenticate(self):
        username = self.ui.username_edit.text()
        password = self.ui.password_edit.text()

        if username == 'user' and password == 'pass':
            qtw.QMessageBox.information(self, 'Success','You are logged in')
        else:
            qtw.QMessageBox.critical(self, 'Fail', 'You did not log in')
        
if __name__ == '__main__':
    app = qtw.QApplication([])
    widget = LoginWindow()
    widget.show()
    sys.exit(app.exec())
    # raise SystemExit(app.exec())

#%% Window 활용(13) : LoginWindow(4) - Ui_Form 객체 생성, 인수 전달

import sys
from PyQt5.QtSql import *
from login_box import Ui_Form
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc

# Ui_Form을 상속받지 않고 초기화 함수에서 Ui_Form 객체를 생성
class LoginWindow(qtw.QWidget):    
         
    def __init__(self, *args, **kwargs):    # 인수(튜플, 딕셔너리) 전달
        print(args, kwargs)
        super().__init__()
        self.ui = Ui_Form()     # Ui_Form()는 클래스임
        self.ui.setupUi(self)   # setupUi()는 클래스에 정의된 함수임.
        self.ui.submit_btn.clicked.connect(self.authenticate)
        
    def authenticate(self):
        username = self.ui.username_edit.text()
        password = self.ui.password_edit.text()

        if username == 'user' and password == 'pass':
            qtw.QMessageBox.information(self, 'Success','You are logged in')
        else:
            qtw.QMessageBox.critical(self, 'Fail', 'You did not log in')
        
if __name__ == '__main__':
    app = qtw.QApplication([])
    widget = LoginWindow(10, 'flag', {'key':30})
    widget.show()
    sys.exit(app.exec())
    # raise SystemExit(app.exec())

#%% Window 활용(14) : Sign In 창 띄우기

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class LogInDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI()

        self.id = None
        self.password = None

    def setupUI(self):
        self.setGeometry(1100, 200, 300, 100)
        self.setWindowTitle("Sign In")
        self.setWindowIcon(QIcon('icon.png'))

        label1 = QLabel("ID: ")         # 이 함수 내부에서만 사용하므로 지역변수 선언
        label2 = QLabel("Password: ")

        self.lineEdit1 = QLineEdit()    # 이 함수 외부에서 접근해야하므로 인스턴스 변수
        self.lineEdit2 = QLineEdit()
        pushButton1= QPushButton("Sign In")
        pushButton1.clicked.connect(self.pushButtonClicked)

        layout = QGridLayout()
        layout.addWidget(label1, 0, 0)
        layout.addWidget(self.lineEdit1, 0, 1)
        layout.addWidget(pushButton1, 0, 2)
        layout.addWidget(label2, 1, 0)
        layout.addWidget(self.lineEdit2, 1, 1)

        self.setLayout(layout)

    def pushButtonClicked(self):
        self.id = self.lineEdit1.text()
        self.password = self.lineEdit2.text()
        self.close()

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(800, 200, 300, 300)
        self.setWindowTitle("PyStock v0.1")
        self.setWindowIcon(QIcon('icon.png'))

        pushButton = QPushButton("Sign In")
        pushButton.clicked.connect(self.pushButtonClicked)
        self.label = QLabel()

        layout = QVBoxLayout()
        layout.addWidget(pushButton)
        layout.addWidget(self.label)

        self.setLayout(layout)

    def pushButtonClicked(self):
        dlg = LogInDialog()
        dlg.exec_()
        id = dlg.id
        password = dlg.password
        self.label.setText("id: %s password: %s" % (id, password))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()

#%% Window 활용(15) : 시그널과 슬롯 구현

import sys, os
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5 import uic

class MyForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi('input.ui', self)
        self.ui.label.setText('input data and click "Save"')
        self.ui.show()
        
    def slot_Save(self):
        msg = self.ui.lineEdit.text()
        with open('saveData.txt', 'at') as f:
            f.write(msg+'\n')
        self.ui.label.setText('Saved input data')
        self.ui.lineEdit.setText('')
        
    def slot_Clear(self):
        self.ui.label.setText('Clear input data')
        self.ui.lineEdit.setText('')
        
    def slot_Exit(self):
        print('Bye Bye ~')
        QApplication.instance().quit()  # 이 문장이 옳은지??
        os._exit(0)                     # 이 문장이 옳은지??
        
def main():
    #os.system('calc.exe')    # os 시스템 명령 실행    
    app = QApplication(sys.argv)
    ex = MyForm()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()  
    
#%% Window 활용(16) : 아이콘 설정하기 / 창 닫기 버튼 만들기(1)

import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import QCoreApplication #QtCore 모듈의 QCoreApplication 클래스를 불러옴

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        btn = QPushButton('Quit', self) 
        # create push button(btn). (btn) is a instance of Class QPushButton.
        # 생성자 (QPushButton())의 첫번째 파라미터에는 버튼에 표시될 텍스트를 입력, 
        # 두번 째 파라미터에는 버튼이 위치 할 부모 위젯을 입력.
        btn.move(200,200)
        btn.resize(btn.sizeHint())
        btn.clicked.connect(QCoreApplication.instance().quit)
        # PyQt5에서의 이벤트 처리는 시그널과 슬롯 메커니즘으로 이루어짐.
        # btn(버튼)을 클릭하면 'clicked' 시그널이 만들어짐
        # instance()메서드는 현재 인스턴스를 반환.
        # clicked 시그널은 어플리케이션을 종료하는 quit() 메서드에 연결
        # 이렇게 sender(버튼(btn)) 와 receiver(어플리케이션 객체(app)) 두 객체 간에 커뮤니케이션이 이루어짐

        self.setWindowTitle('Quit Button')
        self.setWindowIcon(QIcon('web.png'))
        self.setGeometry(300,300,500,400)
        #move()와 resize()를 하나로 합친 것과 같음
        self.show()

def main():
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

#%% Window 활용(17) : 아이콘 설정하기 / 창 닫기 버튼 만들기(2)

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # PushButton 생성 (표시될 텍스트, 버튼이 위치할 부모 위젯)
        btn = QPushButton('Quit', self)
        # clicked 시그널이 만들어질 경우 (버튼이 클릭될 경우)
        # 현재 인스턴스 (instance())를 종료하는 메소드 (quit)에 연결 (connect)
        btn.clicked.connect(QApplication.instance().quit)
        btn.resize(btn.sizeHint())
        btn.move(50, 50)
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Quit Test')        
        self.show()

def main():
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()    
    
#%% Window 활용(18) : 창 닫기 예제(잘 작동됨)

import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        qbtn = QPushButton('Quit', self)
        qbtn.clicked.connect(QApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(50, 50)
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Quit button')
        self.show()

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
        
#%% Window 활용(19) : 창닫기 버튼 클릭시 메시지 박스로 확인하기

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox

class Example(QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):               
        self.setGeometry(300, 300, 250, 150)        
        self.setWindowTitle('Message box')    
        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()        

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

#%% Window 활용(20) : 창 띄우기(함수로 구현)

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

def window():
    app = QApplication(sys.argv)
    win = QWidget()
    #win = QDialog()
    #win = QMainWindow()
    btn = QLabel(win)
    btn.setText("Hello World!")
    win.setGeometry(100,100,200,50)
    btn.move(50,20)
    win.setWindowTitle("PyQt5")
    win.show()
 
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    window()

#%% Window 활용(21) : 창 띄우기(클래스로 구현)

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class window(QWidget):
    #def __init__(self):
    def __init__(self, parent = None):
        super().__init__()
        #super(window, self).__init__()
        #super(window, self).__init__(parent = None)
        self.resize(200,60)
        self.setWindowTitle("PyQt5")
        self.label = QLabel(self)
        self.label.setText("Hello World")
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.move(50,20)
        self.show()
        
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = window()
    # ex.show() 
    sys.exit(app.exec_())
   
#%% Window 활용(22) : QDialog 창 띄우기(함수)

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

def window():
    app = QApplication(sys.argv)
    win = QWidget()
    btn = QPushButton("Hello World!", win)
    #btn = QPushButton(w)
    #btn.setText("Hello World!")
    btn.move(150,50)
    btn.clicked.connect(showdialog)
    win.setWindowTitle("PyQt Dialog demo")
    win.show()
    sys.exit(app.exec_())

def showdialog():
    dlg = QDialog()
    b1 = QPushButton("ok", dlg)
    b1.move(50,50)
    dlg.setWindowTitle("Dialog") # 9. PyQt5 — QDialog Class
    dlg.setWindowModality(Qt.ApplicationModal)
    b1.clicked.connect(dlg.close)
    dlg.exec_()
    
if __name__ == '__main__':
    window()

#%% Window 활용(23) : QDialog 창 띄우기(클래스)

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 윈도우 설정
        self.setGeometry(300, 300, 400, 200)  # x, y, w, h
        self.setWindowTitle('Status Window')

        # QDialog 위젯 생성
        self.dialog = QDialog()

        # QButton 위젯 생성
        self.button = QPushButton('Dialog Button', self)
        self.button.clicked.connect(self.dialog_open)
        self.button.setGeometry(10, 10, 200, 50)

    # 버튼 이벤트 함수
    def dialog_open(self):
        # 버튼 추가
        btnDialog = QPushButton("OK", self.dialog)
        btnDialog.move(100, 50)
        btnDialog.clicked.connect(self.dialog_close)

        # QDialog 세팅
        self.dialog.setWindowTitle('Dialog')
        self.dialog.setWindowModality(Qt.ApplicationModal)
        
        self.dialog.setGeometry(400,400,300,150)
        self.dialog.resize(500, 200)
        self.dialog.show()

    # Dialog 닫기 이벤트
    def dialog_close(self):
        self.dialog.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

#%% Window 활용(24) : MessageBox demo

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# from PyQt5.QtWidgets import QToolTip
# from PyQt5.QtGui import QFont

def window():
    QToolTip.setFont(QFont('맑은 고딕', 8))
    app = QApplication(sys.argv)
    w = QWidget()
    b = QPushButton(w)
    b.setText("Show message!")
    b.setToolTip('이것은 <b>메시지박스 호출</b> 버튼입니다.')
    b.move(100,50)
    b.clicked.connect(showdialog)
    w.setWindowTitle("PyQt MessageBox demo")
    w.show()
    sys.exit(app.exec_())

def showdialog():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("This is a message box")
    msg.setInformativeText("This is additional information")
    msg.setWindowTitle("MessageBox demo")
    msg.setDetailedText("The details are as follows:")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msg.buttonClicked.connect(msgbtn)
    
    retval = msg.exec_()

    # QMessageBox.warning/information/critical
    buttonReply = QMessageBox.question(QMessageBox(), 'APPIA', "Message Box",
        QMessageBox.Yes | QMessageBox.Save | QMessageBox.Cancel | QMessageBox.Reset | \
        QMessageBox.No, QMessageBox.No)
    if buttonReply == QMessageBox.Yes:
        print('Yes clicked.')
    elif buttonReply == QMessageBox.Save:
        print('Save clicked.')
    elif buttonReply == QMessageBox.Cancel:
        print('Cancel clicked.')
    elif buttonReply == QMessageBox.Close:
        print('Close clicked.')
    elif buttonReply == QMessageBox.Reset:
        print('Reset clicked.')
    else:
        print('No clicked.')

def msgbtn(i):
    print ("Button pressed is:",i.text())

if __name__ == '__main__':
    window()
    
#%% Window 활용(25) : 메시지 박스의 리턴값 출력

import sys
from PyQt5.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 윈도우 설정
        self.setGeometry(300, 300, 400, 300)  # x, y, w, h
        self.setWindowTitle('Status Window')

        # QButton 위젯 생성
        self.button = QPushButton('MessageBox Button', self)
        self.button.clicked.connect(self.messagebox_open)
        self.button.setGeometry(10, 10, 200, 50)

        # QDialog 설정
        self.msg = QMessageBox()

    # 버튼 이벤트 함수
    def messagebox_open(self):
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setWindowTitle('MessageBox Test')
        self.msg.setText(' MessageBox Information   ')
        #self.msg.setInformativeText('MessageBox Information')
        self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = self.msg.exec_()

        # 반환값 판단
        print('QMessageBox 리턴값 ', retval)
        if retval == QMessageBox.Ok :
            print('messagebox ok : ', retval)
        elif retval == QMessageBox.Cancel :
            print('messagebox cancel : ', retval)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

#%% Window 활용(26) : ui 파일 불러오기(1)

import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
 
# form_class에 ui 파일을 로드한다.
form_class = uic.loadUiType("C:\\Users\\Administrator\\PyQtTest\\test.ui")[0]
 
# 윈도우 클래스를 정의할 때 인자로 ui 파일인 form_class를 전달한다.
class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.btn_clicked)

    def btn_clicked(self):
        self.label.setText("버튼 클릭")
        print("버튼 클릭")
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()

#%% Window 활용(27) : ui 파일 불러오기(2)

import sys, os, shutil
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QMainWindow
from PyQt5 import uic, QtCore
 
class Form(QMainWindow):
    def __init__(self):
        super().__init__()
        curPath = os.getcwd()
        self.ui = uic.loadUi(curPath + "\\test.ui", self)
        self.ui.show()
        self.pushButton.clicked.connect(self.btn_clicked)

    def btn_clicked(self):
        self.label.setText("버튼 클릭")
        print("버튼 클릭")

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())

# %%
