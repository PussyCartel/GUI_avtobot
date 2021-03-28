from PyQt5 import QtWidgets, uic, QtGui, QtCore
import sys
import cv2
from PyQt5.QtWidgets import QApplication


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('ui/untitled.ui', self)

        self.button = self.findChild(QtWidgets.QPushButton, 'pushButton')
        self.button.clicked.connect(self.continue1)

        self.button1 = self.findChild(QtWidgets.QPushButton, 'pushButton_2')
        self.button1.clicked.connect(self.continue3)

        self.button2 = self.findChild(QtWidgets.QPushButton, 'pushButton_4')
        self.button2.clicked.connect(self.continue2)

        self.show()

    def continue1(self):
        self.close()
        self.next=Rule()


    def continue2(self):
        self.close()
        self.next=Second()

    def continue3(self):
        self.close()
        self.next = Settings()


class Settings(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/settings.ui', self)
        self.show()

    def keyPressEvent(self, e):
        if e.key() in [QtCore.Qt.Key_Escape]:
            self.close()
            self.next = Ui()


class Second(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('ui/names.ui', self)

        self.show()

    def keyPressEvent(self, e):
        if e.key() in [QtCore.Qt.Key_Escape]:
            self.close()
            self.next = Ui()


class FrameGrabber(QtCore.QThread):
    def __init__(self, parent=None):
        super(FrameGrabber, self).__init__(parent)

    signal = QtCore.pyqtSignal(QtGui.QImage)

    def run(self):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 420)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 880)
        while cap.isOpened():
            success, frame = cap.read()
            if success:
                image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_BGR888)
                self.signal.emit(image)


class Rule(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/rule.ui', self)

        self.button = self.findChild(QtWidgets.QPushButton, 'pushButton_3')
        self.button.clicked.connect(self.wasd)

        self.MainWindow = self.findChild(QtWidgets.QMainWindow, 'MainWindow')
        self.webCamDisplay = self.findChild(QtWidgets.QLabel, 'label')
        self.webCamDisplay.setFrameShape(QtWidgets.QFrame.Box)
        self.grabber = FrameGrabber()
        self.grabber.signal.connect(self.updateFrame)
        self.grabber.start()
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)
        self.show()

    def wasd(self):
        self.close()
        self.next = Awsd()

    @QtCore.pyqtSlot(QtGui.QImage)
    def updateFrame(self, image):
        self.webCamDisplay.setPixmap(QtGui.QPixmap.fromImage(image))

    def keyPressEvent(self, e):
        print(e.key())
        if e.key() in [QtCore.Qt.Key_Escape]:
            self.close()
            self.next = Ui()
        if e.key() in [65, 68]:
            print(e.key())


class Awsd(QtWidgets.QMainWindow):
    def __init__(self):
        super(Awsd, self).__init__()
        uic.loadUi('ui/wasd.ui', self)
        self.show()

    def keyPressEvent(self, e):
        if e.key() in [QtCore.Qt.Key_Escape]:
            self.close()
            self.next = Ui()


app = QApplication(sys.argv)
window = Ui()
sys.exit(app.exec_())
