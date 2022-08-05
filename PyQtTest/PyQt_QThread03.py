#%% threading 활용(1) : Thread, join

import threading, time

def do_work(id, stop):
    print("I am thread", id)
    while True:
        print("I am thread {} doing something".format(id))
        if stop():
            print("Exiting loop.")
            break
        # time.sleep(0.2)
    print("Thread {}, signing off".format(id))

def main():
    stop_threads = False
    workers = []
    for id in range(0,5):
        thread = threading.Thread(target = do_work, args = (id, lambda: stop_threads))
        workers.append(thread)
        thread.start()
    time.sleep(1)
    print('\nmain: done sleeping; time to stop the threads.')
    stop_threads = True
    for worker in workers:
        worker.join()
    print('Finis.')

if __name__ == '__main__':
    main()

#%% threading 활용(2) : join() 메서드.
# https://velog.io/@soojung61/Python-Thread

import random
def worker(*args, **kwargs):
    print("child thread start: ")
    print(f"args = {args} kwargs = {kwargs}")
    sleep_time = random.randint(1, 3)
    time.sleep(sleep_time)
    print(f"child thread finished")

if __name__ == '__main__':
    thread = threading.Thread(target = worker, args=(1,3), kwargs={"name": "kim", "age": 10})
    thread.start()
    thread.join()
    print("parents thread finished")

#%% threading 활용(3) : join() 메서드.
    
import threading, time

class sample(threading.Thread):
    def __init__(self, time):
        super(sample, self).__init__()
        # super().__init__()
        self.time = time
        self.start()

    def run(self):
        print(self.time, " starts")
        for i in range(0,self.time):
            time.sleep(1)
        print(self.time, "has finished")

t3 = sample(3)
t2 = sample(2)
t1 = sample(1)

t3.join()
print("t3.join() has finished")
t2.join()
print ("t2.join() has finished")
t1.join()
print ("t1.join() has finished")

#%% threading 활용(4) : 데몬 스레드
# (https://ddangjiwon.tistory.com/144)
# 데몬(daemon) 스레드는 메인 스레드가 종료될 때 자신의 실행 상태와 상관없이 종료되는 서브 스레드

import threading, time

class Worker(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name            # thread 이름 지정

    def run(self):
        print("sub thread start ", threading.currentThread().getName())
        time.sleep(3)
        print("sub thread end !!", threading.currentThread().getName())

print("main thread start")

for i in range(5):
    name = "thread {}".format(i)
    t = Worker(name)                # sub thread 생성
    t.daemon = True
    t.start()                       # sub thread의 run 메서드를 호출
    # t.join()

# for i in range(5):
#     t.join()  
    
print("main thread end")


#%% threading 활용(5) : 전역변수 사용시 문제 발생
# https://coding-groot.tistory.com/103 

import threading
 
class CounterThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, name = 'Timer Thread')
 
    # CounterThread가 실행하는 함수
    def run(self):
        global totalCount
 
        for _ in range(2500000):
            totalCount += 1
        print('2,500,000번 카운팅 끝!')
 
if __name__ == '__main__':
    # 전역 변수로 totalCount를 선언
    global totalCount
    totalCount = 0
 
    # Counter Thread를 4개 만들어서 동작시킨다.
    for _ in range(4):
        timerThread = CounterThread()
        timerThread.start()

        # (방법1) # start()와 동시에 join()을 실행하면 정확한 값을 출력하지만, 병렬처리의 의미가 사라짐(?)
        # timerThread.join() 

    # (방법2) '모든 Thread들이 종료될 때까지 기다린다.'
    mainThread = threading.currentThread()
    for thread in threading.enumerate():
        # Main Thread를 제외한 모든 Thread들이 카운팅을 완료할 때까지 기다린다.
        # if thread is not mainThread:
        if thread.name == 'Timer Thread':
            thread.join()  # 현 위치의 join()을 실행 이전까지 시간에 대한 공유 데이터 문제 발생함
 
    print('totalCount = ' + str(totalCount))


#%% threading 활용(6) : 공유변수 사용(threading.Lock)
# https://coding-groot.tistory.com/103
# 이 방식은 공유변수를 acquire, release하는 과정을 반복하므로 시간이 많이 소요된다.

import time, sys, threading
from threading import Thread
 
