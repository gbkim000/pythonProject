# %% PyQt Widgets 예제
# https://wikidocs.net/128689
# https://wikidocs.net/book/2165 (PyQt5 Tutorial - 파이썬으로 만드는 나만의 GUI 프로그램)
# https://planet.turbogears.org/1.0/docs/Widgets/DataGrid.html#basic-datagrid-usage
# https://python.hotexamples.com/examples/datagrid.core/DataGrid/-/python-datagrid-class-examples.html

# pip install spyder‑kernels==2.1.*

#%% 위젯 활용(1) : 툴팁/상태바 - QToolTip/statusBar

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolTip, QPushButton
from PyQt5.QtGui import QFont

class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('This is a <b>QWidget</b> widget')

        btn = QPushButton('Button', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.move(50, 50)
        btn.resize(btn.sizeHint())        
        
        self.statusBar().showMessage('Ready')

        self.setWindowTitle('Statusbar')
        self.setGeometry(300, 300, 300, 200)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    app.setPalette(app.style().standardPalette())   # default Palette
    sys.exit(app.exec_()) 

#%% 위젯 활용(2) :  날짜와 시간 표시하기.

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QDate, Qt

class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.date = QDate.currentDate()
        self.initUI()

    def initUI(self):
        self.statusBar().showMessage(self.date.toString(Qt.DefaultLocaleLongDate))

        self.setWindowTitle('Date')
        self.setGeometry(300, 300, 400, 200)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())


#%%  날짜, 시간 출력하기.
from PyQt5.QtCore import QTime, Qt, QDateTime

time = QTime.currentTime()
print(time.toString('h.m.s'))
print(time.toString('hh.mm.ss'))
print(time.toString('hh.mm.ss.zzz'))
print(time.toString(Qt.DefaultLocaleLongDate))
print(time.toString(Qt.DefaultLocaleShortDate))

datetime = QDateTime.currentDateTime()
print(datetime.toString('d.M.yy hh:mm:ss'))
print(datetime.toString('dd.MM.yyyy, hh:mm:ss'))
print(datetime.toString(Qt.DefaultLocaleLongDate))
print(datetime.toString(Qt.DefaultLocaleShortDate))

#%% 위젯 활용(3) : 스타일 꾸미기.
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        lbl_red = QLabel('Red')
        lbl_green = QLabel('Green')
        lbl_blue = QLabel('Blue')

        lbl_red.setStyleSheet("color: red;"
                             "border-style: solid;"
                             "border-width: 2px;"
                             "border-color: #FA8072;"
                             "border-radius: 3px")
        lbl_green.setStyleSheet("color: green;"
                               "background-color: #7FFFD4")
        lbl_blue.setStyleSheet("color: blue;"
                              "background-color: #87CEFA;"
                              "border-style: dashed;"
                              "border-width: 3px;"
                              "border-color: #1E90FF")
        
        lbl_red.setAlignment(Qt.AlignCenter)
        lbl_green.setAlignment(Qt.AlignCenter)
        lbl_blue.setAlignment(Qt.AlignVCenter)
        lbl_blue.setAlignment(Qt.AlignRight)
        
        vbox = QVBoxLayout()
        vbox.addWidget(lbl_red)
        vbox.addWidget(lbl_green)
        vbox.addWidget(lbl_blue)

        self.setLayout(vbox)
        self.setWindowTitle('Stylesheet')
        self.setGeometry(300, 300, 300, 200)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    
#%% 위젯 활용(4) : 절대적 배치.
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        label1 = QLabel('Label1', self)
        label1.move(20, 20)
        label2 = QLabel('Label2', self)
        label2.move(20, 60)

        btn1 = QPushButton('Button1', self)
        btn1.move(80, 13)
        btn2 = QPushButton('Button2', self)
        btn2.move(80, 53)

        self.setWindowTitle('Absolute Positioning')
        self.setGeometry(300, 300, 400, 200)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())

#%% 위젯 활용(5) : 박스 레이아웃.

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        okButton = QPushButton('OK')
        cancelButton = QPushButton('Cancel')

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(3)
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        self.setLayout(vbox)
        self.setWindowTitle('Box Layout')
        self.setGeometry(300, 300, 300, 200)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())

