# %% QWidget Layout 기초(1)
#    QHBoxLayout, QVBoxLayout, addStretch

import sys
from PyQt5.QtWidgets import *

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        okButton = QPushButton("OK")
        cancelButton = QPushButton("Cancel")

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Buttons')
        self.show()

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
    
# %% Layout 기초(2) : QSizePolicy, QWidget, QHBoxLayout, window center position.

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QSizePolicy
from PyQt5 import QtGui
import sys

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        ok_button = QPushButton("OK in hbox")
        ok_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        can_button = QPushButton("Cancel in h box")
        can_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

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
    w, h = 500, 500
    ex.setGeometry(int(size.width()/2-w/2), int(size.height()/2-h/2), w, h)
    ex.setWindowTitle('Test Program')
    sys.exit(app.exec_())


# %% Layout 기초(3) : QPalette, QLineEdit, focusInEvent, focusOutEvent
#                     setColor, ColorGroup, ColorRole
'''
https://wikidocs.net/35795
- 커스텀 위젯은 Qt가 제공하는 내장 위젯(built-in widget)을 서브클래싱해서 작성할 수도 있다.
- QLineEdit를 서브클래싱하여 포커스를 가질 때 배경색이 바뀌는 위젯을 만들어 봅니다.
- LineEdit 클래스는 QLinEdit를 서브클래싱. 포커스를 가지면 배경이 연녹색으로, 잃으면 원래 색상으로 변경된다.
- 위젯의 배경은 팔레트(QPalette)를 변경하는 것으로 구현. 생성자에서 원래의 팔레트를 저장하고, 
  포커스를 얻고 잃을 때 팔레트를 스위칭해준다.
- focusInEvent(self,event), focusOutEvent(self,event) 는 포커스를 얻고 잃을 떄 발생되는 이벤트 핸들러,
  이벤트 핸들러 내에서 팔레트 변경을 수행한 후 자신의 부모클래스인 QLineEdit의 이벤트 핸들러를 호출하여 
  원래 처리해야할 작업이 정상적으로 처리될 수 있도록 한다.
'''
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QApplication, QLineEdit, QWidget, QVBoxLayout

class LineEdit(QLineEdit):
    def __init__(self,parent=None):
        QLineEdit.__init__(self,parent)
        self.clearOnFocus = False
        self.originalPalette = self.palette()
        self.newPalette = QPalette(self.palette()) # copy constructor
        self.newPalette.setColor(QPalette.Active, QPalette.Base, QColor(200,255,125))
    
    def setColorOnFocus(self, color):
        self.newPalette.setColor(QPalette.Active ,QPalette.Base, color)
        ''' 
        <형식1> QPalette.setColor(cg, cr, color)
        <형식2> QPalette.setColor(cr, color)
        # ColorGroup(cg) : QPalette.Disabled /Active /Inactive /Normal(=Active)
        # ColorRole(cr)  : QPalette.Window /WindowText /Base /Text /Button /ButtonText/...
        '''
        
    def setClearOnFocus(self, clear):
        self.clearOnFocus = clear

    def focusInEvent(self,e):
        self.setPalette(self.newPalette)
        if self.clearOnFocus : 
            self.clear()
        QLineEdit.focusInEvent(self,e)
        
    def focusOutEvent(self,e):
        self.setPalette(self.originalPalette)
        QLineEdit.focusOutEvent(self,e)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWindow = QWidget()
    mainWindow.resize(250,100)
    lineEditId = LineEdit(mainWindow)
    lineEditPW = LineEdit(mainWindow)
    
    lineEditPW.setEchoMode(QLineEdit.Password)
    lineEditPW.setClearOnFocus(True)
    lineEditPW.setColorOnFocus(Qt.red)

    qp = QPalette()
    qp.setColor(QPalette.Window, Qt.blue)
    qp.setColor(QPalette.ButtonText, Qt.blue)
    mainWindow.setPalette(qp)  
    
    layout = QVBoxLayout()
    layout.addWidget(lineEditId)
    layout.addWidget(lineEditPW)
    
    mainWindow.setLayout(layout)
    mainWindow.setWindowTitle("Line Edit")
    
    mainWindow.show()
    app.exec_()

