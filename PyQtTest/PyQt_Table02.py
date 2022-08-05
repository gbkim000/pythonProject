#%% QTableView 활용(1) : comboBox에 이미지 추가하기
#   QComboBox, QStandardItemModel, QStandardItem, QPixmap
'''
enum ItemDataRole {
    DisplayRole = 0,
    DecorationRole = 1,
    EditRole = 2,
    ToolTipRole = 3,
    StatusTipRole = 4,
    WhatsThisRole = 5,
    // Metadata
    FontRole = 6,
    TextAlignmentRole = 7,
    BackgroundColorRole = 8,
    BackgroundRole = 8,
    TextColorRole = 9,
    ForegroundRole = 9,
    CheckStateRole = 10,
    // Accessibility
    AccessibleTextRole = 11,
    AccessibleDescriptionRole = 12,
    // More general purpose
    SizeHintRole = 13,
    InitialSortOrderRole = 14,
    // Internal UiLib roles. Start worrying when public roles go that high.
    DisplayPropertyRole = 27,
    DecorationPropertyRole = 28,
    ToolTipPropertyRole = 29,
    StatusTipPropertyRole = 30,
    WhatsThisPropertyRole = 31,
    // Reserved
    UserRole = 32
    
    Role            Constant    Desc
    <The general purpose roles>
    Qt.DisplayRole          0   The key data to be rendered in the form of text. (QString)
    Qt.DecorationRole       1   The data to be rendered as a decoration in the form of an icon. (QColor, QIcon or QPixmap)
    Qt.EditRole             2   The data in a form suitable for editing in an editor. (QString)
    Qt.ToolTipRole          3   The data displayed in the item's tooltip. (QString)
    Qt.StatusTipRole        4   The data displayed in the status bar. (QString)
    Qt.WhatsThisRole        5   The data displayed for the item in "What's This?" mode. (QString)
    Qt.SizeHintRole         13  The size hint for the item that will be supplied to views. (QSize)
    
    <Roles describing appearance and meta data (with associated types)>
    Qt.FontRole             6   The font used for items rendered with the default delegate. (QFont)
    Qt.TextAlignmentRole    7   The alignment of the text for items rendered with the default delegate. (Qt.AlignmentFlag)
    Qt.BackgroundRole       8   The background brush used for items rendered with the default delegate. (QBrush)
    Qt.BackgroundColorRole  8   This role is obsolete. Use BackgroundRole instead.
    Qt.ForegroundRole       9   The foreground brush (text color, typically) used for items rendered with the default delegate. (QBrush)
    Qt.TextColorRole        9   This role is obsolete. Use ForegroundRole instead.
    Qt.CheckStateRole       10  This role is used to obtain the checked state of an item. (Qt.CheckState)
    
    <Accessibility roles (with associated types)>
    Qt.AccessibleTextRole   11  The text to be used by accessibility extensions and plugins, such as screen readers. (QString)
    Qt.AccessibleDescriptionRole    12  A description of the item for accessibility purposes. (QString)

    Qt.InitialSortOrderRole 14  This role is used to obtain the initial sort order of a header view section. (Qt.SortOrder). This role was introduced in Qt 4.8.    
    Qt.UserRole             32  The first role that can be used for application-specific purposes.
}
'''
import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QTableView
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QVariant
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap

IMAGE_PATH = "./images/"

class UserModel(QStandardItemModel):
    def __init__(self, fruits = None, parent = None):
        #super().__init__()
        #super().__init__(parent)
        QStandardItemModel.__init__(self, parent)

        for no, dictData in enumerate(fruits):
            print(no, dictData)
            col_1 = QStandardItem(dictData["name"])
            col_2 = QStandardItem(dictData["image"])
            col_3 = QStandardItem(dictData["color"])
            self.setItem(no, 0, col_1)
            self.setItem(no, 1, col_2)
            self.setItem(no, 2, col_3)
            
        self.setHorizontalHeaderLabels(["Name", "Image", "Color"])
        
    def data(self, QModelIndex, role = None):  # 이 함수는 언제 호출되는지 ???
        data = self.itemData(QModelIndex)
        print(data, data[0])
        if role == Qt.DisplayRole:
            if QModelIndex.column() == 1:  # 이미지 경로는 디스플레이 되지 않게 한다.
                return QVariant()
            return data[0]
        if role == Qt.DecorationRole:
            return QPixmap(data[0]).scaledToHeight(20)
        return QVariant()

