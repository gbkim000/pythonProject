#%% Menu Bar 데모(1) : QAction/ QFileDialog/ /getOpenFileName /getSaveFileName 
#  /menuBar/ addMenu /setStyleSheet

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

qss = """
QMenuBar {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 lightgray, stop:1 darkgray);
}
QMenuBar::item {
    spacing: 3px;           
    padding: 2px 20px; /* 상하 좌우 */
    margin : 0px 2px;
    background-color: rgb(210,105,30);
    color: rgb(255,255,255);  
    border-radius: 5px;
}
QMenuBar::item:selected {    
    background-color: rgb(244,164,96);
}
QMenuBar::item:pressed {
    background: rgb(128,0,0);
}

/* +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */  

QMenu {
    background-color: #ABABAB;   
    border: 1px solid black;
    margin: 2px;
}
QMenu::item {
    background-color: transparent;
}
QMenu::item:selected { 
    background-color: #654321;
    color: rgb(255,255,255);
}
"""

class QtGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(400, 400)
        self.setWindowTitle("Appia")
        
        menubar = self.menuBar()
        
        menu1 = menubar.addMenu("&File")
        menu2 = menubar.addMenu("&Edit")
        menu3 = menubar.addMenu("서식")
        
        # [menu1 list]
        loadfile = QAction('laod File ...', self)
        savefile = QAction('save File ...', self)
        exitmenu = QAction(QIcon('exit.png'), 'Exit', self)
        
        loadfile.triggered.connect(self.add_open)
        savefile.triggered.connect(self.add_save)
        exitmenu.triggered.connect(self.close) # (qApp.quit)
        
        loadfile.setStatusTip('laod File ...')
        savefile.setStatusTip('save File ...')        
        exitmenu.setStatusTip('Exit application')

        editfile = QAction('Edit ...', self)
        editfile.triggered.connect(self.edit_file)
        editfile.setShortcut('Ctrl+E')
        editfile.setStatusTip('Edit File ...')
        
        menu1.addAction(loadfile)
        menu1.addAction(savefile)
        menu1.addAction(exitmenu)
        menu2.addAction(editfile)
        
        self.statusBar()
        self.statusBar().showMessage('이곳은 상태바입니다....준비중')
        self.show()
        
    def add_open(self):
        FileOpen = QFileDialog.getOpenFileName(self, 'Open file', './')
 
    def add_save(self):
        FileSave = QFileDialog.getSaveFileName(self, 'Save file', './')
        
    def edit_file(self):
        print("Selected 'edit file menu...'")
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qss) 
    ex = QtGUI()
    ex.setWindowIcon(QIcon('./py-qt.png')) 
    ex.resize(420,440)
    app.exec_()

#%% Menu Bar 데모(2) : menuBar /QAction/ addMenu/ addAction /
# 참조 자료 출처 : http://penguinitis.g1.xrea.com/computer/programming/Python/PyQt5/PyQt5-memo/PyQt5-memo.html

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtWidgets import QAction, qApp

