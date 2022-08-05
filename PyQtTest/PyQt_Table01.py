# QTableWidget - https://blog.naver.com/PostView.nhn?isHttpsRedirect=true&blogId=anakt&logNo=221834285100

'''
Qt Designer에서 TableWidget을 만들어 준후, 더블클릭해서 Column을 4개 만들어 준다.
PyQt5  QtableWidget의 이름이 "Debt_Table"이라고 전제한다. 데이타는 Debt_List에 저장되어 있다고 전제한다.

1. 행을 증가시키는 방법

    self.Debt_Table.setRowCount(10)
    위와 같이 코딩을 하면 10개의 행이 만들어 진다.
    
    QTableWidget을 엑셀시트 처럼 사용하려면 행의 수가 고정되어 있으면 안되고 데이타 값에 따라서 증가되어야 한다. 
    데이타 행을 증가시키려면 다음과 같이 코딩한다.

    self.Debt_Table.setRowCount(len(Debt_List))

​2. 셀에 값을 입력하는 방법

    Table위젯의 각 셀들 중 가장 좌측 위의 셀에 "안녕"을 입력하려면 다음과 같이 코딩을 하면 된다.
    self.Debt_Table.setItem(0, 0, QTableWidgetItem("안녕"))

    3개의 인수들을 넣어야 하는데, 각 인수들은 다음과 같다
    (행번호, 열번호, QtableWidgetItem("입력할 값"))
    
    * 주의 사항
    -테이블 위젯의 행번호, 열번호는 0부터 시작한다.
    -셀에 넣을 때에는 직접 값을 넣을 수는 없고 반드시 QTableWidgetItem()개체로만 입력이 가능하다.
    -QTableWidgetItem()개체의 인수는 반드시 String이어야 한다.

3.셀에 들어 있는 값을 가져오는 방법

    self.Debt_Table.item(행번호, 열번호).text()

4.테이블의 행과 열의 개수를 확인하는 방법

    self.Debt_Table.rowCount()
    self.Debt_Table.columnCount()

5.테이블의 행과 열을 선택하는 방법

    행과 열을 하나씩 선택
    self.Debt_Table.selectRow()
    self.Debt_Table.selectColumn()
    
    행과 열을 여러 개 동시 선택하려는 경우, 다음 코드를 입력하고, 이후 select 코드를 다수 입력
    self.ev_table.setSelectionMode(QAbstractItemView.MultiSelection)
    
    *** 컨트롤 키를 누르고 마우스를 클릭하면, 여러 Row를 동시 선택하고, 마우스만 클릭하면 하나의 Row를 선택하는 코드
    
    self.Debt_Table.cellClicked.connect(self.cell_click) # cellClick 이벤트를 감지하면 cell_click 함수를 실행
    def cell_click(self): 
        modifiers = QApplication.keyboardModifiers() # pyqt에서의 키보드 입력 확인방법
        if modifiers == QtCore.Qt.ControlModifier: # 마우스로 셀을 클릭했을 시에 컨트롤 키가 눌려져 있던 경우
            self.ev_table.setSelectionMode(QAbstractItemView.MultiSelection) # 여러 셀이 함께 선택되도록 한다.
        else:
            self.ev_table.setSelectionMode(QAbstractItemView.ExtendedSelection) # 하나의 셀만 선택되도록 한다.
​
6.선택된 셀의 행번호와 열번호를 확인하는 방법

    x = self.Debt_Table.selectedIndexes() # 리스트로 선택된 행번호와 열번호가 x에 입력된다.
    x[0].row()      #첫번째 선택된 행번호를 부르는 방법
    x[0].column()   #첫번째 선택된 열번호를 부르는 방법

7. 셀의 크기 조정방법

    열의 크기 조정
    self.Debt_Table.setColumnWidth(0, 60)

    ​행의 크기 조정
    self.Debt_Table.setRowHeight(0, 60)

    2개의 인수들을 넣어야 하는데, 각 인수들은 다음과 같다
    (열번호 또는 행번호, 크기)
    
    ​테이블 위젯의 크기에 맞추어서 자동으로 셀들의 크기가 조정되게 하려면 다음과 같이 코딩한다.
    self.Debt_Table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

8. 셀의 정렬 방법

    다음과 같이 코딩하면 첫번째 셀이 중앙정렬이 된다.
    self.Debt_Table.item(0, 0).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
    
    3개 또는 4개의 인수들을 넣어야 하는데, 앞의 두개는 열번호와 행번호이고, 뒤의 2개는 정렬방법이다.
    
    Qt.AlignCenter -> 가운데 정렬
    Qt.AlignLeft ->좌측 정렬
    Qt.AlignRight -> 오른쪽 정렬
    Qt.AlignTop -> 위로 정렬
    Qt.AlignBottom -> 아래로 정렬
    Qt.AlignVCeonter -> 세로방향 가운데 정렬
    
    특이하게 정렬방법 인수를 2개를 넣을 때는 , 대신에  |  를 사용함에 주의

9. 테이블을 sorting 하는 방법

    테이블의 컬럼을 클릭해서 sorting하도록 하는 방법
    self.Debt_Table.setSortingEnabled(True)
    
    ​테이블의 특정 컬럼을 이용해서 sorting하는 방법
    self.Debt_Table.sortByColumn(컬럼번호, Qt.AscendingOrder)

10. 테이블 컬럼의 폭을 설정하는 방법
    self.Debt_table.setColumnWidth(컬럼번호, 폭)

​11. 테이블 위젯에 데이타 값들을 표시하는 방법

    Debt_List 개체가 2개의 속성(SR_Num, Priority)를 가진다고 하면, Debt_List 개체의 수만큼 행을 만들어 주고, 
    그 셀들에 각각 입력해준다. 모든 데이터들이 입력될 때까지 이를 반복한다.
    
    def Show_Debt_Table(self):
          self.Debt_Table.setRowCount(len(Debt_List))  ## Debt_List에 입력된 데이터 수만큼 테이블 위젯에 행을 만들어준다
          Row = 0
          for x in Debt_List:
              self.Debt_Table.setItem(Row, 0, QTableWidgetItem(x.SR_Num))  ## 셀에 데이터를 저장한다. 이때 직접 데이터를 넣을 수는 없고, QTableWidgetItem개체로 만들어 입력해야 한다.
              self.Debt_Table.setItem(Row, 1, QTableWidgetItem(x.Priority))
              self.Debt_Table.item(Row, 0).setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter) ## Table위젯에서 셀 정렬 방법
              self.Debt_Table.item(Row, 1).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
              Row = Row + 1

12. 행의 색깔이 번갈아 나오도록 하는 코드

    QColor(0,0,0,0,) 부분에는 RGBA값을 넣어준다.
    
    self.Debt_Table.setAlternatingRowColors(True)   # 행마다 색깔을 변경 하는 코드
    self.gui_palette = QPalette()                   # 반복되는 행의 색깔을 지정하는 코드
    self.gui_palette.setColor(QPalette.AlternateBase, QColor(0,0,0,0)) #반복되는 행의 색깔을 지정하는 코드

13. 기타 테이블 위젯의 설정
    self.Debt_Table.verticalHeader().setVisible(False) # 행번호 안나오게 하는 코드
    self.Debt_Table.horizontalHeader().setVisible(False) # 열번호 안나오게 하는 코드
    self.Debt_Table.setShowGrid(False) # Table의 Grid를 보이지 않게 하는 코드
    self.Debt_Table.setSelectionBehavior(QAbstractItemView.SelectRows)  # Row 단위 선택
    self.Debt_Table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 셀 edit 금지

# %% IronPython - (for .Net Framwork)
# 출처: https://kenial.tistory.com/772 [GhostOnNetwork]
# IronPython은 C#으로 작성된 Python의 .NET 구현으로 .Net Framework에 직접 접근이 가능하다.
# IronPython에는 C#으로 작성된 WinForm 프로그래밍을 하는 것이 가능하다.
# 그런데 재미있는 것은, 이 IronPython 코드를 유닉스 기반 환경에서도 실행시켜 볼 수 있다는 것이다. 
# .NET 프레임워크 환경은 윈도우 시스템에만 제공되는 것이 아니다. 
# Mono라는 이름의 크로스 플랫폼/오픈 소스 프로젝트가 존재하고 있기 때문이다.

'''
#%% QTableWidget 예제(1) : QTableWidgetItem /setItem /setBackground 

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

