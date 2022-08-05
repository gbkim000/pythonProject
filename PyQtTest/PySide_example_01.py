#%% PySide6 예제(1) - 클래스 생성없이 함수로 구현하기

import os, sys
#import Utilities
 
from PySide6.QtCore import QFileInfo
from PySide6.QtWidgets import QApplication, QWidget, QLabel
# pySide6 설치 폴더 설정하기
pkgDir = 'C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python39\\Lib\\site-packages\\PySide6\\plugins'
# pkgDir = "C:\ProgramData\Miniconda3\envs\spyder-env\Lib\site-packages\PySide6\plugins"
pkgDir = 'C:\ProgramData\Anaconda3\Lib\site-packages\PySide6\plugins'
QApplication.setLibraryPaths([pkgDir])

# from Globals import AppInfo
# from Globals import getPyQt5ModulesDirectory as ModulesDir
# https://vimsky.com/zh-tw/examples/detail/python-ex---Globals-getPyQt5ModulesDirectory-method.html
# import Globals
# def setLibraryPaths():
#     # Module function to set the Qt library paths correctly for windows systems.
#     if Globals.isWindowsPlatform():
#         libPath = os.path.join(Globals.getPyQt5ModulesDirectory(), "plugins")
#         if os.path.exists(libPath):
#             libPath = QDir.fromNativeSeparators(libPath)
#             libraryPaths = QApplication.libraryPaths()
#             if libPath not in libraryPaths:
#                 libraryPaths.insert(0, libPath)
#                 QApplication.setLibraryPaths(libraryPaths)
#     print(libraryPaths) 
                          
def window():

    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()  

    win = QWidget()
    lbl = QLabel("Hello ~~", win)
    lbl.setText("Hello World!!")
    lbl.move(50,20)    
    win.setGeometry(200,100,200,50)
    win.setWindowTitle("PyQt")
    win.show()
    print(QFileInfo("./PySide_example_01.py").path())             # .
    print(QFileInfo("./PySide_example_01.py").absolutePath())     # C:/Users/Administrator/Spyder
    print(QFileInfo("./PySide_example_01.py").absoluteFilePath()) # C:/Users/Administrator/Spyder/classTest01.py
    sys.exit(app.exec())
    
if __name__ == '__main__':
    #setLibraryPaths()
    window()

#%% PySide6 예제(2) - QPushButton, SIGNAL

import sys
from PySide6.QtCore import *
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QDialog, QPushButton

# pySide6 설치 폴더 설정하기
pkgDir = 'C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python39\\Lib\\site-packages\\PySide6\\plugins'
# pkgDir = "C:\ProgramData\Miniconda3\envs\spyder-env\Lib\site-packages\PySide6\plugins"
# pkgDir = 'C:\ProgramData\Anaconda3\Lib\site-packages\PySide6\plugins'
QApplication.setLibraryPaths([pkgDir])

def window():
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
        
    win = QDialog()
    b1= QPushButton(win)
    b1.setText("Button1")
    b1.move(50,20)
    b1.clicked.connect(b1_clicked)
    
    b2=QPushButton(win)
    b2.setText("Button2")
    b2.move(50,50)
    #b2.clicked.connect(b2_clicked)
    QObject.connect(b2,SIGNAL("clicked()"),b2_clicked)
    win.setGeometry(100,100,200,100)
    win.setWindowTitle("PyQt")
    win.show()
    sys.exit(app.exec())
    
def b1_clicked():
    print("Button 1 clicked")
    
def b2_clicked():
    print("Button 2 clicked")
    
if __name__ == '__main__':
    window()

#%% PySide6 예제(3) : QSizePolicy /QSize /getattr /QMenu /QActionGroup /addAction

import os, sys
from PySide6.QtWidgets import QApplication, QWidget, QSizePolicy, QHBoxLayout, QMenu
from PySide6.QtCore import *
from PySide6.QtGui import *

# 위 문장은 import PySide6.QtCore, PySide6.QtGui와 같으나, 
# PySide6.QtCore.QtSize()와 같은 형식으로 메소드에 접근해야 함.

