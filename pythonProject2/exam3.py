import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

app = QApplication(sys.argv)


def btn1_clicked():
    print("버튼 클릭")


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 200, 300, 400)
        self.setWindowTitle("PyQt")
        self.setWindowIcon(QIcon("icon_24.png"))

        btn1 = QPushButton("버튼1", self)
        btn1.move(100, 10)
        btn1.clicked.connect(btn1_clicked)


window = MyWindow()
window.show()
app.exec_()
