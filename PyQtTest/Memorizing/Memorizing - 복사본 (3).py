''' <Memorizing.py>
(1) 실행파일 만들기 : pyinstaller -w -F Memorizing.py
(2) 실행파일 만들기(upx-win64로 용량 줄이기) : pyinstaller --upx-dir ./upxwin64 -w -F Memorizing.py

(3) [get-pip.py 다운로드] : curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
(4) [pip install] : python get-pip.py
(5) [Upgrading pip] : python -m pip install --upgrade pip
(6) [Updating spyder] : pip install -U spyder
(7) [Reset preferences] : spyder --reset
'''
import sys, os, getpass, sqlite3, openpyxl, re, random
from PyQt5.QtGui import QFont, QColor, QIcon, QPixmap
from PyQt5.QtCore import pyqtSignal, Qt, QSize, QThread, pyqtSlot, QObject
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QTableWidget,
           QGroupBox, QCheckBox, QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit, QProgressBar,
           QListView, QComboBox, QHeaderView, QAbstractItemView, QDesktopWidget, QAction, QToolBar,
           QMessageBox, QTableWidgetItem, QFileDialog, QDialog, QTextEdit, QInputDialog)
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

qss = """
/* +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */  
QMenuBar{
    background-color: #A0B4E6;
    padding: 1px; 
}
QMenuBar::item {        
    padding: 2px 10px; /* 상하 좌우 */
    margin: 1px;
    background-color: #3057B9; /* #3057B9(군청색); #D269E6(보라); */
    color: rgb(255,255,255);  
    border-radius: 2px;
}
QMenuBar::item:selected {    
    background-color: #F4A460; /* rgb(244,164,96)-#F4A460(갈색);  #E080E0(보라)*/
}
QMenuBar::item:pressed {
    background: rgb(230,100,100); /*  rgb(230,100,100)-#E66464(립스틱색); */
}
/* +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */  
QMenu {
    background-color: #DBDBFB; /* #DBDBFB(연보라);    */
    border: 1px solid black;
    margin: 2px;
}
QMenu::item {
    background-color: transparent; /* transparent; */
}
QMenu::item:selected { 
    background-color: #6540F0; /* #6540F0(청보라); #654321(고동색); */
    color: rgb(255,255,255);
}
QStatusBar{
    background-color: #A0B4E6;  
    border-style: solid; border-color: white; 
    padding: 3px; border-width: 1px;
}
/* +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ */  
"""

pixSeq = 0
progRatio = 0

class MainWindow(QMainWindow):
    def __init__(self):
        global pixSeq
        #super().__init__()
        super(MainWindow, self).__init__()        
        self.resize(640, 480)
        self.setWindowTitle("영문장 암기 학습 프로그램 - programmed by G.B.Kim")
        self.curDir = os.getcwd()
        self.curDir = self.curDir.replace('\\', '/')
        self.imgDir = self.curDir + "/images_btn/"
        self.pixList = []
        
        if os.path.exists(self.imgDir):
            fileLists = os.listdir(self.imgDir)
            for file in fileLists:
                if re.match('img[0-9]+.png', file) != None:
                   self.pixList.append(file) # ["img1.png", "img2.png"]
        self.imgCnt = len(self.pixList)
        if self.imgCnt > 0:
            pixSeq = random.randint(0, self.imgCnt - 1)
        
        self.label = QLabel(self)
        self.label.setScaledContents(True)
        self.label.setStyleSheet("margin-right: 3px;")
        self.label.mousePressEvent = self.imgSwitch
        self.setCentralWidget(self.label)
        self.toolBarMenu()
        self.imgShow()
        self.show()
        
    def imgShow(self):
        global pixSeq
        if self.imgCnt > 0:
            self.label.setPixmap(QPixmap(self.imgDir + self.pixList[pixSeq]))
        self.statusBar().showMessage(f'현재 폴더 : [ {self.curDir} ]')        

    def imgSwitch(self, event):
        global pixSeq
        if self.imgCnt == 0:
            return
        pixSeq = random.randint(0, self.imgCnt - 1)
        self.imgShow()
        
    def toolBarMenu(self):
        # ----- menuBar 설정하기 ---------------------------------------------        
        menubar = self.menuBar()
        QMenu1 = menubar.addMenu("환경설정")
        QMenu2 = menubar.addMenu("영문장암기")
        QMenu3 = menubar.addMenu("PyQt 예제...")        

        # [QMenu 1 list] -----------------------------------------------------
        menu11 = QAction('DB파일 폴더 지정...', self)
        menu12 = QAction('DB파일 생성하기...', self)
        menu13 = QAction(QIcon(self.imgDir + 'exit.png'), '&Exit', self)

        menu11.triggered.connect(self.call_menu11)
        menu12.triggered.connect(self.call_menu12)
        menu13.triggered.connect(self.call_exitMenu)
        
        menu11.setStatusTip('영문장을 저장한 DB파일을 선택합니다.')
        menu12.setStatusTip('DB파일을 생성후 초기화합니다.)')
        menu13.setStatusTip('Exit application')

        QMenu1.addAction(menu11)
        QMenu1.addAction(menu12)
        QMenu1.addSeparator()
        QMenu1.addAction(menu13)
        
        # [QMenu 2 list] -----------------------------------------------------
        menu21 = QAction(QIcon(self.imgDir + 'icon11.png'), '영문장 암기하기', self)
        menu22 = QAction(QIcon(self.imgDir + 'icon16.png'), '영문장 등록하기', self)
        menu21.setShortcut('Ctrl+W')
        
        menu21.triggered.connect(self.call_menu21)
        menu22.triggered.connect(self.call_menu22)
  
        menu21.setStatusTip('DB에 저장된 영문장을 불러와서 화면에 보여줍니다.')
        menu22.setStatusTip('엑셀에 저장된 영문장을 가져와서 DB파일에 등록(저장)합니다.')
                               
        QMenu2.addAction(menu21)
        QMenu2.addAction(menu22)

        # [QMenu 3 list] -----------------------------------------------------        
        menu31 = QAction('윈도 출력하기...', self)
        menu32 = QAction('테이블 처리하기...', self)
        menu33 = QAction('데이터베이스 관리하기...', self)

        menu31.triggered.connect(self.call_menu31)
        menu32.triggered.connect(self.call_menu12)
        menu33.triggered.connect(self.call_menu13)

        QMenu3.addAction(menu31)
        QMenu3.addSeparator() 
        QMenu3.addAction(menu32)
        QMenu3.addAction(menu33)
        
        # ----- toolBar 설정하기 --------------------------------------------
        toolBtn1 = QAction(QIcon(self.imgDir + "icon11.png"), 'Load excelFile and Save DB file', self)
        toolBtn1.setStatusTip("Load excelFile and Save DB file")
        toolBtn1.setShortcut('Ctrl+Q')

        toolBtn2 = QAction(QIcon(self.imgDir + "icon16.png"), 'Memorizing English Sentances', self)
        toolBtn2.setStatusTip("Memorizing English Sentances")
        
        toolBtn3 = QAction(QIcon(self.imgDir + "icon13.png"), 'This is your button3', self)
        toolBtn3.setStatusTip("This is your button3")

        toolBtn4 = QAction(QIcon(self.imgDir + "icon18.png"), 'This is your button4', self)
        toolBtn4.setStatusTip("This is your button3")
        
        toolBtn5 = QAction(QIcon(self.imgDir + "exit.png"), 'Exit program button5', self)
        toolBtn5.setStatusTip("This is exit button")
        
        toolBtn1.triggered.connect(self.call_menu21)
        toolBtn2.triggered.connect(self.call_menu22)
        toolBtn5.triggered.connect(self.call_exitMenu)
        
        self.toolBar = QToolBar()
        self.toolBar.setIconSize(QSize(32,32))
        self.addToolBar(Qt.LeftToolBarArea, self.toolBar)
        
        self.toolBar.addAction(toolBtn1)
        self.toolBar.addAction(toolBtn2)
        self.toolBar.addSeparator()
        self.toolBar.addSeparator()
        self.toolBar.addAction(toolBtn3) 
        self.toolBar.addAction(toolBtn4)
        self.toolBar.addAction(toolBtn5)
        self.show()
        
    def call_menu11(self):
        pass

    def call_menu12(self):
        pass

    def call_menu13(self):
        print("Selected 'edit file menu...'")

    def call_menu21(self):
        self.hide() 
        self.app21 = App21(self)
        self.app21.show()        
        # self.showMinimized()        
        # os.system("python subMenu21.py")
        # os.system("start /d C:\\Users\\Administrator\\PyQtTest\\Memorizing /min Python.exe subMenu21.py")
        # subprocess.call("subMenu21.py", shell=True)    

    def call_menu22(self):
        self.hide() 
        self.app22 = App22(self)
        self.app22.show()
        
    def call_menu31(self):
        self.hide()
        os.system("python subQMenu31.py")
        self.show() 
        
    def call_exitMenu(self):
        self.close()
        QApplication.instance().quit()

