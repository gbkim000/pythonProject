# %% QRunnable 활용(1) : QThreadPool, QRunnable, globalInstance, maxThreadCount

import sys, time
from PyQt5.QtWidgets import QApplication, QPushButton, QHBoxLayout, QWidget
from PyQt5.QtCore import QThread, QThreadPool, QRunnable

class HelloWorldTask(QRunnable):
    def run(self):
        print("Hello world from thread", QThread.currentThread().objectName())
        time.sleep(5)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(200,100)
        QThreadPool.globalInstance().setMaxThreadCount(100)
        print(QThreadPool.globalInstance().maxThreadCount())

        self.btn1 = QPushButton("btn1")
        self.btn1.clicked.connect(self.btn1_clicked)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.btn1)

        self.setLayout(self.layout)
        self.show()

    def btn1_clicked(self):
        hello = HelloWorldTask()
        # QThreadPool takes ownership and deletes 'hello' automatically
        QThreadPool.globalInstance().start(hello)

        print("활성 쓰레드 개수:", QThreadPool.globalInstance().activeThreadCount())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()

#%% QRunnable 활용(2) : QRunnable and QThreadPool(Reusing Threads)

import sys, time, random, logging

from PyQt5.QtCore import QRunnable, QThreadPool, Qt
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QMessageBox
)

logging.basicConfig(format="%(message)s", level = logging.INFO)

class Worker(QRunnable):
    def __init__(self, n):
        super().__init__()
        self.flag = True
        self.n = n

    def run(self):
        for i in range(5):
            logging.info(f'Working in thread {self.n}, step {i + 1}/5')
            time.sleep(random.randint(7, 15) / 10)
            if not self.flag:
                print('stopped')
                break
        print('thread ended')

    def stop(self):
        self.flag = False

class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("QThreadPool + QRunnable")
        self.resize(250, 150)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.label = QLabel("Hello, World!")
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        countBtn = QPushButton("Click me!")
        stoppBtn = QPushButton("Stop !!")
        countBtn.clicked.connect(self.runTasks)
        stoppBtn.clicked.connect(self.stopTask)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(countBtn)
        layout.addWidget(stoppBtn)
        self.centralWidget.setLayout(layout)

    def runTasks(self):
        threadCount = QThreadPool.globalInstance().maxThreadCount()
        self.label.setText(f"Running {threadCount} Threads")

        self.pool = QThreadPool #.globalInstance()
        # for i in range(1):
        for i in range(threadCount):
            self.worker = Worker(i)
            self.pool.globalInstance().start(self.worker)

    def stopTask(self):
        self.worker.stop()

    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit the program?"
        reply = QMessageBox.question(self, 'Message', quit_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            ''' (실행중인 스레드 모두 삭제 해야함(??))
            # if isinstance(self.x, Thread1):
            #     if self.x.isRunning():
                    # self.x.terminate() # Thread가 여러개 일경우 나머지는 살아 있음.
            '''
            # print(self.pool.globalInstance().activeThreadCount())
            while self.pool.globalInstance().activeThreadCount() > 0:
                self.pool.globalInstance().waitForDone()
                self.pool.globalInstance().thread().currentThread().quit()
                # self.pool.globalInstance().thread().currentThread()
                # self.pool.globalInstance().thread().currentThread().deleteLater()
                print('check')
            event.accept()
        else:
            event.ignore()

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())

#%% QRunnable 활용(3) : QThreadPool, pyqtSignal, QTimer

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QObject, QRunnable, pyqtSlot, QThreadPool, QTimer
import traceback, sys, datetime

# this may be a long sample but you can copy and pase it for test
# the different parts of code are commented so it can be clear what it does

class WorkerSignals(QObject):
    finished = QtCore.pyqtSignal() # create a signal
    result = QtCore.pyqtSignal(object) # create a signal that gets an object as argument