lista = ['aa', 'ab', 'ac']
listb = ['ba', 'bb', 'bc']
listc = ['ca', 'cb', 'cc']
mystruct = {'A':lista, 'B':listb, 'C':listc}

class MyTable(QTableWidget):
    def __init__(self, thestruct, *args):
        # QTableWidget.__init__(self, *args)
        # super(MyTable, self).__init__(*args)
        super().__init__(*args)
        self.data = thestruct
        self.setmydata()
        self.resize(400, 250)

    def setmydata(self):
        n = 0
        for key in self.data: # key는 'A', 'B', 'C'
            m = 0
            for item in self.data[key]:
                newitem = QTableWidgetItem(item)
                if key == 'A':
                    newitem.setBackground(QColor(100,100,250))
                elif key == 'B':
                    newitem.setBackground(QColor(100,250,100))
                else:
                    newitem.setBackground(QColor(250,100,100))
                self.setItem(m, n, newitem)
                m += 1
            n += 1

def main(args):
    app = QApplication(args)
    table = MyTable(mystruct, 5, 3)
    table.show()
    sys.exit(app.exec_())

if __name__=="__main__":
    main(sys.argv)

#%% QTableWidget 예제(2) : RowHeader 배경색 바꾸기

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class MyFrame(QFrame):
    def __init__(self, parent=None, initials=None):
        QFrame.__init__(self, parent)
        self.table = QTableWidget(5,3,self)
        self.table.move(25,25)
        self.table.resize(400,250)

        item1 = QTableWidgetItem('red')
        item1.setBackground(QColor(255, 0, 0))
        self.table.setHorizontalHeaderItem(0,item1)

        item2 = QTableWidgetItem('green')
        item2.setBackground(QColor(0, 255, 0))
        self.table.setHorizontalHeaderItem(1,item2)

        item3 = QTableWidgetItem('blue')
        item3.setBackground(QColor(0, 0, 255))
        self.table.setHorizontalHeaderItem(2,item3)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyle(QStyleFactory.create('Fusion')) # ['Windows', 'WindowsXP', 'WindowsVista', 'Fusion']
    app.setStyle('Fusion')
    Frame = MyFrame(None)
    Frame.resize(450,300)
    Frame.show()
    app.exec_()
    
#%% QTableWidget 예제(3) : setAlternatingRowColors /setFocusPolicy /setBrush /QPalette

import sys
from PyQt5.QtGui import QPalette, QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, \
    QAbstractItemView, QTableWidgetItem, QDesktopWidget

