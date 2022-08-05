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
        self.setMinimumWidth(120) 
        self.setFont(QFont('맑은 고딕', 14)) #self.setFont(QFont('Georgia', 14))
        style = ("QPushButton{background-color: rgb(0, 50, 200); color: white; "
                    "border-style: solid; border-radius: 5;"
                    "padding: 3px; padding-left: 5px; padding-right: 5px;"
                    "border-color: #339; border-width: 1px; font:Bold; }"
                 "QPushButton::hover {background-color: #FF9900; color: #fff;} "
                 "QPushButton::pressed {background-color: #142090;}")
        self.setStyleSheet(style)
        
class QPushButton2(QPushButton):     # 파생 클래스
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
        #font.setBold(True)
        font.setWeight(75)
        self.setFont(font)
        style = ("QPushButton {background-color: #D080F0; color: white; border-radius: 5;}"
                 "QPushButton::hover {background-color: #000000; color: #fff;} "
                 "QPushButton::pressed {background-color: #FF9900;}")        
        self.setStyleSheet(style)

class QGroupBox(QGroupBox):     # 클래스 재정의
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setSizePolicy(7,7)

class DbException(Exception):    # Exception 클래스만 상속받고 구현없음
    pass

# class QFileDialog2(QFileDialog):
#     def __init__(self,parent=None):
#         QFileDialog.__init__(self,parent)
#         self.currentChanged.connect(self.check_first)
#         for bb in self.children():
#             if bb.__class__ == QDialogButtonBox:
#                 self.OK = bb.buttons()[0]
#             if bb.__class__ == QLineEdit:
#                 bb.textChanged.connect(self.check_first)

#     def check_first(self, filestring):
#         print("check")
#         if os.path.exists(self.selectedFiles()[0]):
#             self.OK.setEnabled(True)
#             print("OK")
#         else:
#             self.OK.setEnabled(False)
#             print("Not OK")
            
# ----- MyApp 클래스 --------------------------------------------------------