class Form(QWidget):
    def __init__(self):
        QWidget.__init__(self, flags = Qt.Widget) # Default, 창의 형식과 로고 
        # QWidget.__init__(self, flags = Qt.Dialog)      
        # QWidget.__init__(self, flags = Qt.Window)
        # super().__init__(flags = Qt.Widget)
        # super().__init__()
        self.init_widget()

    def init_widget(self):
        self.setWindowTitle("QComboBox Widget")
        self.setMinimumWidth(350)
        layout = QBoxLayout(QBoxLayout.TopToBottom, parent = self)
        self.setLayout(layout)

        data = [
            {"name": "Apple", "image": IMAGE_PATH + "apple.jpg", "color": "Red"},            
            {"name": "Banana", "image": IMAGE_PATH + "banana.jpg", "color": "Yellow"}]

        model = UserModel(data)

        view = QTableView()
        view.setSelectionBehavior(view.SelectRows)  # 한 줄 단위로 선택
        # self.resize(400,100)
        comboBox = QComboBox()
        comboBox.setView(view)
        comboBox.setModel(model)

        layout.addWidget(comboBox)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())

#%% QTableView 활용(2) : QAbstractTableModel /DataFrame /pandas /numpy
# DataFrame /QAbstractTableModel
# https://stackoverflow.com/questions/10636024/python-pandas-gui-for-viewing-a-dataframe-or-matrix?lq=1

