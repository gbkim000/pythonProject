# -*- coding: utf-8 -*-
# https://www.flaticon.com/
# curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
# python get-pip.py

# 수정할 내용 : db 읽어온 후 암기, 미암기, 중요 보기 수정
# 마우스 이벤트 implemnentation
# 툴바 아이콘

import sys, os, getpass
import sqlite3, openpyxl, re
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlError

# QSizePolicy.Expanding:7, QSizePolicy.Fixed:0, QSizePolicy.Minimum(QSizePolicy.GrowFlag):1
# QSizePolicy.Maximum(QSizePolicy.ShrinkFlag):4, QSizePolicy.Preferred:5, QSizePolicy.Expanding:7
# QSizePolicy.MinimumExpanding:3, QSizePolicy.Ignored:13
# Fixed(0)      : SizeHint() 크기에 따리 위젯의 크기에 정해짐.
# Minimum(1)    : SizeHint()를 반영하긴 하지만 더 커질 수 있음.
# Expanding(7)  : 창의 크기에 맞추어 위젯들이 창을 공백 없이 채움.

class QPushButton(QPushButton):
    def __init__(self, parent = None, *args):
        super().__init__(parent, *args)
        self.setSizePolicy(7, 7)     # (w:QSizePolicy.Expanding, w:QSizePolicy.Expanding)
        self.setMinimumHeight(30)
        self.setMaximumHeight(50)
        self.setMinimumWidth(100) 
        self.setFont(QFont('맑은 고딕', 13)) #self.setFont(QFont('Georgia', 14))
        style = ("QPushButton{background-color: rgb(0, 50, 200); color: white; "
                   "border-style: solid; border-radius: 5; font:Bold; "
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
                
class QGroupBox(QGroupBox):
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
        
class QCheckBox(QCheckBox):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setSizePolicy(7,7)
        self.setFont(QFont('Times', 10))

class DbException(Exception):    # Exception만 상속받고 구현없음
    pass

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
# class MyApp(QWidget):
class MyApp(QTableWidget):    
    
    saveFlag = False    # 클래스 변수
    modifiedRow = []

    def __init__(self, *args):
        # super().__init__()
        QTableWidget.__init__(self, *args)
        #QWidget.__init__(self, *args)
        
        self.resize(1200,1000)
        self.setWindowTitle("영문장 암기 프로그램(by G.B.KIM)")
        
        self.bookMark = []
        self.bookCnt = 0
        
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
        # self.Dir = os.path.dirname(temp).strip() 
        # self.fileName = os.path.basename(temp).strip()
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

    def chkStateLanguage(self):
        #self.updateComboList()
        self.dispData()
        
    def dispTableView(self):
        # --- 맨 좌측 상자 -------------------------------------------------
        groupbox1 = QGroupBox('')
        gboxStyle = ("background-color: #00008C; " #521414 ;"
                      "border-radius: 3; border-color: rgb(200,200,200);")
        groupbox1.setStyleSheet (gboxStyle)
        self.label = QLabel("Memorizing")
        gboxStyle = ("QLabel {background-color: #00008C; color: white; font-size: 25px; font: bold; }") #6F1515
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
        self.check1.stateChanged.connect(self.chkStateLanguage)        
        self.check2.stateChanged.connect(self.chkStateLanguage)
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
        dbBtn1.clicked.connect(self.dbFileOpen) 
        dbBtn1.setStyleSheet(btnStyle)
        dbBtn1.setMinimumWidth(252)
        #dbBtn1.setMaximumWidth(400)
        dbBtn1.setMaximumHeight(35)
        
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
        
        vbox4=QGridLayout()
        vbox4.addWidget(lbl1, 0, 0, 1, 1)
        vbox4.addWidget(lbl2, 1, 0, 1, 1)
        vbox4.addWidget(lbl3, 2, 0, 1, 1)

        # hbox3=QHBoxLayout()
        # hbox3.addWidget(dbBtn1)
        # hbox3.addWidget(dbBtn2)
        # groupBtn = QGroupBox('')
        # groupBtn.setLayout(hbox3)
        # vbox4.addWidget(groupBtn, 0, 1, 1, 15)
        vbox4.addWidget(dbBtn1, 0, 1, 1, 15)
        vbox4.addWidget(self.qLineEdit, 1, 1, 1, 15)
        vbox4.addWidget(self.combo,     2, 1, 1, 15)
        groupbox4.setLayout(vbox4)        
        
        # --- 검색/닫기 버튼 -------------------------------------------------
        groupbox5 = QGroupBox('')
        # style = ("background-color: #FFE7D8;" #DDEBF7;" 
        #               "border-style: solid; border-radius: 3;"
        #               "padding: 3px; padding-left: 10px; padding-right: 10px;"
        #               "border-color: rgb(200,200,200); border-width: 1px;") 
        # groupbox4.setStyleSheet(style)
        
        btnSave = QPushButton(" 저  장 ")
        btnSave.clicked.connect(self.saveData)   
        
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
        # self.view.itemChanged.connect(self.item_Changed)
        self.view.mouseDoubleClickEvent = self.refreshWidth
        # self.view.doubleClicked.connect(self.cell_doubleClicked)
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
        
    # ----- 수정된 데이터 DB에 업데이트 ---------------------------------------
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

            for row in MyApp.modifiedRow:

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
            MyApp.saveFlag = False
            MyApp.modifiedRow.clear()            
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
      
    # ----- DB읽기(방식1) : Sqlite3 전용 DB 읽기 -----------------------------
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

                if not self.check1.isChecked():
                    itm2.setForeground(QColor("#c4c4c4")) # 또는 QColor('gray')
                    itm2.setBackground(QColor("#c4c4c4"))
                    
                if not self.check2.isChecked():
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
            
        except Exception as e: 
            QMessageBox.critical(None, "DB file open Error!", "%s" % e)
            
        finally:
            if 'conn' in locals():  # DB 연결을 성공했으면 conn변수가 존재함
                conn.close()

    # ----- DB읽기(방식2) : Sqlite, MySQL 등 범용 db 파일 ---------------------
    def dispData2(self):

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
            
            conn = QSqlDatabase.addDatabase("QSQLITE")
            conn.setDatabaseName(self.dbFileName)
            conn.open()
            
            query = QSqlQuery()
            sql = 'SELECT * FROM ' + self.tableName
    
            if not query.exec(sql):
                raise DbException('테이블이 존재하지 않습니다.')

            self.bookMark.clear()
            self.view.blockSignals(True)    # 이벤트 감시 중지
            self.view.setRowCount(0)
            
            while query.next():
                row = self.view.rowCount()
                self.view.setRowCount(row + 1)
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
                
                itm1.setFlags(itm1.flags() & ~Qt.ItemIsEditable)
                itm1.setBackground(QColor(200, 100, 100))
                itm1.setTextAlignment(Qt.AlignCenter)
                itm4.setTextAlignment(Qt.AlignCenter)
                itm5.setTextAlignment(Qt.AlignCenter)

                if not self.check1.isChecked():
                    itm2.setForeground(QColor("#c4c4c4")) # 또는 QColor('gray')
                    itm2.setBackground(QColor("#c4c4c4"))
                    
                if not self.check2.isChecked():
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
            
        except Exception as e: 
            QMessageBox.critical(self, "DB file open Error!", "%s" % e)
            
        finally:
            if 'conn' in locals():  # DB 연결을 성공했으면 conn변수가 존재함
                conn.close()

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
        MyApp.saveFlag = True
        
    # ----- 셀 편집 종료 후 값이 바뀌었을 때 발생 -----------------------------        
    def item_Changed(self, data):
        row = self.view.currentRow()
        col = self.view.currentColumn()
        # print("item_Changed (%d, %d) : %s " % (row, col, data.text())) 
        # self.cellEditing = False
        
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
            data = QTableWidgetItem(data)
            data.setTextAlignment(Qt.AlignCenter)   

        self.view.blockSignals(True)
        self.view.setItem(row, col, data)
        self.view.blockSignals(False)

        MyApp.saveFlag = True
        if not (row in MyApp.modifiedRow):
            MyApp.modifiedRow.append(row)
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
            temp = QTableWidgetItem(temp)
            temp.setTextAlignment(Qt.AlignCenter)
            
            self.view.blockSignals(True)
            self.view.setItem(row, col, temp)
            self.view.blockSignals(False)
 
            MyApp.saveFlag = True
            if not (row in MyApp.modifiedRow):
                MyApp.modifiedRow.append(row)
            self.cellEditing = False
            
    def cell_doubleClicked(self, event):
        row = self.view.currentIndex().row()
        col = self.view.currentIndex().column()
        print(f"double clicked ({row}, {col})")
  
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
        if self.cellEditing:
            return
        
        row = self.view.currentRow()
        col = self.view.currentColumn()
        rowCnt = self.view.rowCount()   
            
        if e.modifiers() & Qt.ControlModifier:  # print("Ctrl")      
            if row > 0:
                self.view.setCurrentCell(row-1, col)
                self.tableScroll(row, col)
                
        elif e.modifiers() & Qt.ShiftModifier:  # print('Shift')
            if row < rowCnt-1:
                self.view.setCurrentCell(row+1, col)   
                self.tableScroll(row, col)
        
        elif e.key() == Qt.Key_F2:
            self.view.editItem(self.view.currentItem())
            
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
                        <li> 북마크 표시 :[암기/중요]필드에 '9';</li>\
                        <li> 문장 수정하기 : &lt;F2&gt;</li>\
                        <li> 테이블 다시 그리기 : &lt;더블클릭&gt;</li>\
                        <li> 도움말 보기 : &lt;F1&gt;</li></ul>")
            tBrowser.append(text)
            tBrowser.setStyleSheet(style)
            tBrowser.setAcceptRichText(True)        # 서식있는 문자 허용
            win.show()

        elif e.key() == Qt.Key_Escape:
            if len(self.bookMark) > 0:
                rowPosi = self.bookMark[self.bookCnt]
                self.view.setCurrentCell(rowPosi, 2)
                self.bookCnt += 1
                self.bookCnt %= len(self.bookMark)
    
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
        
        self.view.mouseDoubleClickEvent = None
        QApplication.instance().quit()
        
# ----- 메인함수 ------------------------------------------------------------ 
def main():
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()  

    mainWin = MyApp()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

''' ------------------------------------------------------------------------
# https://wikidocs.net/36794(공학자를 위한 PySide2)
header = view.horizontalHeader()
header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
view.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)   # 0 : 컬럼번호        

# --------------------------------------------------------------------------
QBoxLayout 
    setLayoutDirection(Qt.LeftToRight) 
    setStretch(index, stretch) 
    setSpacing(spacing) 
    setStretchFactor(object, stretch) 
    addWidget(object, stretch) 
    addLayout(layout, stretch) 
    addSeparator() 
    addSpacing(size) 
    addSpacerItem() 
    addStretch(index, stretch)
    
QGridLayout 
    setColumnStretch(column, stretch) 
    setRowStretch(row, stretch) 
    addWidget(object, fromRow, fromColumn, rowSpan, columnSpan)

출처: https://lifeiseggs.tistory.com/866 [어쩌다 한번 하는 삽질]

# --------------------------------------------------------------------------
QBoxLayout
    addSpacing(self, int)   # 단순히 고정된 크기의 공백을 추가.
    addStretch(self, int stretch = 0) # 창의 크기에 따라 늘어나는 공백을 추가
    setStretchFactor(self, QWidget, int) # 늘림 비율 인자의 크기를 특정 크기로 맟추어 준다.
    setStretchFactor(self, QLayout, int) # 늘림 비율 인자의 크기를 특정 크기로 맟추어 준다.

    * 이것을 코드와 스크린샷을 비교해서 살펴보면 아래와 같다.
    buttonLayout = QHBoxLayout()
    buttonLayout.addSpacing(20) # 고정 크기의 공백 20개 추가
    buttonLayout.addWidget(okButton)
    buttonLayout.setStretchFactor(okButton, 2)      # 늘림 비율을 2로 셋팅
    buttonLayout.addStretch(3)                      # 늘림 비율을 3으로 셋팅
    buttonLayout.addWidget(cancelButton)
    buttonLayout.setStretchFactor(cancelButton, 5)  # 늘림 비율을 5으로 셋팅
 
QGridLayout
    setRowStretch(self, int, int)       # 행번호, 늘림인자
    setColumnStretch(self, int, int)    # 열번호, 늘림인자

출처: http://blog.bluekyu.me/2010/08/pyqt-%EB%82%98%EC%95%84%EA%B0%80%EA%B8%B0-5-1.html

'''