#%% 위젯 활용(6) : 그리드 레이아웃.

import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QLabel, 
                             QLineEdit, QTextEdit)

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        grid.addWidget(QLabel('Title:'), 0, 0)
        grid.addWidget(QLabel('Author:'), 1, 0)
        grid.addWidget(QLabel('Review:'), 2, 0)

        grid.addWidget(QLineEdit(), 0, 1)
        grid.addWidget(QLineEdit(), 1, 1)
        grid.addWidget(QTextEdit(), 2, 1)

        self.setWindowTitle('QGridLayout')
        self.setGeometry(300, 300, 300, 200)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())

#%% 위젯 활용(7) :  QPushButton.

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        btn1 = QPushButton('&Button1', self)
        btn1.setCheckable(True)
        btn1.toggle()

        btn2 = QPushButton(self)
        btn2.setText('Button&2')

        btn3 = QPushButton('Button3', self)
        btn3.setEnabled(False)

        vbox = QVBoxLayout()
        vbox.addWidget(btn1)
        vbox.addWidget(btn2)
        vbox.addWidget(btn3)

        self.setLayout(vbox)
        self.setWindowTitle('QPushButton')
        self.setGeometry(300, 300, 300, 200)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    
#%% 위젯 활용(8) :  QLabel.

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        label1 = QLabel('First Label', self)
        label1.setAlignment(Qt.AlignCenter)
        label1
        label2 = QLabel('Second Label', self)
        label2.setAlignment(Qt.AlignHCenter)
        #label2.setAlignment(Qt.AlignVCenter)
        
        font1 = label1.font()
        font1.setPointSize(20)

        font2 = label2.font()
        font2.setFamily('Times New Roman')
        font2.setBold(True)

        label1.setFont(font1)
        label2.setFont(font2)
        label1.setStyleSheet("background-color: lightgreen")
        label2.setStyleSheet("background-color: yellow")
        
        layout = QVBoxLayout()
        layout.addWidget(label1)
        layout.addWidget(label2)

        self.setLayout(layout)

        self.setWindowTitle('QLabel')
        self.setGeometry(300, 300, 300, 200)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    
#%% 위젯 활용(9) :  QCheckBox / QRadioButton

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QCheckBox
from PyQt5.QtCore import Qt

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        cb = QCheckBox('Show title', self)
        cb.move(20, 20)
        cb.toggle()
        cb.stateChanged.connect(self.changeTitle)

        rbtn1 = QRadioButton('First Button', self)
        rbtn1.move(50, 50)
        rbtn1.setChecked(True)

        rbtn2 = QRadioButton(self)
        rbtn2.move(50, 70)
        rbtn2.setText('Second Button')

        self.setWindowTitle('QCheckBox')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def changeTitle(self, state):
        if state == Qt.Checked:
            self.setWindowTitle('QCheckBox')
        else:
            self.setWindowTitle(' ')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    
#%% 위젯 활용(10) : QComboBox.

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.lbl = QLabel('Option1', self)
        self.lbl.move(50, 150)

        cb = QComboBox(self)
        cb.addItem('Option1')
        cb.addItem('Option2')
        cb.addItem('Option3')
        cb.addItem('Option4')
        cb.move(50, 50)
        cb.activated[str].connect(self.onActivated)

        self.setWindowTitle('QComboBox')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def onActivated(self, text):
        self.lbl.setText(text)
        self.lbl.adjustSize()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    
#%% 위젯 활용(11) :  QLineEdit.

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.lbl = QLabel(self)
        self.lbl.move(60, 40)

        self.qle = QLineEdit(self)
        self.qle.setEchoMode(QLineEdit.Password)  # Normal/NoEcho/Password/PasswordEchoOnEdit
        self.qle.move(60, 100)
        self.qle.textChanged[str].connect(self.onChanged)

        self.setWindowTitle('QLineEdit')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def onChanged(self, text):
        self.lbl.setText(text)
        self.lbl.adjustSize()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    
