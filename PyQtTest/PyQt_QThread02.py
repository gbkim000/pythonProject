#%% QThread 활용(1) : 
# QThread, pyqtSignal, moveToThread, deleteLater, run, quit
# https://realpython.com/python-pyqt-qthread/

import sys
from time import sleep
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget)

class Worker(QObject):
    
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def run(self):
        """Long-running task."""
        for i in range(5):
            sleep(1)
            self.progress.emit(i + 1)
        self.finished.emit()

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

        self.clicksLabel = QLabel("Counting: 0 clicks", self)
        self.clicksLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.stepLabel = QLabel("Long-Running Step: 0")
        self.stepLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        
        self.countBtn = QPushButton("Click me!", self)
        self.countBtn.clicked.connect(self.countClicks)
        
        self.longRunningBtn = QPushButton("Long-Running Task!", self)
        self.longRunningBtn.clicked.connect(self.runLongTask)

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

        self.thread = QThread()
        # thread가 메인함수(self=window) 인스턴스이므로 메인 종료시 스레드도 같이 종료(??)
        # thread를 두번 이상 생성하면 오류 발생함.(실행 중일 때는 버튼 disble 필요)
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run) # started는 thread 기본 시그널임
        # thread.started 시그널에 의해 worker.run이 실행되고, 
        # worker.finished 시그널에 의해 thread가 종료됨(quit).
        self.worker.progress.connect(self.reportProgress)        
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()
        # Final resets
        self.longRunningBtn.setEnabled(False)
        # finished 시그널을 최소 1개 이상의 슬롯과 연결해야 오류 없음.
        self.thread.finished.connect(lambda: self.longRunningBtn.setEnabled(True))
        self.thread.finished.connect(lambda: self.stepLabel.setText("Long-Running Step: 0"))
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
    
#%% QThread 활용(2) : Protecting Shared Data With QMutex(은행 출금)
# https://realpython.com/python-pyqt-qthread

import sys, time, logging, random
from time import sleep
from PyQt5.QtCore import QMutex, QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

logging.basicConfig(format = "%(message)s", level = logging.INFO)

balance = 100.00
mutex = QMutex()

class AccountManager(QObject):
    
    finished = pyqtSignal()
    updatedBalance = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.main = parent
        
    def withdraw(self, person, amount):
        logging.info("%s wants to withdraw $%.2f...", person, amount)
        global balance
        
        mutex.lock()        # 공유데이터 잠금
        if balance - amount >= 0:
            sleep(1)
            balance -= amount
            logging.info("-$%.2f accepted", amount)
        else:
            logging.info("-$%.2f rejected", amount)
        logging.info("===Balance===: $%.2f", balance)
        self.updatedBalance.emit()
        mutex.unlock()      # 공유데이터 해제
        
        if person == 'Bob':
            self.main.button.setEnabled(True)
            self.main.button.blockSignals(False)

        time.sleep(1)        
        self.finished.emit()
        
class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()
        self.threads = []
       
    def setupUi(self):
        self.setWindowTitle("Account Manager")
        self.resize(200, 150)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.button = QPushButton("Withdraw Money!")
        self.button.clicked.connect(self.startThreads)
        
        self.balanceLabel = QLabel(f"Current Balance: ${balance:,.2f}")
        layout = QVBoxLayout()
        layout.addWidget(self.balanceLabel)
        layout.addWidget(self.button)
        self.centralWidget.setLayout(layout)
        
    def createThread(self, person, amount):
        thread = QThread()
        worker = AccountManager(self)
        worker.moveToThread(thread)
        
        thread.started.connect(lambda: worker.withdraw(person, amount))
        thread.finished.connect(thread.deleteLater)
        
        worker.updatedBalance.connect(self.updateBalance)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)

        return thread

    def updateBalance(self):
        self.balanceLabel.setText(f"Current Balance: ${balance:,.2f}")

    def startThreads(self):
        self.threads.clear()
        people = {
            "Alice": random.randint(100, 10000) / 100,
            "Bob": random.randint(100, 10000) / 100,
        }
        
        self.threads = [self.createThread(person, amount) for person, amount in people.items()]
        # for person, amount in people.items():
        #     newThread = self.createThread(person, amount)
        #     self.threads.append(newThread)

        self.button.setEnabled(False)
        self.button.blockSignals(True)

        for thread in self.threads:
            thread.start()
        
