''' <Memorizing.py>
(1) 실행파일 만들기 : pyinstaller -w -F Memorizing.py
(2) 실행파일 만들기(upx-win64로 용량 줄이기) : pyinstaller --upx-dir ./upx396 -w -F Memorizing.py
(3) [get-pip.py 다운로드] : curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
(4) [pip install] : python get-pip.py
(5) [Upgrading pip] : python -m pip install --upgrade pip
(6) [Updating spyder] : pip install -U spyder
(7) [Reset preferences] : spyder --reset

<수정할 사항>
 - 
 
'''
import sys, os, getpass, sqlite3, openpyxl, re, random
from PyQt5.QtGui import QFont, QColor, QIcon, QPixmap, QPalette
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import (pyqtSignal, Qt, QSize, QThread, pyqtSlot, QObject, QEvent, QRect, QStringListModel)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QTableWidget,QWidget,
           QGroupBox, QCheckBox, QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit, QProgressBar,
           QListView, QComboBox, QHeaderView, QAbstractItemView, QDesktopWidget, QAction, QToolBar,
           QMessageBox, QTableWidgetItem, QFileDialog, QDialog, QTextEdit, QInputDialog, QSizePolicy,
           QTextBrowser, QStackedLayout, QTabWidget, qApp)
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

#/////////////////////////     Main 메뉴 화면     ////////////////////////////#

pixSeq = 0

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
        
        menu11.setStatusTip('영문장을 저장한 폴더의 DB파일을 선택합니다.')
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
        menu31 = QAction(QIcon(self.imgDir + 'icon5.png'), '윈도/위젯 사용하기...', self)
        menu32 = QAction('테이블 뷰 사용하기...', self)
        menu33 = QAction(QIcon(self.imgDir + 'icon33.png'), 'DB 테이블에서 문장 검색하기', self)

        menu31.triggered.connect(self.call_menu31)
        menu32.triggered.connect(self.call_menu32)
        menu33.triggered.connect(self.call_menu33)

        QMenu3.addAction(menu31)
        QMenu3.addSeparator() 
        QMenu3.addAction(menu32)
        QMenu3.addAction(menu33)
        
        # ----- toolBar 설정하기 --------------------------------------------
        toolBtn1 = QAction(QIcon(self.imgDir + "icon11.png"), 'Memorizing English Sentances', self)
        toolBtn1.setStatusTip("Memorizing English Sentances")
        toolBtn1.setShortcut('Ctrl+W')

        toolBtn2 = QAction(QIcon(self.imgDir + "icon16.png"), 'Load excelFile and Save DB file', self)
        toolBtn2.setStatusTip("Load excelFile and Save DB file")
        
        toolBtn3 = QAction(QIcon(self.imgDir + "icon5.png"), 'Window/Widget Examples', self)
        toolBtn3.setStatusTip("Window/Widget Examples")

        toolBtn4 = QAction(QIcon(self.imgDir + "icon26.png"), 'QTableWiget/QTableView Example', self)
        toolBtn4.setStatusTip("QTableWiget/QTableView Example")
        
        toolBtn5 = QAction(QIcon(self.imgDir + "icon33.png"), 'Searching sentence from DB File', self)
        toolBtn5.setStatusTip("Searching sentence from DB File")

        toolBtn6 = QAction(QIcon(self.imgDir + "exit.png"), 'Exit program', self)
        toolBtn6.setStatusTip("This is exit button")
        
        toolBtn1.triggered.connect(self.call_menu21)
        toolBtn2.triggered.connect(self.call_menu22)
        toolBtn3.triggered.connect(self.call_menu31)
        toolBtn4.triggered.connect(self.call_menu32)
        toolBtn5.triggered.connect(self.call_menu33)
        toolBtn6.triggered.connect(self.call_exitMenu)
        
        self.toolBar = QToolBar()
        self.toolBar.setIconSize(QSize(32,32))
        self.addToolBar(Qt.LeftToolBarArea, self.toolBar)
        
        self.toolBar.addAction(toolBtn1)
        self.toolBar.addAction(toolBtn2)
        self.toolBar.addSeparator()
        self.toolBar.addAction(toolBtn3) 
        self.toolBar.addAction(toolBtn4)
        self.toolBar.addAction(toolBtn5)
        self.toolBar.addAction(toolBtn6)
        self.toolBar.addSeparator()        
        self.show()
        
    def call_menu11(self):
        pass

    def call_menu12(self):
        pass

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
        palette = QPalette()
        palette.setColor(QPalette.Button, QColor(0, 200, 0))
        palette.setColor(QPalette.ButtonText, Qt.red)
        palette.setColor(QPalette.Window, QColor(0, 150, 200))
        palette.setColor(QPalette.WindowText, Qt.blue)
        qApp.setPalette(palette)
        
        self.hide()
        self.app31 = QTabWindow(self)
        self.app31.show() 

    def call_menu32(self):
        pass
        # self.hide()
        # os.system("python subWindow.py")
        # self.show() 

    def call_menu33(self):
        self.hide() 
        self.app33 = App33(self)
        self.app33.show()
        
    def call_exitMenu(self):
        self.close()
        QApplication.instance().quit()


#//////////////////////     클래스 기본 속성 재정의     ///////////////////////#

class QPushButton1(QPushButton):     # 버튼 클래스 재정의
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
        
class QProgressBar(QProgressBar):
    def __init__(self, parent = None):
        super().__init__(parent)
        # style = ("QProgressBar {"
        #         "background-color: rgb(98, 114, 164);"
        #         "color: rgb(200,200,200);"
        #         "border-style: none;"
        #         "border-radius: 5px;"
        #         "text-align: center; }"
        #         "QProgressBar::chunk {"
        #         "background-color: rgb(0,0,200);"
        #         "background-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, \
        #           stop:0 rgba(254, 121, 199, 255), stop:1 rgba(170, 85, 255, 255));"
        #         "border-radius: 5px; }")
        # self.setStyleSheet(style)
        
        # palette = QPalette()
        palette = QPalette(self.palette())
        palette.setColor(QPalette.Highlight, QColor(Qt.blue))
        palette.setColor(QPalette.Window, QColor(250, 250, 100))
        self.setPalette(palette)    

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


