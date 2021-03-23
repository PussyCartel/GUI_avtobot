from PyQt5 import QtWidgets, uic
import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QPushButton


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('untitled.ui', self)

        self.button = self.findChild(QtWidgets.QPushButton, 'pushButton')  # Find the button
        self.button.clicked.connect(self.continue2)

        self.show()

    def continue2(self):
        self.close()
        self.next=Second()



class Second(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('untitled.ui', self)
        self.show()



app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