column_idx_lookup = {'code': 0, 'name': 1, 'cprice': 2}
kospi_top5 = {'code': ['005930', '015760', '005380', '090430', '012330'],
              'name': ['삼성전자', '한국전력', '현대차', '아모레퍼시픽', '현대모비스'],
              'cprice': ['1,269,000', '60,100', '132,000', '414,500', '243,500'] }

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setGeometry(200, 200, 400, 300)
        self.tableWidget = QTableWidget(self)
        self.tableWidget.resize(380, 280)
        self.tableWidget.setRowCount(5)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers) # 항목 수정 불가
        self.setTableWidgetData()
        self.center()
        
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def setTableWidgetData(self):
        column_headers = ['종목코드', '종목명', '종가']
        self.tableWidget.setHorizontalHeaderLabels(column_headers)
            
        for key, val in kospi_top5.items():
            col = column_idx_lookup[key]
            for row, val in enumerate(val):
                item = QTableWidgetItem(val)
                if col == 2:
                    item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                # if key == 'code':
                #     item.setBackground(QColor(100,100,200))
                # elif key == 'name':
                #     item.setBackground(QColor(100,200,100))
                # else:
                #     item.setBackground(QColor(200,100,100))
                self.tableWidget.setItem(row, col, item)
        
        for col in range(3):
            self.tableWidget.setColumnWidth(col, 120)
        # self.tableWidget.resizeColumnsToContents()
        
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.setAlternatingRowColors(True)      # 행마다 색깔을 변경 하는 코드
        self.tableWidget.item(0,0).setBackground(QColor(100,255,0))
        self.tableWidget.setFocusPolicy(Qt.NoFocus) # 포커스 받은 셀 강조색 없음.        
        self.gui_palette = QPalette()                       # 반복되는 행의 색깔을 지정하는 코드
        self.gui_palette.setColor(QPalette.AlternateBase, QColor(255,100,100,200)) # 반복되는 행의 색깔을 지정하는 코드
        self.gui_palette.setBrush(QPalette.Highlight, QBrush(Qt.blue))
        self.gui_palette.setBrush(QPalette.HighlightedText, QBrush(Qt.yellow))
        self.tableWidget.setPalette(self.gui_palette)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.show()
    app.exec_()
    
#%% QTableWidget 고급 예제(4) : setAlternatingRowColors /setFocusPolicy /setBrush /QPalette

import time, sys
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class MyFrame(QWidget):
    def __init__(self):
        super().__init__()
        self.table = QTableWidget(5, 5, self)  # row, column
        self.table.setHorizontalHeaderLabels(["", "종목명", "현재가(문자)",  "현재가(숫자)", "거래량"])
        data = [
            ("삼성전자", "200000", 200000, "25000"),
            ("셀트리온", "2100", 2100, "1500"),
            ("현대차", "190000", 190000, "300000"),
            ("기아차", "150000", 150000, "240000") ]

        for idx, (hname, price_str, price, vol) in enumerate(data):
            # 사용자정의 item과 checkbox widget을 동일한 cell에 넣어서 추후 정렬 가능하게 한다.
            item = MyQTableWidgetItemCheckBox()
            chbox = MyCheckBox(item)
            # self.table.setItem(idx, 0, item)
            self.table.setCellWidget(idx, 0, chbox)

            chbox.stateChanged.connect(self.__checkbox_change)  # sender() 확인용 예..

            self.table.setItem(idx, 1, QTableWidgetItem(hname))
            self.table.setItem(idx, 2, QTableWidgetItem(price_str))
            
            # 숫자를 기준으로 정렬하기 위함. -- default 는 '문자'임.
            item = QTableWidgetItem()
            item.setData(Qt.DisplayRole, price)
            self.table.setItem(idx, 3, item)
            self.table.setItem(idx, 4, QTableWidgetItem(vol))

        self.table.setSortingEnabled(False)  # 정렬기능
        self.table.resizeRowsToContents()
        self.table.resizeColumnsToContents()  # 이것만으로는 checkbox 컬럼은 잘 조절안됨.
        self.table.setColumnWidth(0, 15)  # checkbox 컬럼 폭 강제 조절.

        self.table.cellClicked.connect(self._cellclicked)

        # 컬럼 헤더를 click 시에만 정렬하기.
        hheader = self.table.horizontalHeader()  # qtablewidget --> qtableview --> horizontalHeader() --> QHeaderView
        hheader.sectionClicked.connect(self._horizontal_header_clicked)

        vbox = QVBoxLayout(self)
        vbox.addWidget(self.table)
        self.setLayout(vbox)

    def __checkbox_change(self, checkvalue):
        # print("check change... ", checkvalue)
        chbox = self.sender()  # signal을 보낸 MyCheckBox instance
        print("checkbox sender row = ", chbox.get_row())

    def _cellclicked(self, row, col):
        print("_cellclicked... ", row, col)

    def _horizontal_header_clicked(self, idx):
        """
        컬럼 헤더 click 시에만, 정렬하고, 다시 정렬기능 off 시킴
         -- 정렬기능 on 시켜놓으면, 값 바뀌면 바로 자동으로 data 순서 정렬되어 바뀌어 헷갈린다..
        :param idx -->  horizontalheader index; 0, 1, 2,...
        :return:
        """
        # print("hedder2.. ", idx)
        self.table.setSortingEnabled(True)  # 정렬기능 on
        # time.sleep(0.2)
        self.table.setSortingEnabled(False)  # 정렬기능 off

class MyCheckBox(QCheckBox):
    def __init__(self, item):
        """
        :param item: QTableWidgetItem instance
        """
        super().__init__()
        self.item = item
        self.mycheckvalue = 0   # 0 --> unchecked, 2 --> checked
        self.stateChanged.connect(self.__checkbox_change)
        self.stateChanged.connect(self.item.my_setdata)  # checked 여부로 정렬을 하기위한 data 저장

    def __checkbox_change(self, checkvalue):
        # print("myclass...check change... ", checkvalue)
        self.mycheckvalue = checkvalue
        print("checkbox row= ", self.get_row())

    def get_row(self):
        return self.item.row()