#//////////////////////      전역(공통) 함수 정의      ///////////////////////#

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
            reviewTable = f.readline().strip()

    return (fileName, reviewTable, pathFile)

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
    
    # --------------- 첫번째 테이블명을 가져옴
    tbName = tbnList[0][0]      
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
            if fieldName[id] != row[1]:  # records의 두번째(row[1]) 요소가 테이블의 필드명임
                errFlag = True
    if errFlag:
        QMessageBox.critical(self, "DB file error!", "테이블의 필드명이 일치하지 않습니다. DB파일을 올바르게 지정하세요.")
        return ''

    self.combo.blockSignals(True)
    self.combo.clear()
    
    # ---------------- 최근에 열어본 테이블명 가져오기.
    cnt = 0
    indexNo = -1
    for row in tbnList:
        self.combo.addItem(row[0])
        if self.reviewTable == row[0]:
            indexNo = cnt
        cnt += 1
    self.combo.blockSignals(False)
    
    if indexNo >= 0:
        self.combo.setCurrentIndex(indexNo)
    else:
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
            itm9 = QTableWidgetItem(query.value(0))
            
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
            self.view.setItem(row, 5, itm9)
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
            itm9 = QTableWidgetItem(rowList[row][0])
            
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
            self.view.setItem(row, 5, itm9)
            
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
    '''
    # [참고] QTableWidget.setEditTriggers()를 설정하면 편집용(알파벳, 숫자, ... 등) 키는 
             키 이벤트 함수에서 인식하지 못함.
    '''
    if e.modifiers() & Qt.ControlModifier or  e.key() == Qt.Key_Backspace:  

        if row > 0:
            self.view.setCurrentCell(row-1, col)
            tableScroll(self, row, col)
            
    elif e.modifiers() & Qt.ShiftModifier or e.key() in [Qt.Key_Return, Qt.Key_Enter]:
        
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

    elif e.key() == Qt.Key_Delete:
        
        currentRow = self.view.currentRow()
        reply = QMessageBox.question(self, '문장 삭제 확인!',
            f" 현재({currentRow + 1}번줄)의 문장을 삭제하시겠습니까? ", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply != QMessageBox.Yes:
            return        
        self.view.removeRow(currentRow)
        self.saveFlag = True
        self.saveAll = True
        
    elif e.key() == Qt.Key_Insert:
        
        curRow = self.view.currentRow()
        cols = self.view.columnCount()

        reply = QMessageBox.question(self, '문장 추가 확인!',
            f" 현재({curRow+2}번줄)의 위치에 새 문장을 추가하시겠습니까? ", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply != QMessageBox.Yes:
            return  

        self.view.insertRow(curRow + 1)
        curRow = self.view.currentRow()
        
        for j in range(cols):
            item = self.view.item(curRow, j)
            if not item is None:
                self.view.setItem(curRow + 1, j, QTableWidgetItem(item.text()))

        itm1 = self.view.item(curRow + 1, 0)
        itm1.setFlags(itm1.flags() & ~Qt.ItemIsEditable)    # 해당 비트 클리어
        itm1.setBackground(QColor(255, 255, 0))
        itm1.setTextAlignment(Qt.AlignCenter)
        
        self.view.setCurrentCell(curRow + 1, 1)
        self.saveFlag = True
        self.saveAll = True
            
    elif e.key() == Qt.Key_F1:
        
        win = QDialog(self)
        win.setWindowTitle("도움말 보기")
        win.resize(500, 400)
        xPos = self.pos().x()
        yPos = self.pos().y()
        w = int((self.width()  - win.size().width())/2)  + xPos
        h = int((self.height() - win.size().height())/2) + yPos
        win.move(w, h)
        
        btn = QPushButton1("닫기", win)
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
                f.write(self.dbFileName+'\n')
                f.write(self.tableName)
 
    
#////////////////////////////////////////////////////////////////////////////#
#                               영문장 암기하기                               #
#////////////////////////////////////////////////////////////////////////////#

# ----------------------------App21 클래스 -----------------------------------
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
        self.saveAll = False
        self.modifiedRow = []

        self.dispTableView21()
        
        fileName, self.reviewTable, self.pathFile = getLastFilePath()
        
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
        dbBtn1 = QPushButton1("  DB 파일 / 테이블 선택  ")
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

        btnSave = QPushButton1(" 저  장 ")
        btnSave.clicked.connect(self.saveUpdated)   
        
        btnClose = QPushButton1(" 닫  기 ")
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
        
    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:

            w = self.geometry().width() - 1200 
            self.view.setColumnWidth(1, 502 + int(w/2))
            self.view.setColumnWidth(2, 502 + int(w/2))

            # if event.oldState() and Qt.WindowMinimized:
            #     print("WindowMinimized")                
            # elif self.windowState() == Qt.WindowMaximized:
            #     print("WindowMaximized")
            # elif event.oldState() == Qt.WindowNoState :
            #     print("WindowMaximized 2")
            
    # def changeEvent(self, event):
    #     if event.type() == QEvent.WindowStateChange:
    #         if self.windowState() & Qt.WindowMinimized:
    #             pass
      
    # ----- 테이블 데이터를 모두 저장하기 -------------------------------------
    def saveAllitems(self):

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
        self.thread.finished.connect(self.endOfSave)
        self.thread.start()
        
        # [QThread 방법2]
        # --> class Worker(QThread): #(QObject)
        # self.worker = Worker(self)
        # self.worker.progress.connect(self.progressBar.setValue)
        # self.worker.finished.connect(self.worker.quit)
        # self.worker.finished.connect(self.worker.deleteLater)
        # self.worker.finished.connect(self.endOfInsert)
        # self.worker.start()
            
    def endOfSave(self):
        self.win.close()
        dispData(self)
        self.saveFlag = False
        self.saveAll = False
        
    # ----- 수정된 데이터만 저장하기 ------------------------------------------
    def saveUpdated(self):

        if self.saveFlag == False:
            return
        
        if self.saveAll:
            self.saveAllitems()
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
            self.saveAll = False
            self.modifiedRow.clear()            
            QMessageBox.information(self, " 저장 완료 ", "암기 문장을 DB 테이블에 저장했습니다.")
            
        except Exception as error: 
            QMessageBox.critical(None, "DB file Save Error!", "%s" % error)
            
        finally:
            if 'conn' in locals():   # DB 연결을 성공했으면 conn변수가 존재함
                conn.close()
                
        dispData(self)

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
        
        # w = self.geometry().width() - 1200
        # self.view.setColumnWidth(1, 502 + int(w/2))
        # self.view.setColumnWidth(2, 502 + int(w/2))
            
        
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

        data = self.view.item(row, col)
        data.setTextAlignment(Qt.AlignCenter)
        
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
        # print(e.key())
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

        with open(self.pathFile, 'w', encoding='utf-8') as f:
            f.write(self.dbFileName+'\n')
            f.write(self.tableName)
                
        self.view.mouseDoubleClickEvent = None
        self.close()
        self.parent.show()


# ----- Thread object -------------------------------------------------------
class Worker(QObject):
# class Worker(QThread):
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
    
                itm0 = row + 1  # int(view.item(row, 0).text())
                itm1 = view.item(row, 1).text()
                itm2 = view.item(row, 2).text()
                itm3 = view.item(row, 3).text()
                itm4 = view.item(row, 4).text()                
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

        
#////////////////////////////////////////////////////////////////////////////#
#                          영문장 엑셀 파일 등록하기                          #
#////////////////////////////////////////////////////////////////////////////#

# ---------------------------- App22 클래스 -----------------------------------
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
        
        fileName, self.reviewTable, self.pathFile = getLastFilePath()
        
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
        dbBtn1 = QPushButton1("  DB 파일 / 테이블 선택  ")
        dbBtn1.clicked.connect(lambda: dbFileOpen(self))
        dbBtn1.setStyleSheet(btnStyle)
        dbBtn1.setMinimumWidth(252)
        dbBtn1.setMaximumHeight(35)
        
        dbBtn2 = QPushButton1(" 엑셀 파일(문장) 불러오기 ")
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

        btnSave = QPushButton1(" 저  장 ")
        btnSave.clicked.connect(self.insertData)
          
        btnClose = QPushButton1(" 닫  기 ")
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

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:

            w = self.geometry().width() - 1200 
            self.view.setColumnWidth(1, 502 + int(w/2))
            self.view.setColumnWidth(2, 502 + int(w/2))

            # if event.oldState() and Qt.WindowMinimized:
            #     print("WindowMinimized")                
            # elif self.windowState() == Qt.WindowMaximized:
            #     print("WindowMaximized")
            # elif event.oldState() == Qt.WindowNoState :
            #     print("WindowMaximized 2")
            
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
            f.write(self.dbFileName+'\n')
            f.write(self.tableName)  
        
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

#///////////////////////////////////////////////////////////////////////////#
#                              DB 테이블 문장 검색                           #
#///////////////////////////////////////////////////////////////////////////#

# ---------------------------- App33 클래스 -----------------------------------
class App33(QTableWidget):
    
    querySignal = pyqtSignal() 
    
    def __init__(self, *args):
        self.parent = args[0]
        super().__init__()
        # QTableWidget.__init__(self, *args)
        #QWidget.__init__(self, *args)

        self.resize(1200,1000)
        self.setWindowTitle("DB 파일 영문장 검색하기(by G.B.KIM)")

        self.bookMark = []
        self.bookCnt = 0
        self.saveFlag = False   # Tue이면 저장할 데이터 있음
        
        self.dispTableView33() 
        
        fileName, self.reviewTable, self.pathFile = getLastFilePath()
        
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
        
        self.querySignal.connect(self.searchDB)
        self.show()
            
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
 
    def dispTableView33(self):
        # --- 맨 좌측 상자 -------------------------------------------------
        groupbox1 = QGroupBox('')
        gboxStyle = ("background-color: #7A2F02; " #521414 ;"
                      "border-radius: 3; border-color: rgb(200,200,200);")
        groupbox1.setStyleSheet (gboxStyle)
        
        label = QLabel(" 영문장 검색 ")
        gboxStyle = ('QLabel {background-color: #7A2F02; color: white; font: bold 25px; }') #6F1515
        label.setStyleSheet(gboxStyle)
        label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        vbox1 = QVBoxLayout()
        vbox1.addWidget(label)
        groupbox1.setLayout(vbox1)

        # --- 검색 옵션 체크 ------------------------------------------------
        groupbox2 = QGroupBox('')
        gboxStyle = ("background-color: #A396EA;" #CEA61D; " #63CBEA;" 
                      "border-style: solid; border-radius: 3; padding: 5px;"
                      "border-color: rgb(255,255,255); border-width: 1px;" )
        groupbox2.setStyleSheet (gboxStyle)    

        chkStyle = ("QCheckBox {background-color: #64b5f6; padding: 5px; }"
                    "QCheckBox::hover {background-color: #E9AEF3; color: #fff;}")
        self.check1 = QCheckBox()
        self.check2 = QCheckBox()
        self.check1.setChecked(True)
        self.check2.setChecked(True)
        
        self.check11 = QCheckBox('All DB tables 검색하기  ')
        self.check22 = QCheckBox('Perfect match of Word ')
        self.check11.setChecked(True)
        self.check22.setChecked(False)

        self.check11.setStyleSheet(chkStyle)
        self.check22.setStyleSheet(chkStyle)
        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.check11, 1, Qt.AlignLeft)
        vbox2.addSpacing(10)  # 단순 공백 추가        
        vbox2.addWidget(self.check22, 1, Qt.AlignLeft)
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
        editStyle = ("QLineEdit {background-color: #FFFAC8; color: blue; " #D9EAF7
                  "padding: 5px; font: bold 11pt; }")

        self.queryText = QLineEdit()
        self.queryText.setMaximumHeight(35)
        self.queryText.installEventFilter(self)
        # self.queryText.textEdited.connect(self.showCurrentText)
        self.queryText.setStyleSheet("background-color: #FFF; color: blue; padding: 5px; font: bold 11pt;\
                                     border-color: rgb(0,0,200); border-width: 1px;")
        
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
        
        lbl1=QLabel("검색 문장")
        lbl2=QLabel("경  로  명")
        lbl3=QLabel("DB테이블")
        
        lblStyle = ("QLabel {background-color: #4285F4; color: white; border-radius: 3;"
                    "border-color: rgb(255,255,255); border-width: 1px;}"
                    "QLabel::hover {background-color: #FF9930; color: #fff;}") #64b5f6 #8F8F00 #001040
        lbl2.setStyleSheet(lblStyle)
        lbl2.mousePressEvent = lambda x: dbFileOpen(self)
        
        vbox3=QGridLayout()
        vbox3.addWidget(lbl1, 0, 0, 1, 1)
        vbox3.addWidget(lbl2, 1, 0, 1, 1)
        vbox3.addWidget(lbl3, 2, 0, 1, 1)
        vbox3.addWidget(self.queryText, 0, 1, 1, 15)
        vbox3.addWidget(self.qLineEdit, 1, 1, 1, 15)
        vbox3.addWidget(self.combo,     2, 1, 1, 15)
        groupbox3.setLayout(vbox3)
        
        # --- 저장/닫기 버튼 -------------------------------------------------
        groupbox4 = QGroupBox('')
        btnSave = QPushButton1(" 검  색 ")
        btnSave.clicked.connect(self.searchDB)   
        btnClose = QPushButton1(" 닫  기 ")
        btnClose.clicked.connect(self.finish)
        
        vbox4 = QVBoxLayout()
        vbox4.addWidget(btnSave,  1, Qt.AlignRight)
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
        self.view.setColumnCount(4)
        self.view.setColumnWidth(0, 54)
        self.view.setColumnWidth(1, 502)
        self.view.setColumnWidth(2, 502)
        self.view.setColumnWidth(3, 100)
        
        self.view.setHorizontalHeaderLabels(["순", "한국어", "English", "테이블"])
        self.view.horizontalHeader().setFixedHeight(50)
        self.view.horizontalHeader().setStretchLastSection(True)    # 마지막 칼럼 확장하기  
        
        self.view.verticalHeader().setVisible(False)
        self.view.verticalHeader().setDefaultSectionSize(60)
        self.view.verticalHeader().setSectionResizeMode(QHeaderView.Interactive) #(QHeaderView.Fixed)
        self.view.setAlternatingRowColors(True)
        self.view.setShowGrid(True)

        self.view.setEditTriggers(QAbstractItemView.DoubleClicked) 

        tblStyle = ("QHeaderView::section {background-color: rgb(173, 255, 47); font-size: 18px; }"
                  "QTableView{ background-color:#D3D3D3; font-size: 18px; padding:0px; } ")   #EBDEF1(연보라)

        self.view.setStyleSheet(tblStyle)
        self.view.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.view.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.view.setSizePolicy(7, 7)  
        self.view.setWordWrap(True)
        
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:

            w = self.geometry().width() - 1200 
            self.view.setColumnWidth(1, 502 + int(w/2))
            self.view.setColumnWidth(2, 502 + int(w/2))

            # if event.oldState() and Qt.WindowMinimized:
            #     print("WindowMinimized")                
            # elif self.windowState() == Qt.WindowMaximized:
            #     print("WindowMaximized")
            # elif event.oldState() == Qt.WindowNoState :
            #     print("WindowMaximized 2")
            
    # ----------------------------------------------------------------------            
    def eventFilter(self, source, e):
        result = super(App33, self).eventFilter(source, e)
        if (e.type() == QEvent.KeyPress and 
            source is self.queryText):
            if e.key() in [Qt.Key_Return, Qt.Key_Enter]:
                self.querySignal.emit()
                # print('key press:', e.key(), e.text())
        return result

    # ----------------------------------------------------------------------                
    # def showCurrentText(self, text):
    #     print('current-text:', text)
              
    # ----- DB 테이블 추가하기 -----------------------------------------------
    def searchDB(self):

        if not os.path.exists(self.dbFileName):  # if not QFile.exists(self.dbFileName):
            QMessageBox.critical(self, "데이터베이스 파일 오류", "데이터베이스 파일이 존재하지 않습니다.")
            return

        specialChar = ' @#$%^&*()_{}[]\|;:<>?/' # ’''"!

        option1 = self.check11.isChecked()  # True인 경우 모든 테이블을 대상으로 검색
        option2 = self.check22.isChecked()  # True인 경우 완벽하게 일치한 문장을 검색
        
        keyWord = self.queryText.text()
        if keyWord == '':
            QMessageBox.critical(self, "검색어 입력 오류", "찾고자 하는 문장의 키워드를 입력하십시오.")
            return
        
        if not option2:  # Perfect match 검색이 아닌경우 키워드를 소문자로 치환
            keyWord = keyWord.lower()
            for i in range(len(specialChar)):   # 특수문자 모두 제거
                keyWord = keyWord.replace(specialChar[i], '')

        conn = QSqlDatabase.addDatabase("QSQLITE")
        conn.setDatabaseName(self.dbFileName)
        conn.open()

        # table 목록 가져오기
        allTables = [self.combo.itemText(i) for i in range(self.combo.count())]

        self.view.clear()
        self.view.blockSignals(True)    # 이벤트 감시 중지
        self.view.setRowCount(0)
        
        row = 0
        try:
            for table in allTables:
                curTable = self.combo.currentText()
                if not option1 and table != curTable: 
                    continue
                
                query = QSqlQuery()
                sql = 'SELECT * FROM ' + table
                query.exec(sql)
                
                while query.next():
                    itm1 = str(query.value(1))
                    itm2 = query.value(2)
                    itm3 = query.value(3)

                    temp2 = itm2
                    temp3 = itm3
                    
                    if not option2:     # Perfect match 가 아닌경우 소문자로 치환
                        temp2 = temp2.lower()
                        temp3 = temp3.lower()
                        
                        for i in range(len(specialChar)):   # 특수문자 모두 제거
                            temp2 = temp2.replace(specialChar[i], '')
                        
                        for i in range(len(specialChar)):   # 특수문자 모두 제거
                            temp3 = temp3.replace(specialChar[i], '')
                    
                    if temp2.find(keyWord) != -1 or temp3.find(keyWord) != -1:
                        itm1 = QTableWidgetItem(itm1)
                        itm2 = QTableWidgetItem(itm2)
                        itm3 = QTableWidgetItem(itm3)                             
                        itm4 = QTableWidgetItem(table)
                        
                        itm1.setFlags(itm1.flags() & ~Qt.ItemIsEditable)    # 해당 비트 클리어
                        itm1.setBackground(QColor(200, 100, 100))
                        itm1.setTextAlignment(Qt.AlignCenter)
                        itm4.setTextAlignment(Qt.AlignCenter)
            
                        self.view.insertRow(row)
                        self.view.setItem(row, 0, itm1)
                        self.view.setItem(row, 1, itm2)
                        self.view.setItem(row, 2, itm3)
                        self.view.setItem(row, 3, itm4)
                        row += 1
                    # end if
                # end while
            # end for
            
            self.view.blockSignals(False)   # 이벤트 감시 재개
            self.view.setAlternatingRowColors(True)
            self.refreshWidth(None)
            self.view.show()
                
        except Exception as err: 
            QMessageBox.critical(self, "DB file open Error!", "%s" % err)
            
        finally:
            if 'conn' in locals():  # DB 연결을 성공했으면 conn변수가 존재함
                conn.close()
            
    # ----- table Widget 가로폭 갱신 -----------------------------------------
    def refreshWidth(self, event):
        w = self.width()-200
        self.view.setColumnWidth(1, int(w/2))
        self.view.setColumnWidth(2, int(w/2))      


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

        self.view.mouseDoubleClickEvent = None
        self.close()
        self.parent.show()  


#///////////////////////////////////////////////////////////////////////////#
#                          PyQt5 윈도/위젯 Examples                          #
#///////////////////////////////////////////////////////////////////////////#

class QPushBtn1(QPushButton):
    def __init__(self, parent = None, *args):
        super().__init__(parent, *args)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.setMinimumHeight(30)
        
class QPushBtn2(QPushButton):
    def __init__(self, parent = None, *args):
        super().__init__(parent, *args)
        # self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        # self.setMinimumHeight(30)

class QPushBtn3(QPushButton):     # 파생 클래스 생성
    def __init__(self, parent = None, *args):
        super().__init__(parent, *args)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumHeight(50)
        btnStyle1 = '''                                               
                QPushButton { background-color: #F7F; border-style: outset; border-width: 2px; border-radius: 10px;
                border-color: beige; font: bold 14px; min-width: 10em; padding: 6px;}
        '''
        btnStyle2 = ("QPushButton {background-color: #1D7EB5; color: white; border-radius: 3; border-color: white;}"
                "QPushButton::hover {background-color: #EA90E1; color: #fff;} " #202D4F #EA90E1
                "QPushButton::pressed {background-color: #F90;}")    
        self.setStyleSheet(btnStyle2)

class QLabel2(QLabel):  
    def __init__(self, parent = None, *args):
        super().__init__(parent, *args)
        self.setMinimumHeight(30)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet('background-color: #00F; color: rgb(255,255,255);')
        
# --------------------------------------------------------------------------
class MyWidget(QWidget): 
    def __init__(self, parent=None): 
        super().__init__() 
        self.parent = parent
        btn1 = QPushButton('1') 
        btn2 = QPushButton('2') 
        layout = QHBoxLayout() 
        layout.addWidget(btn1) 
        layout.addWidget(btn2) 
        self.setLayout(layout) 
        self.setGeometry(300, 100, 350, 150)  # x, y, width, height 
        self.setWindowTitle("QWidget") 
        self.show() 
        
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            self.parent.ex2.close()
            self.parent.ex3.close()
            self.parent.ex4.close()
        else:
            event.ignore()
            
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

class MyMainWindow1(QMainWindow): 
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

# --------------------------------------------------------------------------
class SourceView(QWidget):

    def __init__(self, tabIndex):
        super().__init__()
        self.tabIndex = tabIndex
        self.initUI()

    def initUI(self):

        self.tBrowse = QTextBrowser()
        self.tBrowse.setAcceptRichText(True)
        self.tBrowse.setOpenExternalLinks(True)
        self.tBrowse.setReadOnly(False)
        self.clear_btn = QPushButton('Clear')
        self.clear_btn.pressed.connect(self.clear_text)
        self.clear_btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.clear_btn.setMinimumHeight(30)
        self.add_source()
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.tBrowse,   0)
        vbox.addWidget(self.clear_btn, 1)
        self.setLayout(vbox)
        self.setWindowTitle('QTextBrowser')
        self.resize(900, 600)
        self.center()
        self.show()

    def add_source(self):
        text1 = """
        import sys
        from PyQt5.QtCore import Qt
        from PyQt5.QtGui import QPalette, QColor, QFont
        from PyQt5.QtWidgets import *
        
        class QPushBtn1(QPushButton):     # 파생 클래스 생성
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
                
        class QTabWindow(QMainWindow):
            def __init__(self):
                super().__init__()
        
                self.setWindowTitle('Sidebar layout')
                self.Width = 800
                self.height = int(0.618 * self.Width)
                self.resize(self.Width, self.height)
        
                # add all widgets
                self.btn_1 = QPushBtn1('1', self)
                self.btn_2 = QPushBtn1('2', self)
                self.btn_3 = QPushBtn1('3', self)
                self.btn_4 = QPushBtn1('4', self)
                self.btn_5 = QPushButton('소스코드', self)
                
                self.btn_1.clicked.connect(self.button1)
                self.btn_2.clicked.connect(self.button2)
                self.btn_3.clicked.connect(self.button3)
                self.btn_4.clicked.connect(self.button4)
                self.btn_5.clicked.connect(self.button5)
                
                # add tabs
                self.tab1 = self.ui1()  # self.ui1()의 리턴값 -> QWidget()
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
                left_layout.addWidget(self.btn_5)
                left_layout.setSpacing(20)
                left_widget = QWidget()
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
                QTabWidget::pane { border: 1px solid #FFF; background: #000; padding: 0px; border-top: 1px solid #FF0;}
                QTabBar::tab { background: rgb(200, 100, 200); color: #0F0; border-radius: 3px; border: 1px solid white; min-width: 80px; }
                QTabBar::tab:top { margin: 10px 1px 0 0; padding: 5px 5px; border-bottom: 3px solid lightgray; } /* margin: 상,우,하,좌 */
                QTabBar::tab:selected { color: white; background: #000; border: 0px; } 
                QTabBar::tab:top:hover { border-bottom: 3px solid #444; color: #FF0;}
                QTabBar::tab:top:selected { border-bottom: 3px solid #F00; background: #000;}
                QTabBar::tab:hover, QTabBar::tab:focus { border-bottom: 3px solid #FF0; background: #00F;}
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
        
            def button5(self):
                # self.hide() 
                self.win = SourceView()
                # self.win.show()
               
            # ----------------- # pages
            def ui1(self):
                main_layout = QVBoxLayout()
                # main_layout.addWidget(QLabel('page 1'))
                view = QTableWidget(20,5)
                view.setHorizontalHeaderLabels(["순", "한국어", "English", "암기", "중요"])
                view.horizontalHeader().setFixedHeight(30)
                view.horizontalHeader().setStretchLastSection(True)    # 마지막 칼럼 확장하기  
                # view.verticalHeader().setVisible(False)
                view.verticalHeader().setDefaultSectionSize(30)
                view.verticalHeader().setSectionResizeMode(QHeaderView.Interactive) #(QHeaderView.Fixed)
                view.setAlternatingRowColors(True)
                view.setShowGrid(True)
                
                main_layout.addWidget(view)
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
        
        class SourceView(QWidget):
        
            def __init__(self):
                super().__init__()
                self.initUI()
        
            def initUI(self):
                # self.le = QLineEdit()
                # self.le.returnPressed.connect(self.append_text)
        
                self.tBrowse = QTextBrowser()
                self.tBrowse.setAcceptRichText(True)
                self.tBrowse.setOpenExternalLinks(True)
                self.tBrowse.setReadOnly(False)
                self.clear_btn = QPushButton('Clear')
                self.clear_btn.pressed.connect(self.clear_text)
        
                vbox = QVBoxLayout()
                # vbox.addWidget(self.le, 0)
                vbox.addWidget(self.tBrowse,   0)
                vbox.addWidget(self.clear_btn, 1)
                self.setLayout(vbox)
                self.setWindowTitle('QTextBrowser')
                self.resize(800, 600)
                self.center()
                self.show()
        
            # def append_text(self):
            #     text = self.le.text()
            #     self.tBrowse.append(text)
            #     self.le.clear()
        
            def clear_text(self):
                self.tBrowse.clear()
        
            def center(self):
                qr = self.frameGeometry()
                cp = QDesktopWidget().availableGeometry().center()  # 모니터 중심 좌표
                qr.moveCenter(cp)
                self.move(qr.topLeft())
                
        if __name__ == '__main__':
            app = QApplication(sys.argv)
            app.setPalette(app.style().standardPalette())   # default Palette    
            app.setStyle("Windows")  # ['Windows', 'Fusion', 'Breeze', 'Oxygen', 'QtCurve']
            palette = QPalette()
            palette.setColor(QPalette.Button, QColor(0, 200, 0))
            palette.setColor(QPalette.ButtonText, Qt.red)
            palette.setColor(QPalette.Window, QColor(0, 150, 200))
            palette.setColor(QPalette.WindowText, Qt.blue)
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
            ex = QTabWindow()
            ex.show()
            sys.exit(app.exec_())        
        
        """
        
        text2 = """
        def ui2(self):
            layout = QVBoxLayout()
            win = QWidget()
            win.setLayout(layout)
            btn = QPushButton('push button2')
            btn.setStyleSheet("background-color: #C80; color: rgb(255,255,255); ") #D269E6
            btn.clicked.connect(self.winTest02)
            lbl = QLabel('page 2')
            lbl.setStyleSheet('background-color: #00F; color: rgb(255,255,255);')
            layout.addWidget(btn)
            layout.addWidget(lbl)
            return win        

        def winTest02(self):
            self.Form = QWidget()
            self.Form.resize(430, 240)
            self.Form.setWindowTitle("This is Widget")
            addBtn = QPushButton("ADD", self.Form)
            addBtn.setGeometry(QRect(350, 10, 75, 23))
            # self.addBtn.setObjectName("addBtn")
            textBox = QLineEdit(self.Form)
            textBox.setGeometry(QRect(10, 10, 331, 20))
            textList = QListView(self.Form)
            textList.setGeometry(QRect(10, 40, 331, 192))
            exitBtn = QPushButton("EXIT", self.Form)
            exitBtn.setGeometry(QRect(350, 40, 75, 191))
            self.Form.show()
        """
        
        text3 = """
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

        """
        text4 = """
        def ui4(self):
            layout = QVBoxLayout()
            win = QWidget()
            win.setLayout(layout)
            btn = QPushButton('push button4')
            btn.setStyleSheet("background-color: #D269E6; color: rgb(255,255,255); ") 
            btn.clicked.connect(self.winTest04)
            lbl = QLabel('page 4')
            lbl.setAlignment(Qt.AlignCenter)
            layout.addWidget(btn)
            layout.addWidget(lbl)
            return win  

        def winTest04(self):
            self.ex1 = MyWidget(self)
            self.ex2 = MyDialog() 
            self.ex3 = MyMainWindow1() 
            self.ex4 = MyMainWindow2() 
        """
        text5 = """
        def ui5(self):
            layout = QVBoxLayout()
            view = QTableWidget(20,5)
            view.setHorizontalHeaderLabels(["순", "한국어", "English", "암기", "중요"])
            view.horizontalHeader().setFixedHeight(30)
            view.horizontalHeader().setStretchLastSection(True)    # 마지막 칼럼 확장하기  
            # view.verticalHeader().setVisible(False)
            view.verticalHeader().setDefaultSectionSize(30)
            view.verticalHeader().setSectionResizeMode(QHeaderView.Interactive) #(QHeaderView.Fixed)
            view.setAlternatingRowColors(True)
            view.setShowGrid(True)
            
            layout.addWidget(view)
            win = QWidget()
            win.setLayout(layout)
            return win
        """
        
        if self.tabIndex   == 0:
            text = text1
        elif self.tabIndex == 1:
            text = text2
        elif self.tabIndex == 2:
            text = text3
        elif self.tabIndex == 3:
            text = text4
        else:
            text = text5
            
        self.tBrowse.setFont(QFont('맑은 고딕', 12))
        self.tBrowse.setText(text)
        
    def clear_text(self):
        self.tBrowse.clear()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()  # 모니터 중심 좌표
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
# --------------------------------------------------------------------------
class QTabWindow(QMainWindow):
    def __init__(self, *args):
        self.parent = args[0]
        super().__init__()

        self.setWindowTitle('Tab Widget Example')
        self.Width = 800
        self.height = int(0.618 * self.Width)
        self.resize(self.Width, self.height)

        # add all widgets
        self.btn_1 = QPushBtn3('예제 1', self)
        self.btn_2 = QPushBtn3('예제 2', self)
        self.btn_3 = QPushBtn3('예제 3', self)
        self.btn_4 = QPushBtn3('예제 4', self)
        self.btn_5 = QPushBtn3('예제 5', self)        
        self.source = QPushBtn1('소스코드', self)
        
        self.btn_1.clicked.connect(self.button1)
        self.btn_2.clicked.connect(self.button2)
        self.btn_3.clicked.connect(self.button3)
        self.btn_4.clicked.connect(self.button4)
        self.btn_5.clicked.connect(self.button5)
        self.source.clicked.connect(self.sourceView)        
        
        # add tabs
        self.tab1 = self.ui1()  # self.ui1()의 리턴값 -> QWidget()
        self.tab2 = self.ui2()
        self.tab3 = self.ui3()
        self.tab4 = self.ui4()
        self.tab5 = self.ui5()
        self.initUI()

    def initUI(self):
        left_layout = QVBoxLayout()
        left_layout.addSpacing(3)
        left_layout.addWidget(self.source)  
        left_layout.addWidget(self.btn_1)
        left_layout.addWidget(self.btn_2)
        left_layout.addWidget(self.btn_3)
        left_layout.addWidget(self.btn_4)
        left_layout.addWidget(self.btn_5)          
        left_layout.setSpacing(20)
        
        left_widget = QWidget()
        left_widget.setLayout(left_layout)

        self.right_widget = QTabWidget()
        self.right_widget.tabBar().setObjectName("mainTab")
        self.right_widget.addTab(self.tab1, 'Widget(1)')
        self.right_widget.addTab(self.tab2, 'Widget(2)')
        self.right_widget.addTab(self.tab3, 'Widget(3)')
        self.right_widget.addTab(self.tab4, 'Widget(4)')
        self.right_widget.addTab(self.tab5, 'Widget(5)')
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
        QTabWidget { border: 0px; }
        QTabWidget::pane { border: 1px solid #FFF; background: #000; padding: -6px; border-top: 1px solid #FF0; }
        QTabBar::tab { background: rgb(200, 100, 200); color: #0FF; border-radius: 3px; border: 1px solid white; min-width: 80px; }
        QTabBar::tab:top { margin: 10px 1px 0 0; padding: 5px 5px; border-bottom: 3px solid lightgray; } /* margin: 상,우,하,좌 */
        QTabBar::tab:selected { color: white; background: #000; border: 0px; } 
        QTabBar::tab:top:hover { border-bottom: 3px solid #444; color: #FF0;}
        QTabBar::tab:top:selected { border-bottom: 3px solid #F00; background: #000;}
        QTabBar::tab:hover, QTabBar::tab:focus { border-bottom: 3px solid #FF0; background: #00F;}
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

    # -------------------------------- buttons
    def button1(self):
        self.right_widget.setCurrentIndex(0)

    def button2(self):
        self.right_widget.setCurrentIndex(1)
        
    def button3(self):
        self.right_widget.setCurrentIndex(2)

    def button4(self):
        self.right_widget.setCurrentIndex(3)

    def button5(self):
        self.right_widget.setCurrentIndex(4)
        
    def sourceView(self):
        # self.hide() 
        tabIndex = self.right_widget.currentIndex()
        self.win = SourceView(tabIndex)
        # self.win.show()
       
    # -------------------------------- # ui1 page
    def ui1(self):
        layout = QVBoxLayout()
        win = QWidget()
        win.setLayout(layout)
        lbl = QLabel2('page 1(QLabel)')
        lbl.setAlignment(Qt.AlignCenter)

        self.browse = QTextBrowser()
        btn = QPushBtn2('push button1')
        # btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        btn.clicked.connect(lambda: self.printInfo(win))
        layout.addWidget(lbl)
        layout.addWidget(btn)
        layout.addWidget(self.browse)
        win.setLayout(layout)
        return win
    
    def printInfo(self, win):
        self.browse.append(f'{win.size()}, {win.rect()}')
        self.browse.append(f'{win.width(), win.height()}')              # 400 200        
        self.browse.append(f'{win.pos().y(),win.pos().x()}')            # 300 100     
        self.browse.append(f'{win.geometry().y(),win.geometry().x()}')  # 300 100
        self.browse.append(f'{win.geometry().width(),win.geometry().height()}')             # 400 200
        self.browse.append(f'{win.frameGeometry().width(),win.frameGeometry().height()}')   # 400 200  
    
    # -------------------------------- # ui2 page
    def ui2(self):
        layout = QVBoxLayout()
        win = QWidget()
        win.setLayout(layout)
        btn = QPushBtn2('push button2')
        btn.setStyleSheet("background-color: #C80; color: rgb(255,255,255); ") #D269E6
        btn.clicked.connect(self.winTest02)
        lbl = QLabel2('page 2')
        lbl.setStyleSheet('background-color: #00F; color: rgb(255,255,255);')
        layout.addWidget(btn)
        layout.addWidget(lbl)
        return win        

    def winTest02(self):
        self.Form = QWidget()
        self.Form.resize(430, 240)
        self.Form.setWindowTitle("This is Widget")
        addBtn = QPushBtn2("ADD", self.Form)
        addBtn.setGeometry(QRect(350, 10, 75, 23))
        addBtn.clicked.connect(self.appendList)
        self.textBox = QLineEdit(self.Form)
        self.textBox.setGeometry(QRect(10, 10, 331, 20))
        self.textList = QListView(self.Form)
        self.textList.setGeometry(QRect(10, 40, 331, 192))
        exitBtn = QPushBtn2("EXIT", self.Form)
        exitBtn.setGeometry(QRect(350, 40, 75, 191))
        exitBtn.clicked.connect(self.Form.close)
        self.Form.show()

    def getListItems(self):  # ListView의 목록을 읽어서 리스트에 추가
        self.listItems = []
        for index in range(self.model.rowCount()):
            item = self.model.item(index)
            self.listItems.append(item.text())
        # print(self.listItems)
                    
    def appendList(self):
        
        # [방법 1] - QStringListModel
        # self.model = QStringListModel()
        # list = [] #QStringList()
        # list.append("a")
        # list.append("b")
        # list.append("c")
        # self.model.setStringList(list);
        # self.textList.setModel(self.model)
        
        # [방법 2] - QStandardItemModel
        numbers = ["One", "Two", "Three", "Four", "Five"]
        self.model = QStandardItemModel()
        for x in numbers:
            item = QStandardItem(x)
            item.setCheckable(True)
            item.setCheckState(Qt.Unchecked)
            self.model.appendRow(item)
            self.textList.setModel(self.model)
            
        self.getListItems()
        
        for item in self.listItems:
            self.model.appendRow(QStandardItem(item))
        self.textList.setModel(self.model)
     
    # -------------------------------- # ui3 page
    def ui3(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel2('page 3'))
        
        button_layout = QHBoxLayout()
        btn1 = QPushBtn2("red")
        btn1.pressed.connect(self.activate_tab_1)
        button_layout.addWidget(btn1)

        btn2 = QPushBtn2("green")
        btn2.pressed.connect(self.activate_tab_2)
        button_layout.addWidget(btn2)

        btn3 = QPushBtn2("yellow")
        btn3.pressed.connect(self.activate_tab_3)
        button_layout.addWidget(btn3)

        self.stacklayout = QStackedLayout()
        self.stacklayout.addWidget(self.ColorBox("red"))
        self.stacklayout.addWidget(self.ColorBox("green"))
        self.stacklayout.addWidget(self.ColorBox("yellow"))
        
        pagelayout = QVBoxLayout()
        pagelayout.addLayout(layout)
        pagelayout.addLayout(button_layout)
        pagelayout.addLayout(self.stacklayout)

        widget = QWidget()
        widget.setLayout(pagelayout)
        # widget.setPalette(qApp.style().standardPalette())   # default Palette
        return widget

    def ColorBox(self, color):
        widget = QWidget()
        widget.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        widget.setPalette(palette)
        return widget

    def activate_tab_1(self):
        self.stacklayout.setCurrentIndex(0)

    def activate_tab_2(self):
        self.stacklayout.setCurrentIndex(1)

    def activate_tab_3(self):
        self.stacklayout.setCurrentIndex(2)
        
    # -------------------------------- # ui4 page
    def ui4(self):
        layout = QVBoxLayout()
        win = QWidget()
        win.setLayout(layout)
        btn = QPushBtn2('push button4')
        btn.setStyleSheet("background-color: #D269E6; color: rgb(255,255,255); ") 
        btn.clicked.connect(self.winTest04)
        lbl = QLabel2('page 4')
        lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(btn)
        layout.addWidget(lbl)
        return win  

    def winTest04(self):
        self.ex1 = MyWidget(self)
        self.ex2 = MyDialog() 
        self.ex3 = MyMainWindow1() 
        self.ex4 = MyMainWindow2() 
        
    # -------------------------------- # ui5 page
    def ui5(self):
        layout = QVBoxLayout()
        view = QTableWidget(20,5)
        view.setHorizontalHeaderLabels(["순", "한국어", "English", "암기", "중요"])
        view.horizontalHeader().setFixedHeight(30)
        view.horizontalHeader().setStretchLastSection(True)    # 마지막 칼럼 확장하기  
        # view.verticalHeader().setVisible(False)
        view.verticalHeader().setDefaultSectionSize(30)
        view.verticalHeader().setSectionResizeMode(QHeaderView.Interactive) #(QHeaderView.Fixed)
        view.setAlternatingRowColors(True)
        view.setShowGrid(True)
        
        layout.addWidget(view)
        win = QWidget()
        win.setLayout(layout)
        return win

    # ----- 창 닫기 버는 클릭 -----------------------------------------------           
    def closeEvent(self, event):
        reply = QMessageBox.question(self, '종료 확인!',
            " 프로그램을 종료하시겠습니까? ", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            event.ignore()
        else:
            app.setPalette(QApplication.style().standardPalette())   # default Palette   
            # self.view.mouseDoubleClickEvent = None
            self.close()
            self.parent.show()  
            event.accept()    
        
# -----------------------------  메인 함수  -----------------------------------
if __name__ == '__main__':
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()  

    # QApplication.setPalette(QApplication.style().standardPalette())   # default Palette    
    # QApplication.setStyle("Fusion")  # ['Windows', 'Fusion', 'Breeze', 'Oxygen', 'QtCurve']
    app.setPalette(QApplication.style().standardPalette())   # default Palette   
    app.setStyle('Windows')
    app.setStyleSheet(qss)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

