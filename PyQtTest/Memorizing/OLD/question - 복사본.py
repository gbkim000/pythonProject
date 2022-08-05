import sys, time
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QRect
from PyQt5.QtWidgets import *

progVal = 0

class thread(QThread):
    
    signalTh = pyqtSignal(int)
    
    def __init__(self, *args):
        super().__init__()
        self.flag = True
        
    def run(self):
        global progVal
        if self.flag:
            self.signalTh.emit(progVal)
            time.sleep(0.1)
            
    def stop(self):
        self.flag = False
        self.quit()
        self.wait(2)

class MyWindow(QTableWidget):
    def __init__(self):
        global progVal
        super().__init__()
        self.setupUi(self)
        self.show()

        self.test = thread(None)
        self.test.signalTh.connect(self.signal_function)
        self.test.run()
        self.saveData()

    def saveData(self):   
        global progVal
        counts = range(1,31)
        for row in counts:
            progVal = int(row/len(counts)*100) 
            self.test.signalTh.emit(progVal)
            time.sleep(0.1)

    def click1_function(self):

        if self.test.flag:
            self.test.stop()
            self.pb_start.setText('Start!')
        else:
            self.test.flag = True
            self.test.run()
            self.pb_start.setText('Stop!')

    @pyqtSlot(int)
    def signal_function(self, val):
        self.progress.setValue(val)
        self.progress.update()
        self.win.update()
        self.update()

    def setupUi(self, QMainWindow):
        self.resize(500, 400)
        self.pb_start = QPushButton(self)
        self.pb_start.setGeometry(QRect(80, 20, 100, 50))
        self.pb_start.setText("Start")
        self.pb_start.clicked.connect(self.click1_function)

        self.win = QDialog(self)
        self.win.resize(330, 100)
        self.progress = QProgressBar(self.win)
        self.progress.setGeometry(10, 10, 300, 30)
        self.progress.setMaximum(100)        
        self.win.show() 
        
    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit the program?"
        reply = QMessageBox.question(self, 'Message', quit_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.test.stop()
            event.accept()
        else:
            event.ignore()
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myApp = MyWindow()
    myApp.show()
    app.exec_()