#%% 위젯 활용(12) : QProgressBar.

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QProgressBar
from PyQt5.QtCore import QBasicTimer

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)

        self.btn = QPushButton('Start', self)
        self.btn.move(40, 80)
        self.btn.clicked.connect(self.doAction)

        self.timer = QBasicTimer()
        self.step = 0

        self.setWindowTitle('QProgressBar')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()
            self.btn.setText('Finished')
            return

        self.step = self.step + 1
        self.pbar.setValue(self.step)

    def doAction(self):
        if self.timer.isActive():
            self.timer.stop()
            self.btn.setText('Start')
        else:
            self.timer.start(100, self)
            self.btn.setText('Stop')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    
#%% 위젯 활용(13) : QSlider & QDial.

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QSlider, QDial, QPushButton
from PyQt5.QtCore import Qt

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.move(30, 30)
        self.slider.setRange(0, 50)
        self.slider.setSingleStep(2)

        self.dial = QDial(self)
        self.dial.move(30, 50)
        self.dial.setRange(0, 50)

        btn = QPushButton('Default', self)
        btn.move(35, 160)

        self.slider.valueChanged.connect(self.dial.setValue)
        self.dial.valueChanged.connect(self.slider.setValue)
        btn.clicked.connect(self.button_clicked)

        self.setWindowTitle('QSlider and QDial')
        self.setGeometry(300, 300, 400, 200)
        self.show()

    def button_clicked(self):
        self.slider.setValue(0)
        self.dial.setValue(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    
#%% 위젯 활용(14) :  QSplitter.

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QFrame, QSplitter
from PyQt5.QtCore import Qt

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout()

        top = QFrame()
        top.setFrameShape(QFrame.Box)

        midleft = QFrame()
        midleft.setFrameShape(QFrame.StyledPanel)

        midright = QFrame()
        midright.setFrameShape(QFrame.Panel)

        bottom = QFrame()
        bottom.setFrameShape(QFrame.WinPanel)
        bottom.setFrameShadow(QFrame.Sunken)

        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(midleft)
        splitter1.addWidget(midright)

        splitter2 = QSplitter(Qt.Vertical)
        splitter2.addWidget(top)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(bottom)

        hbox.addWidget(splitter2)
        self.setLayout(hbox)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QSplitter')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    
#%% 위젯 활용(15) : QPixmap.
import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        print(os.getcwd())
        pixmap = QPixmap('./images/landscape.jpg')

        lbl_img = QLabel()
        lbl_img.setPixmap(pixmap)
        lbl_size = QLabel('Width: '+str(pixmap.width())+', Height: '+str(pixmap.height()))
        lbl_size.setAlignment(Qt.AlignCenter)

        vbox = QVBoxLayout()
        vbox.addWidget(lbl_img)
        vbox.addWidget(lbl_size)
        self.setLayout(vbox)

        self.setWindowTitle('QPixmap')
        self.move(300, 300)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    
#%% 위젯 활용(16) :  QCalenderWidget.
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QCalendarWidget
from PyQt5.QtCore import QDate

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        cal = QCalendarWidget(self)
        cal.setGridVisible(True)
        cal.clicked[QDate].connect(self.showDate)

        self.lbl = QLabel(self)
        date = cal.selectedDate()
        self.lbl.setText(date.toString())

        vbox = QVBoxLayout()
        vbox.addWidget(cal)
        vbox.addWidget(self.lbl)

        self.setLayout(vbox)

        self.setWindowTitle('QCalendarWidget')
        self.setGeometry(300, 300, 400, 300)
        self.show()

    def showDate(self, date):
        self.lbl.setText(date.toString())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    
#%% 위젯 활용(17) : QSpinBox.
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QSpinBox, QVBoxLayout

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.lbl1 = QLabel('QSpinBox')
        self.spinbox = QSpinBox()
        self.spinbox.setMinimum(-10)
        self.spinbox.setMaximum(30)
        # self.spinbox.setRange(-10, 30)
        self.spinbox.setSingleStep(2)
        self.lbl2 = QLabel('0')

        self.spinbox.valueChanged.connect(self.value_changed)

        vbox = QVBoxLayout()
        vbox.addWidget(self.lbl1)
        vbox.addWidget(self.spinbox)
        vbox.addWidget(self.lbl2)
        vbox.addStretch()

        self.setLayout(vbox)

        self.setWindowTitle('QSpinBox')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def value_changed(self):
        self.lbl2.setText(str(self.spinbox.value()))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
      
#%% 위젯 활용(18) : QDoubleSpinBox.

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QDoubleSpinBox, QVBoxLayout

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.lbl1 = QLabel('QDoubleSpinBox')
        self.dspinbox = QDoubleSpinBox()
        self.dspinbox.setRange(0, 100)
        self.dspinbox.setSingleStep(0.5)
        self.dspinbox.setPrefix('$ ')
        self.dspinbox.setDecimals(1)
        self.lbl2 = QLabel('$ 0.0')

        self.dspinbox.valueChanged.connect(self.value_changed)

        vbox = QVBoxLayout()
        vbox.addWidget(self.lbl1)
        vbox.addWidget(self.dspinbox)
        vbox.addWidget(self.lbl2)
        vbox.addStretch()

        self.setLayout(vbox)
        self.setWindowTitle('QDoubleSpinBox')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def value_changed(self):
        self.lbl2.setText('$ ' + str(self.dspinbox.value()))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    
#%% 위젯 활용(198) : QDateEdit.

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QDateEdit, QVBoxLayout
from PyQt5.QtCore import QDate

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        lbl = QLabel('QDateEdit')

        dateedit = QDateEdit(self)
        dateedit.setDate(QDate.currentDate())
        dateedit.setMinimumDate(QDate(1900, 1, 1))
        dateedit.setMaximumDate(QDate(2100, 12, 31))
        # dateedit.setDateRange(QDate(1900, 1, 1), QDate(2100, 12, 31))

        vbox = QVBoxLayout()
        vbox.addWidget(lbl)
        vbox.addWidget(dateedit)
        vbox.addStretch()

        self.setLayout(vbox)

        self.setWindowTitle('QDateEdit')
        self.setGeometry(300, 300, 300, 200)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    
#%% 위젯 활용(20) : QTimeEdit.
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTimeEdit, QVBoxLayout
from PyQt5.QtCore import QTime

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        lbl = QLabel('QTimeEdit')

        timeedit = QTimeEdit(self)
        timeedit.setTime(QTime.currentTime())
        timeedit.setTimeRange(QTime(3, 00, 00), QTime(23, 30, 00))
        timeedit.setDisplayFormat('hh:mm:ss')

        vbox = QVBoxLayout()
        vbox.addWidget(lbl)
        vbox.addWidget(timeedit)
        vbox.addStretch()

        self.setLayout(vbox)

        self.setWindowTitle('QTimeEdit')
        self.setGeometry(300, 300, 300, 200)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())

