# %% Use PyQt's QThread to Prevent Freezing GUIs
# https://realpython.com/python-pyqt-qthread/
# 스레드 사용하지 않음(runLongTask 실행시 Freezing.)

import sys 
from time import sleep

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clicksCount = 0
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Freezing GUI")
        self.resize(300, 150)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        
        # Create and connect widgets
        self.clicksLabel = QLabel("Counting: 0 clicks", self)
        self.clicksLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.stepLabel = QLabel("Long-Running Step: 0")
        self.stepLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        
        self.countBtn = QPushButton("Click me!", self)
        self.countBtn.clicked.connect(self.countClicks)
        
        self.longRunningBtn = QPushButton("Long-Running Task!", self)
        self.longRunningBtn.clicked.connect(self.runLongTask)
        
        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.clicksLabel)
        layout.addWidget(self.countBtn)
        layout.addStretch()
        layout.addWidget(self.stepLabel)
        layout.addWidget(self.longRunningBtn)
        self.centralWidget.setLayout(layout)

    def countClicks(self):
        self.clicksCount += 1
        self.clicksLabel.setText(f"Counting: {self.clicksCount} clicks")

    def reportProgress(self, n):
        self.stepLabel.setText(f"Long-Running Step: {n}")

    def runLongTask(self):
        """Long-running task in 5 steps."""
        for i in range(5):
            sleep(1)
            self.reportProgress(i + 1)

app = QApplication(sys.argv)
win = Window()
win.show()
sys.exit(app.exec())

#%% 스레드를 처리하는 3가지 방법
# https://www.wake-up-neo.com/ko/python/pyqt에서-qthread가있는-백그라운드-스레드/940504146/

import sys, time
from PyQt5.QtCore import (QCoreApplication, QObject, QRunnable, QThread, QThreadPool, pyqtSignal)

# Subclassing QThread
class AThread(QThread):
    def run(self):
        count = 0
        while count < 5:
            time.sleep(1)
            print("A Increasing")
            count += 1

# Subclassing QObject and using moveToThread
class SomeObject(QObject):
    finished = pyqtSignal()
    def long_running(self):
        count = 0
        while count < 5:
            time.sleep(1)
            print("B Increasing")
            count += 1
        self.finished.emit()

# Using a QRunnable
# Note that a QRunnable isn't a subclass of QObject and therefore does
# not provide signals and slots.
class Runnable(QRunnable):
    def run(self):
        count = 0
        app = QCoreApplication.instance()
        while count < 5:
            print("C Increasing")
            time.sleep(1)
            count += 1
        app.quit()

# ------------------------------------------------------------------------

def using_q_thread():
    app = QCoreApplication([])
    thread = AThread()
    thread.finished.connect(app.exit)
    thread.start()
    sys.exit(app.exec_())

def using_move_to_thread():
    app = QCoreApplication([])
    objThread = QThread()
    obj = SomeObject()
    obj.moveToThread(objThread)
    obj.finished.connect(objThread.quit)
    objThread.started.connect(obj.long_running)
    objThread.finished.connect(app.exit)
    objThread.start()
    sys.exit(app.exec_())

def using_q_runnable():
    app = QCoreApplication([])
    runnable = Runnable()
    QThreadPool.globalInstance().start(runnable)
    sys.exit(app.exec_())

if __name__ == "__main__":
    using_q_thread()
    # using_move_to_thread()
    # using_q_runnable()

# %% multiprocessing
# Python program killing a thread using multiprocessing module
 
import time, multiprocessing
 
start_time = time.time()

def func(number):
    for i in range(1, 10):
        time.sleep(0.01)
        print('Processing ' + str(number) + ': prints ' + str(number*i))

if __name__ == '__main__':
    # list of all processes, so that they can be killed afterwards
    all_processes = []
     
    for i in range(0, 10):
        process = multiprocessing.Process(target = func, args = (i,))
        all_processes.append(process)
        process.start()

    for no, process in enumerate(all_processes):
        if no %2 ==0:
            all_processes.pop(no)
            continue
        process.join()
            
    # kill all processes after 0.5s
    time.sleep(0.5)
    for process in all_processes:
        print(process)
        process.terminate()
    
    print("--- %s seconds ---" % (time.time() - start_time))
