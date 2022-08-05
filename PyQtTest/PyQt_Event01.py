# %% keyPressEvent(1)

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Reimplementing event handler')
        self.setGeometry(300, 300, 300, 200)
        label = QLabel(self)
        label.move(30,50)
        label.setText("최대화 : F, 보통창 : N")
        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        elif e.key() == Qt.Key_F:
            self.showFullScreen()
        elif e.key() == Qt.Key_N:
            self.showNormal()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    

# %% keyPressEvent(2) : e.modifiers

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import Qt

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('key')
        self.resize(320, 240)
        self.show()

    def keyPressEvent(self, e):
        def isPrintable(key):
            printable = [
                Qt.Key_Space,
                Qt.Key_Exclam,
                Qt.Key_QuoteDbl,
                Qt.Key_NumberSign,
                Qt.Key_Dollar,
                Qt.Key_Percent,
                Qt.Key_Ampersand,
                Qt.Key_Apostrophe,
                Qt.Key_ParenLeft,
                Qt.Key_ParenRight,
                Qt.Key_Asterisk,
                Qt.Key_Plus,
                Qt.Key_Comma,
                Qt.Key_Minus,
                Qt.Key_Period,
                Qt.Key_Slash,
                Qt.Key_0,
                Qt.Key_1,
                Qt.Key_2,
                Qt.Key_3,
                Qt.Key_4,
                Qt.Key_5,
                Qt.Key_6,
                Qt.Key_7,
                Qt.Key_8,
                Qt.Key_9,
                Qt.Key_Colon,
                Qt.Key_Semicolon,
                Qt.Key_Less,
                Qt.Key_Equal,
                Qt.Key_Greater,
                Qt.Key_Question,
                Qt.Key_At,
                Qt.Key_A,
                Qt.Key_B,
                Qt.Key_C,
                Qt.Key_D,
                Qt.Key_E,
                Qt.Key_F,
                Qt.Key_G,
                Qt.Key_H,
                Qt.Key_I,
                Qt.Key_J,
                Qt.Key_K,
                Qt.Key_L,
                Qt.Key_M,
                Qt.Key_N,
                Qt.Key_O,
                Qt.Key_P,
                Qt.Key_Q,
                Qt.Key_R,
                Qt.Key_S,
                Qt.Key_T,
                Qt.Key_U,
                Qt.Key_V,
                Qt.Key_W,
                Qt.Key_X,
                Qt.Key_Y,
                Qt.Key_Z,
                Qt.Key_BracketLeft,
                Qt.Key_Backslash,
                Qt.Key_BracketRight,
                Qt.Key_AsciiCircum,
                Qt.Key_Underscore,
                Qt.Key_QuoteLeft,
                Qt.Key_BraceLeft,
                Qt.Key_Bar,
                Qt.Key_BraceRight,
                Qt.Key_AsciiTilde,
            ]

            if key in printable:
                return True
            else:
                return False

        control = False

        if e.modifiers() & Qt.ControlModifier:
            print('Control')
            control = True

        if e.modifiers() & Qt.ShiftModifier:
            print('Shift')

        if e.modifiers() & Qt.AltModifier:
            print('Alt')

        if e.key() == Qt.Key_Delete:
            print('Delete')

        elif e.key() == Qt.Key_Backspace:
            print('Backspace')

        elif e.key() in [Qt.Key_Return, Qt.Key_Enter]:
            print('Enter')

        elif e.key() == Qt.Key_Escape:
            print('Escape')

        elif e.key() == Qt.Key_Right:
            print('Right')

        elif e.key() == Qt.Key_Left:
            print('Left')

        elif e.key() == Qt.Key_Up:
            print('Up')

        elif e.key() == Qt.Key_Down:
            print('Down')

        if not control and isPrintable(e.key()):
            print(e.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Main()
    sys.exit(app.exec_())


# %% mouseMoveEvent(1)

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        x = 0
        y = 0

        self.text = 'x: {0}, y: {1}'.format(x, y)
        self.label = QLabel(self.text, self)
        self.label.move(20, 20)
        self.label.setStyleSheet(
           "color: #4D69E8; border-style: solid; border-width: 2px; border-color: #54A0FF; border-radius:5px; ")
       
        # self.setMouseTracking(True)  
        # Default는 False, False인 경우 마우스 버튼을 클릭한 상태에서만 mouseMoveEvent 감지

        self.setWindowTitle('Reimplementing event handler')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def mouseMoveEvent(self, e):        # mouse가 움직일 때 발생하는 Event, 위치 좌표를 e로 받는다.
        x = e.x()                       # 좌표의 x 값을 받는다.
        y = e.y()                       # 좌표의 y 값을 받는다.

        text = 'x: {0}, y: {1}'.format(x, y)
        self.label.setText(text)
        self.label.adjustSize()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())