#%% 위젯 활용(21) : QDateTimeEdit.

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QDateTimeEdit, QVBoxLayout
from PyQt5.QtCore import QDateTime

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        lbl = QLabel('QTimeEdit')

        datetimeedit = QDateTimeEdit(self)
        datetimeedit.setDateTime(QDateTime.currentDateTime())
        datetimeedit.setDateTimeRange(QDateTime(1900, 1, 1, 00, 00, 00), QDateTime(2100, 1, 1, 00, 00, 00))
        datetimeedit.setDisplayFormat('yyyy.MM.dd hh:mm:ss')

        vbox = QVBoxLayout()
        vbox.addWidget(lbl)
        vbox.addWidget(datetimeedit)
        vbox.addStretch()

        self.setLayout(vbox)

        self.setWindowTitle('QDateTimeEdit')
        self.setGeometry(300, 300, 300, 200)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    
#%% 위젯 활용(22) : QTextBrowser.
import sys
from PyQt5.QtWidgets import (QApplication, QWidget,
                            QLineEdit, QTextBrowser, QPushButton, QVBoxLayout)

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.le = QLineEdit()
        self.le.returnPressed.connect(self.append_text)

        self.tb = QTextBrowser()
        self.tb.setAcceptRichText(True)
        self.tb.setOpenExternalLinks(True)
        self.tb.setReadOnly(False)
        self.clear_btn = QPushButton('Clear')
        self.clear_btn.pressed.connect(self.clear_text)

        vbox = QVBoxLayout()
        vbox.addWidget(self.le, 0)
        vbox.addWidget(self.tb, 1)
        vbox.addWidget(self.clear_btn, 2)

        self.setLayout(vbox)

        self.setWindowTitle('QTextBrowser')
        self.setGeometry(300, 300, 300, 300)
        self.show()

    def append_text(self):
        text = self.le.text()
        self.tb.append(text)
        self.le.clear()

    def clear_text(self):
        self.tb.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    