class MyQTableWidgetItemCheckBox(QTableWidgetItem):
    """
    checkbox widget 과 같은 cell 에  item 으로 들어감.
    checkbox 값 변화에 따라, 사용자정의 data를 기준으로 정렬 기능 구현함.
    """
    def __init__(self):
        super().__init__()
        self.setData(Qt.UserRole, 0)

    def __lt__(self, other):
        # print(type(self.data(Qt.UserRole)))
        return self.data(Qt.UserRole) < other.data(Qt.UserRole)

    def my_setdata(self, value):
        # print("my setdata ", value)
        self.setData(Qt.UserRole, value)
        # print("row ", self.row())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    frame = MyFrame()
    frame.setWindowTitle("정렬하기")
    frame.resize(500, 300)  # width, height
    frame.show()
    app.exec_()

#%% QTableWidget 예제(5) : Add/Copy/Remove on a table widget.

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHeaderView, QAbstractItemView, \
        QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *

class TableWidget(QTableWidget):
    def __init__(self):
        super().__init__(1, 6)
        self.setHorizontalHeaderLabels(list('ABCDE'))
        self.verticalHeader().setDefaultSectionSize(50)
        self.horizontalHeader().setDefaultSectionSize(100)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        
        # 헤더배경색 지정하기 - 방법(1)
        item1 = QTableWidgetItem('AAA')
        item1.setBackground(QColor(0, 255, 0))
        self.setHorizontalHeaderItem(0, item1)

        # 헤더배경색 지정하기 - 방법(2)
        self.horizontalHeaderItem(1).setBackground(QColor(Qt.cyan))
        self.horizontalHeaderItem(2).setBackground(QBrush(Qt.yellow))

        # 헤더배경색 지정하기 - 방법(3)
        for col in range(3, 6): # column no 3 to 5
            hitem = self.horizontalHeaderItem(col)
            if hitem is not None:
                hitem.setBackground(QBrush(Qt.red))
            
        # 테이블 배경색 지정하기
        self.setStyleSheet("background-color: lightblue;")
        """
        palette = QPalette()
        palette.setBrush(QPalette.Base, QBrush(QPixmap("img77.jpg")))
        palette.setColor(QPalette.Base, Qt.yellow)
        palette.setColor(QPalette.Base, QColor(255, 255, 255))   # white
        palette.setColor(QPalette.Base, QColor(0, 255, 0))
        self.table.setPalette(palette)  # table 배경 설정
        """

    def _addRow(self):
        rowCount = self.rowCount()
        self.insertRow(rowCount)
    
    def _removeRow(self):
        if self.rowCount() > 0 :
            self.removeRow(self.rowCount()-1)
            
    def _copyRow(self):
        self.insertRow(self.rowCount())
        rowCount = self.rowCount()
        columnCount = self.columnCount()
        
        for j in range(columnCount):
            if not self.item(rowCount-2, j) is None:
                self.setItem(rowCount-1, j, QTableWidgetItem(self.item(rowCount-2, j).text()))
                
class AppDemo(QWidget):
    def __init__(self):
         super().__init__()
         self.resize(900, 400)
         
         mainLayout=QHBoxLayout()
         table = TableWidget()
         mainLayout.addWidget(table)
         
         buttonLayout=QVBoxLayout()
         
         button_new=QPushButton('New')  
         button_new.clicked.connect(table._addRow)
         buttonLayout.addWidget(button_new)
         
         button_copy=QPushButton('Copy') 
         button_copy.clicked.connect(table._copyRow) 
         buttonLayout.addWidget(button_copy)
         
         button_remove=QPushButton('Remove')   
         button_remove.clicked.connect(table._removeRow)
         buttonLayout.addWidget(button_remove, alignment=Qt.AlignTop)
         
         mainLayout.addLayout(buttonLayout) 
         self.setLayout(mainLayout)
         
app=QApplication(sys.argv)
# QtWidgets.QStyleFactory.keys() ## ['Windows', 'WindowsXP', 'WindowsVista', 'Fusion']
app.setStyle(QStyleFactory.create('Fusion'))
app.setStyleSheet('QPushButton{font-size: 20px; width: 200px; height: 50px}')
demo = AppDemo()
demo.show()
sys.exit(app.exec_())

#%% QTableWidget 예제(6) :  선택/해제된 row, col 출력하기
# selectionModel, selectionChanged

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.window_width, self.window_height = 700, 300
        self.setMinimumSize(self.window_width, self.window_height)
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        tableWidget = QTableWidget(6,6)
        layout.addWidget(tableWidget)
        tableWidget.selectionModel().selectionChanged.connect(self.on_selectionChanged)

    def on_selectionChanged(self, selected, deselected):
        #print(selected, deselected)
        for ix in selected.indexes():
            print('Selected Cell Locaton Row : {0}, Column: {1}'.format(ix.row(), ix.column()))
        
        for ix in deselected.indexes():
            print('Deselected Cell Locaton Row : {0}, Column: {1}'.format(ix.row(), ix.column()))
        
if __name__=='__main__':
    app=QApplication(sys.argv)
    app.setStyleSheet('''QWidget{ font-size : 15px; }''')
    myApp = MyApp()
    myApp.show()
    try:
        sys.exit(app.exec_())
    except SystemError:
        print('Closing window...')    

# %% QTableWidget 종합예제 : QTableWidgetItem, setItem, selectedRanges, currentItem
# 출처: https://freeprog.tistory.com/333 [취미로 하는 프로그래밍 !!!]

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import random

