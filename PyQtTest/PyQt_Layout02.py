
# %% Layout(QDarkPalette 클래스 생성): QPalette, QColor, setStyleSheet

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMessageBox, QGridLayout, QStyleFactory

WHITE =     QColor(255, 255, 255)
BLACK =     QColor(0, 0, 0)
RED =       QColor(255, 0, 0)
PRIMARY =   QColor(53, 53, 53)
SECONDARY = QColor(35, 35, 35)
TERTIARY =  QColor(42, 130, 218)

def css_rgb(color, a = False):
    """Get a CSS `rgb` or `rgba` string from a `QtGui.QColor`."""
    return ("rgba({}, {}, {}, {})" if a else "rgb({}, {}, {})").format(*color.getRgb())     # rgba : r,g,b,alpha(불투명도 0~1)

class QDarkPalette(QPalette):
    """Dark palette for a Qt application meant to be used with the Fusion theme."""
    def __init__(self, *__args):
        super().__init__(*__args)

        # Set all the colors based on the constants in globals
        self.setColor(QPalette.Window,          PRIMARY)
        self.setColor(QPalette.WindowText,      WHITE)
        self.setColor(QPalette.Base,            SECONDARY)
        self.setColor(QPalette.AlternateBase,   PRIMARY)
        self.setColor(QPalette.ToolTipBase,     WHITE)
        self.setColor(QPalette.ToolTipText,     WHITE)
        self.setColor(QPalette.Text,            WHITE)
        self.setColor(QPalette.Button,          PRIMARY)
        self.setColor(QPalette.ButtonText,      WHITE)
        self.setColor(QPalette.BrightText,      RED)
        self.setColor(QPalette.Link,            TERTIARY)
        self.setColor(QPalette.Highlight,       TERTIARY)
        self.setColor(QPalette.HighlightedText, BLACK)

    @staticmethod
    def set_stylesheet(app):
        """Static method to set the tooltip stylesheet to a `QtWidgets.QApplication`."""
        app.setStyleSheet("QToolTip {{"
                          "color: {white};"
                          "background-color: {tertiary};"
                          "border: 1px solid {white};"
                          "}}".format(white=css_rgb(WHITE), tertiary=css_rgb(TERTIARY)))

    def set_app(self, app):
        """Set the Fusion theme and this palette to a `QtWidgets.QApplication`."""
        app.setStyle("Fusion")
        app.setPalette(self)
        self.set_stylesheet(app)    
       
if __name__ == '__main__':
    import sys
    qApp = QApplication(sys.argv)
    
    # qApp.setStyleSheet('')                            # style 미적용
    # qApp.setStyle(QStyleFactory.create('Fusion'))     # Windows/Fusion/...
    qApp.setPalette(qApp.style().standardPalette())   # default Palette
    
    dark_palette = QDarkPalette()
    qApp.setPalette(dark_palette)
    # dark_palette.set_app(qApp)
    
    w = QWidget()
    w.resize(300,100)
    grid = QGridLayout(w)
    grid.addWidget(QPushButton("버튼 1"), 0,0) #0행 0렬
    grid.addWidget(QPushButton("버튼 2"), 0,1) #0행 10렬
    grid.addWidget(QPushButton("버튼 3"), 1,0) #1행 0렬
    grid.addWidget(QPushButton("버튼 4"), 1,1) #1행 1렬

    w.show() # 중요 window는 기본값이 hidden이라 show 해야함
    sys.exit(qApp.exec_()) # 이상태는 이벤트 루프가 돌고있다.   
    
# %% Layout(계산기 UI) : QSizePolicy, QLineEdit, QGridLayout, setSpacing, rowSpan, colSpan

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Button(QPushButton):
    def __init__(self, text, parent, TextObject):
        super().__init__(text, parent = parent or None)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.clicked.connect(TextObject.SLOT_TextInsert('%s' %(text)))        