# %% Layout 기초(4) : QPalette, setStyle, setColor, setPalette, QGridLayout

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMessageBox, QGridLayout

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    qp = QPalette()
    qp.setColor(QPalette.ButtonText, Qt.blue)
    qp.setColor(QPalette.Window, Qt.gray)
    qp.setColor(QPalette.Button, Qt.cyan)
    #만든것을 앱에 추가
    app.setPalette(qp)

    w = QWidget()
    w.resize(300,100)
    grid = QGridLayout(w)
    grid.addWidget(QPushButton("버튼 1"), 0,0) #0행 0렬
    grid.addWidget(QPushButton("버튼 2"), 0,1) #0행 10렬
    grid.addWidget(QPushButton("버튼 3"), 1,0) #1행 0렬
    grid.addWidget(QPushButton("버튼 4"), 1,1) #1행 1렬

    w.show() # 중요 window는 기본값이 hidden이라 show 해야함
    sys.exit(app.exec_()) # 이상태는 이벤트 루프가 돌고있다.
    
# %% Layout(바탕색) : QStackedLayout, QPalette, QColor, setAutoFillBackground

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget,)

class ColorBox(QWidget):
    def __init__(self, color):
        # super().__init__()
        super(ColorBox, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class MainWindow(QMainWindow):
# class MainWindow(QWidget):
    
    def __init__(self): 
        super().__init__() 
        self.resize(300,200)
        self.setWindowTitle("My App")

        button_layout = QHBoxLayout()
        
        btn = QPushButton("red")
        btn.pressed.connect(self.activate_tab_1)
        button_layout.addWidget(btn)

        btn = QPushButton("green")
        btn.pressed.connect(self.activate_tab_2)
        button_layout.addWidget(btn)

        btn = QPushButton("yellow")
        btn.pressed.connect(self.activate_tab_3)
        button_layout.addWidget(btn)

        self.stacklayout = QStackedLayout()
        self.stacklayout.addWidget(ColorBox("red"))
        self.stacklayout.addWidget(ColorBox("green"))
        self.stacklayout.addWidget(ColorBox("yellow"))
        
        pagelayout = QVBoxLayout()
        pagelayout.addLayout(button_layout)
        pagelayout.addLayout(self.stacklayout)

        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)
        # self.setLayout(pagelayout)
        # self.statusBar().showMessage('Palette Color Change')
        
    def activate_tab_1(self):
        self.stacklayout.setCurrentIndex(0)

    def activate_tab_2(self):
        self.stacklayout.setCurrentIndex(1)

    def activate_tab_3(self):
        self.stacklayout.setCurrentIndex(2)

app = QApplication(sys.argv)
app.setPalette(app.style().standardPalette())   # default Palette

window = MainWindow()
window.show()
app.exec()

# %% QFormLayout(회원가입) : QLineEdit, QPlainTextEdit, QHBoxLayout, QComboBox, QSpinBox

import sys
from PyQt5.QtWidgets import QApplication, QDialog, QFormLayout, QLineEdit, QLabel, \
    QHBoxLayout, QVBoxLayout, QComboBox, QSpinBox, QPlainTextEdit, QCheckBox, QPushButton

