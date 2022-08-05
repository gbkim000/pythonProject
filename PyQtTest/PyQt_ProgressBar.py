# %% progressBar 활용(1) : QProgressBar, setValue, timer

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QProgressBar
from PyQt5.QtCore import QBasicTimer

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)

        self.btn = QPushButton('Start', self)
        self.btn.move(40, 80)
        self.btn.clicked.connect(self.doAction)

        self.timer = QBasicTimer()
        self.step = 0

        self.setWindowTitle('QProgressBar')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()
            self.btn.setText('Finished')
            return

        self.step = self.step + 1
        self.pbar.setValue(self.step)

    def doAction(self):
        if self.timer.isActive():
            self.timer.stop()
            self.btn.setText('Start')
        else:
            self.timer.start(100, self)
            self.btn.setText('Stop')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
    
# %% progressBar 활용(2) : QThread, QProgressBar, QWaitCondition, pyqtSignal, QMutex
# 예제로 배우는 PyQt (https://opentutorials.org/module/544/18723)

import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread
from PyQt5.QtCore import QWaitCondition
from PyQt5.QtCore import QMutex
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot

class Thread(QThread):
    """
    단순히 0부터 100까지 카운트만 하는 쓰레드
    값이 변경되면 그 값을 change_value 시그널에 값을 emit 한다.
    """
    # 사용자 정의 시그널 선언
    change_value = pyqtSignal(int)

    def __init__(self):
        QThread.__init__(self)
        self.cond = QWaitCondition()
        self.mutex = QMutex()
        self.cnt = 0
        self._status = True

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            self.mutex.lock()

            if not self._status:
                self.cond.wait(self.mutex)

            if 100 == self.cnt:
                self.cnt = 0
            self.cnt += 1
            self.change_value.emit(self.cnt)
            self.msleep(100)  # ※주의 QThread에서 제공하는 sleep을 사용

            self.mutex.unlock()

    def toggle_status(self):
        self._status = not self._status
        if self._status:
            self.cond.wakeAll()

    @property
    def status(self):
        return self._status

class Form(QWidget):
    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)
        self.pgsb = QProgressBar()
        self.pb = QPushButton("Pause")
        self.th = Thread()
        self.init_widget()
        self.th.start()

    def init_widget(self):
        self.setWindowTitle("QProgressBar with QThread")
        form_lbx = QBoxLayout(QBoxLayout.TopToBottom, parent=self)
        self.setLayout(form_lbx)

        # 시그널 슬롯 연결
        self.pb.clicked.connect(self.slot_clicked_button)
        self.th.change_value.connect(self.pgsb.setValue)

        form_lbx.addWidget(self.pgsb)
        form_lbx.addWidget(self.pb)

    @pyqtSlot()
    def slot_clicked_button(self):
        """
        쓰레드의 status 상태 변경
        쓰레드 재시작
        """
        self.th.toggle_status()
        self.pb.setText({True: "Pause", False: "Resume"}[self.th.status])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    exit(app.exec_())
    
# %% progressBar 활용(3) : QThread, pyqtSignal, threading, QProgressBar

import sys, time, threading
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QDialog, QProgressBar, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class MyThread(QThread):
    # Create a counter thread
    change_value = pyqtSignal(int)
    def run(self):
        cnt = 0
        while cnt < 100:
            cnt += 1
            time.sleep(0.01)
            self.change_value.emit(cnt)
            
class Window(QDialog):
    def __init__(self):
        super().__init__()
        self.title = "PyQt5 ProgressBar"
        self.top = 200
        self.left = 500
        self.width = 300
        self.height = 100
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        vbox = QVBoxLayout()
        self.progressbar = QProgressBar()
        self.progressbar.setMaximum(100)
        self.progressbar.setTextVisible(False) 
        self.progressbar.setStyleSheet("QProgressBar {border: 2px solid gray; border-radius:2px; padding:1px;}"
                                       "QProgressBar::chunk {background:blue}")
        vbox.addWidget(self.progressbar)
        
        self.button = QPushButton("Start Progressbar")
        self.button.clicked.connect(self.startProgressBar)
        self.button.setStyleSheet('background-color:yellow')
        vbox.addWidget(self.button)
        self.setLayout(vbox)
        self.show()

    def startProgressBar(self):
        self.thread = MyThread()
        self.thread.change_value.connect(self.setProgressVal)
        self.thread.start()

    def setProgressVal(self, val):
        self.progressbar.setValue(val)

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())

# %% progressBar 활용(4) : QProgressBar, statusBar, setRange, setFormat,
#                          setSizeGripEnabled, addPermanentWidget

import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import*

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.resize(300,200)
        self.pb = QProgressBar()
        # self.pb.setTextVisible(False) 
        self.pb.setRange(0, 9)
        self.pb.setValue(5)
        self.pb.setFormat('finding resource...')

        self.statusBar().setSizeGripEnabled(False)
        self.statusBar().addPermanentWidget(self.pb, 1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())

# %% progressBar 활용(5) :QProgressBar, QThread, pyqtSignal, moveToThread, isRunning

import sys
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication, QPushButton, QProgressBar, QWidget, QVBoxLayout

class Worker(QObject):
    progressChanged = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._stopped = True

    def run(self):
        count = 0
        self._stopped = False
        while count < 100 and not self._stopped:
            count += 5
            QThread.msleep(250)
            self.progressChanged.emit(count)
        self._stopped = True
        self.finished.emit()

    def stop(self):
        self._stopped = True

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.button = QPushButton('Start')
        self.button.clicked.connect(self.handleButton)
        self.progress = QProgressBar()
        self.progress.setTextVisible(False) 
        layout = QVBoxLayout(self)
        layout.addWidget(self.progress)
        layout.addWidget(self.button)
        
        self.thread = QThread(self)
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.worker.finished.connect(self.handleFinished)
        self.worker.progressChanged.connect(self.progress.setValue)
        self.thread.started.connect(self.worker.run)

    def handleButton(self):
        if self.thread.isRunning():
            self.worker.stop()
        else:
            self.button.setText('Stop')
            self.thread.start()

    def handleFinished(self):
        self.button.setText('Start')
        self.thread.quit()

    def closeEvent(self, event):
        self.worker.stop()
        self.thread.quit()
        self.thread.wait()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.setWindowTitle('Threaded Progress')
    window.setGeometry(600, 100, 250, 50)
    window.show()
    sys.exit(app.exec_())
    