class Text(QLineEdit):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.show()

    def SLOT_TextInsert(self, text):
        return lambda: self.insert('%s' %(text))

    def SLOT_TextGet(self):
        text = self.text()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    app.setStyleSheet('')                           # style 미적용
    app.setStyle(QStyleFactory.create('Fusion'))    # Windows/Fusion/...
    app.setPalette(app.style().standardPalette())   # default Palette
    
    root = QWidget()
    text = Text(root) 
    
    plus = Button('+', root, text)
    minus = Button('-', root, text)
    multiple = Button('*', root, text)
    divide = Button('/', root, text)
    null = Button('0', root, text)
    dot = Button('.', root, text)
    equal = Button('=', root, text)
    clean = Button('Ce', root, text)

    layout = QGridLayout(root)
    layout.setSpacing(2)
    layout.addWidget(text, 1, 1, 1, 5)
    layout.addWidget(plus, 2, 4)
    layout.addWidget(minus, 2, 5)
    layout.addWidget(multiple, 3, 4)
    layout.addWidget(divide, 3, 5)
    layout.addWidget(clean, 4, 4, 1, 2)
    layout.addWidget(null, 5, 1, 1, 2)
    layout.addWidget(dot, 5, 3)
    layout.addWidget(equal, 5, 4, 1, 2)

    num_list = list()
    row = 2; col = 1
    for i in range(0, 9):
        num_list.append(Button('%s' %(i+1), root, text))
        layout.addWidget(num_list[i], row, col )
        col = col+1
        if i == 2 or i == 5:
            col = 1; row = row+1

    root.resize(10,10)
    root.show()        
    sys.exit(app.exec_())


# %% Layout(UI + 기능구현) : QSizePolicy, setSizePolicy, Expanding/Fixed/...

import sys
from PyQt5.QtWidgets import *

### 사이즈 정책을 설정한 새로운 class를 생성합니다. ###
class QPushButton(QPushButton):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

class QLabel(QLabel):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

class QLineEdit(QLineEdit):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        ### 각 위젯을 배치할 레이아웃을 미리 만들어 둠
        layout_operation = QHBoxLayout()
        layout_clear_equal = QHBoxLayout()
        layout_number = QGridLayout()
        layout_equation_solution = QFormLayout()

        ### 수식 입력과 답 출력을 위한 LineEdit 위젯 생성
        label_equation = QLabel("Equation: ")
        label_solution = QLabel("Solution: ")
        self.equation = QLineEdit("")
        self.solution = QLineEdit("")

        print(self.equation.sizeHint())
        print(self.equation.sizePolicy().horizontalPolicy())

        ### layout_equation_solution 레이아웃에 수식, 답 위젯을 추가
        layout_equation_solution.addRow(label_equation, self.equation)
        layout_equation_solution.addRow(label_solution, self.solution)

        ### 사칙연상 버튼 생성
        button_plus = QPushButton("+")
        button_minus = QPushButton("-")
        button_product = QPushButton("x")
        button_division = QPushButton("/")

        ### 사칙연산 버튼을 클릭했을 때, 각 사칙연산 부호가 수식창에 추가될 수 있도록 시그널 설정
        button_plus.clicked.connect(lambda state, operation = "+": self.button_operation_clicked(operation))
        button_minus.clicked.connect(lambda state, operation = "-": self.button_operation_clicked(operation))
        button_product.clicked.connect(lambda state, operation = "*": self.button_operation_clicked(operation))
        button_division.clicked.connect(lambda state, operation = "/": self.button_operation_clicked(operation))

        ### 사칙연산 버튼을 layout_operation 레이아웃에 추가
        layout_operation.addWidget(button_plus)
        layout_operation.addWidget(button_minus)
        layout_operation.addWidget(button_product)
        layout_operation.addWidget(button_division)

        ### =, clear, backspace 버튼 생성
        button_equal = QPushButton("=")
        button_clear = QPushButton("Clear")
        button_backspace = QPushButton("Backspace")

        ### =, clear, backspace 버튼 클릭 시 시그널 설정
        button_equal.clicked.connect(self.button_equal_clicked)
        button_clear.clicked.connect(self.button_clear_clicked)
        button_backspace.clicked.connect(self.button_backspace_clicked)

        ### =, clear, backspace 버튼을 layout_clear_equal 레이아웃에 추가
        layout_clear_equal.addWidget(button_clear)
        layout_clear_equal.addWidget(button_backspace)
        layout_clear_equal.addWidget(button_equal)

        ### 숫자 버튼 생성하고, layout_number 레이아웃에 추가
        ### 각 숫자 버튼을 클릭했을 때, 숫자가 수식창에 입력 될 수 있도록 시그널 설정
        number_button_dict = {}
        for number in range(0, 10):
            number_button_dict[number] = QPushButton(str(number))
            number_button_dict[number].clicked.connect(lambda state, num = number:
                                                       self.number_button_clicked(num))
            if number >0:
                x,y = divmod(number-1, 3)
                layout_number.addWidget(number_button_dict[number], x, y)
            elif number==0:
                layout_number.addWidget(number_button_dict[number], 3, 1)

        ### 소숫점 버튼과 00 버튼을 입력하고 시그널 설정
        button_dot = QPushButton(".")
        button_dot.clicked.connect(lambda state, num = ".": self.number_button_clicked(num))
        layout_number.addWidget(button_dot, 3, 2)

        button_double_zero = QPushButton("00")
        button_double_zero.clicked.connect(lambda state, num = "00": self.number_button_clicked(num))
        layout_number.addWidget(button_double_zero, 3, 0)

        ### 각 레이아웃을 main_layout 레이아웃에 추가
        main_layout.addLayout(layout_equation_solution, stretch=1)
        main_layout.addLayout(layout_operation, stretch=1)
        main_layout.addLayout(layout_clear_equal, stretch=1)
        main_layout.addLayout(layout_number, stretch=4)

        self.setLayout(main_layout)
        self.show()

    #################
    ### functions ###
    #################
    def number_button_clicked(self, num):
        equation = self.equation.text()
        equation += str(num)
        self.equation.setText(equation)

    def button_operation_clicked(self, operation):
        equation = self.equation.text()
        equation += operation
        self.equation.setText(equation)

    def button_equal_clicked(self):
        equation = self.equation.text()
        solution = eval(equation)
        self.solution.setText(str(solution))

    def button_clear_clicked(self):
        self.equation.setText("")
        self.solution.setText("")

    def button_backspace_clicked(self):
        equation = self.equation.text()
        equation = equation[:-1]
        self.equation.setText(equation)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    app.setStyleSheet('')                           # style 미적용
    app.setStyle(QStyleFactory.create('Fusion'))    # Windows/Fusion/...
    app.setPalette(app.style().standardPalette())   # default Palette
    
    main = Main()
    sys.exit(app.exec_())