class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn # Get the function passed in
        self.args = args # Get the arguments passed in
        self.kwargs = kwargs # Get the keyward arguments passed in
        self.signals = WorkerSignals() # Create a signal class
        self.flag=True

    @pyqtSlot()
    def run(self): # our thread's worker function
        result = self.fn(*self.args, **self.kwargs) # execute the passed in function with its arguments
        if self.flag:
            self.signals.result.emit(result)  # return result
            self.signals.finished.emit()  # emit when thread ended

    def stop(self):
        self.flag=False
        print('stoped')

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs): #-------------------------------------
        super(MainWindow, self).__init__(*args, **kwargs) #
        self.threadpool = QThreadPool() #
        print("Maximum Threads : %d" % self.threadpool.maxThreadCount()) #
        self.layout = QVBoxLayout() #
        self.time_label = QLabel("Start") #
        self.btn_thread = QPushButton("Using Thread") #
        self.btn_thread.pressed.connect(self.threadRunner) #
        self.btn_window = QPushButton("Without Thread") #
        self.btn_stop = QPushButton("Stop Thread")
        self.btn_stop.pressed.connect(self.stopThread) #     
        self.layout.addWidget(self.time_label) #
        self.layout.addWidget(self.btn_thread) #
        self.layout.addWidget(self.btn_window) #
        self.layout.addWidget(self.btn_stop) #
        w = QWidget() #
        w.setLayout(self.layout) #
        self.setCentralWidget(w) #
        self.show() #
        self.timer = QTimer() #
        self.timer.setInterval(10) #
        self.timer.timeout.connect(self.time) #
        self.timer.start() #-------------------------------------------------------

        # This button will run foo_window function in window ( main thread ) which will freeze our program
        self.btn_window.pressed.connect(lambda : self.foo_window(1))

        # a function that we'll use in our thread which doesn't make our program freeze
        # it will take around 5 seconds to process
    def foo_thread(self, num):
        # some long processing
        self.btn_thread.setText("Processing...")
        for i in range(50000000):
            num += 10
        return num

        # we'll use this function in window ( window = main thread )
        # it will take around 5 seconds to process
    def foo_window(self, num):
        # some long processing
        print("Window Processing...")
        for i in range(50000000):
            num += 10
        # add a label to layout
        label = QLabel("Result from Window is : "+str(num))
        self.layout.addWidget(label)
        return num

        # we'll use this function when 'finished' signal is emited
    def thread_finished(self):
        print("Finished signal emited.")
        self.btn_thread.setText("Using Thread")
        self.btn_thread.setEnabled(True)

        # we'll use this function when 'result' signal is emited
    def thread_result(self, s):
        label = QLabel("Result from Thread is : " + str(s))
        self.layout.addWidget(label) # add a new label to window with the returned result from our thread

        # in this function we create our thread and run it
    def threadRunner(self):
        self.worker = Worker(self.foo_thread, num=1) # create our thread and give it a function as argument with its args
        self.worker.signals.result.connect(self.thread_result) # connect result signal of our thread to thread_result
        self.worker.signals.finished.connect(self.thread_finished) # connect finish signal of our thread to thread_complete
        self.threadpool.start(self.worker) # start thread
        self.btn_thread.setEnabled(False)
        
    def stopThread(self):
        self.worker.stop()
        self.btn_thread.setEnabled(True)

        # this function just gets current time and displays it in Window
    def time(self):
        now = datetime.datetime.now().time() # current time
        self.time_label.setText("Current Time: "+ str(now)) # desplay current time

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    app.exec_()

#%% QRunnable 활용(4) : traceback, QThreadPool

import time, traceback
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QRunnable, QThreadPool, QTimer

