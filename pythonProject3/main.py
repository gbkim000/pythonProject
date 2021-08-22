import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
import pybithumb
import locale

tickers = ["MBL", "BTT", "MIX", "BTC", "ETH", "XRP"]
form_class = uic.loadUiType("bull.ui")[0]


def get_market_infos(ticker):
    df = pybithumb.get_ohlcv(ticker)
    ma5 = df['close'].rolling(window=5).mean()
    last_ma5 = ma5[-2]
    price = pybithumb.get_current_price(ticker)

    state = None
    if price > last_ma5:
        state = "Rising Market"
    else:
        state = "Falling Market"

    return price, last_ma5, state


class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        timer = QTimer(self)
        timer.start(100)
        timer.timeout.connect(self.timeout)

    def timeout(self):
        for i, ticker in enumerate(tickers):
            item = QTableWidgetItem(ticker)
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget.setItem(i, 0, item)
            price, last_ma5, state = get_market_infos(ticker)
            s = locale.format_string('%.3f', price, 1)
            self.tableWidget.setItem(i, 1, QTableWidgetItem(s))
            s = locale.format_string('%.3f', last_ma5, 1)
            self.tableWidget.setItem(i, 2, QTableWidgetItem(s))
            # self.tableWidget.setItem(i, 2, QTableWidgetItem(str(last_ma5)))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(state))


app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()
