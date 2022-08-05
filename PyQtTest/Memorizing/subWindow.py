# %% 탭 위젯(3) (스타일 적용하기)
# QTabWidget, QVBoxLayout, QHBoxLayout, setSpacing, QPalette, setColor, addTab

import sys, os
from PyQt5.QtCore import Qt, QRect, QCoreApplication
from PyQt5.QtGui import QPalette, QColor, QFont, QIcon
from PyQt5.QtWidgets import *

class QPushBtn1(QPushButton):
    def __init__(self, parent = None, *args):
        super().__init__(parent, *args)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.setMinimumHeight(30)
        
class QPushBtn2(QPushButton):
    def __init__(self, parent = None, *args):
        super().__init__(parent, *args)
        # self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.setMinimumHeight(30)

class QPushBtn3(QPushButton):     # 파생 클래스 생성
    def __init__(self, parent = None, *args):
        super().__init__(parent, *args)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumHeight(50)
        btnStyle1 = '''                                               
                QPushButton { background-color: #F7F; border-style: outset; border-width: 2px; border-radius: 10px;
                border-color: beige; font: bold 14px; min-width: 10em; padding: 6px;}
        '''
        btnStyle2 = ("QPushButton {background-color: #1D7EB5; color: white; border-radius: 3; border-color: white;}"
                "QPushButton::hover {background-color: #EA90E1; color: #fff;} " #202D4F #EA90E1
                "QPushButton::pressed {background-color: #F90;}")    
        self.setStyleSheet(btnStyle2)

class QLabel2(QLabel):  
    def __init__(self, parent = None, *args):
        super().__init__(parent, *args)
        self.setMinimumHeight(30)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet('background-color: #00F; color: rgb(255,255,255);')
        
# --------------------------------------------------------------------------
class MyWidget(QWidget): 
    def __init__(self, parent=None): 
        super().__init__() 
        self.parent = parent
        btn1 = QPushButton('1') 
        btn2 = QPushButton('2') 
        layout = QHBoxLayout() 
        layout.addWidget(btn1) 
        layout.addWidget(btn2) 
        self.setLayout(layout) 
        self.setGeometry(300, 100, 350, 150)  # x, y, width, height 
        self.setWindowTitle("QWidget") 
        self.show() 
        
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            self.parent.ex2.close()
            self.parent.ex3.close()
            self.parent.ex4.close()
        else:
            event.ignore()
            
class MyDialog(QDialog): 
    def __init__(self): 
        super().__init__() 
        btn1 = QPushButton('1') 
        btn2 = QPushButton('2') 
        layout = QHBoxLayout() 
        layout.addWidget(btn1) 
        layout.addWidget(btn2) 
        self.setLayout(layout) 
        self.setGeometry(300, 300, 350, 150) 
        self.setWindowTitle("QDialog") 
        self.show() 

class MyMainWindow1(QMainWindow): 
    """ 
    옳은 방법... 
    QWidget, QDialog 와 달리 QMainWindow 는 자체적으로 layout 가지고 있다. 
    central widget 을 반드시 필요로함. 
    """ 
    def __init__(self): 
        super().__init__() 
        wg = MyWidget()            # placeholder -- QWidget 상속하여 만든것으로 추후 교체하면 됨. 
        self.setCentralWidget(wg)   # 반드시 필요함. 
        self.setGeometry(300, 500, 350, 150) 
        self.setWindowTitle("QWidget") 
        self.show() 
            
class MyMainWindow2(QMainWindow): 
    """ 
    틀린방법... 
    ** QWidget, QDialog 처럼 layout 사용 못함. 
    """ 
    def __init__(self): 
        super().__init__() 
        btn1 = QPushButton('1') 
        btn2 = QPushButton('2') 
        layout = QHBoxLayout() 
        layout.addWidget(btn1) 
        layout.addWidget(btn2) 
        self.setLayout(layout) 
        self.setGeometry(300, 700, 350, 150) 
        self.setWindowTitle("QMainWindow 틀린 방법") 
        self.show() 