class QPushButton(QPushButton):     # 버튼 클래스 재정의
    def __init__(self, parent = None, *args):
        super().__init__(parent, *args)
        self.setSizePolicy(7, 7)     # (w:QSizePolicy.Expanding, w:QSizePolicy.Expanding)
        self.setMinimumHeight(30)
        self.setMaximumHeight(50)
        self.setMinimumWidth(100) 
        self.setFont(QFont('맑은 고딕', 12))
        style = ("QPushButton{background-color: rgb(0, 50, 200); color: white; "
                     "border-style: solid; border-radius: 5; font: bold; "
                     "padding: 3px; padding-left: 5px; padding-right: 5px;"
                     "border-color: rgb(255,255,255); border-width: 2px;}"
                 "QPushButton::hover {background-color: #FF9930; color: #fff;} "
                 "QPushButton::pressed {background-color: #142090;}")
        self.setStyleSheet(style)
        
class QPushButton2(QPushButton):     # 파생 클래스 생성
    def __init__(self, parent = None, *args):
        super().__init__(parent, *args)
        self.setSizePolicy(7, 7)
        self.setMinimumHeight(35)
        self.setMaximumHeight(50)        
        self.setMinimumWidth(180)
        self.setMaximumWidth(180)        
        font = QFont()
        font.setFamily('맑은 고딕')
        font.setPointSize(12)
        self.setFont(font)
        style = ("QPushButton {background-color: #1D7EB5; color: white; border-radius: 3; border-color: white}"
                 "QPushButton::hover {background-color: #EA90E1; color: #fff;} "#202D4F #EA90E1
                 "QPushButton::pressed {background-color: #FF9900;}")    
        self.setStyleSheet(style)
                
class QGroupBox(QGroupBox):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setSizePolicy(7,7)
        gboxStyle = ("background-color: #DDEBF7; " #D3D3D3; " 
                     "border-style: solid; border-radius: 3;"
                     "padding: 3px; padding-left: 10px; padding-right: 10px;"
                     "border-color: rgb(200,200,200); border-width: 1px;")        
        self.setStyleSheet(gboxStyle)

class QLabel(QLabel):     # 클래스 재정의
    def __init__(self, parent = None):
        super().__init__(parent)
        lblStyle = ("background-color: #A0B4E6; " #C0CDEF;" 
                    "border-style: solid; border-radius: 3; border-color: white; "
                    "padding: 3px; padding-left: 10px; padding-right: 10px; border-width: 1px;")        
        self.setStyleSheet(lblStyle)
        
class QCheckBox(QCheckBox):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setSizePolicy(7,7)
        self.setFont(QFont('Times', 10))

class DbException(Exception):    # Exception만 상속받고 구현없음
    pass

class QTableWidget(QTableWidget):  

    cell_EditingStarted = pyqtSignal(int, int)      # 시그널 생성
    
    # edit 메서드 재정의
    def edit(self, index, trigger, event):
        result = super(QTableWidget, self).edit(index, trigger, event)
        if result:
            self.cell_EditingStarted.emit(index.row(), index.column())  # 셀 편집 시작시 시그널 방출
        return result

def getLastFilePath():
    
    fileName = ''
    userAcount = getpass.getuser()
    path1 = 'C:\\Users\\{0}\\Documents\\'.format(userAcount)        # 일반 사용자 내문서 폴더
    path2 = 'C:\\Users\\{0}\\Documents\\'.format('Administrator')   # 관리자 계정 내문서 폴더
    
    pathFile = "C:\\path.txt"
    if os.path.isdir(path1):
        pathFile = path1 + "path.txt"
    elif os.path.isdir(path2):
        pathFile = path2 + "path.txt"

    if os.path.exists(pathFile):       # 이전에 접근한 db파일의 경로가 있으면
        with open(pathFile, 'r', encoding='utf-8') as f:
            fileName = f.readline().strip()

    return (fileName, pathFile)

def getDbFileName(temp):
    
    dbFileName = ''
    dirName, fileName = os.path.split(temp)
    if dirName =='' or fileName =='':
        return ''
    i = 0
    while not dirName[i].isalpha():
        i += 1
    dirName = dirName[i:]    # 시작문자열에 숨김문자/특수문자 있으면 제거. 

    dbFileName = '{0}\\{1}'.format(dirName, fileName)
    os.chdir(dirName)
    
    return dbFileName

def updateComboList(self):
    
    tableName = ''
    self.combo.clear()        
    self.view.setRowCount(0)        # self.view.clearContents()

    if not os.path.exists(self.dbFileName):
        return ''
    
    conn = sqlite3.connect(self.dbFileName)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    
    tbnList = cursor.fetchall() # [('DATA_2019_01',), ('DATA_2019_02',), ('DATA_2019_03',)]
    if not bool(tbnList):
        QMessageBox.information(self, "DB 테이블 목록 갱신 오류!", "DB 파일에 테이블이 존재하지 않습니다.")
        conn.close()
        return ''
    
    tbName = tbnList[0][0]      # 첫번째 테이블명을 가져옴
    cursor.execute("PRAGMA table_info(" + tbName + ")" )
    records = cursor.fetchall()
    # records : [(0, 'YMD', 'CHAR(8)', 0, None, 1), (1, 'seq', 'INTEGER', 0, None, 2), (2, 'korean', ...
    conn.close()
    
    errFlag = False
    fieldName = ['YMD', 'seq', 'korean', 'english', 'done', 'point']
    
    if len(records[0]) != len(fieldName):
        errFlag= True
    else:
        for id, row in enumerate(records):
            if fieldName[id] != row[1]:  # records의 두번째(row[1]) 요소가 필드명임
                errFlag = True
    if errFlag:
        QMessageBox.critical(self, "DB file error!", "테이블의 필드명이 일치하지 않습니다. DB파일을 올바르게 지정하세요.")
        return ''

    self.combo.blockSignals(True)
    self.combo.clear()
    for row in tbnList:
        self.combo.addItem(row[0])
    self.combo.blockSignals(False)
    
    self.combo.setCurrentIndex(len(tbnList)-1)
    tableName = self.combo.currentText()
    
    return tableName

# ----- DB읽기(방식1) : QSqlQuery() 함수 사용 --------------------------------
def dispData(self):

    try:
        if not os.path.exists(self.dbFileName):  # if not QFile.exists(self.dbFileName):
            raise DbException('데이터베이스 파일이 존재하지 않습니다.')
            
        if self.tableName == '':
            return
        
        conn = QSqlDatabase.addDatabase("QSQLITE")
        conn.setDatabaseName(self.dbFileName)
        conn.open()
        
        query = QSqlQuery()
        sql = 'SELECT * FROM ' + self.tableName

        if not query.exec(sql):
            raise DbException('테이블이 존재하지 않습니다.')
        cols = query.record().count()
        
        rows = 0
        query.exec("SELECT COUNT(*) FROM " + self.tableName)
        if query.first():
            rows = query.value(0)
        
        query.exec(sql)
        
        self.bookMark.clear()
        self.view.blockSignals(True)    # 이벤트 감시 중지
        self.view.setRowCount(rows)
        
        row = 0
        while query.next():
            itm1 = QTableWidgetItem(str(query.value(1)))
            itm2 = QTableWidgetItem(query.value(2))
            itm3 = QTableWidgetItem(query.value(3))
            
            itm4 = query.value(4)
            itm5 = query.value(5)
            if itm4 == '9' or itm5 == '9':
                if not (row in self.bookMark):
                    self.bookMark.append(row)
            itm4 = QTableWidgetItem(itm4)
            itm5 = QTableWidgetItem(itm5)
            
            itm1.setFlags(itm1.flags() & ~Qt.ItemIsEditable)    # 해당 비트 클리어
            itm1.setBackground(QColor(200, 100, 100))
            itm1.setTextAlignment(Qt.AlignCenter)
            itm4.setTextAlignment(Qt.AlignCenter)
            itm5.setTextAlignment(Qt.AlignCenter)

            if ('check1' in dir(self)) and not self.check1.isChecked():
                itm2.setForeground(QColor("#c4c4c4")) # 또는 QColor('gray')
                itm2.setBackground(QColor("#c4c4c4"))
                    
            if ('check2' in dir(self)) and not self.check2.isChecked():
                itm3.setForeground(QColor("#c4c4c4")) 
                itm3.setBackground(QColor("#c4c4c4"))

            self.view.setItem(row, 0, itm1)
            self.view.setItem(row, 1, itm2)
            self.view.setItem(row, 2, itm3)
            self.view.setItem(row, 3, itm4)
            self.view.setItem(row, 4, itm5)
            row += 1
            
        self.view.blockSignals(False)   # 이벤트 감시 재개
        self.view.setAlternatingRowColors(True)
        self.refreshWidth(None)
        self.view.show()
        
    except Exception as err: 
        QMessageBox.critical(self, "DB file open Error!", "%s" % err)
        
    finally:
        if 'conn' in locals():  # DB 연결을 성공했으면 conn변수가 존재함
            conn.close()