class MyTable(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.table = QTableWidget(parent)
        self._mainwin = parent

        self.__make_layout()
        self.__make_table()

    def __make_table(self):
        #self.table.setSelectionBehavior(QTableView.SelectRows)  # row 전체 선택 가능
        self.table.setSelectionMode(QAbstractItemView.MultiSelection)
        #self.table.setSelectionMode(QAbstractItemView.SingleSelection)

        # row, column 갯수 설정해야만 tablewidget 사용할수있다.
        self.table.setColumnCount(5)
        self.table.setRowCount(3)

        # column header 명 설정.
        self.table.setHorizontalHeaderLabels(["코드", "종목명"])
        self.table.horizontalHeaderItem(0).setToolTip("코드...")  # header tooltip
        self.table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignRight)  # header 정렬 방식

        header_item = QTableWidgetItem("추가")
        header_item.setBackground(Qt.red)  # 헤더 배경색 설정 --> app.setStyle() 설정해야만 작동한다.
        self.table.setHorizontalHeaderItem(2, header_item)

        # cell 에 data 입력하기
        self.table.setItem(0, 0, QTableWidgetItem("000020"))
        self.table.setItem(0, 1, QTableWidgetItem("삼성전자"))
        self.table.setItem(1, 0, QTableWidgetItem("000030"))
        self.table.setItem(1, 1, QTableWidgetItem("현대차"))
        self.table.setItem(2, 0, QTableWidgetItem("000080"))
        item = QTableWidgetItem("기아차")
        self.table.setItem(2, 1, item)
        # self.table.resizeColumnsToContents()
        # self.table.resizeRowsToContents()

        #self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # edit 금지 모드

        self.table.setCurrentCell(2, 1)  # current cell 위치 지정하기
        self.table.setColumnWidth(2, 150)
        ckbox1 = QCheckBox("Check")
        self.table.setCellWidget(0, 2, ckbox1)
        ckbox2 = QCheckBox('me')
        self.table.setCellWidget(1, 2, ckbox2)

        mycom = QComboBox()
        mycom.addItems(["aa", "dd", "kk"])
        mycom.addItem("cc")
        mycom.addItem("bb")
        self.table.setCellWidget(2, 2, mycom)

        item_widget = QPushButton("test")
        self.table.setCellWidget(1, 3, item_widget)

        self.table.cellClicked.connect(self.__mycell_clicked)
        mycom.currentTextChanged.connect(self.__mycom_text_changed)
        self.table.cellChanged.connect(self.__cell_changed)

    def __make_layout(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.table)
    
        grid = QGridLayout()
        vbox.addLayout(grid)
        # grid.setSpacing(20)
    
        btn1 = QPushButton("전체내용 삭제")
        grid.addWidget(btn1, 0, 0)
        btn2 = QPushButton("table삭제")
        grid.addWidget(btn2, 0, 1)
        btn3 = QPushButton("selection mode")
        grid.addWidget(btn3, 0, 2)
        btn4 = QPushButton("column 추가")
        grid.addWidget(btn4, 0, 3)
    
        btn5 = QPushButton("column 삽입")
        grid.addWidget(btn5, 1, 0)
        btn6 = QPushButton("column 삭제")
        grid.addWidget(btn6, 1, 1)
        btn7 = QPushButton("row 추가")
        grid.addWidget(btn7, 1, 2)
        btn8 = QPushButton("row 삽입")
        grid.addWidget(btn8, 1, 3)
    
        btn9 = QPushButton("row 삭제")
        grid.addWidget(btn9, 2, 0)
        btn10 = QPushButton("row 단위선택")
        grid.addWidget(btn10, 2, 1)
        btn11 = QPushButton("grid line 숨기기")
        grid.addWidget(btn11, 2, 2)
        btn12 = QPushButton("alternate color")
        grid.addWidget(btn12, 2, 3)
    
        btn13 = QPushButton("randorm row 선택")
        grid.addWidget(btn13, 3, 0)
        btn14 = QPushButton("edit")
        grid.addWidget(btn14, 3, 1)
        btn15 = QPushButton("hide row헤더")
        grid.addWidget(btn15, 3, 2)
        btn16 = QPushButton("hide column헤더")
        grid.addWidget(btn16, 3, 3)
    
        btn17 = QPushButton("selected cells")
        grid.addWidget(btn17, 4, 0)
        btn18 = QPushButton("selected ranges")
        grid.addWidget(btn18, 4, 1)
        btn19 = QPushButton("current cell 내용")
        grid.addWidget(btn19, 4, 2)
        btn20 = QPushButton("(0,0) cell 내용")
        grid.addWidget(btn20, 4, 3)
    
        btn21 = QPushButton("span")
        grid.addWidget(btn21, 5, 0)
        btn22 = QPushButton("바탕화면 바꾸기")
        grid.addWidget(btn22, 5, 1)
        btn23 = QPushButton("cell 배경 바꾸기")
        grid.addWidget(btn23, 5, 2)
        btn24 = QPushButton("선택시 색 변경 ")
        grid.addWidget(btn24, 5, 3)
    
        btn25 = QPushButton("헤더배경색 변경")
        grid.addWidget(btn25, 6, 0)
        btn26 = QPushButton("(1,2) checkbox 값")
        grid.addWidget(btn26, 6, 1)
        btn27 = QPushButton("정렬 설정하기")
        grid.addWidget(btn27, 6, 2)
        btn28 = QPushButton("column, row 숨기기")
        grid.addWidget(btn28, 6, 3)
    
        self.setLayout(vbox)
    
        btn1.clicked.connect(self.__btn1_clicked)
        btn2.clicked.connect(self.__btn2_clicked)
        btn3.clicked.connect(self.__btn3_clicked)
        btn4.clicked.connect(self.__btn4_clicked)
        btn5.clicked.connect(self.__btn5_clicked)
        btn6.clicked.connect(self.__btn6_clicked)
        btn7.clicked.connect(self.__btn7_clicked)
        btn8.clicked.connect(self.__btn8_clicked)
        btn9.clicked.connect(self.__btn9_clicked)
        btn10.clicked.connect(self.__btn10_clicked)
        btn11.clicked.connect(self.__btn11_clicked)
        btn12.clicked.connect(self.__btn12_clicked)
        btn13.clicked.connect(self.__btn13_clicked)
        btn14.clicked.connect(self.__btn14_clicked)
        btn15.clicked.connect(self.__btn15_clicked)
        btn16.clicked.connect(self.__btn16_clicked)
        btn17.clicked.connect(self.__btn17_clicked)
        btn18.clicked.connect(self.__btn18_clicked)
        btn19.clicked.connect(self.__btn19_clicked)
        btn20.clicked.connect(self.__btn20_clicked)
        btn21.clicked.connect(self.__btn21_clicked)
        btn22.clicked.connect(self.__btn22_clicked)
        btn23.clicked.connect(self.__btn23_clicked)
        btn24.clicked.connect(self.__btn24_clicked)
        btn25.clicked.connect(self.__btn25_clicked)
        btn26.clicked.connect(self.__btn26_clicked)
        btn27.clicked.connect(self.__btn27_clicked)
        btn28.clicked.connect(self.__btn28_clicked)
    
    @pyqtSlot(int, int)
    def __cell_changed(self, row, col):
        txt = "Cell value changed (row:{0}, col:{1})".format(row, col)
        QMessageBox.information(self, 'combobox changed...', txt)
        
    @pyqtSlot(int, int)
    def __mycell_clicked(self, row, col):
        cell = self.table.item(row, col)
        # print(cell)

        if cell is not None:
            txt = "clicked cell = ({0},{1}) ==>{2}<==".format(row, col, cell.text())
        else:
            txt = "clicked cell = ({0},{1}) ==>None type<==".format(row, col)

        # msg = QMessageBox.information(self, 'clicked cell...', txt)

        self._mainwin.statusbar.showMessage(txt)
        return

    @pyqtSlot(str)
    def __mycom_text_changed(self, txt):
        msg = QMessageBox.information(self, 'combobox changed...', txt)
        return

    @pyqtSlot()
    def __btn1_clicked(self):
        self.table.clearContents()  # 헤더는 제거 안함.

    @pyqtSlot()
    def __btn2_clicked(self):
        self.table.clear()   # 헤더도 제거함.

    @pyqtSlot()
    def __btn3_clicked(self):
        self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)  # drag, Ctrl, Shift 키로 다중 선택 가능.
        # self.table.setSelectionMode(QAbstractItemView.MultiSelection)
        # self.table.setSelectionMode(QAbstractItemView.NoSelection)   # 선택 불능.
        # self.table.setSelectionMode(QAbstractItemView.SingleSelection)  # 다중 선택 불가능.
        # self.table.setSelectionMode(QAbstractItemView.ContiguousSelection)

    @pyqtSlot()
    def __btn4_clicked(self):
        # self.table.setColumnCount(3)  # column 추가.
        col_count = self.table.columnCount()
        # print("col_count = {0}".format(col_count))
        self.table.setColumnCount(col_count+1)

    @pyqtSlot()
    def __btn5_clicked(self):
        self.table.insertColumn(1)  # 1 번재 자리에 column 삽입

    @pyqtSlot()
    def __btn6_clicked(self):
        self.table.removeColumn(2)  # column 삭제

    @pyqtSlot()
    def __btn7_clicked(self):
        row_count = self.table.rowCount()
        self.table.setRowCount(row_count+1)   # row 추가

    @pyqtSlot()
    def __btn8_clicked(self):
        self.table.insertRow(0)   # 0번재 자리에 row 삽입

    @pyqtSlot()
    def __btn9_clicked(self):
        self.table.removeRow(1)   # 1번째 row 삭제

    @pyqtSlot()
    def __btn10_clicked(self):
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)  # row 단위로 선택 가능
        # self.table.setSelectionBehavior(QAbstractItemView.SelectColumns)  # column 단위로 선택
        # self.table.setSelectionBehavior(QAbstractItemView.SelectItems)  # cell 단위로 선택 가능
        return

    @pyqtSlot()
    def __btn11_clicked(self):
        sender_obj = self.sender()
        if sender_obj.text() == "grid line 숨기기":
            self.table.setShowGrid(False)  # grid line 숨기기
            sender_obj.setText("grid line 보이기")
        else:
            self.table.setShowGrid(True)  # grid line 숨기기
            sender_obj.setText("grid line 숨기기")
        return

    @pyqtSlot()
    def __btn12_clicked(self):
        sender_obj = self.sender()
        if sender_obj.text() == "alternate color":
            self.table.setAlternatingRowColors(True)
            sender_obj.setText("no alternate")
        else:
            self.table.setAlternatingRowColors(False)
            sender_obj.setText("alternate color")
        return

    @pyqtSlot()
    def __btn13_clicked(self):
        row_cnt = self.table.rowCount()
        row_idx = random.randint(0, row_cnt-1)

        # current SelectionMode 와 SelectionBehavior 모두 row 선택가능하게 되어야만 작동한다.
        self.table.selectRow(row_idx)  # 해당 index 의 row 선택하기
        return

    @pyqtSlot()
    def __btn14_clicked(self):
        sender_obj = self.sender()
        if sender_obj.text() == "edit":
            self.table.setEditTriggers(QAbstractItemView.AllEditTriggers)
            sender_obj.setText("no edit")
        else:
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # edit 금지 모드
            sender_obj.setText("edit")
        return

    @pyqtSlot()
    def __btn15_clicked(self):
        sender_obj = self.sender()
        if sender_obj.text() == "hide row헤더":
            self.table.verticalHeader().setVisible(False)  # row header 숨기기
            sender_obj.setText("show row헤더")
        else:
            self.table.verticalHeader().setVisible(True)  # row header 보이기
            sender_obj.setText("hide row헤더")
        return

    @pyqtSlot()
    def __btn16_clicked(self):
        sender_obj = self.sender()
        if sender_obj.text() == "hide column헤더":
            self.table.horizontalHeader().setVisible(False)  # column header 숨기기
            sender_obj.setText("show column헤더")
        else:
            self.table.horizontalHeader().setVisible(True)  # column header 보이기
            sender_obj.setText("hide column헤더")
        return

    @pyqtSlot()
    def __btn17_clicked(self):
        aa = self.table.selectedIndexes()
        cell = set( (idx.row(), idx.column()) for idx in aa )
        # print(cell)
        txt1 = "selected cells ; {0}".format(cell)
        msg = QMessageBox.information(self, 'selectedIndexes()...',  txt1)
        return

    @pyqtSlot()
    def __btn18_clicked(self):
        aa = self.table.selectedRanges()
        txt = []
        for idx, sel in enumerate(aa):
            # print(sel.rowCount(), sel.columnCount(), sel.topRow(), sel.leftColumn(), sel.bottomRow(), sel.rightColumn())
            tmp = "ranage {0} ; row/col Count={1}/{2} ".format(idx,sel.rowCount(), sel.columnCount() ) + \
                  "({0},{1}) ~ ({2},{3})".format(sel.topRow(), sel.leftColumn(), sel.bottomRow(), sel.rightColumn())
            txt.append(tmp)
        msg = QMessageBox.information(self, 'selectedRanges()...', '\n'.join(txt))
        return

    @pyqtSlot()
    def __btn19_clicked(self):
        aa = self.table.currentItem()
        # print(aa)

        if aa is not None:
            txt = "row={0}, column={1}, content={2}".format(aa.row(), aa.column(), aa.text())
        else:
            txt = "clicked cell = ({0},{1}) ==>None type<==".format(self.table.currentRow(), self.table.currentColumn())

        msg = QMessageBox.information(self, 'cell 내용', txt)
        return

    @pyqtSlot()
    def __btn20_clicked(self):
        item = self.table.item(0, 0)   # (0,0) cell 의 item 가져오기.
        if item is not None:
            txt = item.text()
        else:
            txt = "no data"
        msg = QMessageBox.information(self, "(0,0) 내용", txt)
        return

    @pyqtSlot()
    def __btn21_clicked(self):
        col_count = self.table.columnCount()
        self.table.setColumnCount(col_count+1)
        self.table.setSpan(1, col_count, 2, 1)  # 2 x 1 크기의 span 생성

        self.table.setCellWidget(1, col_count, QPushButton("span"))
        # self.table.resize(500,600)
        return

    @pyqtSlot()
    def __btn22_clicked(self):
        """
        버튼 누를때 마다 임의의 배경화면...
        
        ** QPalette.Base  ==> text 사용 widget 의 background 로 사용하겠다는 의미.
        :return: 
        """
        palette = QPalette()

        x = random.randint(1, 4)   # 1 <=  x <= 4  사이의 임의의 수
        if x == 1:
            palette.setBrush(QPalette.Base, QBrush(QPixmap("img77.jpg")))
        elif x == 2:
            palette.setColor(QPalette.Base, Qt.yellow)
        elif x == 3:
            palette.setColor(QPalette.Base, QColor(255, 255, 255))   # white
        else:
            palette.setColor(QPalette.Base, QColor(0, 255, 0))

        self.table.setPalette(palette)  # table 배경 설정
        return

    @pyqtSlot()
    def __btn23_clicked(self):
        x = random.randint(1, 3)  # 1 <=  x <= 3  사이의 임의의 수
        myitem = self.table.item(0, 0)
        if x == 1:
            myitem.setBackground(QBrush(QPixmap("exit.png")))  # cell 배경
            myitem.setForeground(QBrush(Qt.red))  # 글자색
            myitem.setFont(QFont("Times", 17, QFont.Bold, italic=True))  # 글자 폰트 설정.
        elif x == 2:
            myitem.setBackground(QBrush(Qt.red))
            myitem.setForeground(QBrush(Qt.yellow))
            myitem.setFont(QFont("Helvetica", 8, QFont.Normal, italic=False))
        else:
            myitem.setBackground(QBrush(QColor(0, 255, 0)))
            myitem.setForeground(QBrush(Qt.blue))
            myitem.setFont(QFont('SansSerif', 25))
        return

    @pyqtSlot()
    def __btn24_clicked(self):
        """
        ** QPalette.Highlight  ==> item 선택시 배경화면 설정.
                                    default ; Qt.darkBlue
        
        ** QPalette.HighlightedText  ==> item 선택시 글자색 설정.
                                          default ; Qt.white
        :return: 
        """
        palette = QPalette()
        palette.setColor(QPalette.Highlight, Qt.yellow)  # default ==> Qt.darkBlue
        palette.setColor(QPalette.HighlightedText, Qt.red)  # default ==> Qt.white
        self.table.setPalette(palette)
        return

    @pyqtSlot()
    def __btn25_clicked(self):
        """
        ** 헤더 배경색 설정 --> app.setStyle() 설정해야만 작동한다.
        ** 헤더명 설정안하고, Qt 가 자동으로 만든 헤더(숫자)는 인식못한다...
        :return: 
        """
        hitem = self.table.horizontalHeaderItem(1)
        if hitem is not None:
            hitem.setBackground(QBrush(Qt.cyan))
        # print(hitem)
        # print(hitem.text())
        return

    @pyqtSlot()
    def __btn26_clicked(self):
        ckbox = self.table.cellWidget(1, 2)
        # print(ckbox)
        if isinstance(ckbox, QCheckBox):
            if ckbox.isChecked():
                print("checked")
                _ = QMessageBox.information(self, 'checkbox', "checked")
            else:
                _ = QMessageBox.information(self, 'checkbox', "no checked")
        else:
            _ = QMessageBox.information(self, 'checkbox', "checkbox 아닙니다.")
        return

    @pyqtSlot()
    def __btn27_clicked(self):
        """
        헤더 click 시에 정렬 가능하게 함.
        :return: 
        """
        sender_obj = self.sender()
        if sender_obj.text() == "정렬 설정하기":
            self.table.setSortingEnabled(True)  # default ; False
            sender_obj.setText("정렬 안함")
        else:
            self.table.setSortingEnabled(False)
            sender_obj.setText("정렬 설정하기")
        return

    @pyqtSlot()
    def __btn28_clicked(self):
        """
        column, row 숨기기
        :return: 
        """
        sender_obj = self.sender()
        if sender_obj.text() == "column, row 숨기기":
            self.table.setColumnHidden(2, True)
            self.table.setRowHidden(0, True)
            sender_obj.setText("column, row 보이기")
        else:
            self.table.setColumnHidden(2, False)
            self.table.setRowHidden(0, False)
            sender_obj.setText("column, row 숨기기")
        return


