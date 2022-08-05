#%% QTableWidget 활용(1) : 행 단위 배경색 변경하기 - setAlternatingRowColors(True)

import sys, numpy as np
from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (QDialog, QTableWidget, QTableWidgetItem, QApplication,
                               QHeaderView, QPushButton, QHBoxLayout,
                               QVBoxLayout,QAbstractItemView, QLineEdit)
# pySide6 설치 폴더 설정하기
pkgDir = 'C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python39\\Lib\\site-packages\\PySide6\\plugins'
# pkgDir = "C:\ProgramData\Miniconda3\envs\spyder-env\Lib\site-packages\PySide6\plugins"
# pkgDir = 'C:\ProgramData\Anaconda3\Lib\site-packages\PySide6\plugins'
QApplication.setLibraryPaths([pkgDir])

class MyTable(QTableWidget):
    def __init__(self, horizonatlHearderLabels, parent = None):
        super().__init__(parent)

        self.setRowCount(1)
        self.setColumnCount(len(horizonatlHearderLabels))
        self.setAlternatingRowColors(True)
        self.setStyleSheet("alternate-background-color: white; background-color: lightblue;")
    
        self.setSelectionMode(QAbstractItemView.ContiguousSelection)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setHorizontalHeaderLabels(horizonatlHearderLabels)
        print(self.columnCount())
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                item = QTableWidgetItem("")
                item.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
                self.setItem(i,j,item)               

        copyShortcut = QShortcut(QKeySequence.Copy,self)
        pasteShortcut = QShortcut(QKeySequence.Paste,self)

        copyShortcut.activated.connect(self.copy)
        pasteShortcut.activated.connect(self.paste)

    def setData(self, data):
        self.setRowCount(0)    # erase data
        row, col = data.shape
        self.setColumnCount(col)
        self.setRowCount(row)
        print(data)
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                item = QTableWidgetItem(str(data[i,j]))
                item.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
                self.setItem(i,j,item)               

    def data(self):
        r = np.zeros(self.rowCount(),self.columnCount())
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                r[i,j]=float(self.items(i,j).text())
        return r   

    def keyPressEvent(self,event):
        super().keyPressEvent(event)

        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter :
            i = self.currentRow() + 1
            j = self.currentColumn()
            if i == self.rowCount():
                self.setRowCount(i+1)
                for kk in range(self.columnCount()):
                    item = QTableWidgetItem()
                    item.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
                    self.setItem(i,kk,item)
            self.setCurrentCell(i,j)
            event.accept()

    def copy(self):
        selectedRangeList = self.selectedRanges()
        if selectedRangeList == [] :
            return

        text = ""
        selectedRange = selectedRangeList[0]
        for i in range(selectedRange.rowCount()):
            if i > 0:
                text += "\n"
            for j in range(selectedRange.columnCount()):
                if j > 0:
                    text += "\t"
                itemA = self.item(selectedRange.topRow()+i,selectedRange.leftColumn()+j)
                if itemA :
                    text += itemA.text()
        text += '\n'

        QApplication.clipboard().setText(text)    

    def paste(self):
        # 1\t2\n2\t3\n 
        text = QApplication.clipboard().text()

        rows = text.split('\n')
        numRows = len(rows)-1
        numColumns = rows[0].count('\t')+1

        if self.currentRow()+numRows > self.rowCount():
            prevRowCount = self.rowCount()
            self.setRowCount(self.currentRow()+numRows)
            for i in range(prevRowCount,self.currentRow()+numRows):
                for kk in range(self.columnCount()):
                    item = QTableWidgetItem()
                    item.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
                    self.setItem(i,kk,item)

        for i in range(numRows):
            columns = rows[i].split('\t')
            for j in range(numColumns):
                row = self.currentRow()+i
                column = self.currentColumn()+j
                if column < self.columnCount():
                    self.item(row,column).setText(columns[j])

class XYTableDialog(QDialog):
    def __init__(self,horizonatlHearderLabels, data, parent=None):
        super().__init__(parent)

        self.table = MyTable(horizonatlHearderLabels, parent)
        self.table.setData(data)

        self.closeButton = QPushButton("&Close")
        bottomLayout = QHBoxLayout()
        bottomLayout.addStretch()
        bottomLayout.addWidget(self.closeButton)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addLayout(bottomLayout)

        self.setLayout(layout)
        self.closeButton.clicked.connect(self.close)
        self.resize(500,400)

