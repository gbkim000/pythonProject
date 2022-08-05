# -*- coding: utf-8 -*-
import sys, os, getpass
import sqlite3
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
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setSizePolicy(7, 7)
        self.setMinimumHeight(30)
        self.setMinimumWidth(100) 
        # self.setMaximumHeight(50)
        # self.setMaximumWidth(300)
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

# ----- MyApp 클래스 --------------------------------------------------------
class MyApp(QWidget):
    
    saveFlag = False
    
    def __init__(self):
        super().__init__()
        # <class TableWidget(QTableWidget)> 메소드 적용시 아래 문장 활성화
        # class MyApp(QTableWidget):
        #     def __init__(self, *args):
        #         QTableWidget.__init__(self, *args)   
        self.resize(1200,1000)
        self.setWindowTitle("영문장 암기 프로그램(by G.B.KIM)")
        # userAcount = getpass.getuser()
        # pathSave = 'C:\\Users\\{0}\\Documents\\'.format(userAcount)
        pathSave= 'C:\\Users\\{0}\\Documents\\'.format('Administrator')
        pathSave = pathSave + "path.txt"

        if os.path.exists(pathSave):
            with open(pathSave, 'r', encoding='utf-8') as f:
                temp = f.read().strip()
        else:
            temp = pathSave + "*.db"
        self.getDbFileName(temp)
        self.dispTableView()        
        self.updateComboList()
        #self.dispData()
        self.view.setFocus()
        self.view.setCurrentCell(0, 2)
        
    def getDbFileName(self, temp):
        self.Dir = os.path.dirname(temp).strip() # temp1, temp2 = os.path.split(파일명)
        if not self.Dir[0].isalpha():
            self.dbDir = self.Dir[1:]    # 시작문자열에 숨김문자 있으면 제거.
        self.fileName = os.path.basename(temp).strip()
        self.dbFileName = '{0}\\{1}'.format(self.dbDir, self.fileName)
        
    def changedCombo(self):
        self.tableName = self.combo.currentText()
        self.dispData()
        self.view.setFocus()
        self.view.setCurrentCell(0, 2)
        
    def changedChkState(self):
        self.updateComboList()
        self.dispData()
        
    def dbFileOpen(self):
        fname = QFileDialog.getOpenFileName(self, 'DB file 지정', self.dbDir, '*.db')
        temp = fname[0]
        if not temp != "":
            temp = temp.replace('/', '\\')
            self.getDbFileName(temp)
            self.qLineEdit.setText(self.dbFileName)
            self.updateComboList()

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
        label = QLabel("Memorize")
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
                      "padding-left: 15px;"
                      "padding-right: 20px;"
                      "border-color: rgb(200,200,200);"
                      "border-width: 1px;" )
        groupbox2.setStyleSheet (stylesheet)    
        
        self.check1 = QCheckBox('한국어 보기')
        self.check2 = QCheckBox('영문장 보기')
        self.check1.setChecked(True)
        self.check2.setChecked(True)
        self.check1.stateChanged.connect(self.changedChkState)        
        self.check2.stateChanged.connect(self.changedChkState)
        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.check1, 1, Qt.AlignLeft)
        #vbox2.addSpacing(20)  # 단순 공백 추가        
        vbox2.addWidget(self.check2, 1, Qt.AlignLeft)
        groupbox2.setLayout(vbox2)
        
        # --- 암기/미암기/중요 체크 ------------------------------------------
        groupbox3 = QGroupBox('')
        stylesheet = ("background-color: rgb(192, 255, 192);"
                      "border-style: solid;"
                      "border-radius: 3;"
                      "padding: 3px;"
                      "padding-left: 15px;"
                      "padding-right: 20px;"
                      "border-color: rgb(200,200,200);"
                      "border-width: 1px;" ) 
        groupbox3.setStyleSheet (stylesheet)   
        
        check3 = QCheckBox('암기 문장   ')
        check4 = QCheckBox('미암기 문장')
        check5 = QCheckBox('중요 보기   ')
        check3.setChecked(True)
        check4.setChecked(True) 
        vbox3 = QVBoxLayout()
        vbox3.addWidget(check3, 1, Qt.AlignLeft)
        vbox3.addWidget(check4, 1, Qt.AlignLeft)
        vbox3.addWidget(check5, 1, Qt.AlignLeft)
        #vbox3.setSpacing(2) # 위젯 사이의 늘림 간격
        groupbox3.setLayout(vbox3)
        
        # --- DB파일명/테이블 선택 -------------------------------------------
        groupbox4 = QGroupBox('')
        dbBtn = QPushButton(" DB파일선택 ")
        dbBtn.clicked.connect(self.dbFileOpen) 
        dbBtn.setStyleSheet('QPushButton {background-color: #00008B; color: white; border-radius: 5;}')
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
        #button1.setFont(QFont('Times', 15))
        #button1.setStyleSheet('QPushButton {background-color: #A3C1DA; color: blue;}')
        #button1.setStyleSheet('QPushButton {background-color: green; color: blue; font-size: 25px;}')
        stylesheet = ("background-color: rgb(0, 50, 180); "
                        "color: white; "
                        "border-style: solid;"
                        "border-radius: 5;"
                        "padding: 3px;"
                        "padding-left: 5px;"
                        "padding-right: 5px;"
                        "border-color: #339;"
                        "border-width: 1px;"
                        "font:Bold;"
                        "font-family: Georgia")
        button1.setStyleSheet(stylesheet)
        button1.clicked.connect(self.dispData)   
        
        button2 = QPushButton(" 닫  기 ")
        button2.setStyleSheet(stylesheet)        
        button2.clicked.connect(self.finish)
        
        vbox5 = QVBoxLayout()
        vbox5.addWidget(button1, 1, Qt.AlignRight)
        vbox5.addWidget(button2, 1, Qt.AlignRight)
        groupbox5.setLayout(vbox5)

        # ---  layout 구성하기 -----------------------------------------------
        layout1 = QHBoxLayout()
        layout2 = QVBoxLayout()
        layout1.addWidget(groupbox1, 2)
        layout1.addWidget(groupbox2, 2)
        layout1.addWidget(groupbox3, 2)
        layout1.addWidget(groupbox4, 5)
        layout1.addWidget(groupbox5, 0)
        layout1.setSpacing(10)

        self.view = QTableWidget()
        # <class TableWidget(QTableWidget)> 메소드 적용시 아래 문장 활성화
        #self.view = TableWidget()
        
        layout2.addWidget(self.view)

        mLayout = QVBoxLayout(self)
        mLayout.addLayout(layout1, 1)
        mLayout.addLayout(layout2, 8)
        #mLayout.setContentsMargins(50, 50, 50, 50)
        self.setLayout(mLayout)
                
        # ---  view(QTableWIdget) 구성하기 -----------------------------------
        self.view.setColumnCount(5)
        self.view.setColumnWidth(0, 50)
        self.view.setColumnWidth(1, 500)
        self.view.setColumnWidth(2, 500)
        self.view.setColumnWidth(3, 50)
        self.view.setColumnWidth(4, 50)        
        self.view.setHorizontalHeaderLabels(["순", "한국어", "English", "암기", "중요"])
        self.view.horizontalHeader().setFixedHeight(50)
        self.view.horizontalHeader().setStretchLastSection(True)    # 마지막 칼럼 확장하기        
        self.view.verticalHeader().setVisible(False)
        self.view.verticalHeader().setDefaultSectionSize(50)
        self.view.verticalHeader().setSectionResizeMode(QHeaderView.Interactive) #(QHeaderView.Fixed)
        self.view.setAlternatingRowColors(True)
        self.view.setShowGrid(True)
        # self.view.setColumnHidden(2, True)
        # self.view.setColumnWidth(2, 10)
        self.view.setEditTriggers(QAbstractItemView.DoubleClicked) 
        # self.view.setEditTriggers(QAbstractItemView.CurrentChanged)
        # (NoEditTriggers, AllEditTriggers, CurrentChanged )
        # self.view.setSortingEnabled(True)
        # self.view.horizontalHeader().setSortIndicator(0, Qt.AscendingOrder)

        style0 = ("QHeaderView::section {background-color: rgb(173, 255, 47); font-size: 18px; }"
                  "QTableView{ background-color:#D3D3D3; font-size: 16px;} ")   #EBDEF1(연보라)
        
        style1 = ("QTableView::item:selected:!active {selection-background-color:#BABABA; font-size: 20px;} \
                  QHeaderView::section {background-color: lightgreen; font-size: 18px;}")
        
        style2 = ("QHeaderView::section {background-color: lightgreen; font-size: 18px; height: 30px; }"
                  "QTableView {background-color: rgb(220,250,250); font-size: 20px; }")
        
        self.view.setStyleSheet(style0)
        self.view.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.view.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.view.setSizePolicy(7, 7)   # (w:QSizePolicy.Expanding, w:QSizePolicy.Expanding)

        # self.view.setItemDelegate(self.delegate)
        # self.view.cellActivated.connect(self.itemChanged)
        
        # self.view.horizontalHeader().setStyleSheet("background-color: rgb(190,200,200); ") # .setVisible(True) 설정 필요함
        # self.view.horizontalHeaderItem(0).setTextAlignment(Qt.AlignCenter) # header 정렬 방식
        # item = QTableWidgetItem('한국어(Item)')
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

        self.view.itemChanged.connect(self.cell_Changed)
        self.view.cellClicked.connect(self.cell_Clicked)

        # <class TableWidget(QTableWidget): > 함수 적용시 아래 이벤트 설정
        # self.view.cell_EditingStarted.connect(self.cell_Editing) 
        
        # eventFilter 작동 허용 설정(eventFilter을 사용시 속도 느려질 수 있음)
        # self.view.viewport().installEventFilter(self)   
        
        self.show()

    def saveUpdatedData(self):
        if MyApp.saveFlag == False:
            return
        
        
        
    # --- 종료 확인 메시지 출력 ----------------------------------------------
    def finish(self):
        reply = QMessageBox.question(self, '종료 확인!',
            " 프로그램을 종료하시겠습니까?     ", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            
            if MyApp.saveFlag:
                self.saveUpdatedData()
                
            QApplication.instance().quit()

    # --- 이벤트 시그널 처리 -------------------------------------------------
    def cell_Editing(self, row, col):    # 셀 편집 시작할 때
        pass
        # print('cell editing :', self.view.item(row, col).text())
        
    def cell_Changed(self):              # 셀 편집 종료한 후
        pass
        # print('cell changing :', self.view.item(row, col).text())

    def cell_Clicked(self):
        
        row = self.view.currentRow()
        col = self.view.currentColumn()
        
        #print(f'clicked at {row, col}')
        if col == 3 or col ==4:    # '필드명: 암기, 중요
            tempTuple = ('0','1','9')
            temp = self.view.item(row, col).text()
            if temp in tempTuple:
                find = tempTuple.index(temp)
                if find == len(tempTuple)-1:
                    find = -1
                temp = tempTuple[find+1]
            else:
                temp='0'
            temp = QTableWidgetItem(temp)
            temp.setTextAlignment(Qt.AlignCenter)
            self.view.setItem(row, col, QTableWidgetItem(temp))

            MyApp.saveFlag = True
            
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
        # elif e.modifiers() & Qt.AltModifier:
        #     print("Alt")
        # if e.key() == Qt.Key_Delete:
        #     print("DELETE")
        # elif e.key() == Qt.Key_Escape:
        #     print('Escape')

        rowIndex = self.view.currentIndex().row()
        item = self.view.item(rowIndex, col)
        self.view.scrollToItem(item, QAbstractItemView.PositionAtTop) # PositionAtCenter)
        # self.view.selectRow(rowIndex)
    
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
        
    # --- DB읽기(방식1) : Sqlite3 전용 DB 읽기 -------------------------------
    def dispData(self):
        
        if MyApp.saveFlag:
            self.saveUpdatedData()
            MyApp.saveFlag = False            
            
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
              
            self.view.blockSignals(True)    # 이벤트 감시 중지
            self.view.setRowCount(rows + 1)
            for row in range(rows):
                item1 = QTableWidgetItem(str(lst[row][1]))
                item2 = QTableWidgetItem(lst[row][2])
                item3 = QTableWidgetItem(lst[row][3])
                item4 = QTableWidgetItem(lst[row][4])
                item5 = QTableWidgetItem(lst[row][5])

                item1.setBackground(QColor(200, 100, 100))
                item1.setTextAlignment(Qt.AlignCenter)
                item4.setTextAlignment(Qt.AlignCenter)
                item5.setTextAlignment(Qt.AlignCenter)

                if not self.check1.checkState():
                    item2.setForeground(QColor("#c4c4c4")) # 또는 QColor('gray')
                    item2.setBackground(QColor("#c4c4c4"))
                    
                if not self.check2.checkState():
                    item3.setForeground(QColor("#c4c4c4")) 
                    item3.setBackground(QColor("#c4c4c4"))

                self.view.setItem(row, 0, item1)
                self.view.setItem(row, 1, item2)
                self.view.setItem(row, 2, item3)
                self.view.setItem(row, 3, item4)
                self.view.setItem(row, 4, item5)
                
            self.view.blockSignals(False)   # 이벤트 감시 재개
            
        except sqlite3.OperationalError as e:
            QMessageBox.critical(None, "DB table Error!", '테이블이 존재하지 않습니다.')
            
        except Exception as e: 
            QMessageBox.critical(None, "DB file Error!", "%s" % e)
            
        finally:
            if 'conn' in locals():
                conn.close()

    # --- DB읽기(방식2) : Sqlite, MySQL 등 범용 db 파일 -----------------------
    def dispData2(self):
        
        if MyApp.saveFlag:
            self.saveUpdatedData()
            MyApp.saveFlag = False
            
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

            self.view.blockSignals(True)    # 이벤트 감시 중지
            while query.next():
                rows = self.view.rowCount()
                self.view.setRowCount(rows + 1)

                item1 = QTableWidgetItem(str(query.value(1)))
                item2 = QTableWidgetItem(query.value(2))
                item3 = QTableWidgetItem(query.value(3))
                item4 = QTableWidgetItem(query.value(4))
                item5 = QTableWidgetItem(query.value(5))

                item1.setBackground(QColor(200, 100, 100))
                item1.setTextAlignment(Qt.AlignCenter)
                item4.setTextAlignment(Qt.AlignCenter)
                item5.setTextAlignment(Qt.AlignCenter)

                if not self.check1.checkState():
                    item2.setForeground(QColor("#c4c4c4")) # 또는 QColor('gray')
                    item2.setBackground(QColor("#c4c4c4"))
                    
                if not self.check2.checkState():
                    item3.setForeground(QColor("#c4c4c4")) 
                    item3.setBackground(QColor("#c4c4c4"))

                self.view.setItem(rows, 0, item1)
                self.view.setItem(rows, 1, item2)
                self.view.setItem(rows, 2, item3)
                self.view.setItem(rows, 3, item4)
                self.view.setItem(rows, 4, item5)
                    
            self.view.blockSignals(False)   # 이벤트 감시 재개

        except Exception as e:
            QMessageBox.critical(None, "DB Error!"," %s" % e)
            
        finally:
            if 'conn' in locals():
                conn.close()

# ------ QTableWidget 클래스의 메서드를 재정의 --------------------------------
class TableWidget(QTableWidget):  

    cell_EditingStarted = pyqtSignal(int, int)
    
    # edit 메서드 재정의
    def edit(self, index, trigger, event):
        result = super(TableWidget, self).edit(index, trigger, event)
        if result:
            self.cell_EditingStarted.emit(index.row(), index.column())
        return result
    
    # # mousePressEvent 메서드 재정의
    # def mousePressEvent(self, e):
    #     super().mousePressEvent(e)
    #     # item = self.itemAt(e.pos())
    #     # if isinstance(item, MyApp):
    #     #     print("Mouse  clicked on cell with parent {}".format(item.parent.id))
    #     # print(f'Press: {e.button()} - (Left:1, Right:2, Middle:4)')        
    #     if e.button() == 1:
    #         mouseButtonID = 'Left'
    #     elif e.button() == 2:
    #         mouseButtonID = 'Right'
    #     #print(f"mouseButtonID: {mouseButtonID}")  

    # # mouseReleaseEvent 메서드 재정의
    # def mouseReleaseEvent(self, e):
    #     super().mouseReleaseEvent(e)
    #     if e.button() == 1:
    #         mouseButtonID = 'Left'
    #     elif e.button() == 2:
    #         mouseButtonID = 'Right'
    #     #print(f"mouseButtonID: {mouseButtonID}")  

# --- 메인함수 ---------------------------------------------------------- 
def main():
    app = QApplication( sys.argv )
    mainWin = MyApp()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()


# DB insertion
# query = QSqlQuery("SELECT id, name, job, email FROM contacts")
# while query.next():
#     rows = self.view.rowCount()
#     self.view.setRowCount(rows + 1)
#     self.view.setItem(rows, 0, QTableWidgetItem(str(query.value(0))))
#     self.view.setItem(rows, 1, QTableWidgetItem(query.value(1)))
#     self.view.setItem(rows, 2, QTableWidgetItem(query.value(2)))
#     self.view.setItem(rows, 3, QTableWidgetItem(query.value(3)))
# self.view.resizeColumnsToContents()
# self.setCentralWidget(self.view )

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