class MyMain(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        table = MyTable(self)
        table.setStyle(QStyleFactory.create('Fusion'))
        self.setCentralWidget(table)

        self.statusbar = self.statusBar()
        self.statusbar.showMessage("this is status bar")
        
        self.setGeometry(600, 300, 600, 600)  # x,y, w,h
        self.setWindowTitle("tablewidget example")

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))  # --> 없으면, 헤더색 변경 안됨.
    # w = MyTable()
    w = MyMain()
    w.show()
    sys.exit(app.exec())
    
# %% PyQt5 context menu 구현방법(1) : ActionsContextMenu /QAction /addAction 

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import *

class TableWidget(QTableWidget):  # QTableWidget 상속
    """
    ContextMenuPolicy --> ActionsContextMenu
    """
    def __init__(self, parent=None):
        QTableWidget.__init__(self, parent)
        self.resize(500, 200)
        self.setColumnCount(3)
        self.setRowCount(3)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)

        copy_action = QAction("복사하기", self)
        quit_action = QAction("Quit", self)

        self.addAction(copy_action)
        self.addAction(quit_action)

        copy_action.triggered.connect(self.__copy)
        quit_action.triggered.connect(app.quit)

    @pyqtSlot()
    def __copy(self):
        print("복사...")

if __name__ == "__main__":
    import sys
    #app = QApplication(sys.argv)   
    app = QApplication([])
    tableWidget = TableWidget()
    tableWidget.show()
    sys.exit(app.exec_())