# %% mouseMoveEvent(2) : Mouse Location Tracking

import sys
from PyQt5.QtWidgets import *

class MouseTracking(QMainWindow):

    def __init__(self):
        super().__init__()
        self.statusbar = self.statusBar()

        # True 일경우에는 Mouse Button 누른 상태가 아니라도 Mouse Tracking 이 활성화됨
        # False 인 경우는 임의적으로 Mouse Button을 눌러야, Mouse Tracking 이 활성화됨.
        self.setMouseTracking(True) 
        self.setGeometry(500, 200, 600, 400)
        self.show()

    def mouseMoveEvent(self, event):
        text = "Tracking For Mouse Location ; x={0}, y={1}, global x, y={2},{3}" \
        .format(event.x(), event.y(), event.globalX(), event.globalY())
        self.statusbar.showMessage(text)

if __name__ == "__main__":
   app = QApplication(sys.argv)
   ex = MouseTracking()
   sys.exit(app.exec_())


# %% mousePress 이벤트(1)

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import pyqtSignal, QObject, Qt

class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.setWindowTitle('Mouse Press Event')
        self.setGeometry(200,300,300,150)
        self.show()

    def mousePressEvent(self, e):   # Mouse를 눌렀을 때 event
        if e.button() == Qt.LeftButton:         # 마우스 왼쪽 클릭하면 Left button press 출력
            print("Left button press")
        elif e.button() == Qt.RightButton:      # 마우스 오른쪽 클릭하면 Right button press 출력
            print("Right button press")
        elif e.button() == Qt.MidButton:        # 마우스 휠 클릭하면 Mid Button Press 출력
            print("Mid Button Press")
        elif e.button() == Qt.MiddleButton:     # 마우스 가운데 버튼 클릭하면 Middle Button Press 출력
            print("Middle Button Press")

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())


# %% mousePress 이벤트(2)

from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget
from PyQt5.QtCore import Qt

class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMouseTracking(True)
        self.setWindowTitle('mouse')
        self.resize(320, 240)
        self.show()

    def mousePressEvent(self, e):  # e ; QMouseEvent
        print('BUTTON PRESS')
        self.mouseButtonKind(e.buttons())

    def mouseReleaseEvent(self, e):  # e ; QMouseEvent
        print('BUTTON RELEASE')
        self.mouseButtonKind(e.buttons())

    def mouseButtonKind(self, buttons):
        if buttons & Qt.LeftButton:
            print('LEFT')
        if buttons & Qt.MidButton:
            print('MIDDLE')
        if buttons & Qt.RightButton:
            print('RIGHT')
            
    def wheelEvent(self, e):  # e ; QWheelEvent
        print('wheel')
        print('(%d %d)' % (e.angleDelta().x(), e.angleDelta().y()))

    def mouseMoveEvent(self, e):  # e ; QMouseEvent
        print('(%d %d)' % (e.x(), e.y()))

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = Main()
    sys.exit(app.exec_())


# %% 마우스 이벤트 (QRubberBand 클래스 사용)
# 사각형 영역으로 드래그했을 때, 시작점(x,y)와 끝점(x,y)를 출력해 줌

import sys
from PyQt5.QtCore import QPoint, QRect, QSize, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, qApp, QWidget, QLabel, QRubberBand
from PyQt5.QtGui import *
 
