#%% QTableWidget 활용(1) : setRangeSelected /QSpinBox
    
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import random

class Widget(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        hlayout = QHBoxLayout()
        self.rbox = QSpinBox(self)
        self.cbox = QSpinBox(self)
        hlayout.addWidget(self.rbox)
        hlayout.addWidget(self.cbox)
        vlayout = QVBoxLayout(self)
        vlayout.addLayout(hlayout)

        nrows = 5
        ncols = 5
        self.rbox.setMaximum(nrows-1)
        self.cbox.setMaximum(ncols-1)

        self.table = QTableWidget(nrows, ncols, self)
        vlayout.addWidget(self.table)
        for r in range(nrows):
            for c in range(nrows):
                it = QTableWidgetItem("{}-{}".format(r, c))
                self.table.setItem(r, c, it)

        self.rbox.valueChanged.connect(self.selectItem)
        self.cbox.valueChanged.connect(self.selectItem)
        self.selectItem()

    def selectItem(self):
        self.table.clearSelection()
        x = self.rbox.value()
        y = self.cbox.value()
        self.table.setRangeSelected(QTableWidgetSelectionRange(x, y, x, y), True)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())

#%% QTableWidget 활용(2) : QTableWidget에서 셀 패딩 제거
# QStyledItemDelegate / QStyle /QPixmap / IconDelegate

import random
from PyQt5.QtCore import *
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import *

class IconDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        icon = index.data(Qt.DecorationRole)
        mode = QIcon.Normal
        if not (option.state & QStyle.State_Enabled):
            mode = QIcon.Disabled
        elif option.state & QStyle.State_Selected:
            mode = QIcon.Selected
        state = (QIcon.On
            if option.state & QStyle.State_Open
            else QIcon.Off
        )
        pixmap = icon.pixmap(option.rect.size(), mode, state)
        painter.drawPixmap(option.rect, pixmap)

    def sizeHint(self, option, index):
        return QSize(60, 60)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        table = QTableWidget(5, 5)
        delegate = IconDelegate(table)
        table.setItemDelegate(delegate)

        self.setCentralWidget(table)

        for i in range(table.rowCount()):
            for j in range(table.columnCount()):

                # create icon
                pixmap = QPixmap(100, 100)
                color = QColor(*random.sample(range(255), 3))
                pixmap.fill(color)
                icon = QIcon(pixmap)

                it = QTableWidgetItem()
                it.setIcon(icon)
                table.setItem(i, j, it)

        table.resizeRowsToContents()
        table.resizeColumnsToContents()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

#%% QTableWidget 활용(3) : QTableWidget의 단어를 강조 표시하는 방법

from PyQt5.QtCore import *
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import *
import random

words = ["Hello dseerfd", "world sdfsdf sdfgsdf sdfsdf", "Stack dasdf", "Overflow",
         "Hello world", """<font color="red">Hello world</font>"""]

class HighlightDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(HighlightDelegate, self).__init__(parent)
        self.doc = QTextDocument(self)
        self._filters = []

    def paint(self, painter, option, index):
        painter.save()
        options = QStyleOptionViewItem(option)
        self.initStyleOption(options, index)
        self.doc.setPlainText(options.text)
        self.apply_highlight()
        options.text = ""
        style = QApplication.style() if options.widget is None \
            else options.widget.style()
        style.drawControl(QStyle.CE_ItemViewItem, options, painter)

        ctx = QAbstractTextDocumentLayout.PaintContext()
        if option.state & QStyle.State_Selected:
            ctx.palette.setColor(QPalette.Text, option.palette.color(
                QPalette.Active, QPalette.HighlightedText))
        else:
            ctx.palette.setColor(QPalette.Text, option.palette.color(
                QPalette.Active, QPalette.Text))

        textRect = style.subElementRect(
            QStyle.SE_ItemViewItemText, options)

        if index.column() != 0:
            textRect.adjust(5, 0, 0, 0)

        the_constant = 4
        margin = (option.rect.height() - options.fontMetrics.height()) // 2
        margin = margin - the_constant
        textRect.setTop(textRect.top() + margin)

        painter.translate(textRect.topLeft())
        painter.setClipRect(textRect.translated(-textRect.topLeft()))
        self.doc.documentLayout().draw(painter, ctx)

        painter.restore()

    def apply_highlight(self):
        cursor = QTextCursor(self.doc)
        cursor.beginEditBlock()
        fmt = QTextCharFormat()
        fmt.setForeground(Qt.red)
        for f in self.filters():
            highlightCursor = QTextCursor(self.doc)
            while not highlightCursor.isNull() and not highlightCursor.atEnd():
                highlightCursor = self.doc.find(f, highlightCursor)
                if not highlightCursor.isNull():
                    highlightCursor.mergeCharFormat(fmt)
        cursor.endEditBlock()

    @QtCore.pyqtSlot(list)
    def setFilters(self, filters):
        if self._filters == filters: return
        self._filters = filters

    def filters(self):
        return self._filters