if __name__ == '__main__':
    
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    data = np.array([ [0.0, 0.9, 3 ],
                      [0.2, 11.0,3],
                      [0.4, 15.4,3],
                      [0.6, 12.9,3],
                      [0.8, 8.5, 3],
                      [1.0, 7.1, 3],
                      [1.2, 4.0 ,3],
                      [1.4, 13.6,3],
                      [1.6, 22.2,3],
                      [1.8, 22.2,3]])

    dlg = XYTableDialog(["X","Y"], data)
    dlg.show()
    # table = MyTable(["X","Y","Z"])
    # table.setData(data)
    # table.resize(500,400)
    # table.show()

    app.exec_()

#%% QTableWidget 활용(2) : 행 단위 배경색 변경하기

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class MyTableModel(QAbstractTableModel):
    
    def __init__(self, parent=None, *args):
        #super().__init__()        
        QAbstractTableModel.__init__(self, parent, *args)
        self.items = [i for i in range(90)]

    def rowCount(self, parent):
        return len(self.items)   
    
    def columnCount(self, parent):
        return 1

    def data(self, index, role):
        if not index.isValid():
            return QVariant()

        row=index.row()
        column=index.column()

        if role == Qt.DisplayRole:
            if row<len(self.items):
                return QVariant(self.items[row])
            else:
                return QVariant()

        if role==Qt.BackgroundColorRole:
            if row%2: bgColor=QColor(Qt.green)
            else: bgColor=QColor(Qt.blue)        
            return QVariant(QColor(bgColor))


class Proxy01(QSortFilterProxyModel):
    def __init__(self):
        super(Proxy01, self).__init__()

    def filterAcceptsRow(self, row, parent):
        if row%3: return True
        else: return False

class MyWindow(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)

        self.tablemodel=MyTableModel(self)               
        self.proxy1=Proxy01()
        self.proxy1.setSourceModel(self.tablemodel)

        tableviewA=QTableView(self) 
        tableviewA.setModel(self.proxy1)
        tableviewA.setSortingEnabled(True) 
        tableviewA.horizontalHeader().setSortIndicator(0, Qt.AscendingOrder)
        tableviewA.horizontalHeader().setStretchLastSection(True)

        layout = QVBoxLayout(self)
        layout.addWidget(tableviewA)

        self.setLayout(layout)

    def test(self, arg):
        print(arg)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MyWindow()
    w.show()
    sys.exit(app.exec_()) 
    
#%% QTableWidget 활용(3) : 행 배경색 변경 /셀 합치기

import sys
from PyQt5 import QtGui, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import *

prev_day = "2020-10-15"

query_result = [(683, 18, 765, 1.73, '1 ring ruby ring', 685.71, 'vincent percy', 'john joseph croft'),
                (684, 14, 900, 4.48, '1 earring ear drop', 534.86, 'Ben Otten', 'Anne Cooksley Beltrame'),
                (684, 14, 900, 2.1, '1 ring cluster ring', 534.86, 'Ben Otten', 'Anne Cooksley Beltrame'),
                (684, 18, 900, 1.3, '1 ring eternity band', 685.71, 'Ben Otten', 'Anne Cooksley Beltrame'),
                (685, 14, 200, 3.26, '1 ring promise ring', 534.86, 'raymond bob', 'owen george taylor'),
                (686, 24, 450, 10.0, '1 bullion Gold bar', 914.28, 'vincent percy', 'owen george taylor'),
                (687, 14, 345, 4.75, '1 earring Dangles Earring', 534.86, 'Ben Otten', 'dan justin balmers'),
                (688, 18, 810, 3.1, '1 earring fish hookEarring', 677.14, 'raymond bob', 'jeff david steve'),
                (688, 21, 810, 2.6, '1 ring ANTIQUE RING', 790, 'raymond bob', 'jeff david steve')]

