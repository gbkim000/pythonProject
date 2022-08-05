# %% ----- QTableWidget : itemChanged / itemSelectionChanged 이벤트(1)

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

list_text = ["a", "b", "c"]

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(300,300)
        self.initUI()

    def initUI(self):
        self.createTable()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)
        self.show()

    def createTable(self):
        # Create table
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(6)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setItem(0, 0, QTableWidgetItem("Text0"))
        self.tableWidget.setItem(0, 1, QTableWidgetItem("Text1"))
        self.tableWidget.setItem(1, 0, QTableWidgetItem("Text2"))
        self.tableWidget.setItem(1, 1, QTableWidgetItem("Text3"))
        self.tableWidget.setItem(2, 1, QTableWidgetItem("Text4"))
        self.tableWidget.setItem(3, 1, QTableWidgetItem("Text5"))
        
        self.cbx = QComboBox()
        self.cbx.addItems(list_text)
        self.tableWidget.setCellWidget(2, 0, self.cbx)

        self.dsb = QDoubleSpinBox(self)
        self.dsb.setDecimals(2)
        self.dsb.setMinimum(1)
        self.dsb.setMaximum(100)
        self.dsb.setSingleStep(0.1)
        self.dsb.setValue(50)
        self.tableWidget.setCellWidget(3, 0, self.dsb)

        # table selection change
        self.tableWidget.itemChanged.connect(self.on_change)
        self.tableWidget.itemSelectionChanged.connect(self.print_row)
         
    def print_row(self):
        items = self.tableWidget.selectedItems()    # 선택 범위의 아이템을 items 리스트에 담음
        if items:                                   # 리스트가 비어있지 않으면 True
            #print(str(items[0].text()))            # items 리스트의 첫번째 아이템의 텍스트를 출력
            for i in items:
                print(i.text())
        else:
            print('None')
            
    def on_change(self):
        row = self.tableWidget.currentRow()
        col = self.tableWidget.currentColumn()
        text = self.tableWidget.currentItem().text()
        print('row:{0}, col:{1}, text:{2}'.format(row, col, text))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setPalette(app.style().standardPalette())   # default Palette  
    ex = App()
    sys.exit(app.exec_())

# %% ----- QTableWidget : itemChanged / itemSelectionChanged 이벤트(2)
import sys
from PyQt5.QtWidgets import *

lista = ['r1c1', 'r1c2', 'r1c3']
listb = ['r2c1', 'r2c2', 'r1c3']
listc = ['r3c1', 'r3c2', 'r3c3']

mystruct = {'row1': lista, 'row2': listb, 'row3': listc}

class MyTable(QTableWidget):
    def __init__(self, thestruct, *args):
        QTableWidget.__init__(self, *args)
        self.resize(400,200)
        
        self.data = thestruct
        r = 0
        for key in self.data:           # row1, row2, row3
            c = 0
            for item in self.data[key]: # r1c1, r1c2, r1c3 ...
                newitem = QTableWidgetItem(item)
                self.setItem(r, c, newitem)  # setItem(row, col, item)
                c += 1
            r += 1

        self.itemChanged.connect(self.on_change)
        self.itemSelectionChanged.connect(self.print_row)
        
    def print_row(self):
        items = self.selectedItems()    # 선택 범위의 아이템을 items 리스트에 담음
        if items:                                   # 리스트가 비어있지 않으면 True
            #print(str(items[0].text()))            # items 리스트의 첫번째 아이템의 텍스트를 출력
            for i in items:
                print(i.text())
        else:
            print('None')
        
    # table selection change
    def on_change(self):
        row = self.currentRow()
        col = self.currentColumn()
        text = self.currentItem().text()
        print('row:{0}, col:{1}, text:{2}'.format(row, col, text))

def main(args):
    app = QApplication(args)
    table = MyTable(mystruct, 3, 3)
    table.show()
    sys.exit(app.exec())

if __name__=="__main__":
    main(sys.argv)

# %% QTableWidget : eidt 재정의, kepress 이벤트, pyqtSignal 방출 - (방식1)
# blockSignals(True/False)

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal

lista = ['r1c1', 'r1c2', 'r1c3']
listb = ['r2c1', 'r2c2', 'r1c3']
listc = ['r3c1', 'r3c2', 'r3c3']

myStruct = {'row1': lista, 'row2': listb, 'row3': listc}