class Window(QMainWindow):
    def __init__(self, parent = None):
        super().__init__()
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPoint()
        self.setFixedSize(500, 300)
        #print(self)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.origin = QPoint(event.pos())
            self.rubberBand.setGeometry(QRect(self.origin, QSize()))
            self.rubberBand.show()
    
    def mouseMoveEvent(self, event):
        if not self.origin.isNull():
            self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.rubberBand.hide()
            print()
            print('self.origin.x():self.origin.y() - {0}:{1}'.format(self.origin.x(), self.origin.y()))
            print('event.pos().x():event.pos().y() - {0}:{1}'.format(event.pos().x(), event.pos().y()))  
              
            self.origin -= QPoint(20,20)    # 포인트 위치 보정 연산도 가능
            print('self.origin - {0}'.format(self.origin))
            print('self.origin.x():self.origin.y() - {0}:{1}'.format(self.origin.x(), self.origin.y()))
            print('event.pos().x():event.pos().y() - {0}:{1}'.format(event.pos().x(), event.pos().y())) 

app = QApplication(sys.argv)
myWindow = Window(None)
myWindow.show()
app.exec_()

# %% mouseEvent, paintEvent 사용하기
# PaintEvent를 사용하여 실시간으로 값 변경하기
# MouseEvent를 사용하여 마우스 값 가져오기

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QStyleFactory

class Form(QWidget):
    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)
        # 마우스 좌표 저장용 변수
        self.mouse_x = 0
        self.mouse_y = 0
        self.properties_list = (
            "width", "height", "x", "y", "geometry",
            "maximumHeight", "maximumWidth", "maximumSize", "minimumSize", "minimumWidth",
            "size", "windowFilePath", "windowTitle",
            "underMouse" )  # 출력할 property 이름
        self.init_widget()

    def init_widget(self):
        self.setWindowTitle("Hello World")
        self.setGeometry(100, 100, 640, 480)    # 창 위치, 크기 설정
        self.setMouseTracking(True)             # 마우스 움직임을 캐치

        # QLabel(str, parent) or QLabel(parent) 등으로 표현 가능
        self.lb = QLabel(self)
        self.lb.setStyleSheet("background-color: yellow")  # 라벨위젯과의 구분을 위한 색
        self.lb.setMouseTracking(True)  # False 값일 경우 Label 위젯에서는 mouse 이벤트가 발생하지 않는다.
        msg = self.get_properties_value(self.properties_list)  # property 이름과 값을 돌려주는 함수 호출
        self.lb.setText(msg)  # Label에 텍스트 설정

    def get_properties_value(self, properties):
        """
        인자 값으로 property의 이름을 담은 시퀀스 자료형
        property를 차례로 호출하며 이름과 값의 문자열 생성
        :param properties list or tuple
        :return str
        """
        msg = []
        for p in properties:
            if not hasattr(self, p):
                continue
            value = getattr(self, p)() # => self.width(), self.x(), ...
            # getattr(object, 속성명) : object에서 속성명에 해당하는 값을 가져옴.
            # getattr(self, 'width') == self.width      # <built-in method width of Form ...
            # getattr(self, 'width')() == self.width()  # 640
            msg.append("{:>20s} : {:<30s}".format(p, str(value)))
        msg.append("{:>20s} : {:<30s}".format("mouse_x", str(self.mouse_x)))
        msg.append("{:>20s} : {:<30s}".format("mouse_y", str(self.mouse_y)))
        msg = "\n".join(msg)
        return msg

    def mouseMoveEvent(self, QMouseEvent):
        """
        위젯 안에서의 마우스 움직임이 일어날 때 호출
        :param QMouseEvent:
        :return:
        """
        self.mouse_x = QMouseEvent.x()
        self.mouse_y = QMouseEvent.y()
        self.update()

    def moveEvent(self, QMoveEvent):
        """
        창이 이동했을 경우(이동 중 아님.) 호출
        :param QMoveEvent:
        :return:
        """
        self.update()

    def paintEvent(self, QPaintEvent):
        """
        창을 다시 그려야 할 때 호출
        """
        msg = self.get_properties_value(self.properties_list)
        self.lb.setText(msg)  # Label에 텍스트 설정

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet('')                           # style 미적용
    app.setStyle(QStyleFactory.create('Fusion'))    # Windows/Fusion/...
    # app.setStyle('Fusion')    # Windows/Fusion/...
    app.setPalette(app.style().standardPalette())   # default Palette
    form = Form()
    form.show()
    sys.exit(app.exec_())
    