# %% Layout(테이블) : QTableWidget), setStyleSheet, setBackground, ItemIsEditable, horizontalHeader

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
    
class Example(QWidget):

    def __init__(self):
        super(Example, self).__init__()
        # super().__init__()
        self.initUI()

    def initUI(self):

        title = QPushButton( 'Title' )
        author = QPushButton( 'Author' )
        other = QPushButton( 'Other' )

        view1 = QTableWidget(10, 5)
        view1.setColumnWidth(0, 50)
        view1.setColumnWidth(1, 300)
        view1.setColumnWidth(2, 300)
        view1.setColumnWidth(3, 50)
        view1.setColumnWidth(4, 50)
        tblStyle = ("QHeaderView::section {background-color: rgb(173, 255, 47); font-size: 18px; }"
                  "QTableView{ background-color:#D3D3D3; font-size: 18px; padding:0px; } ")   #EBDEF1(연보라)
        view1.setStyleSheet(tblStyle)
        # view1.setStyleSheet("QHeaderView::section { background-color:green }")
        view1.setHorizontalHeaderLabels(["seq", "Korean", "English", "Done", "Point"])
        view1.horizontalHeader().setFixedHeight(50)
        view1.horizontalHeader().setStretchLastSection(True)    # 마지막 칼럼 확장 
        view1.verticalHeader().setVisible(False)
        
        rows = 10
        for row in range(rows):
            itm1 = QTableWidgetItem(str(row))
            itm1.setFlags(itm1.flags() & ~Qt.ItemIsEditable)
            itm1.setBackground(QColor(200, 100, 100))
            itm1.setTextAlignment(Qt.AlignCenter)
            view1.setItem(row, 0, itm1)

        view2 = QTableWidget(5,5)
        view2.setColumnWidth(0, 50)
        view2.setColumnWidth(1, 300)
        view2.setColumnWidth(2, 300)
        view2.setColumnWidth(3, 50)
        view2.setColumnWidth(4, 50)        
        view2.setHorizontalHeaderLabels(["seq", "Korean", "English", "Done", "Point"])
        view2.horizontalHeader().setFixedHeight(50)
        view2.horizontalHeader().setStretchLastSection(True)    # 마지막 칼럼 확장
        
        titleEdit = QTextEdit('Hello everyone!')

        horizontalLayout = QHBoxLayout()
        horizontalLayout.addWidget( title )
        horizontalLayout.addWidget( author )
        horizontalLayout.addWidget( other )
        
        vLayout1 = QVBoxLayout()
        vLayout1.addWidget( view1 )

        vLayout2 = QVBoxLayout()
        vLayout2.addWidget( view2 )
        
        verticalLayout = QVBoxLayout()
        verticalLayout.addLayout( horizontalLayout )
        verticalLayout.addLayout( vLayout1 )
        verticalLayout.addLayout( vLayout2 )
        verticalLayout.addWidget( titleEdit )

        self.setLayout( verticalLayout )
        self.setGeometry( 300, 100, 800,800 )
        self.setWindowTitle( 'Review' )
        self.show()

def main():
    app = QApplication( sys.argv )
    ex = Example()
    sys.exit( app.exec_() )

if __name__ == '__main__':
    main()