class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QFormLayout()

        name_widget = QLineEdit()
        birthday_layout = QHBoxLayout()
        year_widget = QComboBox()
        month_widget = QComboBox()
        date_widget = QComboBox()

        birthday_layout.addWidget(year_widget)
        birthday_layout.addWidget(month_widget)
        birthday_layout.addWidget(date_widget)

        for year in range(1900, 2021):
            year_widget.addItem(str(year))
        for month in range(1, 13):
            month_widget.addItem(str(month))
        for date in range(1, 32):
            date_widget.addItem(str(date))

        address_layout = QVBoxLayout()
        address_1 = QComboBox()
        address_1.addItems(["Seoul", "Daejeon", "Daegu", "Busan"])
        address_2 = QLineEdit()
        address_layout.addWidget(address_1)
        address_layout.addWidget(address_2)

        email_layout = QHBoxLayout()
        email_id = QLineEdit()
        email_company = QLineEdit()
        email_combobox = QComboBox()
        email_combobox.addItems(["google.com", "naver.com", "daum.net"])
        email_layout.addWidget(email_id)
        email_layout.addWidget(QLabel("@"))
        email_layout.addWidget(email_company)
        email_layout.addWidget(email_combobox)

        phone_number_layout = QHBoxLayout()
        phone_number_layout.addWidget(QLineEdit())
        phone_number_layout.addWidget(QLabel("-"))
        phone_number_layout.addWidget(QLineEdit())
        phone_number_layout.addWidget(QLabel("-"))
        phone_number_layout.addWidget(QLineEdit())

        height_widget = QSpinBox()
        height_widget.setMaximum(250)

        personal_info = QCheckBox("Agree?")

        self_intro = QPlainTextEdit()

        save_cancel_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        cancel_button = QPushButton("Cancel")
        save_cancel_layout.addWidget(save_button)
        save_cancel_layout.addWidget(cancel_button)

        main_layout.addRow("Name: ", name_widget)
        main_layout.addRow("Birthday: ", birthday_layout)
        main_layout.addRow("Address: ", address_layout)
        main_layout.addRow("E-mail: ", email_layout)
        main_layout.addRow("Phone Number: ", phone_number_layout)
        main_layout.addRow("Height(cm): ", height_widget)
        main_layout.addRow("Personal Information Share: ", personal_info)
        main_layout.addRow("Self Introduction: ", self_intro)
        main_layout.addRow("", save_cancel_layout)

        self.setLayout(main_layout)
        self.resize(500, 500)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())

# %% 위젯 활용하기(1) : QGridLayout/QGroupBox, setFlat, QMenu, setTristate, QRadioButton, QCheckBox

import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QGroupBox, QRadioButton, \
                             QCheckBox, QPushButton, QMenu, QGridLayout, QVBoxLayout)
class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        grid.addWidget(self.createFirstGroup(), 0, 0)
        grid.addWidget(self.createSecondGroup(), 1, 0)
        grid.addWidget(self.createNonGroup(), 0, 1)
        grid.addWidget(self.createPushButtonGroup(), 1, 1)

        self.setLayout(grid)
        self.setWindowTitle('Grid Layout / groupbox')
        self.setGeometry(300, 300, 480, 320)
        self.show()

    def createFirstGroup(self):
        groupbox = QGroupBox('Exclusive Radio Buttons')

        radio1 = QRadioButton('Radio1')
        radio2 = QRadioButton('Radio2')
        radio3 = QRadioButton('Radio3')
        radio1.setChecked(True)

        vbox = QVBoxLayout()
        vbox.addWidget(radio1)
        vbox.addWidget(radio2)
        vbox.addWidget(radio3)
        groupbox.setLayout(vbox)

        return groupbox

    def createSecondGroup(self):
        groupbox = QGroupBox('Exclusive Radio/CheckBox Buttons')
        groupbox.setCheckable(True)
        groupbox.setChecked(False)

        radio1 = QRadioButton('Radio1')
        radio2 = QRadioButton('Radio2')
        radio3 = QRadioButton('Radio3')
        radio1.setChecked(True)
        checkbox = QCheckBox('Independent Checkbox')
        checkbox.setChecked(True)

        vbox = QVBoxLayout()
        vbox.addWidget(radio1)
        vbox.addWidget(radio2)
        vbox.addWidget(radio3)
        vbox.addWidget(checkbox)
        vbox.addStretch(1)
        groupbox.setLayout(vbox)

        return groupbox

    def createNonGroup(self):
        groupbox = QGroupBox('Non-Exclusive Checkboxes')
        groupbox.setFlat(True)

        checkbox1 = QCheckBox('Checkbox1')
        checkbox2 = QCheckBox('Checkbox2')
        checkbox2.setChecked(True)
        tristatebox = QCheckBox('Tri-state Button')
        tristatebox.setTristate(True)

        vbox = QVBoxLayout()
        vbox.addWidget(checkbox1)
        vbox.addWidget(checkbox2)
        vbox.addWidget(tristatebox)
        vbox.addStretch(1)
        groupbox.setLayout(vbox)

        return groupbox

    def createPushButtonGroup(self):
        groupbox = QGroupBox('Push Buttons')
        groupbox.setCheckable(True)
        groupbox.setChecked(True)

        pushBtn = QPushButton('Normal Button')
        toggBtn = QPushButton('Toggle Button')
        toggBtn.setCheckable(True)
        toggBtn.setChecked(True)
        flatBtn = QPushButton('Flat Button')
        flatBtn.setFlat(True)
        popupBtn = QPushButton('Popup Button')
        
        menu = QMenu(self)
        menu.addAction('First Item')
        menu.addAction('Second Item')
        menu.addAction('Third Item')
        menu.addAction('Fourth Item')
        popupBtn.setMenu(menu)

        vbox = QVBoxLayout()
        vbox.addWidget(pushBtn)
        vbox.addWidget(toggBtn)
        vbox.addWidget(flatBtn)
        vbox.addWidget(popupBtn)
        vbox.addStretch(1)
        groupbox.setLayout(vbox)

        return groupbox

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())

