# -*- coding: utf-8 -*-
import sys, os, getpass
import sqlite3
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlError

class QPushButton(QPushButton):
    def __init__(self, parent = None, *args):
        super().__init__(parent, *args)
        self.setSizePolicy(7, 7)
        self.setMinimumHeight(30)
        self.setMinimumWidth(100) 
        self.setFont(QFont('Times', 13))
        
class QGroupBox(QGroupBox):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setSizePolicy(7,7)

class QCheckBox(QCheckBox):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setSizePolicy(7,7)
        self.setFont(QFont('Times', 10))
     
class DbException(Exception):    # Exception만 상속받고 구현없음
    pass

stylesheetBtn = ("QPushButton{background-color: rgb(0, 50, 180); "
                      "color: white; border-style: solid; border-radius: 5;"
                      "padding: 3px; padding-left: 5px; padding-right: 5px;"
                      "border-color: #339; border-width: 1px;"
                      "font:Bold; font-family: Georgia;}"
                 "QPushButton::hover {background-color: #64b5f6; color: #fff;} "
                 "QPushButton::pressed {background-color: #FF9900;}")

# ------ QTableWidget 클래스의 메서드를 재정의 --------------------------------
class TableWidget(QTableWidget):  

    cell_EditingStarted = pyqtSignal(int, int)
    # edit 메서드 재정의
    def edit(self, index, trigger, event):
        result = super(TableWidget, self).edit(index, trigger, event)
        if result:
            self.cell_EditingStarted.emit(index.row(), index.column())
        return result