# --------------------------------------------------------------------------
class SourceView(QWidget):

    def __init__(self, tabIndex):
        super().__init__()
        self.tabIndex = tabIndex
        self.initUI()

    def initUI(self):

        self.tBrowse = QTextBrowser()
        self.tBrowse.setAcceptRichText(True)
        self.tBrowse.setOpenExternalLinks(True)
        self.tBrowse.setReadOnly(False)
        self.clear_btn = QPushButton('Clear')
        self.clear_btn.pressed.connect(self.clear_text)
        self.clear_btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.clear_btn.setMinimumHeight(30)
        self.add_source()
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.tBrowse,   0)
        vbox.addWidget(self.clear_btn, 1)
        self.setLayout(vbox)
        self.setWindowTitle('QTextBrowser')
        self.resize(900, 600)
        self.center()
        self.show()

    def add_source(self):
        text1 = """
        import sys
        from PyQt5.QtCore import Qt
        from PyQt5.QtGui import QPalette, QColor, QFont
        from PyQt5.QtWidgets import *
        
        class QPushBtn1(QPushButton):     # 파생 클래스 생성
            def __init__(self, parent = None, *args):
                super().__init__(parent, *args)
                self.setSizePolicy(7, 7)
                self.setMinimumHeight(100)
                btnStyle1 = '''                                               
                        QPushButton { background-color: #F7F; border-style: outset; border-width: 2px; border-radius: 10px;
                              border-color: beige; font: bold 14px; min-width: 10em; padding: 6px;}
                '''
                btnStyle2 = ("QPushButton {background-color: #1D7EB5; color: white; border-radius: 3; border-color: white}"
                      "QPushButton::hover {background-color: #EA90E1; color: #fff;} "#202D4F #EA90E1
                      "QPushButton::pressed {background-color: #FF9900;}")    
                self.setStyleSheet(btnStyle1)
                
        class QTabWindow(QMainWindow):
            def __init__(self):
                super().__init__()
        
                self.setWindowTitle('Sidebar layout')
                self.Width = 800
                self.height = int(0.618 * self.Width)
                self.resize(self.Width, self.height)
        
                # add all widgets
                self.btn_1 = QPushBtn1('1', self)
                self.btn_2 = QPushBtn1('2', self)
                self.btn_3 = QPushBtn1('3', self)
                self.btn_4 = QPushBtn1('4', self)
                self.btn_5 = QPushButton('소스코드', self)
                
                self.btn_1.clicked.connect(self.button1)
                self.btn_2.clicked.connect(self.button2)
                self.btn_3.clicked.connect(self.button3)
                self.btn_4.clicked.connect(self.button4)
                self.btn_5.clicked.connect(self.button5)
                
                # add tabs
                self.tab1 = self.ui1()  # self.ui1()의 리턴값 -> QWidget()
                self.tab2 = self.ui2()
                self.tab3 = self.ui3()
                self.tab4 = self.ui4()
                self.initUI()
            
            def initUI(self):
                left_layout = QVBoxLayout()
                left_layout.addWidget(self.btn_1)
                left_layout.addWidget(self.btn_2)
                left_layout.addWidget(self.btn_3)
                left_layout.addWidget(self.btn_4)
                left_layout.addWidget(self.btn_5)
                left_layout.setSpacing(20)
                left_widget = QWidget()
                left_widget.setLayout(left_layout)
        
                self.right_widget = QTabWidget()
                self.right_widget.tabBar().setObjectName("mainTab")
                self.right_widget.addTab(self.tab1, '설정')
                self.right_widget.addTab(self.tab2, '기본값')
                self.right_widget.addTab(self.tab3, '사용자')
                self.right_widget.addTab(self.tab4, '기타')
                self.right_widget.setCurrentIndex(0)
                    
                style1 = '''
                QTabWidget::pane { border: 5px solid #CCC; background: #777; padding: 10px; border-top: 1px solid #FF0;}
                QTabBar::tab {width: 150; height: 100; margin: 0; padding: 1; background: #0F8; border-radius: 5; border: 1px solid transparent; }
                '''
                style2 = '''
                QTabWidget::pane { border: 10px solid lightgray; top:-1px; background: rgb(200, 100, 100); } 
                QTabBar::tab { background: rgb(200, 100, 200); border: 1px solid white; padding: 5px; min-width: 100px; min-height: 50px; } 
                QTabBar::tab:selected { background: rgb(100, 200, 200); margin-bottom: -1px; }
                '''
                style3 = '''
                QTabWidget { border: 0; }
                QTabWidget::pane { border: 1px solid #FFF; background: #000; padding: 0px; border-top: 1px solid #FF0;}
                QTabBar::tab { background: rgb(200, 100, 200); color: #0F0; border-radius: 3px; border: 1px solid white; min-width: 80px; }
                QTabBar::tab:top { margin: 10px 1px 0 0; padding: 5px 5px; border-bottom: 3px solid lightgray; } /* margin: 상,우,하,좌 */
                QTabBar::tab:selected { color: white; background: #000; border: 0px; } 
                QTabBar::tab:top:hover { border-bottom: 3px solid #444; color: #FF0;}
                QTabBar::tab:top:selected { border-bottom: 3px solid #F00; background: #000;}
                QTabBar::tab:hover, QTabBar::tab:focus { border-bottom: 3px solid #FF0; background: #00F;}
                '''
                self.right_widget.setStyleSheet(style3)
                main_layout = QHBoxLayout()
                main_layout.addWidget(left_widget)
                main_layout.addWidget(self.right_widget)
                main_layout.setStretch(0, 40)
                main_layout.setStretch(1, 200)
                main_widget = QWidget()
                main_widget.setLayout(main_layout)
                self.setCentralWidget(main_widget)
        
            # ----------------- buttons
            def button1(self):
                self.right_widget.setCurrentIndex(0)
        
            def button2(self):
                self.right_widget.setCurrentIndex(1)
        
            def button3(self):
                self.right_widget.setCurrentIndex(2)
        
            def button4(self):
                self.right_widget.setCurrentIndex(3)
        
            def button5(self):
                # self.hide() 
                self.win = SourceView()
                # self.win.show()
               
            # ----------------- # pages
            def ui1(self):
                main_layout = QVBoxLayout()
                # main_layout.addWidget(QLabel('page 1'))
                view = QTableWidget(20,5)
                view.setHorizontalHeaderLabels(["순", "한국어", "English", "암기", "중요"])
                view.horizontalHeader().setFixedHeight(30)
                view.horizontalHeader().setStretchLastSection(True)    # 마지막 칼럼 확장하기  
                # view.verticalHeader().setVisible(False)
                view.verticalHeader().setDefaultSectionSize(30)
                view.verticalHeader().setSectionResizeMode(QHeaderView.Interactive) #(QHeaderView.Fixed)
                view.setAlternatingRowColors(True)
                view.setShowGrid(True)
                
                main_layout.addWidget(view)
                main = QWidget()
                main.setLayout(main_layout)
                return main
        
            def ui2(self):
                main_layout = QVBoxLayout()
                main_layout.addWidget(QLabel('page 2'))
                main_layout.addStretch(5)
                main = QWidget()
                main.setLayout(main_layout)
                return main
        
            def ui3(self):
                main_layout = QVBoxLayout()
                main_layout.addWidget(QLabel('page 3'))
                main_layout.addStretch(5)
                main = QWidget()
                main.setLayout(main_layout)
                return main
        
            def ui4(self):
                main_layout = QVBoxLayout()
                main_layout.addWidget(QLabel('page 4'))
                main_layout.addStretch(5)
                main = QWidget()
                main.setLayout(main_layout)
                return main
        
        class SourceView(QWidget):
        
            def __init__(self):
                super().__init__()
                self.initUI()
        
            def initUI(self):
                # self.le = QLineEdit()
                # self.le.returnPressed.connect(self.append_text)
        
                self.tBrowse = QTextBrowser()
                self.tBrowse.setAcceptRichText(True)
                self.tBrowse.setOpenExternalLinks(True)
                self.tBrowse.setReadOnly(False)
                self.clear_btn = QPushButton('Clear')
                self.clear_btn.pressed.connect(self.clear_text)
        
                vbox = QVBoxLayout()
                # vbox.addWidget(self.le, 0)
                vbox.addWidget(self.tBrowse,   0)
                vbox.addWidget(self.clear_btn, 1)
                self.setLayout(vbox)
                self.setWindowTitle('QTextBrowser')
                self.resize(800, 600)
                self.center()
                self.show()
        
            # def append_text(self):
            #     text = self.le.text()
            #     self.tBrowse.append(text)
            #     self.le.clear()
        
            def clear_text(self):
                self.tBrowse.clear()
        
            def center(self):
                qr = self.frameGeometry()
                cp = QDesktopWidget().availableGeometry().center()  # 모니터 중심 좌표
                qr.moveCenter(cp)
                self.move(qr.topLeft())
                
        if __name__ == '__main__':
            app = QApplication(sys.argv)
            app.setPalette(app.style().standardPalette())   # default Palette    
            app.setStyle("Windows")  # ['Windows', 'Fusion', 'Breeze', 'Oxygen', 'QtCurve']
            palette = QPalette()
            palette.setColor(QPalette.Button, QColor(0, 200, 0))
            palette.setColor(QPalette.ButtonText, Qt.red)
            palette.setColor(QPalette.Window, QColor(0, 150, 200))
            palette.setColor(QPalette.WindowText, Qt.blue)
            # palette.setColor(QPalette.Base, QColor(0, 200, 200))
            # palette.setColor(QPalette.AlternateBase, QColor(53, 53, 200))
            # palette.setColor(QPalette.ToolTipBase, Qt.white)
            # palette.setColor(QPalette.ToolTipText, Qt.white)
            # palette.setColor(QPalette.Text, Qt.blue)
            # palette.setColor(QPalette.BrightText, Qt.red)
            # palette.setColor(QPalette.Link, QColor(42, 130, 218))
            # palette.setColor(QPalette.Highlight, QColor(0, 200, 0))
            # palette.setColor(QPalette.HighlightedText, Qt.black)
            app.setPalette(palette)
            ex = QTabWindow()
            ex.show()
            sys.exit(app.exec_())        
        
        """
        
        text2 = """
        def ui2(self):
            layout = QVBoxLayout()
            win = QWidget()
            win.setLayout(layout)
            btn = QPushButton('push button2')
            btn.setStyleSheet("background-color: #C80; color: rgb(255,255,255); ") #D269E6
            btn.clicked.connect(self.winTest02)
            lbl = QLabel('page 2')
            lbl.setStyleSheet('background-color: #00F; color: rgb(255,255,255);')
            layout.addWidget(btn)
            layout.addWidget(lbl)
            return win        

        def winTest02(self):
            self.Form = QWidget()
            self.Form.resize(430, 240)
            self.Form.setWindowTitle("This is Widget")
            addBtn = QPushButton("ADD", self.Form)
            addBtn.setGeometry(QRect(350, 10, 75, 23))
            # self.addBtn.setObjectName("addBtn")
            textBox = QLineEdit(self.Form)
            textBox.setGeometry(QRect(10, 10, 331, 20))
            textList = QListView(self.Form)
            textList.setGeometry(QRect(10, 40, 331, 192))
            exitBtn = QPushButton("EXIT", self.Form)
            exitBtn.setGeometry(QRect(350, 40, 75, 191))
            self.Form.show()
        """
        
        text3 = """
        import sys
        from PyQt5.QtCore import Qt
        from PyQt5.QtGui import QColor, QPalette
        from PyQt5.QtWidgets import (
            QApplication,
            QHBoxLayout,
            QLabel,
            QMainWindow,
            QPushButton,
            QStackedLayout,
            QVBoxLayout,
            QWidget,)

        class ColorBox(QWidget):
            def __init__(self, color):
                # super().__init__()
                super(ColorBox, self).__init__()
                self.setAutoFillBackground(True)

                palette = self.palette()
                palette.setColor(QPalette.Window, QColor(color))
                self.setPalette(palette)

        class MainWindow(QMainWindow):
        # class MainWindow(QWidget):
            
            def __init__(self): 
                super().__init__() 
                self.resize(300,200)
                self.setWindowTitle("My App")

                button_layout = QHBoxLayout()
                
                btn = QPushButton("red")
                btn.pressed.connect(self.activate_tab_1)
                button_layout.addWidget(btn)

                btn = QPushButton("green")
                btn.pressed.connect(self.activate_tab_2)
                button_layout.addWidget(btn)

                btn = QPushButton("yellow")
                btn.pressed.connect(self.activate_tab_3)
                button_layout.addWidget(btn)

                self.stacklayout = QStackedLayout()
                self.stacklayout.addWidget(ColorBox("red"))
                self.stacklayout.addWidget(ColorBox("green"))
                self.stacklayout.addWidget(ColorBox("yellow"))
                
                pagelayout = QVBoxLayout()
                pagelayout.addLayout(button_layout)
                pagelayout.addLayout(self.stacklayout)

                widget = QWidget()
                widget.setLayout(pagelayout)
                self.setCentralWidget(widget)
                # self.setLayout(pagelayout)
                # self.statusBar().showMessage('Palette Color Change')
                
            def activate_tab_1(self):
                self.stacklayout.setCurrentIndex(0)

            def activate_tab_2(self):
                self.stacklayout.setCurrentIndex(1)

            def activate_tab_3(self):
                self.stacklayout.setCurrentIndex(2)

        app = QApplication(sys.argv)
        app.setPalette(app.style().standardPalette())   # default Palette

        window = MainWindow()
        window.show()
        app.exec()

        """
        text4 = """
        def ui4(self):
            layout = QVBoxLayout()
            win = QWidget()
            win.setLayout(layout)
            btn = QPushButton('push button4')
            btn.setStyleSheet("background-color: #D269E6; color: rgb(255,255,255); ") 
            btn.clicked.connect(self.winTest04)
            lbl = QLabel('page 4')
            lbl.setAlignment(Qt.AlignCenter)
            layout.addWidget(btn)
            layout.addWidget(lbl)
            return win  

        def winTest04(self):
            self.ex1 = MyWidget(self)
            self.ex2 = MyDialog() 
            self.ex3 = MyMainWindow1() 
            self.ex4 = MyMainWindow2() 
        """
        text5 = """
        def ui5(self):
            layout = QVBoxLayout()
            view = QTableWidget(20,5)
            view.setHorizontalHeaderLabels(["순", "한국어", "English", "암기", "중요"])
            view.horizontalHeader().setFixedHeight(30)
            view.horizontalHeader().setStretchLastSection(True)    # 마지막 칼럼 확장하기  
            # view.verticalHeader().setVisible(False)
            view.verticalHeader().setDefaultSectionSize(30)
            view.verticalHeader().setSectionResizeMode(QHeaderView.Interactive) #(QHeaderView.Fixed)
            view.setAlternatingRowColors(True)
            view.setShowGrid(True)
            
            layout.addWidget(view)
            win = QWidget()
            win.setLayout(layout)
            return win
        """
        
        if self.tabIndex   == 0:
            text = text1
        elif self.tabIndex == 1:
            text = text2
        elif self.tabIndex == 2:
            text = text3
        elif self.tabIndex == 3:
            text = text4
        else:
            text = text5
            
        self.tBrowse.setFont(QFont('맑은 고딕', 12))
        self.tBrowse.setText(text)
        
    def clear_text(self):
        self.tBrowse.clear()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()  # 모니터 중심 좌표
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
# --------------------------------------------------------------------------

class QTabWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Tab Widget Example')
        self.Width = 800
        self.height = int(0.618 * self.Width)
        self.resize(self.Width, self.height)

        # add all widgets
        self.btn_1 = QPushBtn3('예제 1', self)
        self.btn_2 = QPushBtn3('예제 2', self)
        self.btn_3 = QPushBtn3('예제 3', self)
        self.btn_4 = QPushBtn3('예제 4', self)
        self.btn_5 = QPushBtn3('예제 5', self)        
        self.source = QPushBtn1('소스코드', self)
        
        self.btn_1.clicked.connect(self.button1)
        self.btn_2.clicked.connect(self.button2)
        self.btn_3.clicked.connect(self.button3)
        self.btn_4.clicked.connect(self.button4)
        self.btn_5.clicked.connect(self.button5)
        self.source.clicked.connect(self.sourceView)        
        
        # add tabs
        self.tab1 = self.ui1()  # self.ui1()의 리턴값 -> QWidget()
        self.tab2 = self.ui2()
        self.tab3 = self.ui3()
        self.tab4 = self.ui4()
        self.tab5 = self.ui5()
        self.initUI()

    def initUI(self):
        left_layout = QVBoxLayout()
        left_layout.addSpacing(3)
        left_layout.addWidget(self.source)  
        left_layout.addWidget(self.btn_1)
        left_layout.addWidget(self.btn_2)
        left_layout.addWidget(self.btn_3)
        left_layout.addWidget(self.btn_4)
        left_layout.addWidget(self.btn_5)          
        left_layout.setSpacing(20)
        
        left_widget = QWidget()
        left_widget.setLayout(left_layout)

        self.right_widget = QTabWidget()
        self.right_widget.tabBar().setObjectName("mainTab")
        self.right_widget.addTab(self.tab1, 'Widget(1)')
        self.right_widget.addTab(self.tab2, 'Widget(2)')
        self.right_widget.addTab(self.tab3, 'Widget(3)')
        self.right_widget.addTab(self.tab4, 'Widget(4)')
        self.right_widget.addTab(self.tab5, 'Widget(5)')
        self.right_widget.setCurrentIndex(0)
            
        style1 = '''
        QTabWidget::pane { border: 5px solid #CCC; background: #777; padding: 10px; border-top: 1px solid #FF0;}
        QTabBar::tab {width: 150; height: 100; margin: 0; padding: 1; background: #0F8; border-radius: 5; border: 1px solid transparent; }
        '''
        style2 = '''
        QTabWidget::pane { border: 10px solid lightgray; top:-1px; background: rgb(200, 100, 100); } 
        QTabBar::tab { background: rgb(200, 100, 200); border: 1px solid white; padding: 5px; min-width: 100px; min-height: 50px; } 
        QTabBar::tab:selected { background: rgb(100, 200, 200); margin-bottom: -1px; }
        '''
        style3 = '''
        QTabWidget { border: 0px; }
        QTabWidget::pane { border: 1px solid #FFF; background: #000; padding: -6px; border-top: 1px solid #FF0; }
        QTabBar::tab { background: rgb(200, 100, 200); color: #0FF; border-radius: 3px; border: 1px solid white; min-width: 80px; }
        QTabBar::tab:top { margin: 10px 1px 0 0; padding: 5px 5px; border-bottom: 3px solid lightgray; } /* margin: 상,우,하,좌 */
        QTabBar::tab:selected { color: white; background: #000; border: 0px; } 
        QTabBar::tab:top:hover { border-bottom: 3px solid #444; color: #FF0;}
        QTabBar::tab:top:selected { border-bottom: 3px solid #F00; background: #000;}
        QTabBar::tab:hover, QTabBar::tab:focus { border-bottom: 3px solid #FF0; background: #00F;}
        '''
        self.right_widget.setStyleSheet(style3)
        main_layout = QHBoxLayout()
        main_layout.addWidget(left_widget)
        main_layout.addWidget(self.right_widget)
        main_layout.setStretch(0, 40)
        main_layout.setStretch(1, 200)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    # -------------------------------- buttons
    def button1(self):
        self.right_widget.setCurrentIndex(0)

    def button2(self):
        self.right_widget.setCurrentIndex(1)
        
    def button3(self):
        self.right_widget.setCurrentIndex(2)

    def button4(self):
        self.right_widget.setCurrentIndex(3)

    def button5(self):
        self.right_widget.setCurrentIndex(4)
        
    def sourceView(self):
        # self.hide() 
        tabIndex = self.right_widget.currentIndex()
        self.win = SourceView(tabIndex)
        # self.win.show()
       
    # -------------------------------- # ui1 page
    def ui1(self):
        layout = QVBoxLayout()
        win = QWidget()
        win.setLayout(layout)
        lbl = QLabel2('page 1(QLabel)')
        lbl.setAlignment(Qt.AlignCenter)

        self.browse = QTextBrowser()
        btn = QPushBtn2('push button1')
        # btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        btn.clicked.connect(lambda: self.printInfo(win))
        layout.addWidget(lbl)
        layout.addWidget(btn)
        layout.addWidget(self.browse)
        win.setLayout(layout)
        return win
    
    def printInfo(self, win):
        self.browse.append(f'{win.size()}, {win.rect()}')
        self.browse.append(f'{win.width(), win.height()}')              # 400 200        
        self.browse.append(f'{win.pos().y(),win.pos().x()}')            # 300 100     
        self.browse.append(f'{win.geometry().y(),win.geometry().x()}')  # 300 100
        self.browse.append(f'{win.geometry().width(),win.geometry().height()}')             # 400 200
        self.browse.append(f'{win.frameGeometry().width(),win.frameGeometry().height()}')   # 400 200  
    
    # -------------------------------- # ui2 page
    def ui2(self):
        layout = QVBoxLayout()
        win = QWidget()
        win.setLayout(layout)
        btn = QPushBtn2('push button2')
        btn.setStyleSheet("background-color: #C80; color: rgb(255,255,255); ") #D269E6
        btn.clicked.connect(self.winTest02)
        lbl = QLabel2('page 2')
        lbl.setStyleSheet('background-color: #00F; color: rgb(255,255,255);')
        layout.addWidget(btn)
        layout.addWidget(lbl)
        return win        

    def winTest02(self):
        self.Form = QWidget()
        self.Form.resize(430, 240)
        self.Form.setWindowTitle("This is Widget")
        addBtn = QPushBtn2("ADD", self.Form)
        addBtn.setGeometry(QRect(350, 10, 75, 23))
        # self.addBtn.setObjectName("addBtn")
        textBox = QLineEdit(self.Form)
        textBox.setGeometry(QRect(10, 10, 331, 20))
        textList = QListView(self.Form)
        textList.setGeometry(QRect(10, 40, 331, 192))
        exitBtn = QPushBtn2("EXIT", self.Form)
        exitBtn.setGeometry(QRect(350, 40, 75, 191))
        self.Form.show()

    # -------------------------------- # ui3 page
    def ui3(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel('page 3'))
        
        button_layout = QHBoxLayout()
        btn1 = QPushBtn2("red")
        btn1.pressed.connect(self.activate_tab_1)
        button_layout.addWidget(btn1)

        btn2 = QPushBtn2("green")
        btn2.pressed.connect(self.activate_tab_2)
        button_layout.addWidget(btn2)

        btn3 = QPushBtn2("yellow")
        btn3.pressed.connect(self.activate_tab_3)
        button_layout.addWidget(btn3)

        self.stacklayout = QStackedLayout()
        self.stacklayout.addWidget(self.ColorBox("red"))
        self.stacklayout.addWidget(self.ColorBox("green"))
        self.stacklayout.addWidget(self.ColorBox("yellow"))
        
        pagelayout = QVBoxLayout()
        pagelayout.addLayout(layout)
        pagelayout.addLayout(button_layout)
        pagelayout.addLayout(self.stacklayout)

        widget = QWidget()
        widget.setLayout(pagelayout)
        widget.setPalette(app.style().standardPalette())   # default Palette
        return widget

    def ColorBox(self, color):
        widget = QWidget()
        widget.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        widget.setPalette(palette)
        return widget

    def activate_tab_1(self):
        self.stacklayout.setCurrentIndex(0)

    def activate_tab_2(self):
        self.stacklayout.setCurrentIndex(1)

    def activate_tab_3(self):
        self.stacklayout.setCurrentIndex(2)
        
    # -------------------------------- # ui4 page
    def ui4(self):
        layout = QVBoxLayout()
        win = QWidget()
        win.setLayout(layout)
        btn = QPushButton('push button4')
        btn.setStyleSheet("background-color: #D269E6; color: rgb(255,255,255); ") 
        btn.clicked.connect(self.winTest04)
        lbl = QLabel2('page 4')
        lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(btn)
        layout.addWidget(lbl)
        return win  

    def winTest04(self):
        self.ex1 = MyWidget(self)
        self.ex2 = MyDialog() 
        self.ex3 = MyMainWindow1() 
        self.ex4 = MyMainWindow2() 
        
    # -------------------------------- # ui5 page
    def ui5(self):
        layout = QVBoxLayout()
        view = QTableWidget(20,5)
        view.setHorizontalHeaderLabels(["순", "한국어", "English", "암기", "중요"])
        view.horizontalHeader().setFixedHeight(30)
        view.horizontalHeader().setStretchLastSection(True)    # 마지막 칼럼 확장하기  
        # view.verticalHeader().setVisible(False)
        view.verticalHeader().setDefaultSectionSize(30)
        view.verticalHeader().setSectionResizeMode(QHeaderView.Interactive) #(QHeaderView.Fixed)
        view.setAlternatingRowColors(True)
        view.setShowGrid(True)
        
        layout.addWidget(view)
        win = QWidget()
        win.setLayout(layout)
        return win
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setPalette(app.style().standardPalette())   # default Palette    
    app.setStyle("Windows")  # ['Windows', 'Fusion', 'Breeze', 'Oxygen', 'QtCurve']
    palette = QPalette()
    palette.setColor(QPalette.Button, QColor(0, 200, 0))
    palette.setColor(QPalette.ButtonText, Qt.red)
    palette.setColor(QPalette.Window, QColor(0, 150, 200))
    palette.setColor(QPalette.WindowText, Qt.blue)
    app.setPalette(palette)
    ex = QTabWindow()
    ex.show()
    sys.exit(app.exec_())
    