__doc__ = '''PyQt5 QRunnable example
Based on https://mfitzp.io/article/multithreading-pyqt-applications-with-qthreadpool/
but rewritten by me.
'''
class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.
    Supported signals are:
    finished
        No data
    error
        `tuple` (exctype, value, traceback.format_exc() )
    result
        `object` data returned from processing, anything
    progress
        `int` indicating % progress
    Also you can use factory like this:
    def factory(QClass, cls_name, signal_type):
        return type(cls_name, (QClass,), {'signal': pyqtSignal(signal_type)})
    MySlider = factory(QSlider, 'MySlider', int)
    self.sld = MySlider(Qt.Horizontal)
    self.sld.signal.connect(self.on_signal)
    '''
    # You cannot create signals as instance variables, they must be class attributes.
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)

class Worker(QRunnable):
    '''
    Worker thread
    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.
    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''
    def __init__(self, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self._args = args
        self._kwargs = kwargs
        self.signals = WorkerSignals()
        print(self._args, self._kwargs)

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        try:
            for i in range(0, 100, 10):
                self.signals.progress.emit(i)
                time.sleep(1)
            result = 'Result from worker as str'
            self.signals.result.emit(result)  # Return the result of the processing
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            self.signals.finished.emit()

class MainWindow(QMainWindow):
    """
    You can use @pyqtSlot(int) syntax (with parameters), or you can pass this,
    but it make code more readable.
    """

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self._counter = 0
        self.init_ui()
        self._threadpool = QThreadPool()
        #self._threadpool = QtCore.QThreadPool.globalInstance()
        #self._threadpool.setMaxThreadCount(2)
        print("Multithreading with maximum {} threads" .format(self._threadpool.maxThreadCount()))

        self._timer = QTimer()
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self.recurring_timer)
        self._timer.start()

    def init_ui(self):
        layout = QVBoxLayout()

        self._label = QLabel("Start")
        b = QPushButton("Start QRunnable")
        b.pressed.connect(self.start_new_runnable)

        layout.addWidget(self._label)
        layout.addWidget(b)

        w = QWidget()
        w.setLayout(layout)

        self.setCentralWidget(w)

    @pyqtSlot(int)
    def thread_progress_fn(self, n):
        print("{}% done".format(n))

    @pyqtSlot(object)
    def thread_print_output(self, s):
        print('Result: {}'.format(s))

    @pyqtSlot()
    def thread_complete(self):
        print("QRunnable worker COMPLETE!")

    @pyqtSlot(tuple)
    def thread_error(self, err):
        QMessageBox.warning(self, "Warning!", err[1], QMessageBox.Ok)
        print('Error {}\n{}'.format(err[1], err[2]))

    @pyqtSlot()
    def start_new_runnable(self):
        # Pass the function to execute
        worker = Worker(1, debug=True) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.thread_print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.thread_progress_fn)
        worker.signals.error.connect(self.thread_error)
        worker.setAutoDelete(True)
        # Execute (tryStart() better than start() )
        if self._threadpool.tryStart(worker) is False:
            print("Can't create worker!")
            QMessageBox.warning(self, "Warning!", "Can't create worker!", QMessageBox.Ok)

    @pyqtSlot()
    def recurring_timer(self):
        self._counter += 1
        self._label.setText("Counter: {}".format(self._counter))
        print('Active thread count: {}'.format(self._threadpool.activeThreadCount()))

    def closeEvent(self, event):
        """Main window closed, override PyQt5 widget function"""
        print('Try to exit, active thread count: {}'.format(self._threadpool.activeThreadCount()))
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self._threadpool.clear()
            self._threadpool.deleteLater()

            cntActiveTh = self._threadpool.activeThreadCount()
            # for th in range(cntActiveTh):
            #     print(self._threadpool.thread())
            self._threadpool.waitForDone()
            self._timer.stop()
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

#%% QRunnable 활용(5) : traceback, QThreadPool, pyqtSignal, QTimer

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import time, traceback, sys

class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data
    error
        tuple (exctype, value, traceback.format_exc() )
    result
        object data returned from processing, anything
    progress
        int indicating % progress
    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)

