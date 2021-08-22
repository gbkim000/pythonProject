import sys
from PyQt5.QtWidgets import *

print("안녕")
app = QApplication(sys.argv)
btn = QPushButton("Hello")
label = QLabel("Hello")
label.show()
btn.show()
app.exec_()