# ----- DB읽기(방식2) : Sqlite3 전용 함수 ------------------------------------
def dispData2(self):

    try:
        if not os.path.exists(self.dbFileName):  # if not QFile.exists(self.dbFileName):
            raise DbException('데이터베이스 파일이 존재하지 않습니다.')
            
        if self.tableName == '':
            return
        
        conn = sqlite3.connect(self.dbFileName)
        cursor = conn.cursor()

        sql = 'SELECT * FROM ' + self.tableName
        cursor.execute(sql)
        
        rowList = cursor.fetchall()
        rows = len(rowList)

        if rows<1:
            self.view.setRowCount(0)    #self.view.clearContents()
            return
          
        self.bookMark.clear()
        self.view.blockSignals(True)    # 이벤트 감시 중지
        self.view.setRowCount(rows)
        
        for row in range(rows):
            itm1 = QTableWidgetItem(str(rowList[row][1]))
            itm2 = QTableWidgetItem(rowList[row][2])
            itm3 = QTableWidgetItem(rowList[row][3])
            itm4 = rowList[row][4]
            itm5 = rowList[row][5]
            
            if itm4 == '9' or itm5 == '9':
                if not (row in self.bookMark):
                    self.bookMark.append(row)
            itm4 = QTableWidgetItem(itm4)
            itm5 = QTableWidgetItem(itm5)
 
            itm1.setFlags(itm1.flags() & ~Qt.ItemIsEditable)
            itm1.setBackground(QColor(200, 100, 100))
            itm1.setTextAlignment(Qt.AlignCenter)
            itm4.setTextAlignment(Qt.AlignCenter)
            itm5.setTextAlignment(Qt.AlignCenter)

            if ('check1' in dir(self)) and not self.check1.isChecked():
                itm2.setForeground(QColor("#c4c4c4")) # 또는 QColor('gray')
                itm2.setBackground(QColor("#c4c4c4"))
                    
            if ('check2' in dir(self)) and not self.check2.isChecked():
                itm3.setForeground(QColor("#c4c4c4")) 
                itm3.setBackground(QColor("#c4c4c4"))

            self.view.setItem(row, 0, itm1)
            self.view.setItem(row, 1, itm2)
            self.view.setItem(row, 2, itm3)
            self.view.setItem(row, 3, itm4)
            self.view.setItem(row, 4, itm5)
            
        self.view.blockSignals(False)   # 이벤트 감시 재개
        self.view.setAlternatingRowColors(True)
        self.refreshWidth(None)   
        self.view.show()
        
    except Exception as err: 
        QMessageBox.critical(None, "DB file open Error!", "%s" % err)
        
    finally:
        if 'conn' in locals():  # DB 연결을 성공했으면 conn변수가 존재함
            conn.close()
 
# ----- 키 이벤트(keyPressed) 처리 ------------------------------------------       
def keyPressed(self, e, row, col, rowCnt):
    
    if e.modifiers() & Qt.ControlModifier:  # print("Ctrl")      
        if row > 0:
            self.view.setCurrentCell(row-1, col)
            tableScroll(self, row, col)
            
    elif e.modifiers() & Qt.ShiftModifier:  # print('Shift')
        if row < rowCnt-1:
            self.view.setCurrentCell(row+1, col)   
            tableScroll(self, row, col)
    
    elif e.key() == Qt.Key_F2:
        self.view.editItem(self.view.currentItem())

    elif e.key() == Qt.Key_Escape:
        if len(self.bookMark) > 0:
            rowPosi = self.bookMark[self.bookCnt]
            self.view.setCurrentCell(rowPosi, 2)
            self.bookCnt += 1
            self.bookCnt %= len(self.bookMark)
            
    elif e.key() == Qt.Key_F1:
        win = QDialog(self)
        win.setWindowTitle("도움말 보기")
        win.resize(500, 400)
        xPos = self.pos().x()
        yPos = self.pos().y()
        w = int((self.width()  - win.size().width())/2)  + xPos
        h = int((self.height() - win.size().height())/2) + yPos
        win.move(w, h)
        
        btn = QPushButton("닫기", win)
        btn.clicked.connect(lambda : win.close())
        btn.move(380, 20)

        tBrowser = QTextEdit(win)
        tBrowser.resize(win.width() - 40, win.height() - 100)
        tBrowser.move(tBrowser.pos().x() + 20, tBrowser.pos().y() + 75)

        style=("color: blue;"
                "background-color: lightgray;"
                "font: bold 20px; line-height: 150%;"
                "qproperty-alignment: 'AlignVCenter | AlignLeft';"
                "text-align: center;"
                "padding-left:20px; padding-top:20px;"
                "padding-right:20px; padding-bottom:20px;")
        
        text =("<H1 text-align:center> 도움말 보기 화면</H1>\
                <ul><li> 화면 위로 스크롤하기 : &lt;Ctrl&gt;</li>\
                    <li> 화면 아래 스크롤하기 : &lt;Shift&gt;</li>\
                    <li> 북마크 표시로 이동하기 : &lt;Esc&gt;</li>\
                    <li> 북마크 표시 :[암기/중요]필드에 '9';</li>\
                    <li> 문장 수정하기 : &lt;F2&gt;</li>\
                    <li> 테이블 다시 그리기 : &lt;더블클릭&gt;</li>\
                    <li> 도움말 보기 : &lt;F1&gt;</li></ul>")
        tBrowser.append(text)
        tBrowser.setStyleSheet(style)
        tBrowser.setAcceptRichText(True)        # 서식있는 문자 허용
        win.show()

def tableScroll(self, row, col):
    rowIndex = self.view.currentIndex().row()
    item = self.view.item(rowIndex, col)
    self.view.scrollToItem(item, QAbstractItemView.PositionAtCenter) 
    
    # self.view.scrollToItem(item, QAbstractItemView.PositionAtTop) 
    # index = self.view.model().index(row, col)
    # self.view.scrollTo(index)
    # curr_pos = self.view.verticalScrollBar().value()             
    # self.view.scrollToItem(self.view.item(row, 0))            
    # self.view.verticalScrollBar().setValue(curr_pos)

# ----- 데이터베이스 파일 open ----------------------------------------------- 
def dbFileOpen(self):

    curDir = os.getcwd()
    fname, ok = QFileDialog.getOpenFileName(self, 'DB file 지정', curDir, '*.db')
    # 반환값(tuple) -> ('C:/Users/Administrator/PyQtTest/a2.db', '*.db')

    if ok and len(fname) >= 7:   # 'C:\a.db'의 경우 최소 7글자
        fname = fname.replace('/', '\\')
        self.dbFileName = getDbFileName(fname)
        self.qLineEdit.setText(self.dbFileName)
        
        if self.dbFileName != '':
            self.tableName = updateComboList(self)
            self.qLineEdit.setText(self.dbFileName)
            
        if self.tableName != '':
            dispData(self)
            QMessageBox.information(self, "DB file open!", " DB 파일을 열고, 테이블 목록을 갱신하였습니다. ")
            with open(self.pathFile, 'w', encoding='utf-8') as f:
                f.write(self.dbFileName)
                