class Worker(QRunnable):
    '''
    Worker thread
    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.
    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.counter = 0
        layout = QVBoxLayout()
        self.l = QLabel("Start")
        b = QPushButton("DANGER!")
        b.pressed.connect(self.oh_no)

        layout.addWidget(self.l)
        layout.addWidget(b)

        w = QWidget()
        w.setLayout(layout)

        self.setCentralWidget(w)
        self.show()
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()

    def progress_fn(self, n):
        print("%d%% done" % n)

    def execute_this_fn(self, progress_callback):
        for n in range(0, 5):
            time.sleep(1)
            progress_callback.emit(n*100/4)
        return "Done."

    def print_output(self, s):
        print(s)

    def thread_complete(self):
        print("THREAD COMPLETE!")

    def oh_no(self):
        # Pass the function to execute
        worker = Worker(self.execute_this_fn) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)
        # Execute
        self.threadpool.start(worker)

    def recurring_timer(self):
        self.counter +=1
        self.l.setText("Counter: %d" % self.counter)

app = QApplication([])
window = MainWindow()
app.exec_()

#%% QRunnable 활용(6) : traceback, QThreadPool

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui
import time, traceback, sys

uart_result = ['1','2', '3', '4', '5', '6']

#Running all these methods in parallel
@pyqtSlot()
def run1():
    print("Job 1")
    return uart_result

@pyqtSlot()
def run2():
    print("Job 2")
    return uart_result

@pyqtSlot()
def run3():
    print("Job 3")
    return uart_result

@pyqtSlot()
def run4():
    print("Job 4")
    return uart_result

class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)

class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exception()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit(exctype, value, traceback.format_exception())
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done

        '''
        <traceback.print_exc()>
        traceback.print_exc(limit=None, file=None, chain=True)
        예외 정보와 트레이스백 객체 tb의 스택 트레이스 항목을 file로 인쇄합니다
        프로그램을 종료시키지 않고, 에러에 대한 자세한 로그를 출력할 수 있습니다

        <traceback.format_exception(etype, value, tb, limit=None, chain=True)>
        스택 트레이스와 예외 정보를 포맷합니다. 
        인자는 print_exception()의 해당하는 인자와 같은 의미입니다. 
        반환 값은 각각 줄 바꿈으로 끝나고 일부는 내부 줄 바꿈을 포함하는 문자열의 리스트입니다
        
        <sys.exc_info()>
        이 함수는 현재 처리 중인 예외에 대한 정보를 제공하는 세 가지 값의 튜플을 반환합니다. 
        반환된 정보는 현재 스레드와 현재 스택 프레임에만 해당합니다. 
        현재 스택 프레임이 예외를 처리하지 않고 있으면, 호출하는 스택 프레임, 또는 그것의 호출자, 
        그리고 예외를 처리하는 스택 프레임이 발견될 때까지 거슬러 올라가서 발견된 스택 프레임에서 정보를 가져옵니다. 
        여기에서, “예외를 처리하는”은 “except 절을 실행하는”으로 정의됩니다. 
        모든 스택 프레임에서, 현재 처리 중인 예외에 대한 정보만 액세스 할 수 있습니다.
        스택의 어느 곳에서도 예외가 처리되고 있지 않으면, 세 개의 None 값을 포함하는 튜플이 반환됩니다. 
        그렇지 않으면, 반환된 값은 (type, value, traceback)입니다. 의미는 이렇습니다: 
        -type은 처리 중인 예외의 형(BaseException의 서브 클래스)을 얻습니다; 
        -value는 예외 인스턴스(예외 형의 인스턴스)를 얻습니다; 
        -traceback 은 예외가 원래 발생한 지점에서 호출 스택을 캡슐화하는 트레이스백 객체를 얻습니다.
        
        '''
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        b = QPushButton("START!")
        b.pressed.connect(self.runner)
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.addWidget(b)
        self.setCentralWidget(w)
        # worker = Worker(self.update_status)
        # QThreadPool.globalInstance().start(worker)

    # edit
    def update_status(self):
        while True:
            print('get_auto_update_data_from_server')
            time.sleep(2)

    def print_output(self, uart_list):
        print(uart_list)

    def thread_complete(self):
        print("THREAD COMPLETE!")
        thread_pool = QThreadPool.globalInstance()
        if thread_pool.activeThreadCount() == 0:
            print("finished")

    def runner(self):
        thread_pool = QThreadPool.globalInstance()
        print("Multithreading with maximum %d threads" % thread_pool.maxThreadCount())
        print("You pressed the Test button")
        for task in (run1, run2, run3, run4):
            worker = Worker(task)
            worker.signals.result.connect(self.print_output)
            worker.signals.finished.connect(self.thread_complete)
            thread_pool.start(worker)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

#%% QRunnable 활용(7): traceback, QThreadPool

import sys,os,subprocess,time,traceback
import random
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

class App(QDialog):

    def __init__(self):
        QDialog.__init__(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setGeometry(QRect(200, 200, 500, 500))
        self.threadpool = QThreadPool()

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.startbutton = QPushButton('START')
        self.startbutton.clicked.connect(self.run)
        layout.addWidget(self.startbutton)
        self.stopbutton = QPushButton('STOP')
        self.stopbutton.clicked.connect(self.stop)
        layout.addWidget(self.stopbutton)
        self.progressbar = QProgressBar(self)
        self.progressbar.setRange(0,1)
        layout.addWidget(self.progressbar)
        self.info = QTextEdit(self)
        self.info.append('Hello')
        layout.addWidget(self.info)

    def progress_fn(self, msg):

        self.info.append(str(msg))

    def run_threaded_process(self, process, on_complete):
        """Execute a function in the background with a worker"""

        worker = Worker(fn=process)
        self.threadpool.start(worker)
        worker.signals.finished.connect(on_complete)
        worker.signals.progress.connect(self.progress_fn)
        self.progressbar.setRange(0,0)

    def test(self, progress_callback):
        total = 500
        for i in range(0,total):
            time.sleep(.2)
            x = random.randint(1,1e4)
            progress_callback.emit(x)
            if self.stopped == True:
                return

    def run(self):
        self.stopped = False
        self.run_threaded_process(self.test, self.completed)

    def stop(self):
        self.stopped=True

    def completed(self):
        self.progressbar.setRange(0,1)

class Worker(QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.kwargs['progress_callback'] = self.signals.progress

    @Slot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs,)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit(exctype, value, traceback.format_exc())
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()

class WorkerSignals(QObject):

    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int)

if __name__ == '__main__':
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    aw = App()
    aw.show()
    app.exec()

#%% QRunnable 활용(8) : traceback, QThreadPool
#https://programming.vip/docs/about-qthreadpool-cleaning-in-qt.html

import sys, time, traceback
from collections import deque
from PyQt5.QtCore import QObject, QRunnable, QThreadPool
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtCore import pyqtSlot as Slot
from PyQt5.QtWidgets import *

class WorkerSignals(QObject):

    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int)

class Worker(QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super().__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @Slot()
    def run(self):

        # Retrieve args/kwargs here; and fire processing using them
        # print(self.fn, self.args, self.kwargs)
        try:
            result = self.fn(*self.args, **self.kwargs)
        except Exception:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit(exctype, value, traceback.format_exc())
        else:
            # Return the result of the processing
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()  # Done

class GenericThreadPool(QThreadPool):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._signalsQObjectQueue = deque()

    def cleanup(self, timeout=1):
        while self._signalsQObjectQueue:
            signalsQObject = self._signalsQObjectQueue.pop()
            signalsQObject.disconnect()
        self.clear()
        return self.waitForDone(timeout)

    def start(self, worker, priority=0):
        self._signalsQObjectQueue.append(worker.signals)
        super().start(worker, priority)

	# I only need to call start instead of tryStart, so I didn't try to overload tryStart

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)

        self.setWindowTitle("QThreadPool kill !!!")
        self.resize(250, 150)
        self.b = QPushButton("START!")
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.addWidget(self.b)
        w.setLayout(layout)
        self.setCentralWidget(w)
        
 		# setup main window ui and others
        self.b.clicked.connect(self.onSomeSignal)
        self.threadpool_1 = GenericThreadPool()
        self.threadpool_2 = GenericThreadPool()
        self.show()
        
    def cleanup(self):
        for threadpool in [self.threadpool_1, self.threadpool_2]:
            if not threadpool.cleanup(-1):
                time.sleep(30)

    @Slot()
    def onSomeSignal(self):
        self.threadpool_1.cleanup()
		# more cleanup and reset or initialization

        # get input
        input =[1,2,3]
        
        for data in input:
            worker = Worker(self.doit, data)
            worker.signals.result.connect(self.someResultSlot)
            worker.signals.error.connect(self.someErrorSlot)
            worker.signals.finished.connect(self.someFinishedSlot)
            worker.signals.progress.connect(self.someProgressSlot)
            self.threadpool_1.start(worker)

	# other members

    def doit(self, *args, **kwargs):
        print(args)
        for i in range(10):
            print(f'doit i = {i}')
            time.sleep(0.1)
        return 'doit'
    
    def someResultSlot(self):
        print('ResultSlot')

    def someErrorSlot(self):
        print('ErrorSlot')

    def someFinishedSlot(self):
        print('FinishedSlot')        

    def someProgressSlot(self):
        print('ProgressSlot') 
        
    def closeEvent(self, event):

    	self.cleanup()
    	event.accept()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    app.aboutToQuit.connect(mainWindow.cleanup)
    sys.exit(app.exec())
    
#%% 멀티 프로세싱 미사용
import time

start_time = time.time()

#멀티쓰레드 사용 하지 않은 경우 (20만 카운트)
def count(name):
    for i in range(1,50001):
        print(name," : ",i)

num_list = ['p1', 'p2', 'p3', 'p4']
for num in num_list:
    count(num)

print("--- %s seconds ---" % (time.time() - start_time))

#%% 멀티 프로세싱(1) : multiprocessing, close(), join()
import multiprocessing, time

start_time = time.time()

#멀티쓰레드 사용 하는 경우 (20만 카운트)
#Pool 사용해서 함수 실행을 병렬
def count(name):
    for i in range(1,50001):
        print(name," : ",i)

num_list = ['p1', 'p2', 'p3', 'p4']

if __name__ == '__main__':
    #멀티 쓰레딩 Pool 사용
    pool = multiprocessing.Pool(processes = 2) # 현재 시스템에서 사용 할 프로세스 개수
    pool.map(count, num_list)
    pool.close()
    pool.join()
    
    print("--- %s seconds ---" % (time.time() - start_time))

#%% 멀티 프로세싱(2) : multiprocessing, getpid(), join()
from multiprocessing import Process
import time, os

start_time = time.time()

#멀티쓰레드 사용 (40만 카운트 출력)
def count(cnt):
    proc = os.getpid()
    for i in range(cnt):
        print("Process Id : ", proc ," -- ",i)

if __name__ == '__main__':
    #멀티 쓰레딩 Process 사용
    num_arr = [100000, 100000, 100000, 100000]
    procs = []

    for index, number in enumerate(num_arr):
        #Process 객체 생성
        proc = Process(target = count, args = (number,))
        procs.append(proc)
        proc.start()

    #프로세스 종료 대기
    for proc in procs:
        proc.join()

    #종료시간
    print("--- %s seconds ---" % (time.time() - start_time))