class Widget(QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)

        self.table = QTableWidget(30, 6)
        self._delegate = HighlightDelegate(self.table)
        self.table.setItemDelegate(self._delegate)
        for i in range(self.table.rowCount()):
            for j in range(self.table.columnCount()):
                it = QTableWidgetItem(random.choice(words))
                self.table.setItem(i, j, it)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        le = QLineEdit()
        le.textChanged.connect(self.on_textChanged)
        lay = QVBoxLayout(self)
        lay.addWidget(le)
        lay.addWidget(self.table)

        le.setText("ello ack")

    @QtCore.pyqtSlot(str)
    def on_textChanged(self, text):
        self._delegate.setFilters(list(set(text.split())))
        self.table.viewport().update()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = Widget()
    w.showMaximized()
    sys.exit(app.exec_())

#%% QTableWidget 활용(4) : 이벤트 - cellChanged /currentCellChanged /cellClicked

import sys
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, \
    QTableWidgetItem, QAbstractItemView, QTextEdit, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 윈도우 설정
        self.setGeometry(200, 100, 400, 400)  # x, y, w, h
        self.setWindowTitle('QTableWidget Sample Window')

        # QTableWidget
        self.tablewidget = QTableWidget(self)
        self.tablewidget.resize(400, 200)
        self.tablewidget.setRowCount(3) # 행 개수
        self.tablewidget.setColumnCount(3) # 열 개수
        self.tablewidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.edit = QTextEdit(self)
        self.edit.move(10, 210)
        self.btn = QPushButton(self)
        self.btn.setText('0, 0 셀 입력')
        self.btn.move(120, 210)

        # QTableWidget 에 데이터 추가하기
        self.insert_data()

        # 수정 가능한 필드
        # self.tablewidget.setEditTriggers(QAbstractItemView.AllEditTriggers)

        # 데이터 조회
        rowcount = self.tablewidget.rowCount()
        colcount = self.tablewidget.columnCount()

        for i in range(0, rowcount):
            for j in range(0, colcount):
                data = self.tablewidget.item(i, j)
                if data is not None:
                    print(data.text())
                else:
                    print('blank')

        # self.tablewidget.item(0, 0).setText('1111')

        # 테이블 이벤트 지정
        self.tablewidget.cellChanged.connect(self.cellchanged_event)
        self.tablewidget.currentCellChanged.connect(self.currentcellchanged_event)
        self.tablewidget.cellClicked.connect(self.cellclicked_event)
        self.tablewidget.cellDoubleClicked.connect(self.celldoubleclicked_event)

    # 셀 더블클릭 때 발생하는 이벤트
    def celldoubleclicked_event(self, row, col):
        data = self.tablewidget.item(row, col)
        print("셀 더블클릭 셀 값 : ", data.text())

    # 셀 선택할 때 발생하는 이벤트
    def cellclicked_event(self, row, col, pre_row, pre_col):
        data = self.tablewidget.item(row, col)
        print("셀 클릭 셀 값 : ", data.text())

    # 선택한 셀이 바뀌면 발생하는 이벤트
    def currentcellchanged_event(self, row, col, pre_row, pre_col):
        current_data = self.tablewidget.item(row, col) # 현재 선택 셀 값
        pre_data = self.tablewidget.item(pre_row, pre_col) # 이전 선택 셀 값
        if pre_data is not None:
            print("이전 선택 셀 값 : ", pre_data.text())
        else:
            print("이전 선택 셀 값 : 없음")

        print("현재 선택 셀 값 : ", current_data.text())

    # 셀의 내용이 바뀌었을 때 이벤트
    def cellchanged_event(self, row, col):
        data = self.tablewidget.item(row, col)
        print("cellchanged_event 발생 : ", data.text())

    def insert_data(self):
        self.tablewidget.setItem(0, 0, QTableWidgetItem("1행 1열"))
        self.tablewidget.setItem(0, 1, QTableWidgetItem("1행 2열"))
        self.tablewidget.setItem(1, 0, QTableWidgetItem("2행 1열"))
        self.tablewidget.setItem(1, 1, QTableWidgetItem("2행 2열"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
    
# 참고 사이트 : https://wikidocs.net/36797 (공학자를 위한 PySide2)