# %% PyQt5 context menu 구현방법(2) : ActionsContextMenu /QAction/ addAction 

import sys
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import *

class MyTest(QWidget):  # QTableWidget 상속없음
    """
        ContextMenuPolicy --> ActionsContextMenu
    """
    def __init__(self):
        super().__init__()
        
        table = QTableWidget(2, 3, self)
        # table.setRowCount(2)
        # table.setColumnCount(3)

        table.setContextMenuPolicy(Qt.ActionsContextMenu)

        copy_action = QAction("복사하기", table)
        quit_action = QAction("Quit", table)

        table.addAction(copy_action)
        table.addAction(quit_action)

        copy_action.triggered.connect(self.__copy)
        quit_action.triggered.connect(app.quit)

        vbox = QVBoxLayout()
        vbox.addWidget(table)
        self.setLayout(vbox)
        self.resize(500, 200)

    @pyqtSlot()
    def __copy(self):
        print("복사...")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyTest()
    ex.show()
    sys.exit(app.exec_())
    
# %% PyQt5 context menu 구현방법(3) : DefaultContextMenu /mapToGlobal /event.pos /QMenu /addAction

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot

class TableWidget(QTableWidget):
    def __init__(self, *args):
        QTableWidget.__init__(self, *args)
        # super().__init__(*args)
        self.resize(600, 200)
        # self.setColumnCount(3)
        # self.setRowCount(3)

    def contextMenuEvent(self, event):
        """
        ContextMenuPolicy --> DefaultContextMenu
        """
        print(event.pos())
        print(self.mapToGlobal(event.pos()))
        
        menu = QMenu(self)
        copy_action = menu.addAction("복사하기")
        quit_action = menu.addAction("Quit")
        
        copy_action.triggered.connect(self.copy)        
        quit_action.triggered.connect(app.quit)
        menu.exec_(self.mapToGlobal(event.pos()))
        
        # action = menu.exec_(self.mapToGlobal(event.pos()))
        # if action == copy_action:
        #     print("copy...")
        # elif action == quit_action:
        #     app.quit()
            
    @pyqtSlot()
    def copy(self):
        print("복사...")
        