class MyApp(QWidget):
# class MyApp(QTableWidget):
    
    saveFlag = False    # 클래스 변수
    
    def __init__(self, *args):
        #super().__init__()
        #QTableWidget.__init__(self, *args)
        QWidget.__init__(self, *args)

        # savePath= os.getcwd()
        # #QFileDialog2.getSaveFileName(self, 'DB file 생성', savePath, '*.db')
                
        #saveFile.buttonBox.button()
        # saveFile.setOption(QFileDialog.DontUseNativeDialog)
        # saveFile.setLabelText(QFileDialog.Reject, tr("Cancell change"))
        # saveFile.setStandardButtons(QMessageBox.Ok)
        # saveFile.getSaveFileName(self, 'DB file 생성', savePath, '*.db')

        '''
        One option is to override your dialog's show event so as to allow the QDialogButtonBox to be shown, 
        after which it will have set a default button with an AcceptRole, 
        and to then set all buttons to not be defaults.
        
        void MyDialog::showEvent(QShowEvent* event)
        {
            // When a QDialogButtonBox is shown, it will set a default button if none are found so we need to disable the
            // default buttons after the button box has been shown.
            QDialog::showEvent(event);
        
            // For example, with a dialog which has two buttons, Save and Cancel, we remove all defaults
            // It might be good enough to remove the default on just the buttons with have the AcceptRole, but
            // I didn't test extensively enough to see what would happen if any buttons had "autoDefault" set or
            // verify this behavior on all platforms.
            ui->buttonBox->button(QDialogButtonBox::Save)->setDefault(false);
            ui->buttonBox->button(QDialogButtonBox::Cancel)->setDefault(false);
        }
        '''
        self.resize(1200,1000)
        self.setWindowTitle("엑셀파일에 저장된 암기문장 불러오기(by G.B.KIM)")
        self.pathSave= 'C:\\Users\\{0}\\Documents\\'.format('Administrator')
        self.pathSave = self.pathSave + "path.txt"

        temp = ""
        if os.path.exists(self.pathSave):
            with open(self.pathSave, 'r', encoding='utf-8') as f:
                temp = f.read().strip()
        else:
            temp = os.path.dirname(self.pathSave).strip() 
            temp = temp + "\\*.db"
            
        self.getDbFileName(temp)
        self.dispTableView()     
        self.updateComboList()
        
        if self.tableName != "":
            self.dispData()
            self.view.setFocus()
            self.view.setCurrentCell(0, 2)
            
        self.setWindowFlags(
            Qt.Window |
            #Qt.WindowCloseButtonHint |
            Qt.WindowMinimizeButtonHint |
            Qt.WindowMaximizeButtonHint)  
        self.show()
        
    def getDbFileName(self, temp):
        self.Dir, self.fileName = os.path.split(temp)
        if self.Dir != "" and not self.Dir[0].isalpha():
            self.Dir = self.Dir[1:]    # 시작문자열에 숨김문자 있으면 제거.
        self.dbFileName = '{0}\\{1}'.format(self.Dir, self.fileName)
        os.chdir(self.Dir)
        
    def dbFileOpen(self):
        curDir = os.getcwd()
        fname, ok = QFileDialog.getOpenFileName(self, 'DB file 지정', curDir, '*.db')
        # 반환값(tuple) -> ('C:/Users/Administrator/PyQtTest/a2.db', '*.db')
        if ok and len(fname) >= 7:   # 'C:\a.db'의 경우 최소 7글자
            fname = fname.replace('/', '\\')
            self.getDbFileName(fname)
            self.qLineEdit.setText(self.dbFileName)
            self.updateComboList()
            
            if self.tableName != "":
                self.dispData()
                QMessageBox.information(self, "DB file open!", " DB 파일을 열고, 테이블 목록을 갱신하였습니다. ")
                with open(self.pathSave, 'w', encoding='utf-8') as f:
                    f.write(self.dbFileName)
            
    def excelFileOpen(self):
        curDir = os.getcwd()

        #https://doc.qt.io/qtforpython/PySide6/QtWidgets/QDialogButtonBox.html#PySide6.QtWidgets.PySide6.QtWidgets.QDialogButtonBox        
        self.QFD = QFileDialog()
        QFD.buttonBox = QDialogButtonBox(QDialogButtonBox.Open | QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        QFD.buttonBox.accepted.connect(QFD.accept)
        QFD.buttonBox.rejected.connect(QFD.reject)
        
        fname, ok = QFD.getOpenFileName(self, '엑셀 (문장) 파일 지정', curDir, '*.xlsx')
        
        # fname, ok = QFileDialog.getOpenFileName(self, '엑셀 (문장) 파일 지정', curDir, '*.xlsx')
        # 반환값(tuple) -> ('C:/Users/Administrator/Documents/DataDB/DATA_2021_00.xlsx', '*.xlsx')
        
        if ok and len(fname) >= 8:   # 'C:\a.xls'의 경우 최소 8글자
            excelFileName = fname.replace('/', '\\')
            self.dispExcelData(excelFileName)
            msg = "엑셀 파일로부터 암기할 문장을 가져왔습니다. \n\n \
                저장할 [DB테이블]을 선택 후 [저장] 버튼을 클릭하세오. "
            QMessageBox.information(self, "엑셀 파일 가져오기", msg)
            
    def changedCombo(self):
        self.tableName = self.combo.currentText()
        if self.tableName != "":
            self.dispData()
            self.view.setFocus()
            self.view.setCurrentCell(0, 2)
 
    def updateComboList(self):
        # DB 테이블 목록 가져오기
        self.tableName = ""
        self.combo.clear()        
        self.view.setRowCount(0)

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
        stylesheet = ("background-color: rgb(0, 0, 140);"
                      "border-radius: 3; border-color: rgb(200,200,200);")
        groupbox1.setStyleSheet (stylesheet)
        label = QLabel("Data importing")
        stylesheet = ('QLabel {background-color: #00008B; color: white; font-size: 25px; font: bold; }')
        label.setStyleSheet(stylesheet)
        label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        vbox1 = QVBoxLayout()
        vbox1.addWidget(label)
        groupbox1.setLayout(vbox1)
        
        # --- 한국어/영문장 체크 --------------------------------------------
        groupbox2 = QGroupBox('')
        stylesheet = ("background-color: rgb(255, 224, 192);"
                      "border-style: solid;"
                      "border-radius: 3;"
                      "padding: 3px;"
                      "padding-left: 10px;"
                      "padding-right: 10px;"
                      "border-color: rgb(200,200,200);"
                      "border-width: 1px;" )
        groupbox2.setStyleSheet (stylesheet)    
        
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
        style = ("QPushButton {background-color: #8F8F00; color: white; border-radius: 5;}"
                 "QPushButton::hover {background-color: #000000; color: #fff;}" #64b5f6
                 "QPushButton::pressed {background-color: #FF9900;}")
        dbBtn1 = QPushButton("  DB 파일 / 테이블 선택  ")
        dbBtn1.clicked.connect(self.dbFileOpen) 
        dbBtn1.setStyleSheet(style)
        dbBtn1.setMinimumWidth(250)
        dbBtn1.setMaximumWidth(250)
        dbBtn1.setMaximumHeight(35)
        
        dbBtn2 = QPushButton(" 엑셀 파일(문장) 불러오기 ")
        dbBtn2.clicked.connect(self.excelFileOpen) 
        dbBtn2.setStyleSheet(style)
        dbBtn2.setMinimumWidth(250)
        dbBtn2.setMaximumWidth(250)
        dbBtn2.setMaximumHeight(35)

        style = ("QLineEdit {background-color: #D9EAF7; color: blue; "
                 "padding: 3px; font-family: Times; font-size: 11pt; font:Bold; }")
        self.qLineEdit = QLineEdit(self.dbFileName)
        self.qLineEdit.setReadOnly(True)
        self.qLineEdit.setMaximumHeight(35)
        self.qLineEdit.setStyleSheet(style)
        #self.qLineEdit.textChanged.connect(self.updateComboList)

        style = ("QComboBox {padding: 3px; font-family: Times; font-size: 11pt; font:Bold; color: blue; }")        
        self.combo = QComboBox()
        self.combo.setMaximumHeight(35)
        self.combo.setStyleSheet(style)
        listView = QListView()
        listView.setSpacing(3)
        listView.setFont(QFont('Times', 11, QFont.Bold))
        # listView.setStyleSheet("QListView::item{height: 20px; background-color: #EBDEF1; color: blue;}")       
        self.combo.setView(listView)
        self.combo.activated.connect(self.changedCombo)             # 사용자가 list 목록을 변경시 호출
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
        btnSave.clicked.connect(self.saveData)   
        
        btnClose = QPushButton(" 닫  기 ")
        btnClose.clicked.connect(self.finish)
        
        vbox4 = QVBoxLayout()
        vbox4.addWidget(btnSave, 1, Qt.AlignRight)
        vbox4.addWidget(btnClose, 1, Qt.AlignRight)
        groupbox4.setLayout(vbox4)

        # ---  layout 구성하기 ----------------------------------------------
        layout1 = QHBoxLayout()
        layout1.addWidget(groupbox1, 2)
        layout1.addWidget(groupbox2, 2)
        layout1.addWidget(groupbox3, 5)
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
        self.view.setColumnWidth(0, 50)
        self.view.setColumnWidth(1, 500)
        self.view.setColumnWidth(2, 500)
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

        style0 = ("QHeaderView::section {background-color: rgb(173, 255, 47); font-size: 18px; }"
                  "QTableView{ background-color:#D3D3D3; font-size: 18px; padding:0px; } ")   #EBDEF1(연보라)

        self.view.setStyleSheet(style0)
        self.view.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.view.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.view.setSizePolicy(7, 7)  
        self.view.setWordWrap(True)

        self.view.itemChanged.connect(self.cell_Changed)
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
            saveFlag = False
                        
        savePath = os.getcwd()
        fname = QFileDialog.getSaveFileName(self, 'DB file 생성하기', savePath, '*.db')
        fileName = fname[0]
        
        if fileName =="":
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
            saveFlag = False
                
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

        self.qLineEdit.setText(self.dbFileName)
        self.updateComboList()
        self.dispData()
        QMessageBox.information(self, "테이블 추가 성공 !!", "DB 파일에 새 테이블을 추가하였습니다.")        

    # ----- DB 테이블 삭제하기 -----------------------------------------------
    def dropTable(self):

        if MyApp.saveFlag:
            reply = QMessageBox.question(self, '저장 확인!',
                " 저장하지 않은 자료가 있습니다, 저장하시겠습니까? ", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.saveData()
            saveFlag = False
            
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
        
        self.qLineEdit.setText(self.dbFileName)
        self.updateComboList()
        
        self.dispData()
        QMessageBox.information(self, "DB 파일명 삭제 성공 !!", "DB 파일에 1개의 테이블을 삭제하였습니다.")
                
    # ----- 데이터 테이블에 삽입하기 ------------------------------------------
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
                raise DbException('테이블('+self.tableName+'이 존재하지 않습니다.')

            msg = " 저장할 파일명과 테이블명이 모두 맞습니까? \n\n [저장할 DB 파일명] : " + self.dbFileName
            msg += "\n\n [DB테이블명] : " + self.tableName
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
                #sql += "(YMD, seq, korean, english, done, point) VALUES('%s', %d, '%s', '%s', '%s', '%s')" % ('20050501', itm0, itm1, itm2, itm3, itm4)
                sql += "(YMD, seq, korean, english) VALUES('%s', %d, '%s', '%s')" % (itm9, itm0, itm1, itm2)
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
                 
            conn = sqlite3.connect(self.dbFileName)
            cursor = conn.cursor()

            sql = 'SELECT * FROM ' + self.tableName
            cursor.execute(sql)

            rowList = cursor.fetchall()
            rows = len(rowList)
            if rows<1:
                self.view.setRowCount(0)
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

                self.view.setItem(row, 0, itm1)
                self.view.setItem(row, 1, itm2)
                self.view.setItem(row, 2, itm3)
                self.view.setItem(row, 3, itm4)
                self.view.setItem(row, 4, itm5)
                self.view.setItem(row, 5, itm9)
                
            self.view.blockSignals(False)   # 이벤트 감시 재개
            self.view.setAlternatingRowColors(True)
            self.view.show()
            
        except Exception as e: 
            QMessageBox.critical(self, "DB file open Error!", "%s" % e)
            
        finally:
            if 'conn' in locals():  # DB 연결을 성공했으면 conn변수가 존재함
                conn.close()

    # ----- 엑셀 파일 데이터 가져오기 ----------------------------------------
    def dispExcelData(self, excelFileName):

        if MyApp.saveFlag:

            # QMB = QMessageBox()
            # #QMB.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel) 
            # reply = QMB.question(self, '저장 확인!',
            #     " 저장하지 않은 자료가 있습니다, 저장하시겠습니까? ", QMB.Cancel | QMB.No, QMB.Cancel)
            # if reply == QMessageBox.No:
            #     return
            
            reply = QMessageBox.question(self, '저장 확인!',
                " 저장하지 않은 자료가 있습니다, 저장하시겠습니까? ", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.No:
                return
            self.saveData()
            
        try:
            if not os.path.exists(excelFileName):
                 raise DbException('문장을 저장한 엑셀 파일이 존재하지 않습니다.')
    
            wb = openpyxl.load_workbook(excelFileName) 
            sheet = wb.active
            
            max_row = sheet.max_row
            max_column  = sheet.max_column
            
            self.view.setRowCount(max_row)
            self.view.blockSignals(True)    # 이벤트 감시 중지

            for idx, row in enumerate(sheet.iter_rows(max_row = max_row)):
                if idx == 0:    # 엑셀 파일 첫 행(헤더 정보)
                    continue
                rowCnt = idx - 1
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
                
            self.view.blockSignals(True)    # 이벤트 감시 중지
            self.view.setAlternatingRowColors(False)
            self.view.show()
            if rowCnt > 0:
                MyApp.saveFlag = True
            
        except Exception as e:
            QMessageBox.critical(self, "DB Error!"," %s" % e)
            
        finally:
            if 'conn' in locals():   # DB 연결을 성공했으면 conn변수가 존재함
                conn.close()

    # ----- 이벤트 시그널 처리 -----------------------------------------------
    def cell_Editing(self, row, col):    # 셀 편집 시작할 때 이벤트 발생
        pass
        # MyApp.saveFlag = True
        # print('cell editing :', self.view.item(row, col).text())
        
    def cell_Changed(self):              # 셀 편집 종료한 후 이벤트 발생
        pass
        # row = self.view.currentRow()
        # col = self.view.currentColumn()

    # ----------------------------------------------------------------------            
    def keyPressEvent(self, e):
        
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
                    "font-size: 20px;"
                    "font:bold;"
                    "line-height: 150%;"
                    "qproperty-alignment: 'AlignVCenter | AlignLeft';"
                    "text-align: center;"
                    "padding-left:20px;"
                    "padding-top:20px;"
                    "padding-right:20px;"
                    "padding-bottom:20px;")
            
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
        # print("User has clicked the red x on the main window")
        # event.accept()
        event.ignore()
    
    # def mousePressEvent(self, event):
    #     flags = Qt.WindowFlags()
    #     closeFlag = Qt.WindowCloseButtonHint
    #     flags = flags & (~closeFlag)
    #     self.setWindowFlags(flags)
    #     print(closeFlag)
        
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