#%% 위젯 활용(23) : QTextEdit.
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTextEdit, QVBoxLayout

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.lbl1 = QLabel('Enter your sentence:')
        self.te = QTextEdit()
        self.te.setAcceptRichText(False)
        self.lbl2 = QLabel('The number of words is 0')

        self.te.textChanged.connect(self.text_changed)

        vbox = QVBoxLayout()
        vbox.addWidget(self.lbl1)
        vbox.addWidget(self.te)
        vbox.addWidget(self.lbl2)
        vbox.addStretch()

        self.setLayout(vbox)

        self.setWindowTitle('QTextEdit')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def text_changed(self):
        text = self.te.toPlainText()
        self.lbl2.setText('The number of words is ' + str(len(text.split())))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
   
#%% 위젯 활용(24) : QInputDialog.
# getText() / getMultiLineText() / getInt() / getItem()

import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLineEdit, QInputDialog)

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.btn = QPushButton('Dialog', self)
        self.btn.move(30, 30)
        self.btn.clicked.connect(self.showDialog)

        self.le = QLineEdit(self)
        self.le.move(120, 35)

        self.setWindowTitle('Input dialog')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def showDialog(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter your name:')

        if ok:
            self.le.setText(str(text))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    
#%% 위젯 활용(25) : QColorDialog.

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFrame, QColorDialog
from PyQt5.QtGui import QColor

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        col = QColor(0, 0, 0)

        self.btn = QPushButton('Dialog', self)
        self.btn.move(30, 30)
        self.btn.clicked.connect(self.showDialog)

        self.frm = QFrame(self)
        self.frm.setStyleSheet('QWidget { background-color: %s }' % col.name())
        self.frm.setGeometry(130, 35, 100, 100)

        self.setWindowTitle('Color Dialog')
        self.setGeometry(300, 300, 250, 180)
        self.show()

    def showDialog(self):
        col = QColorDialog.getColor()

        if col.isValid():
            self.frm.setStyleSheet('QWidget { background-color: %s }' % col.name())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())

#%% 위젯 활용(26) : QFontDialog.
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QPushButton, QSizePolicy, QLabel, QFontDialog)

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        btn = QPushButton('Dialog', self)
        btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn.move(20, 20)
        btn.clicked.connect(self.showDialog)

        vbox = QVBoxLayout()
        vbox.addWidget(btn)

        self.lbl = QLabel('The quick brown fox jumps over the lazy dog', self)
        self.lbl.move(130, 20)

        vbox.addWidget(self.lbl)
        self.setLayout(vbox)

        self.setWindowTitle('Font Dialog')
        self.setGeometry(300, 300, 250, 180)
        self.show()

    def showDialog(self):
        font, ok = QFontDialog.getFont()

        if ok:
           self.lbl.setFont(font)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    
#%% 위젯 활용(27) : QFileDialog.

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QFileDialog
from PyQt5.QtGui import QIcon

class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()

        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open New File')
        openFile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

        self.setWindowTitle('File Dialog')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './')

        if fname[0]:
            f = open(fname[0], 'r', encoding='UTF-8')

            with f:
                data = f.read()
                self.textEdit.setText(data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())

#%% 위젯 활용(28) : QMessageBox.

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('QMessageBox')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def closeEvent(self, event):
        msgBox = QMessageBox()
        msgBox.setText("The document has been modified.")
        msgBox.setInformativeText("Do you want to save your changes?")
        msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        msgBox.setDefaultButton(QMessageBox.Save)
        reply = msgBox.exec()
        
        reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())

#%% 위젯 활용(29) : QCalendarWidget으로 달력에 공휴일 표시하기

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QDate