class QTableWidget(QTableWidget):
    
    cellEditingStarted = pyqtSignal(int, int)

    def edit(self, index, trigger, event):
        result = super(QTableWidget, self).edit(index, trigger, event)
        if result:
            self.cellEditingStarted.emit(index.row(), index.column())
        return result

class MyTable(QWidget):
    def __init__(self):
        # super().__init__()
        QWidget.__init__(self)
        
# class MyTable(QTableWidget):
#     def __init__(self):
#         # super().__init__()
#         QTableWidget.__init__(self)
        
        self.resize(400, 300)
        self.data = myStruct
        self.view = QTableWidget(5, 3)
        self.view.setEditTriggers(QAbstractItemView.DoubleClicked)         
        self.catch = True
        
        r = 0
        for key in self.data:
            c = 0
            for item in self.data[key]:
                newitem = QTableWidgetItem(item)
                self.view.setItem(r, c, newitem)
                c += 1
            r += 1
        self.view.itemSelectionChanged.connect(self.print_row)
        self.layout = QVBoxLayout()
        self.view.cellEditingStarted.connect(self.editStarted)
        self.layout.addWidget(self.view)
        self.setLayout(self.layout)
    
    def editStarted(self):
        print('Edit started !!')

    def print_row(self):
        items = self.view.selectedItems()
        if items:
            print(str(items[0].text()))
        else:
            print('None')

    def keyPressEvent(self, e):
        if not self.catch:
            return QTableWidget.keyPressEvent(self, e)
        
        if e.modifiers() & Qt.ControlModifier:
            print('Control')
    
        if e.modifiers() & Qt.ShiftModifier:
            print('Shift')
    
        if e.modifiers() & Qt.AltModifier:
            print('Alt')
    
        if e.key() == Qt.Key_Delete:
            print('Delete')
    
        elif e.key() == Qt.Key_Backspace:
            print('Backspace')
    
        elif e.key() in [Qt.Key_Return, Qt.Key_Enter]:
            print('Enter')
    
        elif e.key() == Qt.Key_Escape:
            print('Escape')
    
        elif e.key() == Qt.Key_Right:
            print('Right')
    
        elif e.key() == Qt.Key_Left:
            print('Left')
    
        elif e.key() == Qt.Key_Up:
            print('Up')
    
        elif e.key() == Qt.Key_Down:
            print('Down')

def main(args):
    app = QApplication(args)
    table = MyTable()
    table.show()
    sys.exit(app.exec())

if __name__=="__main__":
    main(sys.argv)
   
# %% QTableWidget : kepress 이벤트, cellEditingStarted 이벤트 - (방식2)

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal

lista = ['r1c1', 'r1c2', 'r1c3']
listb = ['r2c1', 'r2c2', 'r1c3']
listc = ['r3c1', 'r3c2', 'r3c3']

myStruct = {'row1': lista, 'row2': listb, 'row3': listc}

class QTableWidget(QTableWidget): # QTableWidget을 먼저 재정의한 후 MyTable에서 사용.
    
    cellEditingStarted = pyqtSignal(int, int)

    def edit(self, index, trigger, event):
        result = super(QTableWidget, self).edit(index, trigger, event)
        if result:
            self.cellEditingStarted.emit(index.row(), index.column())
        return result