app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())


# %% QThread 활용(3) : QThread, pyqtSignal, pyqtSlot

import sys
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *

class Worker(QThread):
    second_changed = pyqtSignal(str)

    def __init__(self, sec = 0, parent = None):
        super().__init__()
        self.main = parent
        self.working = True
        self.sec = sec
        # self.main.add_second_signal.connect(self.add_second)   
        # self.main(=Worker.main) --> '__main__.MyMain'을 지칭함.
        # 위 방식도 잘 작동함. custom signal from main thread to worker thread

    def __del__(self):  # 이 메서드는 garbage collection에 의해 후에 자동 실행됨.
        print(".... end thread.....")
        self.wait()

    def run(self):      # Worker(QThread)가 start()되면 자동 실행됨.
        while self.working:
            self.second_changed.emit('time (secs)：{}'.format(self.sec))
            self.sleep(1)
            self.sec += 1

    @pyqtSlot()
    def add_second(self):
        print("add_second....")
        self.sec += 100

    @pyqtSlot("PyQt_PyObject")    # @pyqtSlot(object) 도 가능..
    def recive_instance_singal(self, instance):
        print(instance.name)
        print(instance)

class MyMainGUI(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.txt1 = QTextEdit(self)
        self.btn1 = QPushButton("Start", self)
        self.btn2 = QPushButton("Stop", self)
        self.btn3 = QPushButton("add 100", self)
        self.btn4 = QPushButton("send instance", self)

        vbox = QVBoxLayout()
        vbox.addWidget(self.txt1)
        vbox.addWidget(self.btn1)
        vbox.addWidget(self.btn2)
        vbox.addWidget(self.btn3)
        vbox.addWidget(self.btn4)
        self.setLayout(vbox)
        # self.setGeometry(200, 150, 300, 400)

class Test:
    def __init__(self):
        name = ""

class MyMain(MyMainGUI):
    
    add_second_signal = pyqtSignal()
    snd_instan_signal = pyqtSignal("PyQt_PyObject")

    def __init__(self, parent = None):
        super().__init__(parent)

        # widget signal connection
        self.btn1.clicked.connect(self.time_start)
        self.btn2.clicked.connect(self.time_stop)
        self.btn3.clicked.connect(self.add_second)
        self.btn4.clicked.connect(self.send_instance)

        # worker thread signal connedtion...
        self.thread = Worker(parent = self)
        self.thread.second_changed.connect(self.time_update)    # custom signal from worker thread to main thread
        self.add_second_signal.connect(self.thread.add_second)  # custom signal from main thread to worker thread
        self.snd_instan_signal.connect(self.thread.recive_instance_singal)
        self.show()

    @pyqtSlot()
    def time_start(self):
        self.thread.start()
        self.thread.working = True

    @pyqtSlot()
    def time_stop(self):
        self.thread.working = False

    @pyqtSlot(str)
    def time_update(self, msg):
        self.txt1.append(msg)

    @pyqtSlot()
    def add_second(self):
        print("Add singal emit....")
        self.add_second_signal.emit()

    @pyqtSlot()
    def send_instance(self):
        test1 = Test()
        test1.name = "SuperPower!!!"
        self.snd_instan_signal.emit(test1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = MyMain()
    app.exec_()

#%% QThread 활용(4) : QThread, Signal, terminate, isRunning, isinstance, SIGNAL, SLOT

import sys, time
from PySide6.QtCore import QThread, SIGNAL, Signal, SLOT, Qt, QObject
from PySide6.QtWidgets import QApplication, QDialog, QPushButton, QSpinBox, QVBoxLayout

class Worker(QThread):
    
    loop = Signal(int)

    def __init__(self, x):
        QThread.__init__(self)
        self.flag = True
        self.x = x
        print(f'self.x = {self.x}')

    def run(self):
        for i in range(self.x):
            if not self.flag:
                break
            print(f'self.x = {i}')
            self.loop.emit(i)
            time.sleep(0.5)
        
    def stop(self):
        # terminate()는 위험성이 있으므로 권장하지 않음(flag 변수 활용 권장)
        # self.terminate() 
        self.flag = False

class frmMain(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.resize(200,100)
        self.btStart = QPushButton('Start')
        self.btStop = QPushButton('Stop')
        self.spiner = QSpinBox()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.btStart)
        self.layout.addWidget(self.btStop)
        self.layout.addWidget(self.spiner)
        self.setLayout(self.layout)

        self.btStart.clicked.connect(self.start_thread)
        self.btStop.clicked.connect(self.stop_thread)

    def start_thread(self):
        print('Start!')
        self.btStart.setEnabled(False)
        self.btStop.setEnabled(True)
        self.thread = Worker(20)
        self.thread.loop.connect(self.loopfunction)   
        # (방법1) self.thread.loop.connect(self.loopfunction)
        # (방법2) self.connect(self.thread, SIGNAL('loop(int)'), lambda x: self.loopfunction(x), Qt.AutoConnection)
        # (방법3) self.connect(self.thread, SIGNAL('loop(int)'), lambda x: self.spiner.setValue(x))
        # (방법4) self.connect(self.thread, SIGNAL('loop(int)'), self.spiner, SLOT('setValue(int)'))
        self.thread.flag = True
        self.thread.setTerminationEnabled(True)
        self.thread.start()

    def stop_thread(self):
        print('Stop!')
        self.btStart.setEnabled(True)
        self.btStop.setEnabled(False)
        if isinstance(self.thread, Worker):   # self.thread가 Worker의 인스턴스이면 True
            if self.thread.isRunning():
                self.thread.stop()

    def loopfunction(self, x):
        self.spiner.setValue(x)

    # ----- 창 닫기 버는 클릭 -----------------------------------------------
    def closeEvent(self, event):
        # if hasattr(self, 'thread'):         # self 클래스에 'thread' 속성이 있으면 True
        if isinstance(self.thread, Worker):   # self.thread가 Worker의 인스턴스이면 True
            if self.thread.isRunning():
                self.thread.terminate()
                print('close Window!')
        # event.ignore()  # event.accept()

if not QApplication.instance():
    app = QApplication(sys.argv)
else:
    app = QApplication.instance()

win = frmMain()
win.show()
sys.exit(app.exec())

#%% QThread 활용(5) : QThread, pyqtSlot, moveToThread

import time, sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# import worker
# 작업자 코드
import unittest
import time, random

class Worker(QObject):
    finished = pyqtSignal(int)
    intReady = pyqtSignal(int, int)

    def __init__(self, i = 0):
        '''__init__ is called while the worker is still in the Gui thread. 
        Do not put slow or CPU intensive code in the __init__ method'''
        super().__init__()
        self.idd = i

    @pyqtSlot()
    def procCounter(self): # This slot takes no params
        for j in range(1, 10):
            random_time = random.weibullvariate(1, 2)
            # time.sleep(random_time)
            time.sleep(0.3)
            self.intReady.emit(j, self.idd)
            print('Worker {0} in thread {1}'.format(self.idd, self.thread().idd))

        self.finished.emit(self.idd)

# if __name__=='__main__':
#     unittest.main()
 
class Thread(QThread):
    #make new signals to be able to return an id for the thread
    startedx = pyqtSignal(int)
    finishedx = pyqtSignal(int)

    def __init__(self, i, parent = None):
        super().__init__(parent)
        self.idd = i
        self.started.connect(self.starttt)      # started는 QThread 속성임.
        self.finished.connect(self.finisheddd)  # finished는 QThread 속성임.

    @pyqtSlot()
    def starttt(self):
        print('started signal from thread emitted')
        self.startedx.emit(self.idd) 

    @pyqtSlot()
    def finisheddd(self):
        print('finished signal from thread emitted')
        self.finishedx.emit(self.idd)

class Form(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.worker = {}
        self.threadx = {}
        self.i = 0

        #Establish the maximum number of threads the machine can optimally handle
        #Generally relates to the number of processors

        self.threadtest = QThread(self)
        self.idealthreadcount = self.threadtest.idealThreadCount()
        print("This machine can handle {} threads optimally".format(self.idealthreadcount))
        
        i = 0
        while i < self.idealthreadcount:
            self.setupThread(i)
            i += 1

        i = 0
        while i < self.idealthreadcount:
            self.startThread(i)
            i += 1

        print("Main Gui running in thread {}.".format(self.thread()))

    def setupThread(self, i):

        self.worker[i] = Worker(i)  # no parent!
        #print("Worker object runningt in thread {} prior to movetothread".format(self.worker[i].thread()) )
        self.threadx[i] = Thread(i, parent = self)  #  if parent isn't specified then need to be careful to destroy thread 
        self.threadx[i].setObjectName("python thread{}" + str(i))
        #print("Thread object runningt in thread {} prior to movetothread".format(self.threadx[i].thread()) )
        self.threadx[i].startedx.connect(self.threadStarted)
        self.threadx[i].finishedx.connect(self.threadFinished)
        
        self.threadx[i].started.connect(self.worker[i].procCounter)
        self.worker[i].intReady.connect(self.workerResultReady)        
        self.worker[i].finished.connect(self.workerFinished)
        #The next line is optional, you may want to start the threads again without having to create all the code again.
        self.worker[i].finished.connect(self.threadx[i].quit)
        self.worker[i].finished.connect(self.worker[i].deleteLater)
        # self.threadx[i].finished.connect(self.threadx[i].deleteLater)

        #This is the key code that actually get the worker code onto another processor or thread.
        self.worker[i].moveToThread(self.threadx[i])

    def startThread(self,i):
        self.threadx[i].start()

    @pyqtSlot(int)
    def threadStarted(self,i):
        print('Thread {}  started'.format(i))
        print("Thread priority is {}".format(self.threadx[i].priority()))        

    @pyqtSlot(int)
    def threadFinished(self,i):
        print('Thread {} finished'.format(i))

    @pyqtSlot(int)
    def threadTerminated(self,i):
        print("Thread {} terminated".format(i))

    @pyqtSlot(int,int)
    def workerResultReady(self,j,i):
        print('Worker {} result returned'.format(i))
        if i == 0:
            self.label1.setText("{}".format(j))
        if i == 1:
            self.label2.setText("{}".format(j))
        if i == 2:
            self.label3.setText("{}".format(j))
        if i == 3:
            self.label4.setText("{}".format(j)) 

        #print('Thread {} has started'.format(self.threadx[i].currentThreadId()))    

    @pyqtSlot(int)
    def workerFinished(self,i):
        print('Worker {} finished'.format(i))

    def initUI(self):
        self.label1 = QLabel("0")
        self.label2 = QLabel("0")
        self.label3 = QLabel("0")
        self.label4 = QLabel("0")
        grid = QGridLayout(self)
        self.setLayout(grid)
        grid.addWidget(self.label1,0,0)
        grid.addWidget(self.label2,0,1) 
        grid.addWidget(self.label3,0,2) 
        grid.addWidget(self.label4,0,3) #Layout parents the self.labels

        # self.move(300, 150)
        # self.setGeometry(0,0,300,300)
        self.resize(300,200)
        self.setWindowTitle('thread test')
        self.show()

    def closeEvent(self, event):
        print('Closing')

        #this tells the threads to stop running
        i = 0
        while i <self.idealthreadcount:
            self.threadx[i].quit()
            # self.threadx[i].terminate()
            i += 1

        #this ensures window cannot be closed until the threads have finished.
        i = 0
        while i < self.idealthreadcount:
            self.threadx[i].wait() 
            i += 1        

        event.accept()

if __name__=='__main__':
    app = QApplication(sys.argv)
    form = Form()
    sys.exit(app.exec_())


#%% QThread 활용(6) : QThread, pyqtSlot, moveToThread
# 쓰레드를 선언한 간단한 예제
#https://coding-yoon.tistory.com/46

import time, sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Thread1(QThread):
    
    def __init__(self, parent = None): #parent = MainWidget을 상속 받음.
        super().__init__(parent)
        self.flag = True
        self.main = parent
        
    def run(self):
        for i in range(10):
            print("Thread1 :",i)
            time.sleep(1)
            if not self.flag:
                break
        self.stop()
         
    def stop(self):
        self.flag = False
        self.main.startBtn.setEnabled(True)

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.startBtn = QPushButton("시 작!")
        self.startBtn.clicked.connect(self.increaseNumber)

        vbox = QVBoxLayout()
        vbox.addWidget(self.startBtn)

        self.resize(200,200)
        self.setLayout(vbox)

    def increaseNumber(self):
        self.x = Thread1(self)
        self.x.start()
        self.startBtn.setEnabled(False)

    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit the program?"
        reply = QMessageBox.question(self, 'Message', quit_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            if isinstance(self.x, Thread1):
                self.x.stop()
                print('stoped')
                if self.x.isRunning():
                    print('terminated')
                    self.x.terminate() # Thread가 여러개 일경우 나머지는 살아 있음.
            event.accept()
        else:
            event.ignore()
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MainWidget()
    widget.show()
    sys.exit(app.exec_())
    
#%% QThread 활용(7) : 경주마1, 경주마2
# 출처: https://ybworld.tistory.com/39  [투손플레이스]

import time, sys
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi, loadUiType
from PyQt5.QtCore import QThread

#경주마 1을 위한 쓰레드 클래스  
class Thread1(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.flag = True
        
    def run (self):
        self.parent.textBrowser.append("경주마1이 출발하였습니다.")
        for i in range(20):
            if not self.flag:
                return
            self.parent.textBrowser.append("경주마1이"+str(i)+"km째 달리고 있습니다.")
            time.sleep(1)
        self.parent.textBrowser.append("경주마1이 결승지에 도착하였습니다.")

    def stop(self):
        self.flag = False
        
#경주마 2를 위한 쓰레드 클래스  
class Thread2 (QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.flag = True
        
    def run (self):
        self.parent.textBrowser.append("경주마2가 출발하였습니다.")
        for i in range(20):
            if not self.flag:
                return
            self.parent.textBrowser.append("경주마2가"+str(i)+"km째 달리고 있습니다.")
            time.sleep(1)
        self.parent.textBrowser.append("경주마2가 결승지에 도착하였습니다.")

    def stop(self):
        self.flag = False

# class WindowClass(QDialog, form_class):
class WindowClass(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('pyqtThread.ui', self)
        # self.setupUi(self)        

		#각 버튼에 대한 함수 연결  
        self.runButton1.clicked.connect(self.actionFunction1)
        self.runButton2.clicked.connect(self.actionFunction2)

	#경주마1 출발 버튼을 눌렀을 때 실행 될 메서드
    def actionFunction1 (self):
        self.h1 = Thread1(self)
        self.h1.start()

	#경주마2 출발 버튼을 눌렀을 때 실행 될 메서드
    def actionFunction2 (self):
        self.h2 = Thread2(self)
        self.h2.start()

    def closeEvent(self, event):
        msg = "Are you sure you want to exit the program?"
        reply = QMessageBox.question(self, 'Message', msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            if hasattr(self, 'h1') and self.h1.isRunning():
                print('Thread1 closed')
                self.h1.stop()  # Thread1의 self.flag=false이므로 실행중인 스레드 모두 종료
            if hasattr(self, 'h2') and self.h2.isRunning():
                print('Thread2 closed')
                self.h2.stop()  # Thread2의 self.flag=false이므로 실행중인 스레드 모두 종료
            event.accept()
        else:
            event.ignore()
                
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()


#%% QThread 활용(8) : pyqtSignal, pyqtSlot, moveToThread, isRunning, terminate
# https://m.blog.naver.com/townpharm/220959370280

import sys, time
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QApplication
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot

class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.startBtn = QPushButton('Start', self)
        self.cancelBtn = QPushButton('Cancel', self)
        self.status = QLabel('status!!', self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.startBtn)
        layout.addWidget(self.cancelBtn)
        layout.addWidget(self.status)

        self.setFixedSize(400, 200)
        
    @pyqtSlot(int)
    def updateStatus(self, status):
        self.status.setText('{}'.format(status))

class Worker(QObject):
    # 시그널 객체를 하나 생성합니다.
    sig_numbers = pyqtSignal(int)

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)

    @pyqtSlot()    
    def startWork(self):
        _cnt = 0
        while _cnt < 10:
            _cnt += 1
            self.sig_numbers.emit(_cnt) # pyqtSignal 에 숫자데이터를 넣어 보낸다
            print(_cnt)                 # consol에서 어떻게 진행 되는지 보기 위해서 넣어준다
            time.sleep(0.1)

class Example(QObject):

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.gui = Window()
        self.worker = Worker()               # 백그라운드에서 돌아갈 인스턴스 소환
        self.thread = QThread()       # 따로 돌아갈 thread를 하나 생성
        self.worker.moveToThread(self.thread)# worker를 만들어둔 쓰레드에 넣어줍니다
        self.thread.start()           # 쓰레드를 실행합니다.
        self.signals()                # 시그널을 연결하기 위한 함수를 호출
        self.gui.show()
    
    # // 시그널을 연결하기 위한 func.
    def signals(self):
        self.gui.startBtn.clicked.connect(self.worker.startWork)
        self.worker.sig_numbers.connect(self.gui.updateStatus)
        self.gui.cancelBtn.clicked.connect(self.forceWorkerReset)

    # // 쓰레드의 loop를 중단하고 다시 처음으로 대기 시키는 func.
    def forceWorkerReset(self):
        if self.thread.isRunning():  #// 쓰레드가 돌아가고 있다면 
            self.thread.terminate()  #// 현재 돌아가는 thread 를 중지시킨다
            self.thread.wait()       #// 새롭게 thread를 대기한후
            self.thread.start()      #// 다시 처음부터 시작
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    example = Example(app)
    sys.exit(app.exec_())

#%% QThread 활용(9) : pyqtSignal, pyqtSlot, start, stop

import sys, time, signal, os
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QRect
from PyQt5.QtWidgets import *
# from signal import SIGKILL
    
class test_thread(QThread):
    th_val = pyqtSignal(int)

    def run(self):
        self.flag = False
        cnt = 0
        while True:
            cnt += 1
            print('test1 = {%i}' % cnt)
            self.th_val.emit(cnt)
            time.sleep(1)

            if self.flag:
                break

    def stop_test(self):
        self.flag = True

class MyWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.Button_state = True
        self.pb_start.clicked.connect(self.click1_function)

        self.test = test_thread()
        self.test.th_val.connect(self.th_val_function)
        
    def click1_function(self):
        if self.Button_state:
            # self.test = test_thread()
            # self.test.th_val.connect(self.th_val_function)
            self.Button_state = False
            self.pb_start.setText('Stop')
            self.test.start()

        elif self.Button_state == False:
            self.Button_state = True
            self.pb_start.setText('start')
            self.test.stop_test()
            
        print('Mouse Clicked')

    @pyqtSlot(int)
    def th_val_function(self, a):
        print(f'th_val = {a}')

    def setupUi(self, QMainWindow):
        self.resize(500, 500)
        self.centralwidget = QWidget(QMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pb_start = QPushButton(self.centralwidget)
        self.pb_start.setGeometry(QRect(100, 100, 100, 100))
        self.pb_start.setObjectName("pb_start")
        self.pb_start.setText("Start")
        self.setCentralWidget(self.centralwidget)

    def closeEvent(self, event):
        msg = "Are you sure you want to exit the program?"
        reply = QMessageBox.question(self, 'Message', msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            '''
            실행 중인 thread가 여러개 존재할 때 모두 삭제해야 함(??)
            '''
            self.test.stop_test()
            # threadId  = int(self.currentThreadId())
            # self.thread(threadId).terminate()
            if isinstance(self.test, MyWindow) and self.test.isRunning():
                print('Thread terminated...')
                self.test.terminate()
            event.accept()
        else:
            event.ignore()
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myApp = MyWindow()
    myApp.show()
    app_return = app.exec_()
    sys.exit(app_return)

#%% QThread 활용(10) :
# https://joyfulgenie.tistory.com/entry/QThread-분산처리-작업처리후-자동소멸 [즐거운 지니:티스토리]

import sys, time
from PyQt5.QtCore import QThread, QMutex, QRect, QObject, pyqtSignal
from PyQt5.QtWidgets import *

class Worker(QObject):
    dataLock = QMutex()
    data = 0

    finished = pyqtSignal()
    
    def __init__(self, num):
        super(Worker, self).__init__()
        self.num = num
        self.flag = True
        print(f'Woker {self.num} 생성')

    def __del__(self):
        print(f'Worker {self.num} 소멸')

    def run(self) -> None:
        if not self.flag:
            return
        Worker.dataLock.lock()
        Worker.data += 1
        time.sleep(0.2)
        Worker.dataLock.unlock()
        print(f'data = {Worker.data}')
        # self.__del__()
        self.finished.emit()
        
    def stop(self):
        self.flag = False
        
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(500, 500)
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.pb_start = QPushButton(self.centralwidget)
        self.pb_start.setGeometry(QRect(100, 100, 200, 100))
        self.pb_start.setObjectName("pb_start")
        self.pb_start.setText("Start")
        self.pb_start.clicked.connect(self.main)

    def main(self):
        self.workers = []
        self.threads = []
        
        for i in range(30):
            worker = Worker(i)
            self.workers.append(worker)
            thread = QThread()       # 따로 돌아갈 thread를 하나 생성
            self.threads.append(thread)
            # self.threads[i].setParent(app) 
            self.workers[i].moveToThread(self.threads[i])
            self.workers[i].finished.connect(self.threads[i].quit)
            self.workers[i].finished.connect(self.workers[i].deleteLater)
            self.threads[i].finished.connect(self.threads[i].deleteLater)
            self.threads[i].started.connect(self.workers[i].run)
            self.threads[i].start()

    def closeEvent(self, event):
        msg = "Are you sure you want to exit the program?"
        reply = QMessageBox.question(self, 'Message', msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            '''
            중간에 창이 닫힐 때, 이미 실행중인 스레드 모두 삭제하는 방법 미해결됨.
            # for i in range(30):
            #     # if not self.threads[i].isFinished():
            #     if isinstance(self.threads[i], QThread):
            #         if self.threads[i].isRunning():
            #             # self.threads[i].quit()
            #             self.workers[i].stop()
            #             self.threads[i].terminate()
            #             print('Thread terminated...')
            '''
            event.accept()
        else:
            event.ignore()
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myApp = MyWindow()
    myApp.show()
    sys.exit(app.exec_())

#%% QThread 활용(11) :
# https://stackoverflow.com/questions/23452218/proper-use-of-qthread-currentthreadid

from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QRect, QObject
from PyQt5.QtWidgets import *
import time, sys, threading

def logthread(caller):
    print('%-25s: %s, %s,' % (caller, QThread.currentThread(), int(QThread.currentThreadId())))
    print('%-25s: %s, %s,' % (caller, threading.current_thread().name, threading.current_thread().ident))

class Worker(QObject):
    done = pyqtSignal()

    def __init__(self, parent=None):
        logthread('worker.__init__')
        super(Worker, self).__init__(parent)

    def run(self, m=10):
        logthread('worker.run')
        for x in range(m):
            y = x + 2
            time.sleep(0.001) 
        logthread('worker.run finished')

        self.done.emit()

class MainWindow(QWidget):
    def __init__(self, parent=None):
        logthread('mainwin.__init__')
        super(MainWindow, self).__init__(parent)
        self.resize(300,100)
        self.worker = Worker()
        self.workerThread = None

        self.btn1 = QPushButton('Start worker in thread')
        self.btn2 = QPushButton('Run worker here')
        layout = QVBoxLayout(self)
        layout.addWidget(self.btn1)
        layout.addWidget(self.btn2)

        self.run()

    def run(self):
        logthread('mainwin.run')

        self.workerThread = QThread()
        self.worker.moveToThread(self.workerThread)
        self.worker.done.connect(self.workerDone)
        # self.btn1.clicked.connect(self.worker.run)
        self.btn2.clicked.connect(self.runWorkerHere)

        self.worker.done.connect(self.workerThread.quit)
        self.worker.done.connect(self.worker.deleteLater)
        self.workerThread.finished.connect(self.workerThread.deleteLater)
        self.workerThread.started.connect(self.worker.run)
        self.workerThread.start()           # 쓰레드를 실행합니다
        self.show()

    def workerDone(self):
        logthread('mainwin.workerDone')

    def runWorkerHere(self):
        logthread('mainwin.runWorkerHere')
        worker = Worker()
        worker.done.connect(self.workerDone)
        worker.run()
        # self.worker.run()

    def closeEvent(self, event):
        msg = "Are you sure you want to exit the program?"
        reply = QMessageBox.question(self, 'Message', msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            if isinstance(self.workerThread, MainWindow) and self.workerThread.isRunning():
                print('Thread terminated...')
                self.workerThread.terminate()
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication([])
    logthread('main')

    window = MainWindow()
    sys.exit(app.exec_())
    
    
    