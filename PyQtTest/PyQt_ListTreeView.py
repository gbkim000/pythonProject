#%% QTreeView 활용(1) : QStandardItemModel /QStandardItem /QTreeView

import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTreeView
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtCore import QVariant
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

class Model(QStandardItemModel):
    """
    사용자 데이터 모델 설정
    [{"type":str, "objects":[str, ...]}, ...]
    """
    def __init__(self, data):
        
        QStandardItemModel.__init__(self)
        self._data = data
        for j, d in enumerate(data):
            item = QStandardItem(d["type"])
            for obj in d["objects"]:
                child = QStandardItem(obj)
                child.setData(d["picture"], Qt.DecorationRole)  # Role 이름의 키 값을 가지게 될 데이터 정의
                item.appendRow(child)
            self.setItem(j, 0, item)

    def data(self, QModelIndex, role=None):
        # itemData에 인자값으로 받은 QModelIndex를 넣어주면 사전형태의 데이터 값을 돌려준다.
        data = self.itemData(QModelIndex)
        # print(data)
        if role == Qt.DisplayRole:
            ret = data[role]
        elif role in data and role == Qt.DecorationRole:
            ret = QPixmap(data[role]).scaledToHeight(25)
        else:
            ret = QVariant()
        return ret

class Form(QWidget):
    def __init__(self):
        
        QWidget.__init__(self, flags = Qt.Widget)
        self.setWindowTitle("ItemView QTreeView")
        # self.setFixedWidth(250)
        # self.setFixedHeight(180)
        self.resize(250,192)

        data = [
            {"type": "Sword", "objects": ["Long Sword", "Short Sword"], "picture": "sword.png"},
            {"type": "Shield", "objects": ["Wood Shield", "iron Shied"], "picture": "shield.png"}]
        
        # QTreeView 생성 및 설정
        view = QTreeView(self)
        view.setEditTriggers(QAbstractItemView.DoubleClicked)

        model = Model(data)
        view.setModel(model)
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())
    
#%% QTreeView 활용(2) : QStandardItemModel /setHeaderData /setData /QTreeView

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QTreeView
from PyQt5.QtGui import QStandardItemModel
from PyQt5.Qt import Qt

class MainWindow(QMainWindow):
    one, two, tree = range(3)  # treeview 의 열에 해당하는 index 번호 생성

    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 600, 300)
        self.setWindowTitle('Test Signal')
        # QTreeView 추가
        self.treeView = QTreeView()
        self.model = self.create_model()
        self.treeView.setModel(self.model)
        self.add_file(0, 'File1', '350', 'File Folder')
        self.add_file(1, 'File2', '480', 'File Folder')
        self.add_file(2, 'File3', '1000', 'File Folder')
        self.setCentralWidget(self.treeView)

    def create_model(self):
        model = QStandardItemModel(0, 3) # (rows, columns)
        model.setHeaderData(self.one, Qt.Horizontal, "Name")
        model.setHeaderData(self.two, Qt.Horizontal, "Size")
        model.setHeaderData(self.tree, Qt.Horizontal, "Type")
        return model

    def add_file(self, row, file_name, file_size, file_type):
        model = self.model
        model.insertRow(row)
        model.setData(model.index(row, self.one), file_name)
        model.setData(model.index(row, self.two), file_size)
        model.setData(model.index(row, self.tree), file_type)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

#%% QTreeView 활용(3) : QFileSystemModel /setRootPath /rootPath /QTreeView /setModel

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QTreeView
from PyQt5.Qt import QFileSystemModel
from PyQt5.QtCore import QModelIndex, QDir, pyqtSlot

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 600, 300)
        self.setWindowTitle('Test Signal')

        # 전체 파일 경로를 가져온다.
        self.path_root = QDir.rootPath()
        self.model = QFileSystemModel()
        self.model.setRootPath(self.path_root)

        self.index_root = self.model.index(self.model.rootPath())

        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.index_root)
        self.tree_view.clicked.connect(self.on_treeView_clicked)

        self.setCentralWidget(self.tree_view)

    @pyqtSlot(QModelIndex)
    def on_treeView_clicked(self, index):
        indexItem = self.model.index(index.row(), 0, index.parent())

        fileName = self.model.fileName(indexItem)
        filePath = self.model.filePath(indexItem)

        print(fileName)
        print(filePath)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
    
#%% QListView 활용(1) : QAbstractListModel /QListView
# 수정이 가능한 모델

import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QListView
from PyQt5.QtCore import QAbstractListModel
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