# pySide6 설치 폴더 설정하기
pkgDir = 'C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python39\\Lib\\site-packages\\PySide6\\plugins'
# pkgDir = "C:\\ProgramData\\Miniconda3\\envs\\spyder-en\v\Lib\\site-packages\\PySide6\\plugins"
#pkgDir = 'C:\ProgramData\Anaconda3\Lib\site-packages\PySide6\plugins'
QApplication.setLibraryPaths([pkgDir])

policyNames = ['Fixed', 'Minimum', 'Maximum', 'Preferred', 'Expanding']
policyNameDict = {}
policyValueDict = {}

for name in policyNames:
    policy = getattr(QSizePolicy, name)
    policyNameDict[policy] = name
    policyValueDict[name] = policy

class TestWidget(QWidget):
    
    def sizeHint(self):
        return QSize(150, 30)

    def minimumSizeHint(self):
        return QSize(10, 10)

    def contextMenuEvent(self, event):
        currentPolicy = self.sizePolicy()
        menu = QMenu()
        group = QActionGroup(menu, exclusive=True)
        for name in policyNames:
            action = group.addAction(name)
            action.setCheckable(True)
            policy = policyValueDict[name]
            action.setData(policy)
            if policy == currentPolicy.horizontalPolicy():
                action.setChecked(True)
                
        menu.addActions(group.actions())
        res = menu.exec_(event.globalPos())
        if res:
            # PySide requires reconversion of the data, on PyQt the
            # res.data() alone is enough;
            currentPolicy.setHorizontalPolicy(
                QSizePolicy.Policy(res.data()))
            self.setSizePolicy(currentPolicy)
            self.update()

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.drawRect(self.rect().adjusted(0, 0, -1, -1))
        text = '{policy}\n{width}x{height}'.format(
            policy=policyNameDict[self.sizePolicy().horizontalPolicy()], 
            width=self.sizeHint().width(), 
            height=self.sizeHint().height(), 
        )
        qp.drawText(self.rect(), Qt.AlignCenter, text)

if __name__ == '__main__':
    
    if not QApplication.instance():
        app = QApplication([])
    else:
        app = QApplication.instance()   
    
    window = QWidget()
    layout = QHBoxLayout(window)
    for i in range(3):
        layout.addWidget(TestWidget())
    window.show()
    sys.exit(app.exec())

#%% PySide6 창 가운데 정렬하기

import sys
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

pkgDir = 'C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python39\\Lib\\site-packages\\PySide6\\plugins'
# pkgDir = "C:\ProgramData\Miniconda3\envs\spyder-env\Lib\site-packages\PySide6\plugins"
# pkgDir = 'C:\ProgramData\Anaconda3\Lib\site-packages\PySide6\plugins'
QApplication.setLibraryPaths([pkgDir])

class MyWidget( QWidget):
    def __init__(self):
        super( MyWidget, self).__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setGeometry( 100, 50, 300, 200)
        self.setWindowTitle("SvrCheck PySide")
        self.setWindowIcon(  QIcon( 'main.png' ))
        self.setToolTip(' This is a <b>QWidget</b> widget')
        
        #배경화면 칠하기 1
        palette = QPalette()
        palette.setColor( QPalette.Window , QColor(144, 112, 144))
        self.setAutoFillBackground( True)
        self.setPalette(palette)
        self.center()

        testBtn = QPushButton( 'TestButton', self)
        testBtn.setToolTip(' This is a <b>QPushButton</b> widget')
        testBtn.resize( testBtn.sizeHint())
        testBtn.move(20,0)

        quitBtn = QPushButton( "Quit", self )
        quitBtn.resize(quitBtn.sizeHint())
        quitBtn.clicked.connect(QCoreApplication.instance().quit)
        quitBtn.setStyleSheet("QWidget { background-color: %s }" %  "yellow")
        quitBtn.move(100, 0)      
       
        self.show()
    def closeEvent(self, event):
        ' 상단의 x버튼을 누르면 자동으로  QCloseEvent 발생.'
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):       
        qr = self.frameGeometry()
        cp = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
              

def main():
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()  
    win = MyWidget()
    sys.exit( app.exec_())

if __name__ == '__main__':
    main()
