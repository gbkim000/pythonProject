# https://www.flaticon.com/

# -*- coding: utf-8 -*-
import sys, os, getpass
import sqlite3, openpyxl, re

from pathlib import Path
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlError

class QPushButton(QPushButton):     # 클래스 재정의
    def __init__(self, parent = None, *args):
        super().__init__(parent, *args)
        self.setSizePolicy(7, 7)     # (w:QSizePolicy.Expanding, w:QSizePolicy.Expanding)
        self.setMinimumHeight(30)
        self.setMaximumHeight(50)
        self.setMinimumWidth(100) 
        self.setFont(QFont('맑은 고딕', 13)) #self.setFont(QFont('Georgia', 14))
        style = ("QPushButton{background-color: rgb(0, 50, 200); color: white; "
                   "border-style: solid; border-radius: 5;"
                   "padding: 3px; padding-left: 5px; padding-right: 5px;"
                   "border-color: #339; border-width: 1px; font:Bold; }"
                 "QPushButton::hover {background-color: #FF9900; color: #fff;} "
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
        #self.setFont(QFont('Terminal', 13))
        font = QFont()
        font.setFamily("Segoe UI Symbol")
        font.setPointSize(13)
        self.setFont(font)
        
        # style = ("QPushButton {background-color: #1D7EB5; color: white; border-radius: 3; border-color: white}"
        #           "QPushButton::hover {background-color: #202D4F; color: #fff;} "#202D4F #EA90E1
        #           "QPushButton::pressed {background-color: #FF9900;}") 
        style = ("QPushButton {background-color: #1D7EB5; color: white; border-radius: 3; border-color: white}"
                  "QPushButton::hover {background-color: #EA90E1; color: #fff;} "#202D4F #EA90E1
                  "QPushButton::pressed {background-color: #FF9900;}")    
        self.setStyleSheet(style)

class QGroupBox(QGroupBox):     # 클래스 재정의
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setSizePolicy(7,7)
        # gboxStyle = ("background-color: rgb(255, 224, 192);"
        #               "border-style: solid; border-radius: 3;"
        #               "padding: 3px; padding-left: 10px; padding-right: 10px;"
        #               "border-color: rgb(200,200,200); border-width: 1px;")
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

class DbException(Exception):    # Exception 클래스만 상속받고 구현없음
    pass

# ------ QTableWidget 클래스의 edit() 메서드를 재정의 ------------------------
class QTableWidget(QTableWidget):  

    cell_EditingStarted = pyqtSignal(int, int)
    
    # edit 메서드 재정의
    def edit(self, index, trigger, event):
        result = super(QTableWidget, self).edit(index, trigger, event)
        if result:
            # 셀 편집을 시작할 때 이벤트 시그널 방출
            self.cell_EditingStarted.emit(index.row(), index.column())
        return result

# ----- MyApp 클래스 --------------------------------------------------------

#class MyApp(QWidget):
class MyApp(QTableWidget):
    
    saveFlag = False    # 클래스 변수('True'이면 저자할 데이터 있음)
    
    def __init__(self, *args):
        #super().__init__()
        QTableWidget.__init__(self, *args)
        #QWidget.__init__(self, *args)

        self.resize(1200,1000)
        self.setWindowTitle("엑셀파일에 저장된 암기문장 불러오기(by G.B.KIM)")
 
        userAcount = getpass.getuser()
        path1 = 'C:\\Users\\{0}\\Documents\\'.format(userAcount)        # 일반 사용자 내문서 폴더
        path2 = 'C:\\Users\\{0}\\Documents\\'.format('Administrator')   # 관리자 계정 내문서 폴더
        
        self.pathSave = "C:\\path.txt"
        if os.path.isdir(path1):
            self.pathSave = path1 + "path.txt"
        elif os.path.isdir(path2):
            self.pathSave = path2 + "path.txt"
        
        if os.path.exists(self.pathSave):       # 이전에 접근한 db파일의 경로가 있으면
            with open(self.pathSave, 'r', encoding='utf-8') as f:
                temp = f.read().strip()
        else:
            temp = ''            

        self.getDbFileName(temp)
        self.dispTableView()     
        self.updateComboList()
        
        if self.tableName != '':
            self.dispData()
            self.view.setFocus()
            self.view.setCurrentCell(0, 2)
            
        self.setWindowFlags(
            Qt.Window |
            #Qt.WindowCloseButtonHint |     # 창닫기('X')
            Qt.WindowMinimizeButtonHint |   # 창 최소화
            Qt.WindowMaximizeButtonHint)    # 창 최대화
        
        self.show()
        
    def getDbFileName(self, temp):
        self.dbFileName = ''
        
        dirName, fileName = os.path.split(temp)
        if dirName =='' or fileName =='':
            return
        i = 0
        while not dirName[i].isalpha():
            i += 1
        dirName = dirName[i:]    # 시작문자열에 숨김문자/특수문자 있으면 제거. 

        self.dbFileName = '{0}\\{1}'.format(dirName, fileName)
        os.chdir(dirName)
        
    def dbFileOpen(self):
        curDir = os.getcwd()
        fname, ok = QFileDialog.getOpenFileName(self, 'DB file 지정', curDir, '*.db')
        # 반환값(tuple) -> ('C:/Users/Administrator/PyQtTest/a2.db', '*.db')

        if ok and len(fname) >= 7:   # 'C:\a.db'의 경우 최소 7글자
            fname = fname.replace('/', '\\')
            self.getDbFileName(fname)
            self.qLineEdit.setText(self.dbFileName)
            
            if self.dbFileName != '':
                self.updateComboList()
                
            if self.tableName != '':
                self.dispData()
                QMessageBox.information(self, "DB file open!", " DB 파일을 열고, 테이블 목록을 갱신하였습니다. ")
                with open(self.pathSave, 'w', encoding='utf-8') as f:
                    f.write(self.dbFileName)
            
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
        self.tableName = self.combo.currentText()
        if self.tableName != '':
            self.dispData()
            self.view.setFocus()
            self.view.setCurrentCell(0, 2)
 
    def updateComboList(self):
        # DB 테이블 목록 가져오기
        self.tableName = ''
        self.combo.clear()        
        self.view.setRowCount(0)
        #self.view.clearContents()

        if os.path.exists(self.dbFileName):
            conn = sqlite3.connect(self.dbFileName)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            
            tbnList = cursor.fetchall() # [('DATA_2019_01',), ('DATA_2019_02',), ('DATA_2019_03',)]
            if not bool(tbnList):
                QMessageBox.information(self, "DB 테이블 목록 갱신", "DB 파일에 테이블이 존재하지 않습니다.")
                conn.close()
                return
            
            tbName = tbnList[0][0]      # 첫번째 테이블명을 가져옴
            cursor.execute("PRAGMA table_info(" + tbName + ")" )
            records = cursor.fetchall()
            # records : [(0, 'YMD', 'CHAR(8)', 0, None, 1), (1, 'seq', 'INTEGER', 0, None, 2), (2, 'korean', ...

            errFlag = False
            fieldName = ['YMD', 'seq', 'korean', 'english', 'done', 'point']
            
            if len(records[0]) != len(fieldName):
                errFlag= True
            else:
                for id, row in enumerate(records):
                    if fieldName[id] != row[1]:  # records의 두번째(row[1]) 요소가 필드명임
                        errFlag = True
            if errFlag:
                QMessageBox.critical(self, "DB file error!", "테이블의 필드명 오류입니다. DB파일을 올바르게 지정하세요.")
                conn.close()
                return

            self.combo.blockSignals(True)
            self.combo.clear()
            for row in tbnList:
                self.combo.addItem(row[0])
            self.combo.blockSignals(False)
            
            self.combo.setCurrentIndex(len(tbnList)-1)
            self.tableName = self.combo.currentText()
            conn.close()
            
    def dispTableView(self):
        # --- 맨 좌측 상자 -------------------------------------------------
        groupbox1 = QGroupBox('')
        gboxStyle = ("background-color: #521414 ;"
                      "border-radius: 3; border-color: rgb(200,200,200);")
        groupbox1.setStyleSheet (gboxStyle)
        label = QLabel(" Data importing ")
        gboxStyle = ('QLabel {background-color: #6F1515; color: white; font-size: 25px; font: bold; }')
        label.setStyleSheet(gboxStyle)
        label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        vbox1 = QVBoxLayout()
        vbox1.addWidget(label)
        groupbox1.setLayout(vbox1)
        
        # --- 한국어/영문장 체크 --------------------------------------------
        groupbox2 = QGroupBox('')
        # gboxStyle = ("background-color: rgb(255, 224, 192);"
        #               "border-style: solid; border-radius: 3;"
        #               "padding: 3px; padding-left: 10px; padding-right: 10px;"
        #               "border-color: rgb(200,200,200); border-width: 1px;")
        # groupbox2.setStyleSheet(gboxStyle)    
        
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
        
        btnStyle = ("QPushButton {background-color: #001040; color: white; border-radius: 5;}"
                 "QPushButton::hover {background-color: #4285F4; color: #fff;}" #64b5f6 #8F8F00
                 "QPushButton::pressed {background-color: #FF9900;}")
        
        gboxStyle = ("background-color: #C0CDEF; " #DDEBF7;" #FFE7D8;" #A0B4E6;"
                      "border-style: solid; border-radius: 3;"
                      "padding: 3px; padding-left: 10px; padding-right: 10px;"
                      "border-color: rgb(200,200,200); border-width: 1px;") 
        
        groupbox3.setStyleSheet(gboxStyle)
        dbBtn1 = QPushButton("  DB 파일 / 테이블 선택  ")
        dbBtn1.clicked.connect(self.dbFileOpen) 
        dbBtn1.setStyleSheet(btnStyle)
        dbBtn1.setMinimumWidth(252)
        #dbBtn1.setMaximumWidth(400)
        dbBtn1.setMaximumHeight(35)
        
        dbBtn2 = QPushButton(" 엑셀 파일(문장) 불러오기 ")
        dbBtn2.clicked.connect(self.excelFileOpen) 
        dbBtn2.setStyleSheet(btnStyle)
        dbBtn2.setMinimumWidth(252)
        #dbBtn2.setMaximumWidth(400)
        dbBtn2.setMaximumHeight(35)

        editStyle = ("QLineEdit {background-color: #FFFAC8; color: blue; " #D9EAF7
                 "padding: 5px; font-size: 11pt; font: Bold; }")
        self.qLineEdit = QLineEdit(self.dbFileName)
        self.qLineEdit.setReadOnly(True)
        self.qLineEdit.setMaximumHeight(35)
        self.qLineEdit.setStyleSheet(editStyle)
        #self.qLineEdit.textChanged.connect(self.updateComboList)

        lstStyle = ("QListView{background-color: white; padding: 3px; font-size: 11pt; font: Bold; }"
                    "QListView::item{height: 20px; background-color: white; color: blue;}")
        listView = QListView()
        listView.setSpacing(3)
        listView.setStyleSheet(lstStyle) 
        
        cboStyle = ("QComboBox {background-color: #EBDEF1; padding: 3px; font-size: 11pt; font: Bold; padding: 5px; }")        
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

        # hbox3=QHBoxLayout()
        # hbox3.addWidget(dbBtn1)
        # hbox3.addWidget(dbBtn2)
        # groupBtn = QGroupBox('')
        # groupBtn.setLayout(hbox3)
        # vbox3.addWidget(groupBtn, 0, 1, 1, 15)
        vbox3.addWidget(dbBtn1, 0, 1, 1, 1)
        vbox3.addWidget(dbBtn2, 0, 2, 1, 14, Qt.AlignRight)
        vbox3.addWidget(self.qLineEdit, 1, 1, 1, 15)
        vbox3.addWidget(self.combo,     2, 1, 1, 15)
        groupbox3.setLayout(vbox3)
        
        # --- 저장/닫기 버튼 -------------------------------------------------
        groupbox4 = QGroupBox('')
        # style = ("background-color: #FFE7D8;" #DDEBF7;" 
        #               "border-style: solid; border-radius: 3;"
        #               "padding: 3px; padding-left: 10px; padding-right: 10px;"
        #               "border-color: rgb(200,200,200); border-width: 1px;") 
        # groupbox4.setStyleSheet(style)
        
        btnSave = QPushButton(" 저  장 ")
        btnSave.clicked.connect(self.saveData)   
        
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
        # self.view.itemChanged.connect(self.item_Changed)
        self.view.cell_EditingStarted.connect(self.cell_Editing) 
        
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    # ----- DB 파일 생성하기 -------------------------------------------------
    def createDbase(self):
        
        if MyApp.saveFlag:
            reply = QMessageBox.question(self, '저장 확인!',
                " 저장하지 않은 자료가 있습니다, 저장하시겠습니까? ", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.saveData()
            MyApp.saveFlag = False
                        
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
        self.getDbFileName(fileName)

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
        self.updateComboList()
        self.dispData()
        QMessageBox.information(self, "DB 파일명 생성 성공 !!", "DB 파일 생성을 성공하였습니다.")
        with open(self.pathSave, 'w', encoding='utf-8') as f:
            f.write(self.dbFileName)
        
    # ----- DB 테이블 추가하기 -----------------------------------------------
    def createTable(self):

        if MyApp.saveFlag:
            reply = QMessageBox.question(self, '저장 확인!',
                " 저장하지 않은 자료가 있습니다, 저장하시겠습니까? ", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.saveData()
            MyApp.saveFlag = False
                
        if not os.path.exists(self.dbFileName):
             raise DbException('데이터베이스 파일이 존재하지 않습니다.')
             
        conn = QSqlDatabase.addDatabase("QSQLITE")
        conn.setDatabaseName(self.dbFileName)
        conn.open()
        query = QSqlQuery()
        
        tableName, ok = QInputDialog.getText(self, '추가할 DB 테이블명 입력', 'Enter DB table name(only 한글/영숫자/밑줄):')

        # temp = re.match('[a-zA-Z_]+[0-9]*[a-zA-Z0-9_]*', tableName)
        # if (not ok) or (temp == None):
        #     QMessageBox.information(self, "DB 테이블명 입력 오류!", '테이블명을 입력하지 않았거나 잘못 입력하였습니다.')
        #     return
        # tableName = temp.group(0)
        
        temp = tableName.replace('_', '')
        if not(ok and temp.isalnum()):
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
        
        self.updateComboList()
        self.dispData()
    
    # ----- DB 테이블 삭제하기 -----------------------------------------------
    def dropTable(self):

        if MyApp.saveFlag:
            reply = QMessageBox.question(self, '저장 확인!',
                " 저장하지 않은 자료가 있습니다, 저장하시겠습니까? ", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.saveData()
            MyApp.saveFlag = False
            
        if not os.path.exists(self.dbFileName):
             raise DbException('데이터베이스 파일이 존재하지 않습니다.')
             
        conn = QSqlDatabase.addDatabase("QSQLITE")
        conn.setDatabaseName(self.dbFileName)
        conn.open()
        query = QSqlQuery()
        
        tableName, ok = QInputDialog.getText(self, '삭제할 DB 테이블명 입력', 'Enter DB table name(only 한글/영숫자/밑줄):')
        
        temp = tableName.replace('_', '')
        if not(ok and temp.isalnum()):
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
        
        self.tableName = ''
        self.updateComboList()
        self.dispData()
                
    # ----- 테이블에 데이터 저장하기 ------------------------------------------
    def saveData(self):
        
        if MyApp.saveFlag == False:
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
            
            sql = 'DELETE FROM ' + self.tableName
            query.exec(sql)
            
            rows = self.view.rowCount()
            for row in range(rows):

                if self.view.item(row, 0) is None:
                    continue

                itm0 = int(self.view.item(row, 0).text())
                itm1 = self.view.item(row, 1).text()
                itm2 = self.view.item(row, 2).text()
                itm9 = self.view.item(row, 5).text()
                # itm3 = '0'
                # itm4 = '0'

                sql = "INSERT INTO " + self.tableName
                sql += "(YMD, seq, korean, english) VALUES('%s', %d, '%s', '%s')" % (itm9, itm0, itm1, itm2)
                #sql += "(YMD, seq, korean, english, done, point) VALUES('%s', %d, '%s', '%s', '%s', '%s')" % ('20050501', itm0, itm1, itm2, itm3, itm4)
                query.exec(sql)
                
            conn.commit()
            MyApp.saveFlag = False
            QMessageBox.information(self, " 저장 완료 ", "암기 문장을 DB 테이블에 저장했습니다.")
        except Exception as error:
        
            QMessageBox.critical(self, "DB file Save Error!", "%s" % error)
            
        finally:
            if 'conn' in locals():   # DB 연결을 성공했으면 conn변수가 존재함
                conn.close()
                
    # ----- DB 파일 데이터 가져오기 -----------------------------------------
    def dispData(self):
        
        if MyApp.saveFlag:
            reply = QMessageBox.question(self, '저장 확인!',
                " 저장하지 않은 자료가 있습니다, 저장하시겠습니까? ", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.saveData()
            MyApp.saveFlag = False
            
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
                self.view.setRowCount(0)
                #self.view.clearContents()
                return
            
            self.view.blockSignals(True)    # 이벤트 감시 중지
            self.view.setRowCount(rows)
            for row in range(rows):
                itm1 = QTableWidgetItem(str(rowList[row][1]))  
                itm2 = QTableWidgetItem(rowList[row][2])
                itm3 = QTableWidgetItem(rowList[row][3])
                itm4 = QTableWidgetItem(rowList[row][4])
                itm5 = QTableWidgetItem(rowList[row][5])
                itm9 = QTableWidgetItem(rowList[row][0]) # row[0] - YMD
                
                itm1.setFlags(itm1.flags() & ~Qt.ItemIsEditable)
                itm1.setBackground(QColor(200, 100, 100))
                itm1.setTextAlignment(Qt.AlignCenter)
                itm4.setTextAlignment(Qt.AlignCenter)
                itm5.setTextAlignment(Qt.AlignCenter)
                itm4.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled) # 편집불가
                itm5.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled) # 편집불가
                
                self.view.setItem(row, 0, itm1)
                self.view.setItem(row, 1, itm2)
                self.view.setItem(row, 2, itm3)
                self.view.setItem(row, 3, itm4)
                self.view.setItem(row, 4, itm5)
                self.view.setItem(row, 5, itm9)
                
            self.view.blockSignals(False)   # 이벤트 감시 재개
            self.view.setAlternatingRowColors(True)
            self.refreshWidth()           
            self.view.show()
            
        except Exception as e: 
            QMessageBox.critical(self, "DB file open Error!", "%s" % e)
            
        finally:
            if 'conn' in locals():  # DB 연결을 성공했으면 conn변수가 존재함
                conn.close()

    # ----- 엑셀 파일 데이터 가져오기 ----------------------------------------
    def dispExcelData(self, excelFileName):

        if MyApp.saveFlag:
            
            reply = QMessageBox.question(self, '저장 확인!',
                " 저장하지 않은 자료가 있습니다, 저장하시겠습니까? ", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.No:
                return
            self.saveData()
            
        try:
            if not os.path.exists(excelFileName):
                 raise DbException('문장을 저장한 엑셀 파일이 존재하지 않습니다.')
    
            wb = openpyxl.load_workbook(excelFileName) 
            sheet = wb.active # wb.get_sheet_by_name('LOG')
            
            max_row = sheet.max_row
            max_column  = sheet.max_column
            
            self.view.setRowCount(max_row)
            self.view.blockSignals(True)    # 이벤트 감시 중지
            
            rowCnt = 0
            for idx, row in enumerate(sheet.iter_rows(max_row = max_row)):
  
                if (row[1].value is None) or idx == 0:
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
            self.refreshWidth()
            self.view.show()
            if rowCnt > 0:
                MyApp.saveFlag = True
            
        except Exception as e:
            QMessageBox.critical(self, "DB Error!"," %s" % e)
            
        finally:
            if 'conn' in locals():   # DB 연결을 성공했으면 conn변수가 존재함
                conn.close()

    # ----- 셀 편집 시작할 때 발생 -------------------------------------------
    def refreshWidth(self):    
        w = self.width()-200
        self.view.setColumnWidth(1, int(w/2))
        self.view.setColumnWidth(2, int(w/2))   
            
    # ----- 셀 편집 시작할 때 발생 -------------------------------------------
    def cell_Editing(self, row, col):
        self.cellEditing = True
        MyApp.saveFlag = True
        
    # ----- 셀 편집 종료 후 값이 바뀌었을 때 발생 -----------------------------        
    def item_Changed(self, data):
        row = self.view.currentRow()
        col = self.view.currentColumn()
        # print("item_Changed (%d, %d) : %s " % (row, col, data.text())) 
        # self.cellEditing = False
        
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
        
    # ----- 선택한 셀이 바뀌면 발생하는 이벤트 ---------------------------------
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
        if self.cellEditing:
            return
        
        row = self.view.currentRow()
        col = self.view.currentColumn()
        rowCnt = self.view.rowCount()   
            
        if e.modifiers() & Qt.ControlModifier:  # print("Ctrl")      
            if row > 0:
                self.view.setCurrentCell(row-1, col)
                
        elif e.modifiers() & Qt.ShiftModifier:  # print('Shift')
            if row < rowCnt-1:
                self.view.setCurrentCell(row+1, col)   
                
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
                    "font-size: 20px; font:bold; line-height: 150%;"
                    "qproperty-alignment: 'AlignVCenter | AlignLeft';"
                    "text-align: center;"
                    "padding-left:20px; padding-top:20px;"
                    "padding-right:20px; padding-bottom:20px;")
            
            text =("<H1 text-align:center> 도움말 보기 화면</H1>\
                    <ul><li> 화면 위로 스크롤하기 : &lt;Ctrl&gt;</li>\
                        <li> 화면 아래 스크롤하기 : &lt;Shift&gt;</li>\
                        <li> 북마크 표시로 이동하기 : &lt;Esc&gt;</li>\
                        <li> 도움말 보기 : &lt;F1&gt;</li>\
                        <li> 북마크 표시 :[암기/중요]필드에 '9';</li>\
                    </ul>")
            
            tBrowser.append(text)
            tBrowser.setStyleSheet(style)
            tBrowser.setAcceptRichText(True)        # 서식있는 문자 허용
            win.show()
            
        rowIndex = self.view.currentIndex().row()
        item = self.view.item(rowIndex, col)
        self.view.scrollToItem(item, QAbstractItemView.PositionAtTop) # PositionAtCenter) 
               
    # ----- 창 닫기 버는 클릭 -----------------------------------------------           
    def closeEvent(self, event):
        
        event.ignore()  # event.accept()
        
    # ----- 종료 확인 메시지 출력 --------------------------------------------
    def finish(self):
        
        reply = QMessageBox.question(self, '종료 확인!',
            " 프로그램을 종료하시겠습니까? ", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return
        
        if MyApp.saveFlag:
            reply = QMessageBox.question(self, '저장 확인!',
                " 저장하지 않은 자료가 있습니다, 저장하시겠습니까? ", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.saveData()
        QApplication.instance().quit()

# ----- 메인함수 ------------------------------------------------------------ 
def main():
    app = QApplication( sys.argv )
    mainWin = MyApp()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