if __name__ == "__main__":
    app = QApplication([])
    # tableWidget = TableWidget()
    tableWidget = TableWidget(4,5)
    tableWidget.show()
    sys.exit(app.exec_())
    
# %% PyQt5 context menu 구현방법(4) : CustomContextMenu /customContextMenuRequested /QMenu /addAction

import sys
from PyQt5.QtCore import Qt, QPoint, pyqtSlot
from PyQt5.QtWidgets import *

class MyTest(QWidget):
    """
    ContextMenuPolicy --> CustomContextMenu
    ; QPoint를 매개변수로 사용하는 customContextMenuRequested singal을 사용한다.
    """
    def __init__(self):
        super().__init__()
        self.resize(600, 300)
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setRowCount(3)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.__context_menu)
        #self.table.resize(400, 200)
        #self.table.resizeColumnsToContents()
        vbox = QVBoxLayout()
        vbox.addWidget(self.table)
        self.setLayout(vbox)

    @pyqtSlot(QPoint)
    def __context_menu(self, position):
        
        menu = QMenu()
        copy_action = menu.addAction("복사하기")
        quit_action = menu.addAction("Quit")
        
        action = menu.exec_(self.table.mapToGlobal(position))
        
        if action == copy_action:
            print("copy...")
        elif action == quit_action:
            app.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyTest()
    ex.show()
    sys.exit(app.exec_())