# ----- App21 클래스 --------------------------------------------------------
class App21(QTableWidget):    

    def __init__(self, *args):
        self.parent = args[0]
        # super().__init__()
        QTableWidget.__init__(self, *args)
        #QWidget.__init__(self, *args)
        
        self.resize(1200,1000)
        self.setWindowTitle("영문장 암기 프로그램(by G.B.KIM)")
        
        self.bookMark = []
        self.bookCnt = 0
        self.saveFlag = False      # Tue이면 저장할 데이터 있음
        self.modifiedRow = []

        self.dispTableView21()
        
        fileName, self.pathFile = getLastFilePath()
        
        self.dbFileName = getDbFileName(fileName)
        self.qLineEdit.setText(self.dbFileName)
        self.tableName = updateComboList(self)

        if self.tableName != '':
            dispData(self)
            self.view.setFocus()
            self.view.setCurrentCell(0, 2)

        self.setWindowFlags(
            Qt.Window |
            # Qt.WindowCloseButtonHint |     # 창닫기('X')
            Qt.WindowMinimizeButtonHint |   # 창 최소화
            Qt.WindowMaximizeButtonHint)    # 창 최대화
        
        #self.show()

    def changedCombo(self):
        if self.saveFlag:
            reply = QMessageBox.question(self, '저장 확인!',
                " 저장하지 않은 자료는 삭제됩니다, 계속하시겠습니까? ", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return
          
            self.saveFlag = False
        
        self.tableName = self.combo.currentText()
        if self.tableName != '':
            dispData(self)
            self.view.setFocus()
            self.view.setCurrentCell(0, 2)

    def chkBoxClicked(self):
    
        dispData(self)
            
    def dispTableView21(self):
        # --- 맨 좌측 상자 -------------------------------------------------
        groupbox1 = QGroupBox('')
        gboxStyle = ("background-color: #00008C; " #521414 ;"
                      "border-radius: 3; border-color: rgb(200,200,200);")
        groupbox1.setStyleSheet (gboxStyle)
        self.label = QLabel("Memorizing")
        gboxStyle = ("QLabel {background-color: #00008C; color: white; font: bold 25px; }") #6F1515
        self.label.setStyleSheet(gboxStyle)
        self.label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.label)
        groupbox1.setLayout(vbox1)
        
        # --- 한국어/영문장 체크 --------------------------------------------
        groupbox2 = QGroupBox('')
        gboxStyle = ("background-color: #A396EA;" #CEA61D; " #63CBEA;" 
                     "border-style: solid; border-radius: 3; padding: 5px;"
                     "border-color: rgb(255,255,255); border-width: 1px;" )
        groupbox2.setStyleSheet (gboxStyle)    

        chkStyle = ("QCheckBox {background-color: #64b5f6; padding: 5px; }"
                    "QCheckBox::hover {background-color: #E9AEF3; color: #fff;}")
        
        self.check1 = QCheckBox('한국어 보기')
        self.check2 = QCheckBox('영문장 보기')
        self.check1.setChecked(True)
        self.check2.setChecked(True)

        self.check1.setStyleSheet(chkStyle)
        self.check2.setStyleSheet(chkStyle)
        self.check1.stateChanged.connect(self.chkBoxClicked)
        self.check2.stateChanged.connect(self.chkBoxClicked)
        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.check1, 1, Qt.AlignLeft)
        vbox2.addSpacing(10)  # 단순 공백 추가        
        vbox2.addWidget(self.check2, 1, Qt.AlignLeft)
        groupbox2.setLayout(vbox2)
        
        # --- 암기/미암기/중요 체크 ------------------------------------------
        groupbox3 = QGroupBox('')
        groupbox3.setStyleSheet (gboxStyle)   
        
        self.check3 = QCheckBox('암기 문장   ')
        self.check4 = QCheckBox('미암기 문장')
        self.check5 = QCheckBox('중요 보기   ')
        self.check3.setChecked(True)
        self.check4.setChecked(True) 
        self.check3.setStyleSheet(chkStyle)
        self.check4.setStyleSheet(chkStyle)
        self.check5.setStyleSheet(chkStyle)
        self.check3.stateChanged.connect(self.tableRepaint)
        self.check4.stateChanged.connect(self.tableRepaint)
        self.check5.stateChanged.connect(self.tableRepaint)        
        vbox3 = QVBoxLayout()
        vbox3.addWidget(self.check3, 1, Qt.AlignLeft)
        vbox3.addWidget(self.check4, 1, Qt.AlignLeft)
        vbox3.addWidget(self.check5, 1, Qt.AlignLeft)
        #vbox3.setSpacing(2) # 위젯 사이의 늘림 간격
        groupbox3.setLayout(vbox3)
        
        # --- DB파일명/테이블 선택 -------------------------------------------
        groupbox4 = QGroupBox('')
        
        btnStyle = ("QPushButton {background-color: #4285F4; color: white; border-radius: 5;"
                    "border-color: rgb(255,255,255); border-width: 1px;}"
                    "QPushButton::hover {background-color: #FF9930; color: #fff;}" #64b5f6 #8F8F00 #001040 
                    "QPushButton::pressed {background-color:142090 ;}") #FF9900

        gboxStyle = ("background-color: #C0CDEF; " #DDEBF7;" #FFE7D8;" #A0B4E6;"
                      "border-style: solid; border-radius: 3;"
                      "padding: 3px; padding-left: 10px; padding-right: 10px;"
                      "border-color: rgb(200,200,200); border-width: 1px;") 
     
        groupbox4.setStyleSheet(gboxStyle)
        dbBtn1 = QPushButton("  DB 파일 / 테이블 선택  ")
        dbBtn1.clicked.connect(lambda: dbFileOpen(self))
        dbBtn1.setStyleSheet(btnStyle)
        dbBtn1.setMinimumWidth(252)
        dbBtn1.setMaximumHeight(35)
        
        editStyle = ("QLineEdit {background-color: #FFFAC8; color: blue; " #D9EAF7
                 "padding: 5px; font: bold 11pt; }")
        self.qLineEdit = QLineEdit()
        self.qLineEdit.setReadOnly(True)
        self.qLineEdit.setMaximumHeight(35)
        self.qLineEdit.setStyleSheet(editStyle)

        lstStyle = ("QListView{background-color: white; padding: 3px; font: bold 12pt '맑은 고딕'; }"
                    "QListView::item{height: 20px; background-color: white; color: blue;}")
        listView = QListView()
        listView.setSpacing(3)
        listView.setStyleSheet(lstStyle) 
        
        cboStyle = ("QComboBox {background-color: #EBDEF1; padding: 3px; font: bold 12pt '굴림'; padding: 5px; }")        
        self.combo = QComboBox()
        self.combo.setView(listView)        
        self.combo.setMaximumHeight(35)
        self.combo.setStyleSheet(cboStyle)
        self.combo.activated.connect(self.changedCombo)               # 사용자가 list 목록을 변경시 호출
        # self.combo.currentIndexChanged.connect(self.changedCombo)   # 프로그램 or 사용자에 의해 내용 변경시 호출
        
        lbl1=QLabel("DB파일명:")
        lbl2=QLabel("경  로  명:")
        lbl3=QLabel("DB테이블:")
        
        vbox4=QGridLayout()
        vbox4.addWidget(lbl1, 0, 0, 1, 1)
        vbox4.addWidget(lbl2, 1, 0, 1, 1)
        vbox4.addWidget(lbl3, 2, 0, 1, 1)

        vbox4.addWidget(dbBtn1, 0, 1, 1, 15)
        vbox4.addWidget(self.qLineEdit, 1, 1, 1, 15)
        vbox4.addWidget(self.combo,     2, 1, 1, 15)
        groupbox4.setLayout(vbox4)        
        
        # --- 검색/닫기 버튼 -------------------------------------------------
        groupbox5 = QGroupBox('')

        btnSave = QPushButton(" 저  장 ")
        btnSave.clicked.connect(self.saveUpdated)   
        
        btnClose = QPushButton(" 닫  기 ")
        btnClose.clicked.connect(self.finish)
        
        vbox5 = QVBoxLayout()
        vbox5.addWidget(btnSave, 1, Qt.AlignRight)
        vbox5.addWidget(btnClose, 1, Qt.AlignRight)
        groupbox5.setLayout(vbox5)
        
        # ---  layout 구성하기 ----------------------------------------------
        layout1 = QHBoxLayout()
        layout1.addWidget(groupbox1, 0)
        layout1.addWidget(groupbox2, 0)
        layout1.addWidget(groupbox3, 0)
        layout1.addWidget(groupbox4, 2)
        layout1.addWidget(groupbox5, 0)
        layout1.setSpacing(10)

        # ---  view(QTableWIdget) 생성 및 레이어 배치-------------------------
        self.view = QTableWidget()
        layout2 = QVBoxLayout()        
        layout2.addWidget(self.view)

        mLayout = QVBoxLayout(self)
        mLayout.addLayout(layout1, 1)
        mLayout.addLayout(layout2, 8)
        #mLayout.setContentsMargins(50, 50, 50, 50)
        self.setLayout(mLayout)
                
        # ---  view(QTableWIdget) 속성 설정 ----------------------------------
        self.view.setColumnCount(6)
        self.view.setColumnWidth(0, 54)
        self.view.setColumnWidth(1, 502)
        self.view.setColumnWidth(2, 502)
        self.view.setColumnWidth(3, 50)
        self.view.setColumnWidth(4, 50)  
        self.view.setColumnHidden(5, True)
        
        self.view.setHorizontalHeaderLabels(["순", "한국어", "English", "암기", "중요"])
        self.view.horizontalHeader().setFixedHeight(50)
        self.view.horizontalHeader().setStretchLastSection(True)    # 마지막 칼럼 확장하기  
        
        self.view.verticalHeader().setVisible(False)
        self.view.verticalHeader().setDefaultSectionSize(60)
        self.view.verticalHeader().setSectionResizeMode(QHeaderView.Interactive) #(QHeaderView.Fixed)
        self.view.setAlternatingRowColors(True)
        self.view.setShowGrid(True)

        self.view.setEditTriggers(QAbstractItemView.DoubleClicked) 
        # self.view.setEditTriggers(QAbstractItemView.CurrentChanged)
        # (NoEditTriggers, AllEditTriggers, CurrentChanged )

        tblStyle = ("QHeaderView::section {background-color: rgb(173, 255, 47); font-size: 18px; }"
                  "QTableView{ background-color:#D3D3D3; font-size: 18px; padding:0px; } ")   #EBDEF1(연보라)
        
        self.view.setStyleSheet(tblStyle)
        self.view.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.view.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.view.setSizePolicy(7, 7)   # (w:QSizePolicy.Expanding, w:QSizePolicy.Expanding)
        self.view.setWordWrap(True)

        self.view.cellClicked.connect(self.cell_Clicked)
        self.view.cellChanged.connect(self.cellChanged_event) 
        self.view.currentCellChanged.connect(self.currentcellChanged_event)
        self.view.cell_EditingStarted.connect(self.cell_Editing)
        self.view.mouseDoubleClickEvent = self.refreshWidth
        # self.view.itemChanged.connect(self.item_Changed)        
        # self.view.setMouseTracking(True)
        self.center()
        self.show()

        # self.view.setItemDelegate(self.delegate)
        # self.view.cellActivated.connect(self.itemChanged)
        
        # self.view.horizontalHeader().setStyleSheet("background-color: rgb(190,200,200); ") # .setVisible(True) 설정 필요함
        # self.view.horizontalHeaderItem(0).setTextAlignment(Qt.AlignCenter) # header 정렬 방식
        # item = QTableWidgetItem('필드내용(Item)')
        # item.setBackground(Qt.red) # QColor(100, 255, 0))
        # item.setTextAlignment(Qt.AlignCenter)
        # self.view.setHorizontalHeaderItem(1, item)  
        # self.view.horizontalHeader().setDefaultSectionSize(100)
        
        # self.view.setHorizontalHeaderLabels(["코드", "종목명"])
        # self.view.horizontalHeaderItem(0).setToolTip("코드...") # header tooltip
        # self.view.setSelectionMode(QAbstractItemView.SingleSelection)
        # self.view.setSelectionMode(QAbstractItemView.ExtendedSelection) # drag, Ctrl, Shift 키로 다중 선택 가능.
        # self.view.setSelectionMode(QAbstractItemView.MultiSelection)
        # self.view.setSelectionMode(QAbstractItemView.NoSelection) # 선택 불능.
        # self.view.setSelectionMode(QAbstractItemView.SingleSelection) # 다중 선택 불가능.
        # self.view.setSelectionMode(QAbstractItemView.ContiguousSelection)
        # self.view.setSelectionBehavior(QTableView.SelectRows) # multiple row 선택 가능
        # self.view.setSelectionBehavior(QAbstractItemView.SelectRows)    # row 단위로 선택 가능
        # self.view.setSelectionBehavior(QAbstractItemView.SelectColumns) # column 단위로 선택
        # self.view.setSelectionBehavior(QAbstractItemView.SelectItems)   # cell 단위로 선택 가능
        
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # ----- 수정 데이터 업데이트 ----------------------------------------------
    def saveUpdated(self):
        
        if self.saveFlag == False:
            return
        
        try:
            if not os.path.exists(self.dbFileName):  # if not QFile.exists(self.dbFileName):
                 raise DbException('데이터베이스 파일이 존재하지 않습니다.')
      
            conn = QSqlDatabase.addDatabase("QSQLITE")
            conn.setDatabaseName(self.dbFileName)
            conn.open()
            query = QSqlQuery()
    
            sql = 'SELECT * FROM ' + self.tableName
            if not query.exec(sql):
                raise DbException('테이블('+self.tableName+')이 존재하지 않습니다.')
    
            msg = " 저장할 DB파일명과 테이블명이 모두 맞습니까? \n\n [저장할 DB 파일명] : " + self.dbFileName
            msg += "\n\n [테이블명] : " + self.tableName
            reply = QMessageBox.question(self, '저장할 DB파일 확인!', msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            
            if reply == QMessageBox.No:
                conn.close()
                return
    
            for row in self.modifiedRow:
    
                if self.view.item(row, 0) is None:
                    continue
    
                itm0 = int(self.view.item(row, 0).text())
                itm1 = self.view.item(row, 1).text()
                itm2 = self.view.item(row, 2).text()
                itm3 = self.view.item(row, 3).text()
                itm4 = self.view.item(row, 4).text()
    
                sql = "UPDATE " + self.tableName
                sql += " SET seq=%d, korean='%s', english='%s', done='%s', point='%s' WHERE seq=%d " % (itm0, itm1, itm2, itm3, itm4, itm0)
    
                query.exec(sql)
            
            conn.commit()
            self.saveFlag = False
            self.modifiedRow.clear()            
            QMessageBox.information(self, " 저장 완료 ", "암기 문장을 DB 테이블에 저장했습니다.")
            
        except Exception as error: 
            QMessageBox.critical(None, "DB file Save Error!", "%s" % error)
            
        finally:
            if 'conn' in locals():   # DB 연결을 성공했으면 conn변수가 존재함
                conn.close()        

    # ----------------------------------------------------------------------
    def tableRepaint(self):
        
        chk3 = self.check3.isChecked()     # 암기 문장 보기
        chk4 = self.check4.isChecked()     # 미암기 문장 보기
        chk5 = self.check5.isChecked()     # 중요 문장 보기

        rows = self.view.rowCount()
        
        for row in range(rows):
            itm4 = self.view.item(row,3).text()     # 암기 필드
            itm5 = self.view.item(row,4).text()     # 중요 필드
            
            if chk5 and itm5 =='0':             # 중요 필드가 '0'인 경우 숨김
                self.view.hideRow(row)
                
            else:
                if (not chk3 and not chk4):     # 암기/미암기 모두 체크 해제
                    self.view.hideRow(row)
                    
                elif (chk3 and chk4):           # 암기/미암기 모두 체크 선택
                    self.view.showRow(row)
                    
                elif (chk3 and not chk4):       # 암기 체크 / 미암기 해제
                
                    if itm4 != "0":
                        self.view.showRow(row)
                    else:
                        self.view.hideRow(row)
                        
                elif (not chk3 and chk4):       # 암기 해제 / 미암기 체크
                
                    if itm4 == "0":
                        self.view.showRow(row)
                    else:
                        self.view.hideRow(row)

    # ----- table Widget 가로폭 갱신 -----------------------------------------
    def refreshWidth(self, event):
        # row = self.view.currentRow()
        # col = self.view.currentColumn()
        # print("doubleClicked - refreshWidth: (%d, %d) " % (row, col))         
        w = self.width()-200
        self.view.setColumnWidth(1, int(w/2))
        self.view.setColumnWidth(2, int(w/2))   
        
    # ----- 셀 편집 시작할 때 발생 -------------------------------------------
    def cell_Editing(self, row, col):
        self.cellEditing = True
        self.saveFlag = True
        
    # ----- 셀 편집 종료 후 값이 바뀌었을 때 발생 -----------------------------        
    # def item_Changed(self, data):
    #     row = self.view.currentRow()
    #     col = self.view.currentColumn()
    #     print("item_Changed (%d, %d) : %s " % (row, col, data.text())) 
    #     self.cellEditing = False
        
    # ----- 셀 편집 종료 후 값이 바뀌었을 때 발생 ----------------------------- 
    def cellChanged_event(self, row, col):
        
        if col == 1 or col == 2:  
            data = self.view.item(row, col).text()
            data = re.sub("'", "’", data)
            data = QTableWidgetItem(data)

        elif col == 3 or col == 4:
            data = self.view.item(row, col).text()+' '
            if "019".find(data[0]) < 0:
                data = '0'
                
            if data == '9' and not(row in self.bookMark):
                self.bookMark.append(row)
                
            data = QTableWidgetItem(data)
            data.setTextAlignment(Qt.AlignCenter)   
        
        self.view.blockSignals(True)
        self.view.setItem(row, col, data)
        self.view.blockSignals(False)

        self.saveFlag = True
        if not (row in self.modifiedRow):
            self.modifiedRow.append(row)
        self.cellEditing = False  
        
        # print("cellChanged_event 발생 (%d, %d) : %s " % (row, col, data))
        # specialChar = "'!@#$%^&*()_{}[]\|;:<>?/"
        # for i in range(len(specialChar)):
        #     data = data.replace(specialChar[i], '’')

    def cell_Clicked(self):
        row = self.view.currentRow()
        col = self.view.currentColumn()
        
        if col == 3 or col == 4:    # '필드명: (암기, 중요)
            tempTuple = ('0','1','9')
            temp = self.view.item(row, col).text()
            
            if temp in tempTuple:
                find = tempTuple.index(temp)
                if find == len(tempTuple) - 1:
                    find = -1
                temp = tempTuple[find + 1]
            else:
                temp = '0'
                
            if temp == '9' and not(row in self.bookMark):
                self.bookMark.append(row)
                    
            temp = QTableWidgetItem(temp)
            temp.setTextAlignment(Qt.AlignCenter)
            
            self.view.blockSignals(True)
            self.view.setItem(row, col, temp)
            self.view.blockSignals(False)
 
            self.saveFlag = True
            if not (row in self.modifiedRow):
                self.modifiedRow.append(row)
            self.cellEditing = False

    # ----- 선택한 셀이 바뀌면 발생하는 이벤트 ---------------------------------
    def currentcellChanged_event(self, row, col, pre_row, pre_col):

        self.cellEditing = False
        
        # cur_data = self.view.item(row, col)
        # if cur_data is None:
        #     cur_data = ''
        # else:
        #     cur_data = cur_data.text()
            
        # self.pre_data = self.view.item(pre_row, pre_col)
        # if self.pre_data is None:
        #     self.pre_data = ''
        # else:
        #     self.pre_data = self.pre_data.text()  
            
        # if self.pre_data is not None:
        #     print("이전 선택 셀 (%d, %d) : %s " % (pre_row, pre_col, self.pre_data))
        # else:
        #     print("이전 선택 셀 : 없음")
        # print("현재 선택 셀 (%d, %d) : %s " % (row, col, cur_data))

    # ----------------------------------------------------------------------            
    def keyPressEvent(self, e):

        if not hasattr(self, 'cellEditing') or self.cellEditing:
            return
        
        row = self.view.currentRow()
        col = self.view.currentColumn()
        rowCnt = self.view.rowCount()   
          
        keyPressed(self, e, row, col, rowCnt)
    
    # ----- 창 닫기 버는 클릭 -----------------------------------------------           
    def closeEvent(self, event):
        pass
        # event.ignore()  # event.accept()
        
    # ----- 종료 확인 메시지 출력 --------------------------------------------
    def finish(self):
        
        reply = QMessageBox.question(self, '종료 확인!',
            " 프로그램을 종료하시겠습니까? ", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return
        
        if self.saveFlag:
            reply = QMessageBox.question(self, '저장 확인!',
                " 저장하지 않은 자료는 삭제됩니다, 계속하시겠습니까? ", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return
        
        self.view.mouseDoubleClickEvent = None
        self.close()
        self.parent.show()


# ----- Thread object -------------------------------------------------------
# class Worker(QThread):
class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    
    def __init__(self, parent): 
        super().__init__(parent) 
        self.parent = parent

    def run(self):
        dbFileName = self.parent.dbFileName
        tableName = self.parent.tableName
        view = self.parent.view
        
        try:
            if not os.path.exists(dbFileName):  # if not QFile.exists(dbFileName):
                  raise DbException('데이터베이스 파일이 존재하지 않습니다.')
  
            conn = QSqlDatabase.addDatabase("QSQLITE")
            conn.setDatabaseName(dbFileName)
            conn.open()
            query = QSqlQuery()
            
            sql = 'SELECT * FROM ' + tableName
            if not query.exec(sql):
                raise DbException('테이블('+tableName+')이 존재하지 않습니다.')

            msg = " 저장할 DB파일명과 테이블명이 모두 맞습니까? \n\n [저장할 DB 파일명] : " + dbFileName
            msg += "\n\n [테이블명] : " + tableName
            reply = QMessageBox.question(self.parent, '저장할 DB파일 확인!', msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
           
            if reply == QMessageBox.No:
                raise DbException('데이터를 DB에 저장하지 못했습니다.')
            
            sql = 'DELETE FROM ' + tableName
            query.exec(sql)

            # self.parent.win.show()
            progress = 0
            rows = view.rowCount()
            for row in range(rows):
                
                progVal = int(((row+1)/rows)*100)
                self.progress.emit(progVal)
                
                if view.item(row, 0) is None:
                    continue
    
                itm0 = int(view.item(row, 0).text())
                itm1 = view.item(row, 1).text()
                itm2 = view.item(row, 2).text()
                itm9 = view.item(row, 5)
                if itm9 is None:
                    itm9 = '20200101'
                # itm3 = '0'
                # itm4 = '0'
    
                sql = "INSERT INTO " + tableName
                sql += "(YMD, seq, korean, english) VALUES('%s', %d, '%s', '%s')" % (itm9, itm0, itm1, itm2)
                #sql += "(YMD, seq, korean, english, done, point) VALUES('%s', %d, '%s', '%s', '%s', '%s')" % ('20050501', itm0, itm1, itm2, itm3, itm4)
                query.exec(sql)

            conn.commit()
            QMessageBox.information(self.parent, " 저장 완료 ", "암기 문장을 DB 테이블에 저장했습니다.")
            
        except Exception as error:
        
            QMessageBox.critical(self.parent, "DB file Save Error!", "%s" % error)
            
        finally:
            if 'conn' in locals():   # DB 연결을 성공했으면 conn변수가 존재함
                conn.close()
            self.finished.emit()
        
# ----- App22 클래스 --------------------------------------------------------
class App22(QTableWidget):
    
    def __init__(self, *args):
        self.parent = args[0]
        super().__init__()
        # QTableWidget.__init__(self, *args)
        #QWidget.__init__(self, *args)

        self.resize(1200,1000)
        self.setWindowTitle("엑셀파일에 저장된 암기문장 불러오기(by G.B.KIM)")

        self.bookMark = []
        self.bookCnt = 0
        self.saveFlag = False   # Tue이면 저장할 데이터 있음
        
        self.dispTableView22() 
        
        fileName, self.pathFile = getLastFilePath()
        
        self.dbFileName = getDbFileName(fileName)
        self.qLineEdit.setText(self.dbFileName)
        self.tableName = updateComboList(self)
        
        if self.tableName != '':
            dispData(self)
            self.view.setFocus()
            self.view.setCurrentCell(0, 2)
            
        self.setWindowFlags(
            Qt.Window |
            # Qt.WindowCloseButtonHint |      # 창닫기('X')
            Qt.WindowMinimizeButtonHint |   # 창 최소화
            Qt.WindowMaximizeButtonHint)    # 창 최대화

        self.show()

    def excelFileOpen(self):
        curDir = os.getcwd()
        fname, ok = QFileDialog.getOpenFileName(self, '엑셀 (문장) 파일 지정', curDir, '*.xlsx')
        # 반환값(tuple) -> ('C:/Users/Administrator/Documents/DataDB/DATA_2021_00.xlsx', '*.xlsx')
        
        if ok and len(fname) >= 8:   # 'C:\a.xls'의 경우 최소 8글자
            excelFileName = fname.replace('/', '\\')
            self.dispExcelData(excelFileName)
            msg = "엑셀 파일로부터 암기할 문장을 가져왔습니다. \n\n 저장할 [DB테이블]을 선택 후 [저장] 버튼을 클릭하세오. "
            QMessageBox.information(self, "엑셀 파일 가져오기", msg)
            
    def changedCombo(self):

        if self.saveFlag:
            reply = QMessageBox.question(self, '저장 확인!',
                " 저장하지 않은 자료는 삭제됩니다, 계속하시겠습니까? ", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return
      
            self.saveFlag = False
            
        self.tableName = self.combo.currentText()
        if self.tableName != '':
            dispData(self)
            self.view.setFocus()
            self.view.setCurrentCell(0, 2)
 
    def dispTableView22(self):
        # --- 맨 좌측 상자 -------------------------------------------------
        groupbox1 = QGroupBox('')
        gboxStyle = ("background-color: #3057B9; " #521414 ;"
                     "border-radius: 3; border-color: rgb(200,200,200);")
        groupbox1.setStyleSheet (gboxStyle)
        
        label = QLabel("Data importing")
        gboxStyle = ('QLabel {background-color: #3057B9; color: white; font: bold 25px; }') #6F1515
        label.setStyleSheet(gboxStyle)
        label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        vbox1 = QVBoxLayout()
        vbox1.addWidget(label)
        groupbox1.setLayout(vbox1)
        
        # --- DB 파일 생성 및 테이블 추가/삭제--------------------------------
        groupbox2 = QGroupBox('')
        gboxStyle = ("background-color: rgb(255, 224, 192);"
                     "border-style: solid; border-radius: 3;"
                     "padding: 3px; padding-left: 10px; padding-right: 10px;"
                     "border-color: rgb(200,200,200); border-width: 1px;")
        groupbox2.setStyleSheet(gboxStyle)    
        
        self.btnDBcreate = QPushButton2('DB파일 생성하기')
        self.btnTBcreate = QPushButton2('테이블 추가하기')
        self.btnTBdrop = QPushButton2('테이블 삭제하기')
        self.btnDBcreate.clicked.connect(self.createDbase)        
        self.btnTBcreate.clicked.connect(self.createTable)   
        self.btnTBdrop.clicked.connect(self.dropTable) 
        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.btnDBcreate, 1, Qt.AlignLeft)
        vbox2.addWidget(self.btnTBcreate, 1, Qt.AlignLeft)
        vbox2.addWidget(self.btnTBdrop, 1, Qt.AlignLeft)
        groupbox2.setLayout(vbox2)

        # --- DB파일명/테이블 선택 -------------------------------------------
        groupbox3 = QGroupBox('')

        btnStyle = ("QPushButton {background-color: #4285F4; color: white; border-radius: 5;"
                    "border-color: rgb(255,255,255); border-width: 1px;}"
                    "QPushButton::hover {background-color: #FF9930; color: #fff;}" #64b5f6 #8F8F00 #001040
                    "QPushButton::pressed {background-color:142090 ;}") #FF9900        
        gboxStyle = ("background-color: #C0CDEF; " #DDEBF7;" #FFE7D8;" #A0B4E6;"
                     "border-style: solid; border-radius: 3;"
                     "padding: 3px; padding-left: 10px; padding-right: 10px;"
                     "border-color: rgb(200,200,200); border-width: 1px;") 
        
        groupbox3.setStyleSheet(gboxStyle)
        dbBtn1 = QPushButton("  DB 파일 / 테이블 선택  ")
        dbBtn1.clicked.connect(lambda: dbFileOpen(self))
        dbBtn1.setStyleSheet(btnStyle)
        dbBtn1.setMinimumWidth(252)
        dbBtn1.setMaximumHeight(35)
        
        dbBtn2 = QPushButton(" 엑셀 파일(문장) 불러오기 ")
        dbBtn2.clicked.connect(self.excelFileOpen) 
        dbBtn2.setStyleSheet(btnStyle)
        dbBtn2.setMinimumWidth(252)
        dbBtn2.setMaximumHeight(35)

        editStyle = ("QLineEdit {background-color: #FFFAC8; color: blue; " #D9EAF7
                 "padding: 5px; font: bold 11pt; }")
        self.qLineEdit = QLineEdit()
        self.qLineEdit.setReadOnly(True)
        self.qLineEdit.setMaximumHeight(35)
        self.qLineEdit.setStyleSheet(editStyle)

        lstStyle = ("QListView{background-color: white; padding: 3px; font: bold 12pt '맑은 고딕'; }"
                    "QListView::item{height: 20px; background-color: white; color: blue;}")
        listView = QListView()
        listView.setSpacing(3)
        listView.setStyleSheet(lstStyle) 
        
        cboStyle = ("QComboBox {background-color: #EBDEF1; padding: 3px; font: bold 12pt '굴림'; padding: 5px; }")     
        self.combo = QComboBox()
        self.combo.setView(listView)        
        self.combo.setMaximumHeight(35)
        self.combo.setStyleSheet(cboStyle)
        self.combo.activated.connect(self.changedCombo)               # 사용자가 list 목록을 변경시 호출
        # self.combo.currentIndexChanged.connect(self.changedCombo)   # 프로그램 or 사용자에 의해 내용 변경시 호출
        
        lbl1=QLabel("DB파일명:")
        lbl2=QLabel("경  로  명:")
        lbl3=QLabel("DB테이블:")
        
        vbox3=QGridLayout()
        vbox3.addWidget(lbl1, 0, 0, 1, 1)
        vbox3.addWidget(lbl2, 1, 0, 1, 1)
        vbox3.addWidget(lbl3, 2, 0, 1, 1)
        vbox3.addWidget(dbBtn1, 0, 1, 1, 1)
        vbox3.addWidget(dbBtn2, 0, 2, 1, 14, Qt.AlignRight)
        vbox3.addWidget(self.qLineEdit, 1, 1, 1, 15)
        vbox3.addWidget(self.combo,     2, 1, 1, 15)
        groupbox3.setLayout(vbox3)
        
        # --- 저장/닫기 버튼 -------------------------------------------------
        groupbox4 = QGroupBox('')

        btnSave = QPushButton(" 저  장 ")
        btnSave.clicked.connect(self.insertData)
          
        btnClose = QPushButton(" 닫  기 ")
        btnClose.clicked.connect(self.finish)
        
        vbox4 = QVBoxLayout()
        vbox4.addWidget(btnSave, 1, Qt.AlignRight)
        vbox4.addWidget(btnClose, 1, Qt.AlignRight)
        groupbox4.setLayout(vbox4)

        # ---  layout 구성하기 ----------------------------------------------
        layout1 = QHBoxLayout()
        layout1.addWidget(groupbox1, 0)
        layout1.addWidget(groupbox2, 0)
        layout1.addWidget(groupbox3, 2)
        layout1.addWidget(groupbox4, 0)
        layout1.setSpacing(10)

        # ---  view(QTableWIdget) 생성 및 레이어 배치-------------------------
        self.view = QTableWidget()
        layout2 = QVBoxLayout()
        layout2.addWidget(self.view)

        mLayout = QVBoxLayout(self)
        mLayout.addLayout(layout1, 1)
        mLayout.addLayout(layout2, 8)
        #mLayout.setContentsMargins(50, 50, 50, 50)
        self.setLayout(mLayout)
                
        # ---  view(QTableWIdget) 속성 설정 ----------------------------------
        self.view.setColumnCount(6)
        self.view.setColumnWidth(0, 54)
        self.view.setColumnWidth(1, 502)
        self.view.setColumnWidth(2, 502)
        self.view.setColumnWidth(3, 50)
        self.view.setColumnWidth(4, 50)
        self.view.setColumnHidden(5, True)
        
        self.view.setHorizontalHeaderLabels(["순", "한국어", "English", "암기", "중요"])
        self.view.horizontalHeader().setFixedHeight(50)
        self.view.horizontalHeader().setStretchLastSection(True)    # 마지막 칼럼 확장하기  
        
        self.view.verticalHeader().setVisible(False)
        self.view.verticalHeader().setDefaultSectionSize(60)
        self.view.verticalHeader().setSectionResizeMode(QHeaderView.Interactive) #(QHeaderView.Fixed)
        self.view.setAlternatingRowColors(True)
        self.view.setShowGrid(True)

        self.view.setEditTriggers(QAbstractItemView.DoubleClicked) 
        # self.view.setEditTriggers(QAbstractItemView.CurrentChanged)
        # (NoEditTriggers, AllEditTriggers, CurrentChanged )

        tblStyle = ("QHeaderView::section {background-color: rgb(173, 255, 47); font-size: 18px; }"
                  "QTableView{ background-color:#D3D3D3; font-size: 18px; padding:0px; } ")   #EBDEF1(연보라)

        self.view.setStyleSheet(tblStyle)
        self.view.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.view.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.view.setSizePolicy(7, 7)  
        self.view.setWordWrap(True)

        self.view.cellChanged.connect(self.cellChanged_event) 
        self.view.currentCellChanged.connect(self.currentcellChanged_event)
        self.view.cell_EditingStarted.connect(self.cell_Editing) 
        self.view.mouseDoubleClickEvent = self.refreshWidth
        
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    # ----- DB 파일 생성하기 -------------------------------------------------
    def createDbase(self):

        if self.saveFlag:
            reply = QMessageBox.question(self, '저장 확인!',
                " 저장하지 않은 자료는 삭제됩니다, 계속하시겠습니까? ", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return

            self.saveFlag = False
                        
        curPath = os.getcwd()
        
        options = QFileDialog.Options()
        options |= QFileDialog.DontConfirmOverwrite 
        #options |= QFileDialog.DontUseNativeDialog | QFileDialog.ShowDirsOnly  
        
        fname = QFileDialog.getSaveFileName(self, 'DB file 생성하기', curPath, '*.db', options = options)
        fileName = fname[0]
        
        if fileName =='':
            return

        temp = fileName.replace('_', '').replace('/','').replace(':','',1).replace('.','',1)
        if not temp.isalnum():
            QMessageBox.information(self, "DB 파일명 입력 오류!", "DB 파일명(<한글>,<영숫자>,'_'로 구성)을 잘못 입력하였습니다.")
            return
        
        fileName = fileName.replace('/', '\\')

        self.dbFileName = getDbFileName(fileName)        

        if os.path.exists(self.dbFileName):
            msg = "같은 이름의 파일이 존재합니다. 새 파일명을 입력하십시오."
            QMessageBox.critical(self, "파일명 입력 오류!", msg) 
            return

        conn = sqlite3.connect(self.dbFileName)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS sample")
        
        sql ='''CREATE TABLE sample(
            YMD char(8),
            seq integer,
            korean text,
            english text,
            done CHAR(1) DEFAULT '0',
            point CHAR(1) DEFAULT '0',
            PRIMARY KEY(seq)
        )'''
        cursor.execute(sql)
        conn.commit()
        conn.close()

        self.qLineEdit.setText(self.dbFileName)
        self.tableName = updateComboList(self)
        dispData(self)
        QMessageBox.information(self, "DB 파일명 생성 성공 !!", "DB 파일 생성을 성공하였습니다.")
        with open(self.pathFile, 'w', encoding='utf-8') as f:
            f.write(self.dbFileName)
        
    # ----- DB 테이블 추가하기 -----------------------------------------------
    def createTable(self):

        if self.saveFlag:
            reply = QMessageBox.question(self, '저장 확인!',
                " 저장하지 않은 자료는 삭제됩니다, 계속하시겠습니까? ", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return
                # self.insertData()
            self.saveFlag = False
                
        if not os.path.exists(self.dbFileName):
             raise DbException('데이터베이스 파일이 존재하지 않습니다.')
             
        conn = QSqlDatabase.addDatabase("QSQLITE")
        conn.setDatabaseName(self.dbFileName)
        conn.open()
        query = QSqlQuery()
        
        tableName, ok = QInputDialog.getText(self, '추가할 DB 테이블명 입력', 'Enter DB table name(only 한글/영숫자/밑줄):')
        if not ok:
            return
        
        # temp = re.match('[a-zA-Z_]+[0-9]*[a-zA-Z0-9_]*', tableName)
        # if (not ok) or (temp == None):
        #     QMessageBox.information(self, "DB 테이블명 입력 오류!", '테이블명을 입력하지 않았거나 잘못 입력하였습니다.')
        #     return
        # tableName = temp.group(0)
        
        temp = tableName.replace('_', '')
        if not temp.isalnum():
            QMessageBox.information(self, "DB 테이블명 입력 오류!", '테이블명을 입력하지 않았거나 잘못 입력하였습니다.')
            return

        sql = 'SELECT * FROM ' + tableName
        if query.exec(sql):
            QMessageBox.information(self, "DB 테이블명 중복!", '테이블명(' + tableName + ')이 이미 존재합니다.')
            return
        
        sql ="CREATE TABLE %s(YMD char(8), seq integer, korean text, english text, \
            done CHAR(1) DEFAULT '0', point CHAR(1) DEFAULT '0', PRIMARY KEY(seq))" % tableName

        query.exec(sql)
        conn.commit()
        conn.close()
        QMessageBox.information(self, "테이블 추가 성공 !!", "DB 파일에 새 테이블을 추가하였습니다.")    
        
        self.tableName = updateComboList(self)
        dispData(self)
    
    # ----- DB 테이블 삭제하기 -----------------------------------------------
    def dropTable(self):

        if self.saveFlag:
            reply = QMessageBox.question(self, '저장 확인!',
                " 저장하지 않은 자료는 삭제됩니다, 계속하시겠습니까? ", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return

            self.saveFlag = False
            
        if not os.path.exists(self.dbFileName):
             raise DbException('데이터베이스 파일이 존재하지 않습니다.')
             
        conn = QSqlDatabase.addDatabase("QSQLITE")
        conn.setDatabaseName(self.dbFileName)
        conn.open()
        query = QSqlQuery()
        
        tableName, ok = QInputDialog.getText(self, '삭제할 DB 테이블명 입력', 'Enter DB table name(only 한글/영숫자/밑줄):')
        if not ok:
            return
        
        temp = tableName.replace('_', '')
        if not temp.isalnum():
            QMessageBox.information(self, "DB 테이블명 입력 오류!", '테이블명을 입력하지 않았거나 잘못 입력하였습니다.')
            return
        
        sql = 'SELECT * FROM ' + tableName
        if not query.exec(sql):
            QMessageBox.information(self, "DB 테이블명 삭제 오류!", '테이블명(' + tableName + ')이 존재하지 않습니다.')
            return

        msg = " 테이블명을 삭제하면 저장된 자료가 모두 삭제됩니다. 삭제할까요? \n\n [DB 파일명] : " + self.dbFileName
        msg += "\n\n [삭제할 DB테이블명] : " + tableName
        reply = QMessageBox.question(self, '삭제할 DB 테이블 확인!', msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.No:
            return

        sql ="DROP TABLE IF EXISTS " + tableName
        query.exec(sql)
        conn.commit()
        conn.close()
        QMessageBox.information(self, "DB 테이블 삭제 성공 !!", "DB 파일에서 1개의 테이블을 삭제하였습니다.")
        
        self.tableName = updateComboList(self)
        dispData(self)

    # ----- 테이블에 데이터 저장하기 ------------------------------------------
    def insertData(self):
        if self.saveFlag == False:
            return

        self.win = QDialog(self)
        self.win.resize(400, 90)
        self.win.setWindowTitle('자료 저장중 ...')

        self.progressBar = QProgressBar(self.win)
        self.progressBar.setGeometry(15, 25, 380, 25)
        self.progressBar.setMaximum(100) 
        # self.win.setWindowFlags(Qt.WindowStaysOnTopHint) # | Qt.FramelessWindowHint)
        self.win.show()
        
        # [QThread 방법1]
        self.thread = QThread()
        self.worker = Worker(self)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.progressBar.setValue)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.endOfInsert)
        self.thread.start()
        
        # [QThread 방법2]
        # --> class Worker(QThread): #(QObject)
        # self.worker = Worker(self)
        # self.worker.progress.connect(self.progressBar.setValue)
        # self.worker.finished.connect(self.worker.quit)
        # self.worker.finished.connect(self.worker.deleteLater)
        # self.worker.finished.connect(self.endOfInsert)
        # self.worker.start()
            
    def endOfInsert(self):
        self.win.close()
        dispData(self)
        self.saveFlag = False
        
    # ----- 엑셀 파일 데이터 가져오기 ----------------------------------------
    def dispExcelData(self, excelFileName):

        if self.saveFlag:
            
            reply = QMessageBox.question(self, '저장 확인!',
                " 저장하지 않은 자료가 있습니다, 저장하시겠습니까? ", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.No:
                return
            self.insertData()
            
        try:
            if not os.path.exists(excelFileName):
                 raise DbException('문장을 저장한 엑셀 파일이 존재하지 않습니다.')
    
            wb = openpyxl.load_workbook(excelFileName) 
            sheet = wb.active # wb.get_sheet_by_name('LOG')
            
            max_row = sheet.max_row
            
            self.view.setRowCount(max_row)
            self.view.blockSignals(True)    # 이벤트 감시 중지
            
            rowCnt = 0
            for idx, row in enumerate(sheet.iter_rows(max_row = max_row)):
  
                if (row[1].value is None) or idx == 0 or str(row[1].value) < '0':                    
                    continue

                itm1 = QTableWidgetItem(str(row[1].value))
                itm2 = QTableWidgetItem(row[2].value)
                itm3 = QTableWidgetItem(row[3].value)
                itm4 = QTableWidgetItem(0)
                itm5 = QTableWidgetItem(0)
                itm9 = QTableWidgetItem(str(row[0].value))

                itm1.setFlags(itm1.flags() & ~Qt.ItemIsEditable)
                itm1.setBackground(QColor(200, 100, 100))
                itm1.setTextAlignment(Qt.AlignCenter)

                self.view.setItem(rowCnt, 0, itm1)
                self.view.setItem(rowCnt, 1, itm2)
                self.view.setItem(rowCnt, 2, itm3)
                self.view.setItem(rowCnt, 3, itm4)
                self.view.setItem(rowCnt, 4, itm5)
                self.view.setItem(rowCnt, 5, itm9)
           
                rowCnt += 1
                
            self.view.blockSignals(False)    # 이벤트 감시 재개
            self.view.setAlternatingRowColors(False)
            self.refreshWidth(None)
            self.view.show()
            if rowCnt > 0:
                self.saveFlag = True
            
        except Exception as e:
            QMessageBox.critical(self, "DB Error!"," %s" % e)

    # ----- table Widget 가로폭 갱신 -----------------------------------------
    def refreshWidth(self, event):
        # row = self.view.currentRow()
        # col = self.view.currentColumn()
        # print("doubleClicked - refreshWidth: (%d, %d) " % (row, col))         
        w = self.width()-200
        self.view.setColumnWidth(1, int(w/2))
        self.view.setColumnWidth(2, int(w/2))   
       
    # ----- 셀 편집 시작할 때 발생 -------------------------------------------
    def cell_Editing(self, row, col):
        self.cellEditing = True
        self.saveFlag = True
        
    # ----- 셀 편집 종료 후 값이 바뀌었을 때 발생 -----------------------------        
    # def item_Changed(self, data):
    #     row = self.view.currentRow()
    #     col = self.view.currentColumn()
    #     print("item_Changed (%d, %d) : %s " % (row, col, data.text())) 
    #     self.cellEditing = False
        
    # ----- 셀 편집 종료 후 값이 바뀌었을 때 발생 ----------------------------- 
    def cellChanged_event(self, row, col):
        data = self.view.item(row, col).text()
        data = re.sub("'", "’", data)
        self.view.blockSignals(True)
        self.view.setItem(row, col, QTableWidgetItem(data))
        self.view.blockSignals(False)
        self.cellEditing = False
        
        # print("cellChanged_event 발생 (%d, %d) : %s " % (row, col, data))
        # specialChar = "'!@#$%^&*()_{}[]\|;:<>?/"
        # for i in range(len(specialChar)):
        #     data = data.replace(specialChar[i], '’')
        
    # ----- 선택된 셀이 바뀌면 발생하는 이벤트 ---------------------------------
    def currentcellChanged_event(self, row, col, pre_row, pre_col):

        self.cellEditing = False
        
        # cur_data = self.view.item(row, col)
        # if cur_data is None:
        #     cur_data = ''
        # else:
        #     sur_data = cur_data.text()
        # pre_data = self.view.item(pre_row, pre_col)
        # if cur_data is None:
        #     pre_data = ''
        # else:
        #     pre_data = cur_data.text()  
            
        # print("currentcellChanged_event 발생 (%d, %d)  " % (row, col))
        # if pre_data is not None:
        #     print("이전 선택 셀 (%d, %d) : %s " % (pre_row, pre_col, pre_data))
        # else:
        #     print("이전 선택 셀 : 없음")
        # print("현재 선택 셀 (%d, %d) : %s " % (row, col, cur_data))
        
    # ----------------------------------------------------------------------            
    def keyPressEvent(self, e):
        
        if not hasattr(self, 'cellEditing') or self.cellEditing:
            return
        
        row = self.view.currentRow()
        col = self.view.currentColumn()
        rowCnt = self.view.rowCount()   
        
        keyPressed(self, e, row, col, rowCnt)
        
    # ----- 창 닫기 버는 클릭 -----------------------------------------------           
    def closeEvent(self, event):
        pass
        # event.ignore()  # event.accept()
        
    # ----- 종료 확인 메시지 출력 --------------------------------------------
    def finish(self):

        reply = QMessageBox.question(self, '종료 확인!',
            " 프로그램을 종료하시겠습니까? ", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return

        if self.saveFlag:

            reply = QMessageBox.question(self, '저장 확인!',
                " 저장하지 않은 자료는 삭제됩니다, 계속하시겠습니까? ", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
     
            if reply == QMessageBox.No:
                return
  
        self.view.mouseDoubleClickEvent = None
        self.close()
        self.parent.show()  
        
# ----- 메인함수 ------------------------------------------------------------ 
def main():

    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()  
    app.setStyleSheet(qss)  
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