# %% 위젯 활용하기(2) :  : QGroupBox, QGridLayout, QCheckBox, QComboBox, QTextEdit, QDial, ...

from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)

class Widget(QDialog):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)

        self.orgPalette = QApplication.palette()

        styleComboBox = QComboBox()
        styleComboBox.addItems(QStyleFactory.keys())

        styleLabel = QLabel("&Style:")
        styleLabel.setBuddy(styleComboBox)

        self.paletteChkBox = QCheckBox("&Use style's standard palette")
        self.paletteChkBox.setChecked(True)

        disableChkBox = QCheckBox("&Disable widgets")

        self.createTopLeftGBox()
        self.createTopRightGBox()
        self.createBtmLeftTab()
        self.createBtmRightGBox()
        self.createProgressBar()

        styleComboBox.activated[str].connect(self.changeStyle)
        self.paletteChkBox.toggled.connect(self.changePalette)
        disableChkBox.toggled.connect(self.topLeftGroupBox.setDisabled)
        disableChkBox.toggled.connect(self.topRightGBox.setDisabled)
        disableChkBox.toggled.connect(self.btmLeftTab.setDisabled)
        disableChkBox.toggled.connect(self.btmRightGBox.setDisabled)

        topLayout = QHBoxLayout()
        topLayout.addWidget(styleLabel)
        topLayout.addWidget(styleComboBox)
        topLayout.addStretch(1)
        topLayout.addWidget(self.paletteChkBox)
        topLayout.addWidget(disableChkBox)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        mainLayout.addWidget(self.topRightGBox, 1, 1)
        mainLayout.addWidget(self.btmLeftTab, 2, 0)
        mainLayout.addWidget(self.btmRightGBox, 2, 1)
        mainLayout.addWidget(self.progressBar, 3, 0, 1, 2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle("Styles")
        self.changeStyle('Windows')

    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    def changePalette(self):
        if (self.paletteChkBox.isChecked()):
            QApplication.setPalette(QApplication.style().standardPalette())
        else:
            QApplication.setPalette(self.orgPalette)

    def advanceProgressBar(self):
        curVal = self.progressBar.value()
        maxVal = self.progressBar.maximum()
        self.progressBar.setValue(curVal + (maxVal - curVal) // 100)

    def createTopLeftGBox(self):
        self.topLeftGroupBox = QGroupBox("Group 1")

        rdoBtn1 = QRadioButton("Radio button 1")
        rdoBtn2 = QRadioButton("Radio button 2")
        rdoBtn3 = QRadioButton("Radio button 3")
        rdoBtn1.setChecked(True)

        checkBox = QCheckBox("Tri-state check box")
        checkBox.setTristate(True)
        checkBox.setCheckState(Qt.PartiallyChecked)

        layout = QVBoxLayout()
        layout.addWidget(rdoBtn1)
        layout.addWidget(rdoBtn2)
        layout.addWidget(rdoBtn3)
        layout.addWidget(checkBox)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)    

    def createTopRightGBox(self):
        self.topRightGBox = QGroupBox("Group 2")

        defaultPushBtn = QPushButton("Default Push Button")
        defaultPushBtn.setDefault(True)

        togPushBtn = QPushButton("Toggle Push Button")
        togPushBtn.setCheckable(True)
        togPushBtn.setChecked(True)

        flatPushBtn = QPushButton("Flat Push Button")
        flatPushBtn.setFlat(True)

        layout = QVBoxLayout()
        layout.addWidget(defaultPushBtn)
        layout.addWidget(togPushBtn)
        layout.addWidget(flatPushBtn)
        layout.addStretch(1)
        self.topRightGBox.setLayout(layout)

    def createBtmLeftTab(self):
        self.btmLeftTab = QTabWidget()
        self.btmLeftTab.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)

        tab1 = QWidget()
        tableWidget = QTableWidget(10, 10)

        tab1hbox = QHBoxLayout()
        tab1hbox.setContentsMargins(5, 5, 5, 5)
        tab1hbox.addWidget(tableWidget)
        tab1.setLayout(tab1hbox)

        tab2 = QWidget()
        textEdit = QTextEdit()
        textEdit.setPlainText("Twinkle, twinkle, little star,\n"
                              "How I wonder what you are.\n" 
                              "Up above the world so high,\n"
                              "Like a diamond in the sky.\n"
                              "Twinkle, twinkle, little star,\n" 
                              "How I wonder what you are!\n")
        tab2hbox = QHBoxLayout()
        tab2hbox.setContentsMargins(5, 5, 5, 5)
        tab2hbox.addWidget(textEdit)
        tab2.setLayout(tab2hbox)

        self.btmLeftTab.addTab(tab1, "&Table")
        self.btmLeftTab.addTab(tab2, "Text &Edit")

    def createBtmRightGBox(self):
        self.btmRightGBox = QGroupBox("Group 3")
        self.btmRightGBox.setCheckable(True)
        self.btmRightGBox.setChecked(True)

        lineEdit = QLineEdit('s3cRe7')
        lineEdit.setEchoMode(QLineEdit.Password)

        spinBox = QSpinBox(self.btmRightGBox)
        spinBox.setValue(50)

        dateTimeEdit = QDateTimeEdit(self.btmRightGBox)
        dateTimeEdit.setDateTime(QDateTime.currentDateTime())

        slider = QSlider(Qt.Horizontal, self.btmRightGBox)
        slider.setValue(40)

        scrollBar = QScrollBar(Qt.Horizontal, self.btmRightGBox)
        scrollBar.setValue(60)

        dial = QDial(self.btmRightGBox)
        dial.setValue(30)
        dial.setNotchesVisible(True)

        layout = QGridLayout()
        layout.addWidget(lineEdit, 0, 0, 1, 2)
        layout.addWidget(spinBox, 1, 0, 1, 2)
        layout.addWidget(dateTimeEdit, 2, 0, 1, 2)
        layout.addWidget(slider, 3, 0)
        layout.addWidget(scrollBar, 4, 0)
        layout.addWidget(dial, 3, 1, 2, 1)
        layout.setRowStretch(5, 1)
        self.btmRightGBox.setLayout(layout)

    def createProgressBar(self):
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 10000)
        self.progressBar.setValue(0)

        timer = QTimer(self)
        timer.timeout.connect(self.advanceProgressBar)
        timer.start(1000)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    gallery = Widget()
    gallery.show()
    sys.exit(app.exec()) 
    
   