class MyTable(QTableWidget):
    def __init__(self, thestruct, *args):
        QTableWidget.__init__(self, *args)
        self.resize(400, 300)
        self.data = thestruct 
        
        r = 0
        for key in self.data:
            c = 0
            for item in self.data[key]:
                newitem = QTableWidgetItem(item)
                self.setItem(r, c, newitem)
                c += 1
            r += 1
            
        self.itemSelectionChanged.connect(self.print_row)
        self.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.cellEditingStarted.connect(self.editStarted)

    def print_row(self):
        items = self.selectedItems()
        print(str(items[0].text()))

    def editStarted(self):
        print('Edit started !!')
        
    def keyPressEvent(self, e):

        def isPrintable(key):
            printable = [
                Qt.Key_Space,
                Qt.Key_Exclam,
                Qt.Key_QuoteDbl,
                Qt.Key_NumberSign,
                Qt.Key_Dollar,
                Qt.Key_Percent,
                Qt.Key_Ampersand,
                Qt.Key_Apostrophe,
                Qt.Key_ParenLeft,
                Qt.Key_ParenRight,
                Qt.Key_Asterisk,
                Qt.Key_Plus,
                Qt.Key_Comma,
                Qt.Key_Minus,
                Qt.Key_Period,
                Qt.Key_Slash,
                Qt.Key_0,
                Qt.Key_1,
                Qt.Key_2,
                Qt.Key_3,
                Qt.Key_4,
                Qt.Key_5,
                Qt.Key_6,
                Qt.Key_7,
                Qt.Key_8,
                Qt.Key_9,
                Qt.Key_Colon,
                Qt.Key_Semicolon,
                Qt.Key_Less,
                Qt.Key_Equal,
                Qt.Key_Greater,
                Qt.Key_Question,
                Qt.Key_At,
                Qt.Key_A,
                Qt.Key_B,
                Qt.Key_C,
                Qt.Key_D,
                Qt.Key_E,
                Qt.Key_F,
                Qt.Key_G,
                Qt.Key_H,
                Qt.Key_I,
                Qt.Key_J,
                Qt.Key_K,
                Qt.Key_L,
                Qt.Key_M,
                Qt.Key_N,
                Qt.Key_O,
                Qt.Key_P,
                Qt.Key_Q,
                Qt.Key_R,
                Qt.Key_S,
                Qt.Key_T,
                Qt.Key_U,
                Qt.Key_V,
                Qt.Key_W,
                Qt.Key_X,
                Qt.Key_Y,
                Qt.Key_Z,
                Qt.Key_BracketLeft,
                Qt.Key_Backslash,
                Qt.Key_BracketRight,
                Qt.Key_AsciiCircum,
                Qt.Key_Underscore,
                Qt.Key_QuoteLeft,
                Qt.Key_BraceLeft,
                Qt.Key_Bar,
                Qt.Key_BraceRight,
                Qt.Key_AsciiTilde, ]

            if key in printable:
                return True
            else:
                return False

        control = False
    
        if e.modifiers() & Qt.ControlModifier:
            print('Control')
            control = True
    
        if e.modifiers() & Qt.ShiftModifier:
            print('Shift')
    
        if e.modifiers() & Qt.AltModifier:
            print('Alt')
    
        if e.key() == Qt.Key_Delete:
            print('Delete')
        
        if not control and isPrintable(e.key()):
            print(e.text())

def main(args):
    app = QApplication(args)
    table = MyTable(myStruct, 3, 3)
    table.show()
    sys.exit(app.exec())

if __name__=="__main__":
    main(sys.argv)

# %% --- QTableView : QTableView / QStandardItemModel 사용하기

import sys,os
from PyQt5.QtGui import QIcon,QStandardItemModel,QStandardItem,QPainter, QBrush, QColor, QFont
from PyQt5.QtCore import Qt,QSize,QModelIndex,QEvent,QPoint,QRect,QObject,pyqtSignal
# from PyQt5.QtWidgets import (QMainWindow, QAction, QApplication, QHBoxLayout, QSplitter, QWidget, QTableView,QGroupBox,
#                              QVBoxLayout,QDialogButtonBox,QPushButton,QCheckBox,QFileDialog,QListView,QHeaderView,
#                              QPlainTextEdit,QMessageBox,QProgressDialog,QItemDelegate,QToolBar,QStackedLayout,QTabWidget,
#                              QToolBox,QStyleOptionViewItem,QStyle,QStyledItemDelegate,QStyleOptionButton)
from PyQt5.QtWidgets import *

class TableWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(600, 300)
        self.initUI()

    def initUI(self):

        Model = QStandardItemModel()
        Model.setColumnCount(5)
        Model.setHorizontalHeaderLabels(["clmn1","clmn2","clmn3"])
        
        Model.appendRow([QStandardItem('11'), QStandardItem('12'), QStandardItem('13')])
        Model.appendRow([QStandardItem('21'), QStandardItem('22'), QStandardItem('23')])
        Model.appendRow([QStandardItem('31'), QStandardItem('32'), QStandardItem('33')])
        Model.appendRow([QStandardItem(str(41)), QStandardItem('42'), QStandardItem(str(43))])

        Model.setItem(1, 0, QStandardItem("==="))
        Model.setItem(2, 1, QStandardItem("20120203000000000000000"))

        Model.item(0, 0).setForeground(Qt.red)
        Model.item(0, 0).setBackground(QBrush(QColor(0, 255, 0)))
        Model.item(0, 0).setFont(QFont("Times", 13, QFont.Bold))
        Model.item(2, 1).setBackground(QBrush(QColor(255, 255, 0)))
        
        Table = QTableView(self)
        Table.setModel(Model)
        Table.clicked.connect(self.printIndex)

        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(20,20,40,40)
        mainLayout.addWidget(Table)

        self.setLayout(mainLayout)

    def printIndex(self, index):
        print(index.row(), index.column())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TableWidget()
    ex.show()
    sys.exit(app.exec_())