# Ribbon Menu를 만들기 위한 QMainwindow Class 선언
class Ribbon_Menu(QMainWindow) :
    def __init__(self) :
        super () .__init__ ()
        self.setWindowTitle("Ribbon Menu Demonstration")  # Window Menu Title 설정
        self.resize(500, 300)

        # 기본 리본 메뉴 바를 선언함.
        # Action 5개를 선언함.

        mainMenuBar = self.menuBar()

        # 기본 리본 메뉴 바에 메뉴 추가
        Menu01 = mainMenuBar.addMenu("&First Ribbon Menu")
        Menu02 = mainMenuBar.addMenu("&Second Ribbon Menu")
        # Menu01.addAction(action1)
        # Menu02.addAction(action1)

        # Action 5개를 선언함.
        action1 = QAction("&First Menu Action", self)
        action1.triggered.connect(self.First_Ribbon_Menu_Action)
        action1.setShortcut("Ctrl + e")

        action2 = QAction("&Second Menu Action", self)
        action2.triggered.connect (self.Second_Ribbon_Menu_Action)

        action3 = QAction("&Third Menu Action", self)
        action3.triggered.connect(self.Third_Ribbon_Menu_Action)
        
        action4 = QAction("&Forth Menu Action", self)
        action4.triggered.connect(self.Fourth_Ribbon_Menu_Action)

        ExitAction = QAction("&ExitMenu Action", self)
        ExitAction.triggered.connect(self.close) # (qApp.quit)

        FirstMenu = Menu01.addMenu("&First Menu")
        FirstMenu.addAction(action1)
        
        # First Menu에 Second menu를 삽입 + Action 를 삽입
        SecondMenu = Menu01.addMenu("&Second Menu")
        SecondMenu.addAction(action2)

        # First Menu에 Third menu를 삽입 + Action 를 삽입
        ThirdMenu = Menu01.addMenu("&Third Menu")
        ThirdMenu.addAction(action3)
        
        # 메뉴 내에서, 구분바를 설정을 해줌 그리고 마지막 Exit Action을 선언함.
        Menu01.addSeparator()

        # First Menu에 Fourth menu를 삽입 + Action 를 삽입
        FourthMenu = Menu01.addMenu("&Fourth Menu")
        FourthMenu.addAction(action4)
        
        Menu01.addAction(ExitAction)

        action21 = QAction("&칼럼2의 First Menu Action", self)
        action21.triggered.connect(self.Menu21_Action)

        action22 = QAction("&칼럼2의 Second Menu Action", self)
        action22.triggered.connect(self.Menu22_Action)

        menu21 = Menu02.addMenu("&칼럼2의 First Menu")
        menu21.addAction(action21)
        
        menu22 = Menu02.addMenu("&칼럼2의 Second Menu")
        menu22.addAction(action22)
        
        action221 = QAction("&칼럼22의 First Menu Action", self)
        action221.triggered.connect(self.Menu221_Action)
        
        menu221 = menu22.addMenu("&칼럼22의 First Menu")
        menu221.addAction(action221)

        menu21Icon = QAction(QIcon('./icon18.png'), 'Menu21', self)
        menu21Icon.setShortcut('Ctrl+W')
        
        exitAction = QAction(QIcon('./icon25.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close) # (qApp.quit)
        
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)
        
        self.toolbar.addAction(menu21Icon)
        
        self.setWindowTitle ("Ribbon Menu Demonstration")
        self.show ()

    # 각 Action 마다 Message를 띄우면서, Event를 발생 시킴.
    def First_Ribbon_Menu_Action (self):
        reply = QMessageBox.information(self, "Main Ribbon Menu Action","Main Ribbon Menu Action Activated")

    def Second_Ribbon_Menu_Action (self):
        reply = QMessageBox.information(self, "Second Ribbon Menu Action","Second Ribbon Menu Action Activated")

    def Third_Ribbon_Menu_Action (self):
        reply = QMessageBox.information(self, "Third Ribbon Menu Action","Third Ribbon Menu Action Activated")

    def Fourth_Ribbon_Menu_Action (self):
        reply = QMessageBox.information(self, "Fourth Ribbon Menu Action","Fourth Ribbon Menu Action Activated")

    def Menu21_Action (self):
        reply = QMessageBox.information(self, "칼럼2의 First Ribbon Menu Action","칼럼2의 First Ribbon Menu Action Activated")
        
    def Menu22_Action (self):
        reply = QMessageBox.information(self, "칼럼2의 Second Ribbon Menu Action","칼럼2의 Second Ribbon Menu Action Activated")

    def Menu221_Action (self):
        reply = QMessageBox.information(self, "칼럼221의 First Ribbon Menu Action","칼럼221의 First Ribbon Menu Action Activated")
                
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(None) 
    win = Ribbon_Menu()
    sys.exit(app.exec_())
    
#%% Menu Bar 데모(3)
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp, QFileDialog
 
class QtGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(400, 400)
        self.setWindowTitle("Appia")
        menubar = self.menuBar()
        Filemenu = menubar.addMenu("파일")
        Filemenu1 = menubar.addMenu("편집")
        Filemenu2 = menubar.addMenu("서식")
        loadfile = QAction('laod File ...', self)
        savefile = QAction('save File ...', self)
        exit = QAction('Exit',self)
        loadfile.triggered.connect(self.add_open)
        savefile.triggered.connect(self.add_save)
        exit.triggered.connect(qApp.quit)
        Filemenu.addAction(loadfile)
        Filemenu.addAction(savefile)
        Filemenu.addAction(exit)
        self.statusBar().showMessage('이곳은 상태바입니다....준비중')
        self.show()
        
    def add_open(self):
        FileOpen = QFileDialog.getOpenFileName(self, 'Open file', './')
 
    def add_save(self):
        FileSave = QFileDialog.getSaveFileName(self, 'Save file', './')
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = QtGUI()
    app.exec_()
    
#%% 툴바 만들기(1) : QAction /addToolBar /addAction

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp
from PyQt5.QtGui import QIcon

class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        exitAction = QAction(QIcon('exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        self.statusBar()
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)
        self.setWindowTitle('Toolbar')
        self.setGeometry(300, 300, 300, 200)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    
# %% 탭 위젯(1) : QTabWidget, addTab, QVBoxLayout

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        tab1 = QWidget()
        tab2 = QWidget()

        tabs = QTabWidget()
        tabs.addTab(tab1, 'Tab1')
        tabs.addTab(tab2, 'Tab2')

        vbox = QVBoxLayout()
        vbox.addWidget(tabs)

        self.setLayout(vbox)

        self.setWindowTitle('QTabWidget')
        self.setGeometry(300, 300, 300, 200)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())


# %% 탭 위젯(2) : QTabWidget, addTab, setAutoFillBackground, QPalette, QColor

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui  import QColor, QPalette

from PyQt5.QtWidgets import (
    QApplication, 
    QMainWindow,
    QTabWidget,
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

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.West)
        tabs.setMovable(True)

        for n, color in enumerate(["red", "pink", "skyblue", "yellow"]):
            tabs.addTab(Color(color), color)

        self.setCentralWidget(tabs)

app = QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec_()

# %% 탭 위젯(3) (스타일 적용하기)
# QTabWidget, QVBoxLayout, QHBoxLayout, setSpacing, QPalette, setColor, addTab

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtWidgets import *

class QPushButton(QPushButton):     # 파생 클래스 생성
    def __init__(self, parent = None, *args):
        super().__init__(parent, *args)
        self.setSizePolicy(7, 7)
        self.setMinimumHeight(100)
        btnStyle1 = '''                                               
               QPushButton { background-color: #F7F; border-style: outset; border-width: 2px; border-radius: 10px;
                     border-color: beige; font: bold 14px; min-width: 10em; padding: 6px;}
        '''
        btnStyle2 = ("QPushButton {background-color: #1D7EB5; color: white; border-radius: 3; border-color: white}"
              "QPushButton::hover {background-color: #EA90E1; color: #fff;} "#202D4F #EA90E1
              "QPushButton::pressed {background-color: #FF9900;}")    
        self.setStyleSheet(btnStyle1)
        
class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Sidebar layout')
        self.Width = 800
        self.height = int(0.618 * self.Width)
        self.resize(self.Width, self.height)

        # add all widgets
        self.btn_1 = QPushButton('1', self)
        self.btn_2 = QPushButton('2', self)
        self.btn_3 = QPushButton('3', self)
        self.btn_4 = QPushButton('4', self)

        self.btn_1.clicked.connect(self.button1)
        self.btn_2.clicked.connect(self.button2)
        self.btn_3.clicked.connect(self.button3)
        self.btn_4.clicked.connect(self.button4)

        # add tabs
        self.tab1 = self.ui1()
        self.tab2 = self.ui2()
        self.tab3 = self.ui3()
        self.tab4 = self.ui4()
        self.initUI()
    
    def initUI(self):
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.btn_1)
        left_layout.addWidget(self.btn_2)
        left_layout.addWidget(self.btn_3)
        left_layout.addWidget(self.btn_4)
        left_layout.addStretch(5)
        left_layout.setSpacing(20)
        left_widget = QWidget()
        
        # palette = QPalette()
        # palette.setColor(QPalette.Button, QColor(200, 200, 0))
        # palette.setColor(QPalette.ButtonText, Qt.white)
        # palette.setColor(QPalette.Window, QColor(0, 200, 200))
        # palette.setColor(QPalette.WindowText, Qt.white)
        # left_widget.setPalette(palette)
        
        left_widget.setLayout(left_layout)

        self.right_widget = QTabWidget()
        self.right_widget.tabBar().setObjectName("mainTab")

        self.right_widget.addTab(self.tab1, '설정')
        self.right_widget.addTab(self.tab2, '기본값')
        self.right_widget.addTab(self.tab3, '사용자')
        self.right_widget.addTab(self.tab4, '기타')

        self.right_widget.setCurrentIndex(0)
            
        style1 = '''
        QTabWidget::pane { border: 5px solid #CCC; background: #777; padding: 10px; border-top: 1px solid #FF0;}
        QTabBar::tab {width: 150; height: 100; margin: 0; padding: 1; background: #0F8; border-radius: 5; border: 1px solid transparent; }
        '''
        style2 = '''
        QTabWidget::pane { border: 10px solid lightgray; top:-1px; background: rgb(200, 100, 100); } 
        QTabBar::tab { background: rgb(200, 100, 200); border: 1px solid white; padding: 5px; min-width: 100px; min-height: 50px; } 
        QTabBar::tab:selected { background: rgb(100, 200, 200); margin-bottom: -1px; }
        '''
        style3 = '''
        QTabWidget { border: 0; }
        QTabWidget::pane { border: 5px solid #CCC; background: #777; padding: 10px; border-top: 1px solid #FF0;}
        QTabBar::tab { background: rgb(200, 100, 200); color: #0F0; border-radius: 3px; border: 1px solid white; min-width: 80px; }
        QTabBar::tab:top { margin: 30px 1px 0 0; padding: 4px 8px; border-bottom: 3px solid lightgray; } /* margin: 상,우,하,좌 -*/
        QTabBar::tab:selected { color: white; border: 0; } 
        QTabBar::tab:top:hover { border-bottom: 3px solid #444; color: #FF0;}
        QTabBar::tab:top:selected { border-bottom: 3px solid #F00; background: #000;}
        QTabBar::tab:hover, QTabBar::tab:focus { border-bottom: 3px solid #FF0; background: #F00;}
        '''
        self.right_widget.setStyleSheet(style3)
        
        main_layout = QHBoxLayout()
        main_layout.addWidget(left_widget)
        main_layout.addWidget(self.right_widget)
        main_layout.setStretch(0, 40)
        main_layout.setStretch(1, 200)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    # ----------------- buttons
    def button1(self):
        self.right_widget.setCurrentIndex(0)

    def button2(self):
        self.right_widget.setCurrentIndex(1)

    def button3(self):
        self.right_widget.setCurrentIndex(2)

    def button4(self):
        self.right_widget.setCurrentIndex(3)

    # ----------------- # pages
    def ui1(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('page 1'))
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    def ui2(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('page 2'))
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    def ui3(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('page 3'))
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    def ui4(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('page 4'))
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    app.setStyle("Windows")  # ['Windows', 'Fusion', 'Breeze', 'Oxygen', 'QtCurve']
    palette = QPalette()
    palette.setColor(QPalette.Button, QColor(200, 200, 0))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.Window, QColor(0, 150, 200))
    palette.setColor(QPalette.WindowText, Qt.yellow)
    # palette.setColor(QPalette.Base, QColor(0, 200, 200))
    # palette.setColor(QPalette.AlternateBase, QColor(53, 53, 200))
    # palette.setColor(QPalette.ToolTipBase, Qt.white)
    # palette.setColor(QPalette.ToolTipText, Qt.white)
    # palette.setColor(QPalette.Text, Qt.blue)
    # palette.setColor(QPalette.BrightText, Qt.red)
    # palette.setColor(QPalette.Link, QColor(42, 130, 218))
    # palette.setColor(QPalette.Highlight, QColor(0, 200, 0))
    # palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())