class Window(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("mini_ui")
        self.setGeometry(300, 150, 800, 600)
        self.Ui()
        
    def Ui(self):
        vbox = QVBoxLayout()
        btn_show_table = QPushButton("view sample data")
        btn_show_table.clicked.connect(self.today_sales_table)
        self.viewTodayTable = QTableWidget()
        self.viewTodayTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.viewTodayTable.setObjectName("viewTodayTable")
        self.viewTodayTable.setColumnCount(8)
        self.viewTodayTable.setRowCount(0)
        self.viewTodayTable.setHorizontalHeaderItem(0, QTableWidgetItem("Order ID"))
        self.viewTodayTable.setHorizontalHeaderItem(1, QTableWidgetItem("Karat"))
        self.viewTodayTable.setHorizontalHeaderItem(2, QTableWidgetItem("Price"))
        self.viewTodayTable.setHorizontalHeaderItem(3, QTableWidgetItem("Weight"))
        self.viewTodayTable.setHorizontalHeaderItem(4, QTableWidgetItem("Description"))
        self.viewTodayTable.setHorizontalHeaderItem(5, QTableWidgetItem("Gram price"))
        self.viewTodayTable.setHorizontalHeaderItem(6, QTableWidgetItem("Employee"))
        self.viewTodayTable.setHorizontalHeaderItem(7, QTableWidgetItem("Client"))
        self.viewTodayTable.horizontalHeader().setDefaultSectionSize(130)
        self.viewTodayTable.horizontalHeader().setSortIndicatorShown(True)
        self.viewTodayTable.horizontalHeader().setStretchLastSection(True)
        #self.viewTodayTable.setAlternatingRowColors(True)
        
        vbox.addWidget(btn_show_table)
        vbox.addWidget(self.viewTodayTable)
        self.setLayout(vbox)
        self.show()

    def apply_span_to_sales_table(self, row, nrow):
        if nrow <= 1:
            return
        for c in (0, 2, 6, 7):
            self.viewTodayTable.setSpan(row, c, nrow, 1)
            for r in range(row + 1, row + nrow):
                t = self.viewTodayTable.takeItem(r, c)
                del t
                
    def today_sales_table(self):
        today_result = query_result
        self.viewTodayTable.setRowCount(0)

        last_id = -1
        start_row = 0
        for row_number, row_data in enumerate(today_result):
            self.viewTodayTable.insertRow(row_number)
            current_id, *other_values = row_data

            for column_number, data in enumerate(row_data):
                it = QTableWidgetItem(str(data))

                self.viewTodayTable.setItem(row_number, column_number, it)

                if current_id % 2 == 1:
                    self.viewTodayTable.item(row_number, column_number).setBackground(QColor(185, 206, 172))
                    #print("whats up")
                elif current_id % 2 == 0:
                    self.viewTodayTable.item(row_number, column_number).setBackground(QColor(193, 171, 206))
                    #print("whats up 2")

                if last_id != current_id and last_id != -1:
                    self.apply_span_to_sales_table(start_row, row_number - start_row)
                    start_row = row_number

                last_id = current_id
                if start_row != row_number:
                    self.apply_span_to_sales_table(start_row, self.viewTodayTable.rowCount() - start_row)
                    
def main():
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())
    
if __name__ == '__main__':
    main()
    
#%% QTableWidget 활용(4) : 클릭한 셀 배경색 하이라이트

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(950, 650)
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 930, 630))
        self.tableWidget.setRowCount(15)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setObjectName("tableWidget")
        
        for i, col_name in enumerate(['symbol', 'step', 'factor', 'initial_lot', 'max_streak', 'status']):
            self.tableWidget.setHorizontalHeaderItem(i, QTableWidgetItem(col_name))
            
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setMinimumSectionSize(20)

        self.tableWidget.horizontalHeader().setStyleSheet(
            "QHeaderView::section{"
            "border-bottom: 1px solid #4a4848;"
            "background-color:white;}")
        
        self.tableWidget.cellClicked.connect(lambda y, x: self.print_selected(y, x))
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        
        rowlist=[1,3,5]
        self.rowColorChange(rowlist)
        
    def setColortoRow(self, rowIndex, color):
        for j in range(self.tableWidget.columnCount()):
            item=self.tableWidget.item(rowIndex, j)
            if item is not None:
                self.tableWidget.item(rowIndex, j).setBackground(Qt.red)
                #self.tableWidget.item(rowIndex, j).setBackground(QColor(100,255,0))
            
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

    def print_selected(self, y, x):
        pallete = self.tableWidget.palette()
        hightlight_brush = pallete.brush(QPalette.Highlight)
        hightlight_brush.setColor(QColor('yellow'))
        pallete.setBrush(QPalette.Highlight, hightlight_brush)
        self.tableWidget.setPalette(pallete)
        self.setColortoRow(2, QColor('red'))
        self.tableWidget.setBackgroundRole(QPalette.ColorRole())
        print(f"row:{y},col:{x}")
        
    def rowColorChange(self, rowlist):
        for row in rowlist:
            for col in range(self.tableWidget.columnCount()):
                newItem = QTableWidgetItem("")
                newItem.setData(Qt.BackgroundColorRole, QColor(100,255,0)) #QColor('green'))
                self.tableWidget.setItem(row,col,newItem)
            
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
    