# %% QTableWidget : focusInEvent, focusOutEvent, event함수 재정의
    
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtWidgets import QTableWidget, QWidget, QVBoxLayout, QApplication, \
     QAbstractItemView, QTableWidgetItem, QHeaderView

class MyTableWidget(QTableWidget):
    def __init__(self):
        QTableWidget.__init__(self)
        self.keys = [Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right]
        self.catch = False 
        self.setEditTriggers(QAbstractItemView.DoubleClicked) 
        
    def focusInEvent(self, event):
        print('focusInEvent')
        self.catch = False
        return QTableWidget.focusInEvent(self, event)

    def focusOutEvent(self, event):
        print('focusOutEvent')
        self.catch = True
        return QTableWidget.focusOutEvent(self, event)    

    def event(self, event):
        # print('event')
        if self.catch and event.type() == QEvent.KeyRelease and event.key() in self.keys:
            self._moveCursor(event.key())
        return QTableWidget.event(self, event)

    def keyPressEvent(self, event):
        # print('key event')
        if not self.catch:
            return QTableWidget.keyPressEvent(self, event)
        self._moveCursor(event.key())

    def _moveCursor(self, key):
        row = self.currentRow()
        col = self.currentColumn()
        print(row, col)
        self.setCurrentCell(row, col)
        # self.edit(self.currentIndex())

class Widget(QWidget): 
    def __init__(self, parent=None): 
        QWidget.__init__(self)            
        self.resize(800, 400)
        
        table = MyTableWidget()
        table.setRowCount(10)
        table.setColumnCount(10)
        
        for i in range(table.colorCount()):
            table.setHorizontalHeaderItem(i, QTableWidgetItem(f'Title {i}'))
            
        table.resizeColumnsToContents()
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        layout = QVBoxLayout() 
        layout.addWidget(table)  
        self.setLayout(layout) 

app = QApplication([]) 
widget = Widget() 
widget.show() 
app.exec_()

# %% QTableWidget(특정 셀만 수정 허용) : QStyledItemDelegate, createEditor

import sys, random
from PyQt5.QtWidgets import QStyledItemDelegate, QApplication, QTableWidget, QTableWidgetItem

class Delegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        if index.data() == "NN":
            return super(Delegate, self).createEditor(parent, option, index)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    texts = ["Hello", "Stack", "Overflow", "NN"]
    table = QTableWidget(10, 5)
    delegate = Delegate(table)
    table.setItemDelegate(delegate)

    for i in range(table.rowCount()):
        for j in range(table.columnCount()):
            text = random.choice(texts)
            it = QTableWidgetItem(text)
            table.setItem(i, j, it)

    table.resize(640, 480)
    table.show()
    sys.exit(app.exec_())
    
# %% QFrame : setFocusPolicy, focusInEvent

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys, os

class Widget(QLabel):
    def __init__(self, name=''):
        super().__init__(name)
        self.setFocusPolicy(Qt.ClickFocus)
        # self.grabKeyboard()
        self.name = name

    def keyPressEvent(self, *args, **kwargs):
        print('key press on : ', self.name)
        print(args, kwargs)
        super().keyPressEvent(*args, **kwargs)

    def focusInEvent(self, *args, **kwargs):
        super().focusInEvent(*args, **kwargs)
        print('focus in: ', self.name)