from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5 import QtGui
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class PandasModel(QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """
    def __init__(self, data, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role = Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                if(index.column() != 0):
                    return str('%.2f'%self._data.values[index.row()][index.column()])
                else:
                    return str(self._data.values[index.row()][index.column()])
        return None

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[section]
        elif orientation == Qt.Vertical and role == Qt.DisplayRole:
            return str(self._data.index[section])
        return None

    def flags(self, index):
        flags = super(self.__class__,self).flags(index)
        flags |= Qt.ItemIsSelectable
        flags |= Qt.ItemIsEnabled
        return flags

if __name__=='__main__':
    
    df = pd.DataFrame()
    df['Field1']=np.arange(0,10,.5)
    df['Field2']=np.arange(0,10,.5)
    
    app = QApplication([])
    table = QTableView()
    table.resize(300, 600)
    mymodel = PandasModel(df)
    table.setModel(mymodel)
    table.show()
    app.exec_()
    
#%% QTableView 활용(3) : QStandardItemModel /QSortFilterProxyModel /setModel

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(500, 500)

        self.Table1()
        self.Table2()
        self.Layout()

    def Table1(self):
        self.select_guorpbox = QGroupBox()
        self.select_guorpbox.setTitle("Article 1")

        self.rowcount = 10
        self.columncount = 10

        self.mainTable1_model = QStandardItemModel(self.rowcount, self.columncount)
        # self.mainTable1_model.setHorizontalHeaderLabels(['a', 'b', 'c', 'd'])

        for i in range(self.rowcount):
            for j in range(self.columncount):
                table = QStandardItem("TEST[{},{}]".format(i,j))
                self.mainTable1_model.setItem(i, j, table)
                table.setTextAlignment(Qt.AlignCenter)

        self.textFilter = QSortFilterProxyModel()
        self.textFilter.setSourceModel(self.mainTable1_model)
        self.textFilter.setFilterKeyColumn(2)

        self.SerchLineEdit = QLineEdit()
        self.SerchLineEdit.textChanged.connect(self.textFilter.setFilterRegExp)

        self.mainTable1 = QTableView()
        self.mainTable1.setModel(self.textFilter)
        self.mainTable1.setColumnWidth(1, 150)
        self.mainTable1.setColumnWidth(2, 300)
        self.mainTable1.setEditTriggers(QTableView.NoEditTriggers)
        self.mainTable1.setSelectionBehavior(QTableView.SelectRows)
        # self.mainTable1.setContextMenuPolicy(Qt.CustomContextMenu)
        self.mainTable1.doubleClicked.connect(self.Table1_DoubleClicked)
        # self.mainTable1.customContextMenuRequested.connect(self.table1_CustomContextMenu)

        # column auto sort
        # self.mainTable1.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        # self.mainTable1.resizeColumnsToContents()

        v = QVBoxLayout()
        v.addWidget(self.mainTable1)
        self.select_guorpbox.setLayout(v)

    def Table2(self):
        self.serch_groupbox = QGroupBox()
        self.serch_groupbox.setTitle("Article 2")
        lable = QLabel("~")
        lable.setFixedWidth(10)
        lable.setAlignment(Qt.AlignCenter)
        insertbutton = QPushButton("insert")
        self.startdate = QDateEdit()
        self.startdate.setDate(QDate.currentDate())
        self.startdate.setFixedWidth(150)
        self.startdate.setCalendarPopup(True)
        self.enddate = QDateEdit()
        self.enddate.setDate(QDate.currentDate())
        self.enddate.setFixedWidth(150)
        self.enddate.setCalendarPopup(True)
        self.article_serch_button = QPushButton("ARTICL SERTCH")
        self.article_serch_button.setFixedWidth(250)

        self.mainTable2_model = QStandardItemModel()

        self.mainTable2 = QTableView()
        self.mainTable2.setSelectionBehavior(QTableView.SelectRows)
        self.mainTable2.setContextMenuPolicy(Qt.CustomContextMenu)
        self.mainTable2.customContextMenuRequested.connect(self.Table2_CustomContextMenu)

        h1 = QHBoxLayout()
        h1.addWidget(insertbutton)
        h1.addWidget(self.startdate)
        h1.addWidget(lable)
        h1.addWidget(self.enddate)
        h1.addWidget(self.article_serch_button)
        h2 = QHBoxLayout()
        h2.addWidget(self.mainTable2)

        v = QVBoxLayout()
        v.addLayout(h1)
        v.addLayout(h2)

        self.modelListSave = []
        self.codeSave = []
        self.serch_groupbox.setLayout(v)

    def Table1_DoubleClicked(self):
        row = []
        select_row = self.mainTable1.selectedIndexes()
        for row_value in range(len(select_row)):
            row.append(self.mainTable1.model().data(select_row[row_value]))

        if not self.codeSave:
            self.modelListSave.append(row)
            for i in range(len(self.modelListSave)):
                for j in range(self.columncount):
                    self.mainTable2_model.setItem(i, j, QStandardItem(self.modelListSave[i][j]))
            self.mainTable2.setModel(self.mainTable2_model)
            self.codeSave.append(row[0])
            spinBox = QSpinBox()
            mainTable2_ModelIndex = self.mainTable2.model().index(0, 4)
            self.mainTable2.setIndexWidget(mainTable2_ModelIndex, spinBox)

        elif row[0] in self.codeSave:
            QMessageBox.about(self, " ", "overlap.")

        else:
            self.modelListSave.append(row)
            for i in range(len(self.modelListSave)):
                for j in range(self.columncount):
                    self.mainTable2_model.setItem(i, j, QStandardItem(self.modelListSave[i][j]))
            self.mainTable2.setModel(self.mainTable2_model)
            self.codeSave.append(row[0])
            for k in range(5):
                spinBox = QSpinBox()
                mainTable2_ModelIndex = self.mainTable2.model().index(k, 4)
                self.mainTable2.setIndexWidget(mainTable2_ModelIndex, spinBox)

    def Table2_CustomContextMenu(self, position):
        menu = QMenu()
        delete = menu.addAction("delete")
        action = menu.exec_(self.mainTable2.mapToGlobal(position))
        indexRow = [index.row() for index in self.mainTable2.selectionModel().selectedRows()]
        if delete == action:
            del self.modelListSave[indexRow[0]]
            self.mainTable2.model().removeRow(indexRow[0], self.mainTable2.rootIndex())
            for i in range(len(self.modelListSave)):
                for j in range(self.columncount):
                    self.mainTable2_model.setItem(i, j, QStandardItem(self.modelListSave[i][j]))
            self.mainTable2.setModel(self.mainTable2_model)
            for k in range(5):
                spinBox = QSpinBox()
                mainTable2_ModelIndex = self.mainTable2.model().index(k, 4)
                self.mainTable2.setIndexWidget(mainTable2_ModelIndex, spinBox)

    def Layout(self):
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.SerchLineEdit)
        self.vbox.addWidget(self.select_guorpbox)
        self.vbox.addWidget(self.serch_groupbox)
        self.setLayout(self.vbox)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fream = MainWindow()
    fream.show()
    app.exec_()
    
#%% QTableView 활용(4) : QAbstractTableModel /setModel

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
        
    def data(self, index, role):
        # print(f'index type={type(index)}, role={role},\
        #       rowCount={self.rowCount(index)}, colCount={self.columnCount(index)}')
        row = index.row()
        col = index.column()
        data = self._data[row][col]
        print(f'row={row}, col={col}, data={data}')
        
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[row][col]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(400,300)
        self.table = QTableView()
        data = [[4, 9, 2],
                [1, 0, 0],
                [3, 5, 0],
                [3, 3, 2],
                [7, 8, 9]]
        self.model = TableModel(data)
        self.table.setModel(self.model)
        self.setCentralWidget(self.table)

app = QApplication(sys.argv)
window=MainWindow()
window.show()
sys.exit(app.exec())
# app.exec_()

#%% QTableView(5) : 틀 고정(Frozen Columns) /QAbstractTableModel
# https://zbaekhk.blogspot.com/2021/02/pyqt5-qtableview-frozen-columns.html
# This is FreezeTableWidget module

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
  
class FreezeTableWidget(QTableView):
    def __init__(self, parent = None, fixed_col_count = 2, *args):
        QTableView.__init__(self, parent, *args)
 
        self._fixed_col_count = fixed_col_count
        self.frozenTableView = QTableView(self)
        self.frozenTableView.verticalHeader().hide()
        self.frozenTableView.setFocusPolicy(Qt.NoFocus)
        self.frozenTableView.setStyleSheet('''border: none; background-color: #CCC''')
        self.frozenTableView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.frozenTableView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.frozenTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
 
        self.viewport().stackUnder(self.frozenTableView)
        self.setShowGrid(True)
 
        hh = self.horizontalHeader()
        hh.setDefaultAlignment(Qt.AlignCenter)
        hh.setStretchLastSection(True)
 
        self.resizeColumnsToContents()
 
        vh = self.verticalHeader()
        vh.setDefaultSectionSize(25)
        vh.setDefaultAlignment(Qt.AlignCenter)
        vh.setVisible(True)
        self.frozenTableView.verticalHeader().setDefaultSectionSize(vh.defaultSectionSize())
 
        self.frozenTableView.show()
        self.updateFrozenTableGeometry()
 
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.frozenTableView.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
 
        # connect the headers and scrollbars of both table view's together
        self.horizontalHeader().sectionResized.connect(self.updateSectionWidth)
        self.verticalHeader().sectionResized.connect(self.updateSectionHeight)
        self.frozenTableView.verticalScrollBar().valueChanged.connect(self.verticalScrollBar().setValue)
        self.verticalScrollBar().valueChanged.connect(self.frozenTableView.verticalScrollBar().setValue)
 
    @property
    def fixed_col_count(self):
        return self._fixed_col_count
 
    @fixed_col_count.setter
    def fixed_col_count(self, value):
        self._fixed_col_count = value
 
    def setModel(self, model: QAbstractTableModel):
        QTableView.setModel(self, model)
        self.frozenTableView.setModel(model)
        self.frozenTableView.verticalHeader().hide()
        self.frozenTableView.setFocusPolicy(Qt.NoFocus)
 
        # cols = model.columnCount()
        cols = model.columnCount(model.index)
        # print(model.data(model.index().row(), model.index().column()))
        for col in range(cols):
            if col not in range(self._fixed_col_count):
                self.frozenTableView.setColumnHidden(col, True)
            else:
                self.frozenTableView.setColumnWidth(col, self.columnWidth(col))
 
    def updateSectionWidth(self, logicalIndex, oldSize, newSize):
        if logicalIndex in range(self._fixed_col_count):
            self.frozenTableView.setColumnWidth(logicalIndex, newSize)
            self.updateFrozenTableGeometry()
 
    def updateSectionHeight(self, logicalIndex, oldSize, newSize):
        self.frozenTableView.setRowHeight(logicalIndex, newSize)
 
    def resizeEvent(self, event):
        QTableView.resizeEvent(self, event)
        self.updateFrozenTableGeometry()
 
    def scrollTo(self, index, hint):
        if index.column() >= self._fixed_col_count:
            QTableView.scrollTo(self, index, hint)
 
    def updateFrozenTableGeometry(self):
        frozen_width = sum([self.frozenTableView.columnWidth(col) for col in range(self._fixed_col_count)])
        if self.verticalHeader().isVisible():
            self.frozenTableView.setGeometry(self.verticalHeader().width() + self.frameWidth(),
                                             self.frameWidth(), frozen_width,
                                             self.viewport().height() + self.horizontalHeader().height())
        else:
            self.frozenTableView.setGeometry(self.frameWidth(),
                                             self.frameWidth(), frozen_width,
                                             self.viewport().height() + self.horizontalHeader().height())
 
    def moveCursor(self, cursorAction, modifiers):
        current = QTableView.moveCursor(self, cursorAction, modifiers)
        x = self.visualRect(current).topLeft().x()
        frozen_width = sum([self.frozenTableView.columnWidth(col) for col in range(self._fixed_col_count)])

        if cursorAction == self.MoveLeft:
            if current.column() >= self._fixed_col_count and x < frozen_width:
                new_value = self.horizontalScrollBar().value() + x - frozen_width
                self.horizontalScrollBar().setValue(new_value)
            elif current.column() < self._fixed_col_count:
                current = self.model().index(current.row(), current.column() + 1)
        
        elif cursorAction == self.MoveHome:
            new_value = self.horizontalScrollBar().value() + x - frozen_width
            self.horizontalScrollBar().setValue(new_value)
            current = self.model().index(current.row(), self._fixed_col_count)
 
        return current

class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
        
    def data(self, index, role):
        # print(f'index type={type(index)}, role={role},\
        #       rowCount={self.rowCount(index)}, colCount={self.columnCount(index)}')
        row = index.row()
        col = index.column()
        data = self._data[row][col]
        print(f'row={row}, col={col}, data={data}')
        
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[row][col]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])
    
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(400,300)
        data = [[4, 9, 2, 7,7,7],
                [1, 0, 0, 7,7,7],
                [3, 5, 0, 7,7,7],
                [3, 3, 2, 7,7,7],
                [7, 8, 9, 7,7,7]]
        self.table = FreezeTableWidget()
        self.model = TableModel(data)
        self.table.setModel(self.model)
        self.setCentralWidget(self.table)

app = QApplication(sys.argv)
window=MainWindow()
window.show()
sys.exit(app.exec())
# app.exec_()

#%% QTableView 활용(6) : QSqlQueryModel /QSqlDatabase /

import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtSql import QSqlQuery, QSqlDatabase, QSqlQueryModel

class RowHeightSlider(QSlider):
    def __init__(self, parent=None):
        #QSlider.__init__(self, parent)
        super(RowHeightSlider, self).__init__(parent)
        self.setOrientation(Qt.Horizontal)
        self.setMinimum(4)
        self.setMaximum(72)
        self.setSingleStep(1)
        self.setPageStep(2)
        self.setTickPosition(QSlider.TicksAbove)
        self.setTickInterval(1)

class Window(QWidget):
    def __init__(self, parent=None):
        #QWidget.__init__(self, parent)
        super(Window, self).__init__(parent)
        self.parentModel = QSqlQueryModel(self)
        self.refreshParent()
        self.parentProxyModel = QSortFilterProxyModel()
        self.parentProxyModel.setSourceModel(self.parentModel)
        self.parentView = QTableView()
        self.parentView.setModel(self.parentProxyModel)
        self.parentView.setSelectionMode(QTableView.SingleSelection)
        self.parentView.setSelectionBehavior(QTableView.SelectRows)
        self.parentView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.parentView.horizontalHeader().setStretchLastSection(True)
        self.parentView.verticalHeader().setVisible(False)
        self.parentView.setSortingEnabled(True)
        self.parentView.horizontalHeader().setSortIndicator(0, Qt.AscendingOrder)
        self.parentView.setAlternatingRowColors(True)
        self.parentView.setShowGrid(False)
        #self.parentView.verticalHeader().setDefaultSectionSize(24)
        self.parentView.setStyleSheet("QTableView::item:selected:!active { selection-background-color:#BABABA; }")
        for i, header in enumerate(self.parentHeaders):
            self.parentModel.setHeaderData(i, Qt.Horizontal, self.parentHeaders[self.parentView.horizontalHeader().visualIndex(i)])
        self.parentView.resizeColumnsToContents()

        self.childModel = QSqlQueryModel(self)
        self.refreshChild()
        self.childProxyModel = QSortFilterProxyModel()
        self.childProxyModel.setSourceModel(self.childModel)
        self.childView = QTableView()
        self.childView.setModel(self.childProxyModel)
        self.childView.setSelectionMode(QTableView.SingleSelection)
        self.childView.setSelectionBehavior(QTableView.SelectRows)
        self.childView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.childView.horizontalHeader().setStretchLastSection(True)
        self.childView.verticalHeader().setVisible(False)
        self.childView.setSortingEnabled(True)
        self.childView.horizontalHeader().setSortIndicator(0, Qt.AscendingOrder)
        self.childView.setAlternatingRowColors(True)
        self.childView.setShowGrid(False)
        #self.childView.verticalHeader().setDefaultSectionSize(24)
        self.childView.setStyleSheet("QTableView::item:selected:!active { selection-background-color:#BABABA; }")
        for i, header in enumerate(self.childHeaders):
            self.childModel.setHeaderData(i, Qt.Horizontal, self.childHeaders[self.childView.horizontalHeader().visualIndex(i)])
        self.childView.resizeColumnsToContents()

        self.parentSlider = RowHeightSlider()
        self.childSlider = RowHeightSlider()

        self.parentRowHeightLabel = QLabel('Row height: 32')
        self.childRowHeightLabel = QLabel('Row height: 32')

        parentLayout = QVBoxLayout()
        parentLayout.addWidget(self.parentSlider)
        parentLayout.addWidget(self.parentRowHeightLabel)
        parentLayout.addWidget(self.parentView)

        childLayout = QVBoxLayout()
        childLayout.addWidget(self.childSlider)
        childLayout.addWidget(self.childRowHeightLabel)
        childLayout.addWidget(self.childView)

        layout = QHBoxLayout()
        layout.addLayout(parentLayout)
        layout.addLayout(childLayout)
        self.setLayout(layout)

        self.parentView.selectionModel().currentRowChanged.connect(self.parentChanged)
        self.parentSlider.valueChanged.connect(self.changeParentRowHeight)
        self.childSlider.valueChanged.connect(self.changeChildRowHeight)

        self.parentView.setCurrentIndex(self.parentView.model().index(0, 0))
        self.parentView.setFocus()

        self.parentSlider.setValue(36)
        self.childSlider.setValue(36)

    def refreshParent(self):
        self.parentHeaders = ['Parent']
        queryString = "SELECT parent.parent_name FROM parent"
        query = QSqlQuery()
        query.exec(queryString)
        self.parentModel.setQuery(query)
        while self.parentModel.canFetchMore():
            self.parentModel.fetchMore()

    def refreshChild(self, parent_name=''):
        #parent_name='parent_name_001'
        self.childHeaders = ['Child']
        queryString = ("SELECT child.child_name FROM child WHERE child.parent_name = '{parent_name}'").format(parent_name = parent_name)
        query = QSqlQuery()
        query.exec(queryString)
        self.childModel.setQuery(query)
        while self.childModel.canFetchMore():
            self.childModel.fetchMore()

    def parentChanged(self, index):
        if index.isValid():
            index = self.parentProxyModel.mapToSource(index)
            record = self.parentModel.record(index.row())
            temp=record.value("parent_name")
            self.refreshChild(temp)
            #self.childView.scrollToBottom() # if needed

    def changeParentRowHeight(self, rowHeight):
        parentVerticalHeader = self.parentView.verticalHeader()

        # (any)one of these two rows (or both) has to be uncommented
        parentVerticalHeader.setMinimumSectionSize(rowHeight)
        #parentVerticalHeader.setMaximumSectionSize(rowHeight)

        for section in range(parentVerticalHeader.count()):
            parentVerticalHeader.resizeSection(section, rowHeight)
        self.displayParentRowHeightLabel(rowHeight)

    def changeChildRowHeight(self, rowHeight):
        childVerticalHeader = self.childView.verticalHeader()

        # (any)one of these two rows (or both) has to be uncommented
        childVerticalHeader.setMinimumSectionSize(rowHeight)
        childVerticalHeader.setMaximumSectionSize(rowHeight)

        for section in range(childVerticalHeader.count()):
            childVerticalHeader.resizeSection(section, rowHeight)
        self.displayChildRowHeightLabel(rowHeight)

    def displayParentRowHeightLabel(self, rowHeight):
        visibleRows = self.parentView.rowAt(self.parentView.height()) - self.parentView.rowAt(0)
        if self.parentView.rowAt(self.parentView.height()) == -1:
            visibleRowsString = str(self.parentView.model().rowCount()) + '+'
        else:
            visibleRowsString = str(visibleRows)
        self.parentRowHeightLabel.setText('Row height: ' + str(rowHeight) + ', Visible rows: ' + visibleRowsString)

    def displayChildRowHeightLabel(self, rowHeight):
        visibleRows = self.childView.rowAt(self.childView.height()) - self.childView.rowAt(0)
        if self.childView.rowAt(self.childView.height()) == -1:
            visibleRowsString = str(self.childView.model().rowCount()) + '+'
        else:
            visibleRowsString = str(visibleRows)
        self.childRowHeightLabel.setText('Row height: ' + str(rowHeight) + ', Visible rows: ' + visibleRowsString)

    def resizeEvent(self, event):
        # make it resize-friendly
        self.displayParentRowHeightLabel(self.parentSlider.value())
        self.displayChildRowHeightLabel(self.childSlider.value())

def createFakeData():
    parent_names = []
    #import random
    query = QSqlQuery()
    query.exec("CREATE TABLE parent(parent_name TEXT)")
    for i in range(1, 101):
        parent_num = str(i).zfill(3)
        parent_name = 'parent_name_' + parent_num
        parent_names.append((parent_name, parent_num))
        query.prepare("INSERT INTO parent (parent_name) VALUES(:parent_name)")
        query.bindValue(":parent_name", parent_name)
        query.exec_()
    query.exec("CREATE TABLE child(parent_name TEXT, child_name TEXT)")
    counter = 1
    for parent_name, parent_num in parent_names:
        for i in range(1, 11):
            child_name = 'child_name_' + parent_num + '_' + str(counter).zfill(5)
            counter += 1
            query.prepare("INSERT INTO child (parent_name, child_name) VALUES(:parent_name, :child_name)")
            query.bindValue(":parent_name", parent_name)
            query.bindValue(":child_name", child_name)
            query.exec_()

def createConnection():
    db = QSqlDatabase.addDatabase("QSQLITE")
    #db.setDatabaseName("test04.db")
    db.setDatabaseName(":memory:")
    db.open()
    createFakeData()

app = QApplication(sys.argv)
createConnection()
window = Window()
window.resize(800, 600)
window.show()
#window.showMaximized()
app.exec()

#%% QTableView 활용(7) : 테이블 출력 및 그래프 그리기 
#   QAbstractTableModel /QTableView /QVXYModelMapper /QChartView /QLineSeries

import sys
from random import randrange
from PySide6.QtCore import QAbstractTableModel, QModelIndex, QRect, Qt
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import (QApplication, QGridLayout, QHeaderView, QTableView, QWidget)
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QVXYModelMapper

# pySide6 설치 폴더 설정하기
pkgDir = 'C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python39\\Lib\\site-packages\\PySide6\\plugins'
# pkgDir = "C:\\ProgramData\\Miniconda3\\envs\\spyder-en\v\Lib\\site-packages\\PySide6\\plugins"
# pkgDir = 'C:\ProgramData\Anaconda3\Lib\site-packages\PySide6\plugins'
QApplication.setLibraryPaths([pkgDir])

class CustomTableModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.input_data = []
        self.mapping = {}
        self.column_count = 4
        self.row_count = 15

        for i in range(self.row_count):
            data_vec = [0] * self.column_count
            for k in range(len(data_vec)):
                if k % 2 == 0:
                    data_vec[k] = i * 50 + randrange(30)
                else:
                    data_vec[k] = randrange(100)
            self.input_data.append(data_vec)

    def rowCount(self, parent = QModelIndex()):
        return len(self.input_data)

    def columnCount(self, parent = QModelIndex()):
        return self.column_count

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            if section % 2 == 0:
                return "x"
            else:
                return "y"
        else:
            return str(section + 1)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self.input_data[index.row()][index.column()]
        elif role == Qt.EditRole:
            return self.input_data[index.row()][index.column()]
        elif role == Qt.BackgroundRole:
            for color, rect in self.mapping.items():
                if rect.contains(index.column(), index.row()):
                    return QColor(color)
            # cell not mapped return white color
            return QColor(Qt.white)
        return None

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            self.input_data[index.row()][index.column()] = float(value)
            self.dataChanged.emit(index, index)
            return True
        return False

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable

    def add_mapping(self, color, area):
        self.mapping[color] = area

    def clear_mapping(self):
        self.mapping = {}

class TableWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.model = CustomTableModel()

        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.AllAnimations)

        self.series = QLineSeries()
        self.series.setName("Line 1")
        self.mapper = QVXYModelMapper(self)
        self.mapper.setXColumn(0)
        self.mapper.setYColumn(1)
        self.mapper.setSeries(self.series)
        self.mapper.setModel(self.model)
        self.chart.addSeries(self.series)

        # for storing color hex from the series
        seriesColorHex = "#000000"

        # get the color of the series and use it for showing the mapped area
        self.model.add_mapping(self.series.pen().color().name(), QRect(0, 0, 2, self.model.rowCount()))

        # series 2
        self.series = QLineSeries()
        self.series.setName("Line 2")

        self.mapper = QVXYModelMapper(self)
        self.mapper.setXColumn(2)
        self.mapper.setYColumn(3)
        self.mapper.setSeries(self.series)
        self.mapper.setModel(self.model)
        self.chart.addSeries(self.series)

        # get the color of the series and use it for showing the mapped area
        self.model.add_mapping(self.series.pen().color().name(), QRect(2, 0, 2, self.model.rowCount()))

        self.chart.createDefaultAxes()
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view.setMinimumSize(640, 480)

        # create main layout
        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.table_view, 1, 0)
        self.main_layout.addWidget(self.chart_view, 1, 1)
        self.main_layout.setColumnStretch(1, 1)
        self.main_layout.setColumnStretch(0, 0)
        self.setLayout(self.main_layout)

if __name__ == "__main__":
    
    if not QApplication.instance():
        app = QApplication([])
    else:
        app = QApplication.instance()   

    w = TableWidget()
    w.show()
    sys.exit(app.exec())