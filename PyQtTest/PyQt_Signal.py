# %% 시그널 생성하기 기초(1)

import sys
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QMainWindow

class Worker(QObject):          # Worker 클래스 선언
    closeApp = pyqtSignal()     # pyqtSignal 로 closeApp이라는 Signal 을 만듬

class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.worker = Worker()      # Worker 클래스 객체 생성
        self.worker.closeApp.connect(self.print_out)
        self.worker.closeApp.connect(self.close) # Worker 안에 closeApp Signal 을 self.close 슬롯과 연결

        self.setWindowTitle('Emitting Signal')
        self.setGeometry(300, 300, 300, 200)
        self.show()
        
    def print_out(self):
        print('Mouse clicked')
        
    def mousePressEvent(self, e):       # 마우스를 누르면 
        self.worker.closeApp.emit()     # Worker 클래스의 closeApp Signal 이 방출되어 close() 슬롯 작동

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    
# %% 시그널 생성하기 기초(2)

import sys 
from PyQt5.QtCore import pyqtSlot, QObject, pyqtSignal, Qt
from PyQt5.QtWidgets import * 

class CustomSignal(QObject):
    signal = pyqtSignal(int, str)  # 반드시 클래스 변수로 선언할 것

    def run(self):
        tempstr = "emit으로 전달"
        for i in range(1, 11):
            self.signal.emit(i, tempstr)
            #customFunc 메서드 실행시 signal의 emit 메서드사용

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        customsignal = CustomSignal()  # Mysignal 클래스의 객체 선언
        customsignal.signal.connect(self.funcEmit)  # 객체에 대한시그널 및 슬롯 설정
        customsignal.run()  # 객체의 customFunc 메서드 실행
        #customFunc에서 emit 메서드 실행시 GUI에서 받음.

    @pyqtSlot(int, str)
    def funcEmit(self, i, tempstr):
        self.i = i
        # emit을 통해 받은 값을 GUI 객체 변수에
        self.tempstr = tempstr
        print(str(self.i)+"번째 출력 : ", self.tempstr)

if __name__ == "__main__":
    app=QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()
    
# %% 클릭 시그널이 없는 위젯에 클릭 시그널 넣기 - "Making non-clickable widgets clickable"
# 유용한 사이트 : https://martinii.fun/
# 회사원 코딩 : 파이썬으로 직접 구현하면서 배우는 회사업무 자동화 블로그

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow
from PyQt5.QtGui import QIcon, QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        #super().__init__()
        super(MainWindow, self).__init__()
        self.widget = QLabel(self)
        self.pixmap1 = QPixmap("C:/Users/Administrator/Pictures/img1.png")
        self.pixmap2 = QPixmap("C:/Users/Administrator/Pictures/img2.png")
        self.widget.setPixmap(self.pixmap1)
        self.widget.setScaledContents(True)
        self.setCentralWidget(self.widget)
        self.origin_photo = False  # 추가
        self.widget.mousePressEvent = self.photo_toggle  # 추가
        self.show()
        
    def photo_toggle(self, event):  # 추가
        if self.origin_photo:
            self.widget.setPixmap(self.pixmap1)
            self.origin_photo = False
        else:
            self.widget.setPixmap(self.pixmap2)
            self.origin_photo = True

if __name__ == '__main__':
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()  

    window = MainWindow()
    sys.exit(app.exec())

# %%
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, \
    QVBoxLayout, QPushButton
from PySide6.QtGui import QIcon, QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.widget = QLabel(self)
        self.pixmap1 = QPixmap("C:/Users/Administrator/Pictures/img1.png")
        self.pixmap2 = QPixmap("C:/Users/Administrator/Pictures/img2.png")

        self.widget.setPixmap(self.pixmap1)
        self.widget.setScaledContents(True)
        self.button = QPushButton(text="클릭")

        layout = QVBoxLayout()
        layout.addWidget(self.widget)
        layout.addWidget(self.button)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.origin_photo = False
        self.button.clicked.connect(self.button_clicked)  # 여기만 참고
        # self.show()
        
    def button_clicked(self):
        if self.origin_photo:
            self.widget.setPixmap(self.pixmap1)
            self.origin_photo = False
        else:
            self.widget.setPixmap(self.pixmap2)
            self.origin_photo = True

if __name__ == '__main__':
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance() 
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

# %%
import sys
# from PyQt5.QtCore import pyqtSignal, QObject, QEvent
# from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
# from PyQt5.QtGui import QIcon, QPixmap

from PySide6.QtCore import Signal, QObject, QEvent
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow
from PySide6.QtGui import QIcon, QPixmap

def click(widget):  # QLabel은 클릭 시그널이 없으므로 'click' 시그널 생성
    class Filter(QObject):
        # clickLabel = pyqtSignal()
        clickLabel = Signal()

        def eventFilter(self, object, event):
            if object == widget and event.type() == QEvent.MouseButtonPress:
                self.clickLabel.emit()
                return True
            return False

    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clickLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.widget = QLabel(self)
        self.pixmap1 = QPixmap("C:/Users/Administrator/Pictures/img1.png")
        self.pixmap2 = QPixmap("C:/Users/Administrator/Pictures/img2.png")
        self.widget.setPixmap(self.pixmap1)
        self.widget.setScaledContents(True)
        self.setCentralWidget(self.widget)
        click(self.widget).connect(self.photo_toggle)  # click함수 사용법. 시그널과 비슷.
        self.origin_photo = False
        # self.show()
        
    def photo_toggle(self):
        if self.origin_photo:
            self.widget.setPixmap(self.pixmap1)
            self.origin_photo = False
        else:
            self.widget.setPixmap(self.pixmap2)
            self.origin_photo = True

if __name__ == '__main__':
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance() 
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

    