class MyWin(QFrame):
    def __init__(self):
        super().__init__()
        self.resize(250, 200)
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.w1 = Widget('w1')
        self.w1.setStyleSheet('background-color: rgb(255, 0, 0)')
        layout.addWidget(self.w1)

        self.w2 = Widget('w2')
        self.w2.setStyleSheet('background-color: rgb(0, 255, 0)')
        layout.addWidget(self.w2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWin()
    window.show()
    app.exec_()

    
# %% QTableWidget(마우스 우클릭시 팝업 메뉴) : setContextMenuPolicy, eventFilter

import sys
from PyQt5.QtCore import Qt, QObject, QEvent
from PyQt5.QtWidgets import *

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        ######UI 세팅########
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(2)
        self.tableWidget.setColumnCount(2)

        self.tableWidget.setItem(0, 0, QTableWidgetItem('Apple'))
        self.tableWidget.setItem(0, 1, QTableWidgetItem('Banana'))
        self.tableWidget.setItem(1, 0, QTableWidgetItem('Orange'))
        self.tableWidget.setItem(1, 1, QTableWidgetItem('Grape'))

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

        self.setWindowTitle('PyQt5 - QTableWidget')
        self.setGeometry(300, 100, 600, 400)
        self.show()
        
        # 메뉴바 활성화
        self.tableWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        
        # 우클릭시 메뉴바 생성
        self.tableWidget.customContextMenuRequested.connect(self.generateMenu)

        # 만약 다른(더블) 클릭으로 메뉴바 생성하고 싶다면
        # self.tableWidget.viewport().installEventFilter(self)

    # installEventFilter사용시 작동(실시간을 요구하기때문에 과부하 많이 걸림)
    def eventFilter(self, source:QObject, event:QEvent):    
        
        # 마우스 더블클릭시
        if( event.type() == QEvent.Type.MouseButtonDblClick and
            event.buttons() == Qt.MouseButton.LeftButton and
            source is self.tableWidget.viewport()
        ):
            self.generateMenu(event.pos())
        
        return super(MyApp, self).eventFilter(source, event)
            
    def generateMenu(self, pos):
        # 빈공간에서
        if(self.tableWidget.itemAt(pos) is None):
            self.emptymMenu = QMenu(self)
            self.emptymMenu.addAction("추가", self.addRow)      
            self.emptymMenu.exec_(self.tableWidget.mapToGlobal(pos)) 
            
        # 아이템에서
        else:
            self.menu = QMenu(self)
            self.menu.addAction("삭제",lambda: self.deleteRow(pos))      
            self.menu.exec_(self.tableWidget.mapToGlobal(pos)) 

    def addRow(self):
        print("추가")
        # 마지막줄에 추가하기 위함
        rowPosition = self.tableWidget.rowCount()
        columnPosition =self.tableWidget.columnCount()
        
        self.tableWidget.insertRow(rowPosition)
        
        # 모든 열에 세팅
        for column in range(columnPosition):
            self.tableWidget.setItem(rowPosition, column, QTableWidgetItem(''))
        
    def deleteRow(self,pos):
        print("삭제", pos)
        self.tableWidget.removeRow(self.tableWidget.indexAt(pos).row())
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    
# %% keyPressEvent : Qt.Key, event.modifiers, Qt.ControlModifier/Qt.ShiftModifier/...
# https://www.python2.net/questions-839609.htm

from PyQt5.QtWidgets import *
from PyQt5.QtGui     import * 
from PyQt5.QtCore    import *

class Widget(QWidget):
    def __init__(self, *args, **kwargs):
        super(Widget, self).__init__(*args, **kwargs)
        self.resize(300,200)
        self.keymap = {}

        for key, value in vars(Qt).items():
            if isinstance(value, Qt.Key):
                self.keymap[value] = key.partition('_')[2]
                print(f'{key} : {self.keymap[value]}')

        self.modmap = {
            Qt.ControlModifier: self.keymap[Qt.Key_Control],
            Qt.AltModifier:     self.keymap[Qt.Key_Alt],
            Qt.ShiftModifier:   self.keymap[Qt.Key_Shift],
            Qt.MetaModifier:    self.keymap[Qt.Key_Meta],
            Qt.GroupSwitchModifier: self.keymap[Qt.Key_AltGr],
            Qt.KeypadModifier:  self.keymap[Qt.Key_NumLock]}
        
        self.label = QLabel()
        self.grid = QGridLayout(self)
        self.grid.addWidget(self.label, 0, 0, alignment = Qt.AlignCenter)
        
    def keyevent_to_string(self, event):
        
        sequence = []
        print()
        for modifier, text in self.modmap.items():
            print(f'{modifier} : {text}')
            if event.modifiers() & modifier:
                sequence.append(text)
                
        key = self.keymap.get(event.key(), event.text())
        
        if key not in sequence:
            sequence.append(key)

        return '+'.join(sequence)
    
    def keyPressEvent(self, event):
        
        keyNames = self.keyevent_to_string(event)
        self.label.setText(keyNames)
        
        if keyNames == "D":
            self.label.setText("{} <- {}".format(self.label.text(), 'Works!'))
            
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())

