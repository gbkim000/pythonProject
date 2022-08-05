import sys, os, subprocess
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, 
                             QToolBar, QMenuBar, QAction, QFileDialog)
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap

qss = """
QMenuBar{
    background-color: #A0B4E6;
    padding: 1px; 
}
QMenuBar::item {
    spacing: 3px;           
    padding: 2px 10px;
    margin: 1px;
    background-color: #3057B9; /*rgb(210,105,230); */
    color: rgb(255,255,255);  
    border-radius: 2px;
}
QMenuBar::item:selected {    
    background-color: #F4A460; /* rgb(244,164,96); #F4A460 #E080E0*/
}
QMenuBar::item:pressed {
    background: rgb(230,100,100);
}
/* +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */  
QMenu {
    background-color: #DBDBFB; /* white;    */
    border: 1px solid black;
    margin: 2px;
}
QMenu::item {
    background-color: transparent;
}
QMenu::item:selected { 
    background-color: #6540F0; /*#654321; */
    color: rgb(255,255,255);
}
QStatusBar{
    background-color: #A0B4E6;  
    border-style: solid; border-color: white; 
    padding: 3px; border-width: 1px;
}
"""

pixSeq = 0
class Window(QMainWindow):
    def __init__(self):
        #super().__init__()
        super(Window, self).__init__()        
        self.resize(640, 480)
        self.setWindowTitle("영문장 암기 학습 프로그램 - programmed by G.B.Kim")
        self.curDir = os.getcwd()
        self.curDir = self.curDir.replace('\\', '/')
        self.imgDir = self.curDir + "/images_btn/"
        self.toolBarMenu()
        self.Ui()
        
    def Ui(self):
        global pixSeq
        self.label = QLabel(self)
        self.pixList = ["img1.png", "img2.png"]
        self.label.setPixmap(QPixmap(self.imgDir + self.pixList[pixSeq]))
        self.label.setScaledContents(True)
        self.setCentralWidget(self.label)
        self.label.setStyleSheet("margin-right: 3px;")
        self.label.mousePressEvent = self.photo_toggle
        self.statusBar().showMessage(f'현재 폴더 : [ {self.curDir} ]')        
        self.show()
        
    def photo_toggle(self, event):
        global pixSeq
        pixSeq += 1
        pixSeq %= 2
        self.label.setPixmap(QPixmap(self.imgDir + self.pixList[pixSeq]))
        self.Ui()
        
    def toolBarMenu(self):

        # ----- menuBar 설정하기 --------------------------------------------        
        menubar = self.menuBar()
        Menu1 = menubar.addMenu("환경설정")
        Menu2 = menubar.addMenu("영문장암기")
        Menu3 = menubar.addMenu("PyQt 예제...")        

        # [menu1 list]
        menu11 = QAction('DB파일 폴더 지정...', self)
        menu12 = QAction('DB파일 생성하기...', self)
        menu13 = QAction(QIcon('exit.png'), '&Exit', self)
        
        menu11.triggered.connect(self.add_menu11)
        menu12.triggered.connect(self.add_menu12)
        menu13.triggered.connect(self.exitMenu)
        
        menu11.setStatusTip('영문장을 저장한 DB파일을 선택합니다.')
        menu12.setStatusTip('DB파일을 생성후 초기화합니다.)')
        menu13.setStatusTip('Exit application')

        Menu1.addAction(menu11)
        Menu1.addAction(menu12)
        Menu1.addSeparator()
        Menu1.addAction(menu13)
        
        menu21 = QAction('영문장 암기하기', self)
        menu22 = QAction('영문장 등록하기', self)
        menu21.setShortcut('Ctrl+W')
        
        menu21.triggered.connect(self.add_menu21)
        menu22.triggered.connect(self.add_menu22)
  
        menu21.setStatusTip('DB에 저장된 영문장을 불러와서 화면에 보여줍니다.')
        menu22.setStatusTip('엑셀에 저장된 영문장을 가져와서 DB파일에 등록(저장)합니다.')
                               
        Menu2.addAction(menu21)
        Menu2.addAction(menu22)
        
        menu31 = QAction('윈도 출력하기...', self)
        menu32 = QAction('테이블 처리하기...', self)
        menu33 = QAction('데이터베이스 관리하기...', self)

        menu31.triggered.connect(self.add_menu31)
        menu32.triggered.connect(self.add_menu12)
        menu33.triggered.connect(self.add_menu13)

        Menu3.addAction(menu31)
        Menu3.addSeparator() 
        Menu3.addAction(menu32)
        Menu3.addAction(menu33)
        
        # ----- toolBar 설정하기 --------------------------------------------
        toolBtn1 = QAction(QIcon(self.imgDir + "toolBtn1.png"), 'This is your button1', self)
        toolBtn1.setStatusTip("This is your button1")
        toolBtn1.setShortcut('Ctrl+Q')

        toolBtn2 = QAction(QIcon(self.imgDir + "toolBtn2.png"), 'This is your button2', self)
        toolBtn2.setStatusTip("This is your button2")
        
        toolBtn3 = QAction(QIcon(self.imgDir + "toolBtn3.png"), 'This is your button3', self)
        toolBtn3.setStatusTip("This is your button3")

        toolBtn3 = QAction(QIcon(self.imgDir + "toolBtn3.png"), 'This is your button3', self)
        toolBtn3.setStatusTip("This is your button3")
        
        toolBtn4 = QAction(QIcon(self.imgDir + "toolBtn3.png"), 'Exit application', self)
        toolBtn4.setStatusTip("This is exit button")
        
        toolBtn1.triggered.connect(self.add_menu21)
        toolBtn2.triggered.connect(self.add_menu22)
        toolBtn4.triggered.connect(self.exitMenu)
        
        self.toolBar = QToolBar()
        self.toolBar.setIconSize(QSize(32,32))
        self.addToolBar(Qt.LeftToolBarArea, self.toolBar)
        
        self.toolBar.addAction(toolBtn1)
        self.toolBar.addAction(toolBtn2)
        self.toolBar.addSeparator()
        self.toolBar.addSeparator()
        self.toolBar.addAction(toolBtn3) 
        self.toolBar.addAction(toolBtn4)
        self.show()
        
    def add_menu11(self):
        FileOpen = QFileDialog.getOpenFileName(self, 'Open file', './')

    def add_menu12(self):
        FileSave = QFileDialog.getSaveFileName(self, 'Save file', './')

    def add_menu13(self):
        print("Selected 'edit file menu...'")

    def add_menu21(self):
        self.hide()
        os.system("python subMenu21.py")
        # os.system("start /d C:\\Users\\Administrator\\PyQtTest\\Memorizing /min Python.exe subMenu21.py")
        # subprocess.call("subMenu21.py", shell=True)        
        self.show()     

    def add_menu22(self):
        self.hide()
        os.system("python subMenu22.py")
        self.show() 

    def add_menu31(self):
        self.hide()
        os.system("python subMenu31.py")
        self.show() 
        
    def exitMenu(self):
        # print("Bye ~ ")
        # QApplication.instance().quit()
        self.close()
        QApplication.instance().quit()

    # ----- 창 닫기 버는 클릭 -----------------------------------------------           
    # def closeEvent(self, event):
        
    #     event.ignore()  # event.accept()
        
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     app.setStyleSheet(qss)  
#     ex = Window()
#     sys.exit(app.exec())

        
# ----- 메인함수 ------------------------------------------------------------ 
def main():
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()  
    app.setStyleSheet(qss)  
    Win = Window()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