# 공유된 변수를 위한 클래스
class ThreadVariable():
    def __init__(self):
        
        self.lock = threading.Lock()
        self.lockedValue = 0
 
    # 한 Thread만 접근할 수 있도록 설정한다
    def plus(self, value):
        # Lock해서 다른 Thread는 기다리게 만든다.
        self.lock.acquire()
        try:
            self.lockedValue += value
        finally:
            # Lock을 해제해서 다른 Thread도 사용할 수 있도록 만든다.
            self.lock.release()
 
class CounterThread(Thread):
    def __init__(self):
        Thread.__init__(self, name = 'Timer Thread')
        # self.event_stop = threading.Event()
        
    def run(self):
        global totalCount
        # if self.event_stop.is_set():
        #     return
        
        for _ in range(2500000):
            totalCount.plus(1)
        print('2,500,000번 카운팅 끝!')
    # def stop(self):
    #     self.event_stop.set()
        
if __name__ == '__main__':

    global totalCount
    totalCount = ThreadVariable()
 
    for _ in range(4):
        timerThread = CounterThread()
        timerThread.start()

    print('모든 Thread들이 종료될 때까지 기다린다.')
    
    mainThread = threading.current_thread()
    for thread in threading.enumerate():
        # Main Thread를 제외한 모든 Thread들이 카운팅을 완료하고 끝날 때까지 기다린다.
        # if thread is not mainThread:
        if thread.name == 'Timer Thread':
            thread.join()
 
    print('totalCount = ' + str(totalCount.lockedValue))

#%% threading 활용(7) : Thread, Event(), set(), is_set(), KeyboardInterrupt

import threading, time, sys

event = threading.Event()
a = 0

def worker():
    global a
    while(True):
        a += 1
        print('t2:', a)
        time.sleep(0.50)  
        if event.is_set():
            break
        
thread = threading.Thread(target = worker)
thread.start()

print('Ctrl+C : to stop')
while True:
    try:
        time.sleep(0.1)
    except KeyboardInterrupt:
        event.set()
        break
    
#%% threading 활용(8) : Event(), event.set(), event.is_set()
# https://www.pythonforthelab.com/blog/handling-and-sharing-data-between-threads/

from threading import Thread, Event
from time import sleep

event = Event()

def modify_variable(var):
    while True:
        for i in range(len(var)):
            var[i] += 1
        if event.is_set():
            break
        sleep(0.5)
    print('Stop printing')

my_var = [1, 2, 3]
t = Thread(target = modify_variable, args=(my_var, ))
t.start()

print('Ctrl+C : to stop')
while True:
    try:
        print(my_var)
        sleep(0.5)
    except KeyboardInterrupt:
        event.set()
        break
# t.join()
# print(my_var)

#%% threading 활용(9) : Event(), set(), is_set(), join()

import threading, time

class MyThread(threading.Thread):
    
    def __init__(self, sleep_time = 0.2):
        self._stop_event = threading.Event()
        self._sleep_time = sleep_time
        """call base class constructor"""
        super().__init__()

    def run(self):
        """main control loop"""
        while not self._stop_event.is_set():
            #do work
            print("hi")
            self._stop_event.wait(self._sleep_time)

    def join(self, timeout = None):
        """set stop event and join within a given time period"""
        self._stop_event.set()
        super().join(timeout)

if __name__ == "__main__":
    t = MyThread()
    t.start()
    time.sleep(2)
    t.join(1) #wait 1s max
   
#%% threading 활용(10) : Thread, current_thread(), getattr()

import threading, time

def doit(arg):
    t = threading.current_thread()
    while getattr(t, "do_run", True):   # t 객체에 'do_run' 속성이 'True'이면 실행
        print ("working on %s" % arg)
        time.sleep(1)
    print("Stopping as you wish.")

def main():
    t = threading.Thread(target = doit, args = ("task",))
    t.start()
    time.sleep(3)
    t.do_run = False

if __name__ == "__main__":
    main()
    
#%% threading 활용(11) : Thread, Event(), set(), is_set(), join()

import threading, time

class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    # def __init__(self):
    #     super().__init__()
    #     # super().__init__()
    #     # super(StoppableThread, self).__init__()
    #     self._stop_event = threading.Event()
        
    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__()
        # super(StoppableThread, self).__init__()
        # super(StoppableThread, self).__init__(*args, **kwargs)
        print(args, kwargs)
        self._stop_event = threading.Event()
        
    def stop(self):
        self._stop_event.set()

    def join(self, *args, **kwargs):
        self.stop()
        print(args, kwargs)
        super(StoppableThread,self).join()

    def run(self):
        while not self._stop_event.is_set():
            print("Still running!")
            time.sleep(1)
        print("run() is stopped!")

    def stopped(self):
        return self._stop_event.is_set()