class MyMain(QWidget):
    def __init__(self):
        super().__init__()

        holidays = ['20171003', '20171004', '20171005', '20171006', '20171009']

        vbox = QVBoxLayout()
        self.cal = QCalendarWidget()
        self.cal.setVerticalHeaderFormat(0)  # vertical header 숨기기

        fm = QTextCharFormat()
        fm.setForeground(Qt.red)
        fm.setBackground(Qt.yellow)

        for dday in holidays:
            dday2 = QDate.fromString(dday, "yyyyMMdd")
            self.cal.setDateTextFormat(dday2, fm)

        vbox.addWidget(self.cal)
        self.setLayout(vbox)

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    myWindow = MyMain()

    myWindow.show()
    app.exec_()

#%% 위젯 활용(30) : QLCDNumber /QDial /이벤트

import sys
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QLCDNumber, QDial, QPushButton, QVBoxLayout, QHBoxLayout)

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        lcd = QLCDNumber(self)
        dial = QDial(self)
        btn1 = QPushButton('Big', self)
        btn2 = QPushButton('Small', self)

        hbox = QHBoxLayout()
        hbox.addWidget(btn1)
        hbox.addWidget(btn2)

        vbox = QVBoxLayout()
        vbox.addWidget(lcd)
        vbox.addWidget(dial)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        dial.valueChanged.connect(lcd.display)
        btn1.clicked.connect(self.resizeBig)
        btn2.clicked.connect(self.resizeSmall)

        self.setWindowTitle('Signal and Slot')
        self.setGeometry(200, 200, 200, 250)
        self.show()

    def resizeBig(self):
        self.resize(400, 500)

    def resizeSmall(self):
        self.resize(200, 250)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    
#%% 위젯 활용(31) : Label 스타일 변경(색상, 경계선, 정렬)

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

class stylesheetApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        red_label = QLabel('빨간 라벨')
        blue_label = QLabel('파란 라벨')
        green_label = QLabel('초록 라벨')

        red_label.setStyleSheet("color: #FF5733; border-style: solid; border-width: 2px; border-color: #FFC300; border-radius: 10px; ")
        blue_label.setStyleSheet(
            "color: #4D69E8; border-style: solid; border-width: 2px; border-color: #54A0FF; border-radius: 10px; ")
        green_label.setStyleSheet(
            "color: #41E881; border-style: solid; border-width: 2px; border-color: #67E841; border-radius: 10px; ")
        
        red_label.setAlignment(Qt.AlignCenter)
        
        vbox = QVBoxLayout()
        vbox.addWidget(red_label)
        vbox.addWidget(blue_label)
        vbox.addWidget(green_label)

        self.setLayout(vbox)
        self.setWindowTitle('스타일 변경')
        self.setGeometry(500,500,500,400)
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = stylesheetApp()
    sys.exit(app.exec_())

#%% 위젯 활용(32) : 점 그리기1 (drawPoint).

import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('Points')
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_point(qp)
        qp.end()

    def draw_point(self, qp):
        qp.setPen(QPen(Qt.blue, 8))
        qp.drawPoint(int(self.width()/2), int(self.height()/2))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())

#%% 위젯 활용(33) : 직선 그리기 (drawLine).

import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('drawLine')
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_line(qp)
        qp.end()

    def draw_line(self, qp):
        qp.setPen(QPen(Qt.blue, 8))
        qp.drawLine(30, 230, 200, 50)
        qp.setPen(QPen(Qt.green, 12))
        qp.drawLine(140, 60, 320, 280)
        qp.setPen(QPen(Qt.red, 16))
        qp.drawLine(330, 250, 40, 190)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    
#%% 위젯 활용(34) :  직사각형 그리기 (drawRect)

import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush
from PyQt5.QtCore import Qt

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('drawRect')
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_rect(qp)
        qp.end()

    def draw_rect(self, qp):
        qp.setBrush(QColor(180, 100, 160))
        qp.setPen(QPen(QColor(60, 60, 60), 3))
        qp.drawRect(20, 20, 100, 100)

        qp.setBrush(QColor(40, 150, 20))
        qp.setPen(QPen(Qt.blue, 2))
        qp.drawRect(180, 120, 50, 120)

        qp.setBrush(Qt.yellow)
        qp.setPen(QPen(Qt.red, 5))
        qp.drawRect(280, 30, 80, 40)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())

