from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QRadioButton, QWidget
from PyQt5 import QtGui
from settings import *

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
import sys, gui


# gui 첫 시작 페이지
# 버튼 클릭을 통해 난이도를 gui로 넘겨 난이도별 화면 출력

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.count = 0
        self.initialize()

    def initialize(self):
        self.setGeometry(700, 300, 500, 400)
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel("Minesweeper")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QtGui.QFont('Hack', 15))
        layout.addWidget(self.label)

        # GUI를 실행하는 버튼
        btnRun0 = QPushButton("초급", self)  # 버튼 텍스트
        btnRun0.move(BTN_X, BTN_Y)  # 버튼 위치
        btnRun0.clicked.connect(self.btnRun_clicked_0)  # 클릭 시 실행할 function

        btnRun1 = QPushButton("중급", self)  # 버튼 텍스트
        btnRun1.move(BTN_X, BTN_Y + 30)  # 버튼 위치
        btnRun1.clicked.connect(self.btnRun_clicked_1)  # 클릭 시 실행할 function

        btnRun2 = QPushButton("고급", self)  # 버튼 텍스트
        btnRun2.move(BTN_X, BTN_Y + 60)  #  버튼 위치
        btnRun2.clicked.connect(self.btnRun_clicked_2)  # 클릭 시 실행할 function

    def btnRun_clicked_0(self):  # 버튼을 눌렀을 때 gui 실행
        gui.GUI("초급")

    def btnRun_clicked_1(self):  # 버튼을 눌렀을 때 gui 실행
        gui.GUI("중급")

    def btnRun_clicked_2(self):  # 버튼을 눌렀을 때 gui 실행
        gui.GUI("고급")


app = QApplication(sys.argv)
screen = Window()
screen.show()
sys.exit(app.exec_())