def main():
    # t = StoppableThread()
    t = StoppableThread(1,2, msg='from Main')
    t.start()
    time.sleep(3)
    print(f'_stop_event={t.stopped()}')    
    t.join((1,2,3), msg='from Join')
    # t.stop()
    print(f'_stop_event={t.stopped()}')
    print('Finished')

if __name__ == "__main__":
    main()

#%% threading 활용(12) : Thread, current_thread(), activeCount(), daemon, join()

import threading, time, random

class ActivePool(object):
    def __init__(self):
        super(ActivePool, self).__init__()
        self.active = []
        self.lock = threading.Lock()
        
    def makeActive(self, name):
        with self.lock:
            self.active.append(name)

    def makeInactive(self, name):
        with self.lock:
            self.active.remove(name)
            
    def numActive(self):
        with self.lock:
            return len(self.active)

    def __str__(self):
        with self.lock:
            return str(self.active)

def worker(pool):
    
    name = threading.current_thread().name
    pool.makeActive(name)
    print('Now running: %s' % str(pool))
    # time.sleep(random.randint(1,3))
    time.sleep(3)
    pool.makeInactive(name)

if __name__=='__main__':
    
    jobs = []
    poolA = ActivePool()
    poolB = ActivePool()    

    for i in range(5):
        # target: 스레드가 실행할 함수 / agrs: 함수에 넘겨줄 인수(튜풀) / name: 스레드 이름
        jobs.append(threading.Thread(target = worker, args = (poolA,), name = 'A{0}'.format(i)))
        jobs.append(threading.Thread(target = worker, args = (poolB,), name = 'B{0}'.format(i)))
        # time.sleep(0.2)
        
    for j in jobs:
        j.daemon = True
        j.start()
        
    cnt = 0
    while threading.activeCount() > 1 and cnt < 10:
        for j in jobs:
            j.join(1)
            print('A-threads active: {0}, B-threads active: {1}'.format(poolA.numActive(), poolB.numActive()))
        cnt += 1

#%% threading 활용(13) : Thread, get_id(), hasattr(), threading._active.items()
# ctypes.pythonapi, PyThreadState_SetAsyncExc(thread_id), ctypes.py_object(SystemExit)

import time, sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import threading, ctypes
  
# Python program raising exceptions in a python thread
class thread_with_exception(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
             
    def run(self):
        cnt = 0
        try:
            while True and cnt < 10:
                print(f'cnt: {cnt}, running: {self.name}')
                time.sleep(0.5)
                cnt += 1
        finally:
            print('thread ended')
          
    def get_id(self):  # 스레드의 id를 반환
         # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        
        for id, thread in threading._active.items():
            if thread is self:
                return id
  
    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.pb1 = QPushButton("시 작!")
        self.pb1.clicked.connect(self.start)
        self.pb2 = QPushButton("종 료!")
        self.pb2.clicked.connect(self.stop)
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.pb1)
        vbox.addWidget(self.pb2)        

        self.resize(200, 100)
        self.setLayout(vbox)
        
        # self.t1 = thread_with_exception('Thread 1')
        # self.t1.join()
        
    def start(self):
        self.t1 = thread_with_exception('Thread 1')
        self.t1.start()
        # self.pb1.blockSignals(True)
        self.pb1.setEnabled(False)
        
    def stop(self):
        # self.pb1.blockSignals(False)
        self.pb1.setEnabled(True)
        if hasattr(self, 't1'):  # self 클래스에 't1' 인스턴스가 있으면 'True'
            self.t1.raise_exception()

    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit the program?"
        reply = QMessageBox.question(self, 'Message', quit_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            if hasattr(self, 't1'):
                if isinstance(self.t1, thread_with_exception):
                    if self.t1.is_alive():
                        self.t1.raise_exception()
                        print('thread killed') #  Thread가 여러개 일경우 나머지는 살아 있음.
            event.accept()
        else:
            event.ignore()
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MainWidget()
    widget.show()
    # sys.exit(app.exec_())
    app.exec_()
            