#%% QTableWidget 활용(5) : Key 이벤트 처리하기

import sys
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(20)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.keyPressEvent = self.tableKeyPressEvent
        
        self.clearBtn = QPushButton('Clear')
        self.clearBtn.clicked.connect(self.tableWidget.clear)
        self.label = QLabel('')

        self.scrollToTop = QPushButton('Scroll to Top')
        self.scrollToTop.clicked.connect(self.tableWidget.scrollToTop)
        self.scrollToBottom = QPushButton('Scroll to Bottom')
        self.scrollToBottom.clicked.connect(self.tableWidget.scrollToBottom)
        self.tableWidget.cellClicked.connect(self.set_label)

        rand_items = np.random.randint(1, 100, size=(20, 4))

        for i in range(20):
            for j in range(4):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(rand_items[i, j])))

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        layout.addWidget(self.label)        
        layout.addWidget(self.clearBtn)        

        layout.addWidget(self.scrollToTop)
        layout.addWidget(self.scrollToBottom)
        self.setLayout(layout)

        self.setWindowTitle('PyQt5 - QTableWidget')
        self.setGeometry(300, 100, 600, 400)
        self.show()

    def set_label(self, row, column):
        item = self.tableWidget.item(row, column)
        value = item.text()
        label_string = 'Row: ' + str(row+1) + ', Column: ' + str(column+1) + ', Value: ' + str(value)
        self.label.setText(label_string)

    def tableKeyPressEvent(self, event):
        row = self.tableWidget.currentRow()
        col = self.tableWidget.currentColumn()
        print(f"row:{row},col:{col}")
        
        # call the base implementation, do *not* use super()!
        QTableWidget.keyPressEvent(self.tableWidget, event)
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            current = self.tableWidget.currentIndex()
            nextIndex = current.sibling(current.row() + 1, current.column())
            if nextIndex.isValid():
                self.tableWidget.setCurrentIndex(nextIndex)
                self.tableWidget.edit(nextIndex)
                
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())

#%% QTableWidget 활용(6) : 이벤트 QComboBox-currentIndexChanged

import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class tabdemo(QMainWindow):
    def __init__(self):
        super(tabdemo, self).__init__()
        self.setGeometry(50,50,400,300)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.table()
        self.mainHBOX_param_scene = QHBoxLayout()
        self.mainHBOX_param_scene.addWidget(self.tableWidget)
        self.centralWidget.setLayout(self.mainHBOX_param_scene)

    def table(self):

        self.tableWidget = QTableWidget() 
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(5)

        attr = ['one', 'two', 'three', 'four', 'five']
        i = 0
        for j in attr:
            self.tableWidget.setItem(i, 0, QTableWidgetItem(j))
            combobox = QComboBox()
            for txt in ["Sinus","Triangle","Square"]:
                combobox.addItem(txt)
                
            combobox.setProperty('row', i) # 콤보박스에 속성값('row = i') 추가
            combobox.currentIndexChanged.connect(self.Combo_indexchanged)
            self.tableWidget.setCellWidget(i, 1, combobox)
            i += 1   
        
        #self.tableWidget.itemChanged.connect(self.Table_itemchanged)
        
    def Combo_indexchanged(self):
        combo = self.sender()
        row = combo.property('row')
        index = combo.currentIndex()
        print('combo row %d indexChanged to %d' % (row, index))
    
    def Table_itemchanged(self):
        print('Changed')

def main():
   app = QApplication(sys.argv)
   ex = tabdemo()
   ex.show()
   sys.exit(app.exec_())

if __name__ == '__main__':
   main()