# ----- MyApp 클래스 --------------------------------------------------------
class MyApp(QTableWidget):
    saveFlag = False    # 클래스 변수
    modifiedRow = []

    def __init__(self, *args):
        QTableWidget.__init__(self, *args)   
        self.resize(1200,1000)
        self.setWindowTitle("영문장 암기 프로그램(by G.B.KIM)")
        self.bookMark = []
        self.bookCnt = 0
        # userAcount = getpass.getuser()
        # self.pathSave = 'C:\\Users\\{0}\\Documents\\'.format(userAcount)
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

        self.view.setFocus()
        self.view.setCurrentCell(0, 2)
        
    def getDbFileName(self, temp):
        self.Dir, self.fileName = os.path.split(temp)
        if self.Dir != "" and not self.Dir[0].isalpha():
            self.Dir = self.Dir[1:]    # 시작문자열에 숨김문자 있으면 제거.
        self.dbFileName = '{0}\\{1}'.format(self.Dir, self.fileName)
        
    def changedCombo(self):
        self.tableName = self.combo.currentText()
        self.dispData()
        self.view.setFocus()
        self.view.setCurrentCell(0, 2)
        
    def chkStateLanguage(self):
        #self.updateComboList()
        self.dispData()

    def dbFileOpen(self):
        fname = QFileDialog.getOpenFileName(self, 'DB file 지정', self.Dir, '*.db')
        temp = fname[0]
        if len(temp) > 0:
            temp = temp.replace('/', '\\')
            self.getDbFileName(temp)
            self.qLineEdit.setText(self.dbFileName)
            self.updateComboList()
            with open(self.pathSave, 'w', encoding='utf-8') as f:
                f.write(self.dbFileName)

    def updateComboList(self):
        # DB 테이블 목록 가져오기   
        if os.path.exists(self.dbFileName):
            conn = sqlite3.connect(self.dbFileName)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            lst = cursor.fetchall()
            
            self.combo.blockSignals(True)
            self.combo.clear()
            for row in lst:
                self.combo.addItem(row[0])
            self.combo.blockSignals(False)
            
            self.combo.setCurrentIndex(len(lst)-1)
            self.tableName = self.combo.currentText()
        
    def dispTableView(self):
        # --- 맨 좌측 상자 -------------------------------------------------
        groupbox1 = QGroupBox('')
        stylesheet = ("background-color: rgb(0, 0, 140);"
                      "border-radius: 3; border-color: rgb(200,200,200);")
        groupbox1.setStyleSheet (stylesheet)
        label = QLabel(" Memorizing ")
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
        
        self.check1 = QCheckBox('한국어 보기')
        self.check2 = QCheckBox('영문장 보기')
        self.check1.setChecked(True)
        self.check2.setChecked(True)
        self.check1.setStyleSheet("background-color: rgb(192, 255, 255);")
        self.check2.setStyleSheet("background-color: rgb(192, 255, 255);")
        self.check1.stateChanged.connect(self.chkStateLanguage)        
        self.check2.stateChanged.connect(self.chkStateLanguage)
        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.check1, 1, Qt.AlignLeft)
        vbox2.addSpacing(10)  # 단순 공백 추가        
        vbox2.addWidget(self.check2, 1, Qt.AlignLeft)
        groupbox2.setLayout(vbox2)
        
        # --- 암기/미암기/중요 체크 ------------------------------------------
        groupbox3 = QGroupBox('')
        groupbox3.setStyleSheet (stylesheet)   
        
        self.check3 = QCheckBox('암기 문장   ')
        self.check4 = QCheckBox('미암기 문장')
        self.check5 = QCheckBox('중요 보기   ')
        self.check3.setChecked(True)
        self.check4.setChecked(True) 
        self.check3.setStyleSheet("background-color: rgb(192, 255, 255);")
        self.check4.setStyleSheet("background-color: rgb(192, 255, 255);")
        self.check5.setStyleSheet("background-color: rgb(192, 255, 255);")
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
        dbBtn = QPushButton(" DB파일선택 ")
        dbBtn.clicked.connect(self.dbFileOpen) 
        #dbBtn.setStyleSheet('QPushButton {background-color: #00008B; color: white; border-radius: 5;}')
        dbBtn.setStyleSheet(stylesheetBtn)
        dbBtn.setMinimumWidth(250)
        dbBtn.setMaximumWidth(250)
        dbBtn.setMinimumHeight(35)
        dbBtn.setMaximumHeight(50)
        
        self.qLineEdit = QLineEdit(self.dbFileName)
        self.qLineEdit.setReadOnly(True)
        self.qLineEdit.setMinimumHeight(30)
        self.qLineEdit.textChanged.connect(self.updateComboList)
        
        self.combo = QComboBox()
        self.combo.setMinimumHeight(30)
        listView = QListView(self.combo)
        listView.setSpacing(3)
        listView.setFont(QFont('Times', 10))
        #listView.setStyleSheet("QListView::item{height: 20px; background-color: #EBDEF1; color: blue;}")       
        self.combo.setView(listView)
        self.combo.currentIndexChanged.connect(self.changedCombo)   # 프로그램 or 사용자에 의해 내용 변경시 호출
        #self.combo.activated.connect(self.changedCombo)            # 사용자에 의해 내용 변경시 호출
        
        lbl1=QLabel("DB파일명:")
        lbl2=QLabel("경  로  명:")
        lbl3=QLabel("DB테이블:")
        
        vbox4=QGridLayout()
        vbox4.addWidget(lbl1, 0, 0, 1, 1)
        vbox4.addWidget(lbl2, 1, 0, 1, 1)
        vbox4.addWidget(lbl3, 2, 0, 1, 1)
        vbox4.addWidget(dbBtn, 0, 1, 1, 1)
        vbox4.addWidget(self.qLineEdit, 1, 1, 1, 20)
        vbox4.addWidget(self.combo, 2, 1, 1, 20)
        groupbox4.setLayout(vbox4)
        
        # --- 검색/단기 버튼 -------------------------------------------------
        groupbox5 = QGroupBox('')
        button1 = QPushButton(" 검  색 ")
        button1.setStyleSheet(stylesheetBtn)
        button1.clicked.connect(self.dispData)   
        
        button2 = QPushButton(" 닫  기 ")
        button2.setStyleSheet(stylesheetBtn)        
        button2.clicked.connect(self.finish)
        
        vbox5 = QVBoxLayout()
        vbox5.addWidget(button1, 1, Qt.AlignRight)
        vbox5.addWidget(button2, 1, Qt.AlignRight)
        groupbox5.setLayout(vbox5)

        # ---  layout 구성하기 ----------------------------------------------
        layout1 = QHBoxLayout()
        layout2 = QVBoxLayout()
        layout1.addWidget(groupbox1, 2)
        layout1.addWidget(groupbox2, 1)
        layout1.addWidget(groupbox3, 1)
        layout1.addWidget(groupbox4, 6)
        layout1.addWidget(groupbox5, 0)
        layout1.setSpacing(10)

        # ---  view(QTableWIdget) 생성 및 레이어 배치-------------------------
        self.view = TableWidget()
        
        layout2.addWidget(self.view)

        mLayout = QVBoxLayout(self)
        mLayout.addLayout(layout1, 1)
        mLayout.addLayout(layout2, 8)
        #mLayout.setContentsMargins(50, 50, 50, 50)
        self.setLayout(mLayout)
                
        # ---  view(QTableWIdget) 속성 설정 ----------------------------------
        self.view.setColumnCount(5)
        self.view.setColumnWidth(0, 50)
        self.view.setColumnWidth(1, 500)
        self.view.setColumnWidth(2, 500)
        self.view.setColumnWidth(3, 50)
        self.view.setColumnWidth(4, 50)  
        self.view.setColumnWidth(5, 50)
        
        self.view.setHorizontalHeaderLabels(["순", "한국어", "English", "암기", "중요"])
        self.view.horizontalHeader().setFixedHeight(50)
        self.view.horizontalHeader().setStretchLastSection(True)    # 마지막 칼럼 확장하기  
        
        self.view.verticalHeader().setVisible(False)
        self.view.verticalHeader().setDefaultSectionSize(60)
        self.view.verticalHeader().setSectionResizeMode(QHeaderView.Interactive) #(QHeaderView.Fixed)
        self.view.setAlternatingRowColors(True)
        self.view.setShowGrid(True)
        self.view.setEditTriggers(QAbstractItemView.DoubleClicked) 

        style0 = ("QHeaderView::section {background-color: rgb(173, 255, 47); font-size: 18px; }"
                  "QTableView{ background-color:#D3D3D3; font-size: 18px; padding:0px; } ")   #EBDEF1(연보라)
        
        style1 = ("QTableView::item:selected:!active {selection-background-color:#BABABA; font-size: 20px;} \
                  QHeaderView::section {background-color: lightgreen; font-size: 18px;}")
        
        style2 = ("QHeaderView::section {background-color: lightgreen; font-size: 18px; height: 30px; }"
                  "QTableView {background-color: rgb(220,250,250); font-size: 20px; }")
        
        self.view.setStyleSheet(style0)
        self.view.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.view.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.view.setSizePolicy(7, 7)   # (w:QSizePolicy.Expanding, w:QSizePolicy.Expanding)
        self.view.setWordWrap(True)
        self.view.itemChanged.connect(self.cell_Changed)
        self.view.cellClicked.connect(self.cell_Clicked)
        self.view.cell_EditingStarted.connect(self.cell_Editing) 

        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    # ----- 수정된 데이터 DB에 업데이트 ---------------------------------------
    def saveUpdatedData(self):
        
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
            
            MyApp.saveFlag = False
            MyApp.modifiedRow.clear()
            
        except Exception as error: 
            QMessageBox.critical(None, "DB file open Error!", "%s" % error)
            
        finally:
            if 'conn' in locals():
                conn.close()

    # ----- 종료 확인 메시지 출력 --------------------------------------------
    def finish(self):
        
        reply = QMessageBox.question(self, '종료 확인!',
            " 프로그램을 종료하시겠습니까?     ", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return
        
        if MyApp.saveFlag:
            reply = QMessageBox.question(self, '저장 확인!',
                " 수정된 자료를 저장하시겠습니까?     ", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.saveUpdatedData()

        QApplication.instance().quit()

    # ----- 이벤트 시그널 처리 -----------------------------------------------
    def cell_Editing(self, row, col):    # 셀 편집 시작할 때 이벤트 발생
        pass
        # MyApp.saveFlag = True
        # print('cell editing :', self.view.item(row, col).text())
        
    def cell_Changed(self):              # 셀 편집 종료한 후 이벤트 발생
        # pass
        row = self.view.currentRow()
        col = self.view.currentColumn()
        
        if col == 1 or col == 2:    # '필드명: (한국어, 영어)
            MyApp.saveFlag = True
            if not (row in MyApp.modifiedRow):
                MyApp.modifiedRow.append(row)        

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
                temp = tempTuple[find+1]
            else:
                temp='0'
            temp = QTableWidgetItem(temp)
            temp.setTextAlignment(Qt.AlignCenter)
            self.view.setItem(row, col, QTableWidgetItem(temp))
 
            MyApp.saveFlag = True
            if not (row in MyApp.modifiedRow):
                MyApp.modifiedRow.append(row)

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
            btn.move(380,20)

            tBrowser = QTextEdit(win)
            tBrowser.resize(win.width()-40, win.height()-100)
            tBrowser.move(tBrowser.pos().x()+20, tBrowser.pos().y()+75)

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
            #tBrowser.setOpenExternalLinks(True)     # 외부 링크 연결 가능
            win.show()
            
        elif e.key() == Qt.Key_Escape:
            
            if len(self.bookMark) > 0:
                rowPosi = self.bookMark[self.bookCnt]
                self.view.setCurrentCell(rowPosi, 2)
                self.bookCnt += 1
                self.bookCnt %= len(self.bookMark)

        rowIndex = self.view.currentIndex().row()
        item = self.view.item(rowIndex, col)
        self.view.scrollToItem(item, QAbstractItemView.PositionAtTop) # PositionAtCenter)
    
    # ----------------------------------------------------------------------
    def eventFilter(self, source ,e):
        # def eventFilter(self, source:QtCore.QObject, event:QtCore.QEvent)
        # installEventFilter사용시 작동(실시간을 요구하기때문에 과부하 많이 걸림) 
        
        if self.view.selectedIndexes() != []:
            if e.type() == QEvent.MouseButtonPress:
                
                if e.button() == Qt.LeftButton:
                    # 셀이 이동했을 때, row, col값은 이전 셀의 위치를 반환함.
                    row = self.view.currentRow()
                    col = self.view.currentColumn()
                  
                elif e.button() == Qt.RightButton:
                    row = self.view.currentRow()
                    col = self.view.currentColumn()
        return QObject.event(source, e)

    # ----------------------------------------------------------------------
    def tableRepaint(self):
        
        chk3 = self.check3.isChecked()     # 암기 문장
        chk4 = self.check4.isChecked()     # 미암기 문장
        chk5 = self.check5.isChecked()     # 중요 문장

        rows = self.view.rowCount()
        
        for row in range(rows):
            itm4 = self.view.item(row,3).text()
            itm5 = self.view.item(row,4).text()
            
            if chk5 and itm5 =='0':
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
    def dispData1(self):
        
        if MyApp.saveFlag:
            reply = QMessageBox.question(self, '저장 확인!',
                " 수정된 자료를 저장하시겠습니까?     ", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.No:
                return
            self.saveUpdatedData()
            
        try:
            if not os.path.exists(self.dbFileName):  # if not QFile.exists(self.dbFileName):
                 raise DbException('데이터베이스 파일이 존재하지 않습니다.')
            conn = sqlite3.connect(self.dbFileName)
            cursor = conn.cursor()
            conn.commit()

            sql = 'SELECT * FROM ' + self.tableName
            cursor.execute(sql)
            lst = cursor.fetchall()
            rows = len(lst)
              
            self.bookMark.clear()
            self.view.blockSignals(True)    # 이벤트 감시 중지
            self.view.setRowCount(rows + 1)
            for row in range(rows):
                itm1 = QTableWidgetItem(str(lst[row][1]))
                itm2 = QTableWidgetItem(lst[row][2])
                itm3 = QTableWidgetItem(lst[row][3])
                itm4 = lst[row][4]
                itm5 = lst[row][5]
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
            
        except Exception as e: 
            QMessageBox.critical(None, "DB file open Error!", "%s" % e)
            
        finally:
            if 'conn' in locals():
                conn.close()

    # ----- DB읽기(방식2) : Sqlite, MySQL 등 범용 db 파일 ---------------------
    def dispData(self):

        if MyApp.saveFlag:
            reply = QMessageBox.question(self, '저장 확인!',
                " 수정된 자료를 저장하시겠습니까?     ", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.No:
                return
            self.saveUpdatedData()
            
        try:
            if not os.path.exists(self.dbFileName):  # if not QFile.exists(self.dbFileName):
                 raise DbException('데이터베이스 파일이 존재하지 않습니다.')
            conn = QSqlDatabase.addDatabase("QSQLITE")
            conn.setDatabaseName(self.dbFileName)
            conn.open()
            
            query = QSqlQuery()
            sql = 'SELECT * FROM ' + self.tableName
    
            if not query.exec(sql):
                raise DbException('테이블이 존재하지 않습니다.')

            self.bookMark.clear()
            self.view.blockSignals(True)    # 이벤트 감시 중지
            #self.view.clear()
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
            
        except Exception as e:
            QMessageBox.critical(None, "DB Error!"," %s" % e)
            
        finally:
            if 'conn' in locals():
                conn.close()

# ----- 메인함수 ------------------------------------------------------------ 
def main():
    app = QApplication( sys.argv )
    app.setStyleSheet(stylesheetBtn)
    #app.setStyleSheet("QTableView::item { border:0px; padding: 20px; }")
    mainWin = MyApp()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