class UserModel(QAbstractListModel):
    """
    ListModel은 두 가지의 필수 메소드를 작성해야 한다.
    int rowCount(self, parent=None, *args, **kwargs)
    QVariant data(self, QModelIndex, role=None)
    """
    def __init__(self, data=None, parent=None):
        QAbstractListModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None, *args, **kwargs):
        """
        데이터의 개 수를 반환
        """
        return len(self._data)

    def data(self, QModelIndex, role=None):
        """
        어떠한 이벤트가 일어났을 때 View가 Model.data를 호출
        View의 요구를 role을 참고하여 해당하는 값을 반환
        해당하는 role에 대한 대응이 없을 경우 QVariant를 반환
        """
        item = self._data[QModelIndex.row()]

        if role == Qt.DisplayRole:  # 값 출력시
            return "%s, %s, %s" % (item['name'], item['color'], item['bg_color'])
        elif role == Qt.EditRole:  # 값 수정시
            return "%s" % item['name']
        return QVariant()

    def flags(self, QModelIndex):
        """
        모델 아이템별에 대한 정책
        """
        return Qt.ItemIsEditable | Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsTristate

    def setData(self, QModelIndex, value, role=None):
        """
        값 수정시 호출
        """
        self._data[QModelIndex.row()]['name'] = value
        return True

class Form(QWidget):
    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)
        self.setWindowTitle("ItemView QListView")
        self.setFixedWidth(250)
        self.setFixedHeight(100)

        fruits = [
            {"name": "banana", "color": "yellow", "bg_color": "yellow"},
            {"name": "apple", "color": "red", "bg_color": "red"},
            {"name": "pear", "color": "green", "bg_color": "gray"} ]

        view = QListView(self)
        view.setEditTriggers(QAbstractItemView.DoubleClicked)

        model = UserModel(fruits)
        view.setModel(model)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())

# %% QListView, QStandardItemModel

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QStandardItemModel, QStandardItem

app = QApplication(sys.argv)

# Our main window will be a QListView
list = QListView()
list.setWindowTitle('Example List')
list.setMinimumSize(600, 400)

# Create an empty model for the list's data
model = QStandardItemModel(list)

# Add some textual items
foods = [
    'Cookie dough', # Must be store-bought
    'Hummus',       # Must be homemade
    'Spaghetti',    # Must be saucy
    'Dal makhani',  # Must be spicy
    'Chocolate whipped cream'] # Must be plentiful

for food in foods:
    # create an item with a caption
    item = QStandardItem(food)

    # add a checkbox to it
    item.setCheckable(True)

    # Add the item to the model
    model.appendRow(item)

# Apply the model to the list view
list.setModel(model)

# Show the window and run the app
list.show()
app.exec_()

#%% QListView /QStandardItemModel /QStandardItem

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt

class MyApp(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.resize(300,200)

        btn1 = QPushButton('Selected List', self)
        btn1.clicked.connect(self.printList)
        btn2 = QPushButton('Checked List', self)
        btn2.clicked.connect(self.print_checked_items)
        
        btnLayout = QHBoxLayout()
        btnLayout.addWidget(btn1)
        btnLayout.addWidget(btn2)

        # self.listView = QListView(self)
        self.listView = QListView(
            editTriggers = QAbstractItemView.NoEditTriggers,
            selectionMode = QAbstractItemView.MultiSelection, #SingleSelection,
            selectionBehavior = QAbstractItemView.SelectRows)   
        
        layout = QVBoxLayout()
        layout.addLayout(btnLayout)
        layout.addWidget(self.listView)
        self.setLayout(layout)
        self.showList()
        self.show()
        
    def showList(self):

        # [방법 1] - QStringListModel
        # self.model = QStringListModel()
        # list = [] #QStringList()
        # list.append("a")
        # list.append("b")
        # list.append("c")
        # self.model.setStringList(list);
        # self.textList.setModel(self.model)
        
        # [방법 2] - QStandardItemModel
        numbers = ["One", "Two", "Three", "Four", "Five"]
        self.model = QStandardItemModel()
        for x in numbers:
            item = QStandardItem(x)
            item.setCheckable(True)
            item.setCheckState(Qt.Unchecked)
            self.model.appendRow(item)
            self.listView.setModel(self.model)

    def printList(self):
        print('Selected List')
        for index in self.listView.selectedIndexes():
            item = self.listView.model().itemFromIndex(index)
            print(item.text())

    def print_checked_items(self):
        print('Checked List')
        for index in range(self.model.rowCount()):
            item = self.model.item(index)
            if item.checkState() == Qt.Checked:
                print ('%s' % item.text())
                
app = QApplication(sys.argv)
me = MyApp()
sys.exit(app.exec())

#%% QListView /QStandardItemModel /QStandardItem 

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QItemSelectionModel

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.listView = QListView(
            editTriggers = QAbstractItemView.NoEditTriggers,
            selectionMode = QAbstractItemView.MultiSelection, #SingleSelection,
            selectionBehavior = QAbstractItemView.SelectRows)
        
        self.entry = QStandardItemModel()
        self.listView.setModel(self.entry)

        for letter in list("abcdefghijklmnopqrstuvwxyz"):
            it = QStandardItem(letter)
            self.entry.appendRow(it)

        ix = self.entry.index(0, 0)
        sm = self.listView.selectionModel()
        sm.select(ix, QItemSelectionModel.Select)

        self.setCentralWidget(self.listView)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())