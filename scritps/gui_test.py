import pickle
import socket
import struct
import sys
import numpy as np
import cv2

main_route = '/home/kali/PycharmProjects/pythonProject/'

import face_recognition
import tensorflow as tf
config = tf.compat.v1.ConfigProto()
sess = tf.compat.v1.Session(config=config)

pasha = face_recognition.load_image_file(main_route+'img/pasha.jpg')
pasha_encod = face_recognition.face_encodings(pasha)[0]

vadim = face_recognition.load_image_file(main_route+'img/vadim.jpg')
vadim_encod = face_recognition.face_encodings(vadim)[0]

vitya = face_recognition.load_image_file(main_route+'img/vitya1.jpg')
vitya_encod = face_recognition.face_encodings(vitya)[0]

serg = face_recognition.load_image_file(main_route+'img/serg.jpg')
serg_encode = face_recognition.face_encodings(serg)[0]

alina = face_recognition.load_image_file(main_route + 'img/alina.jpg')
alina_encod = face_recognition.face_encodings(alina)[0]

known_face_encodings = [
    vitya_encod,
    pasha_encod,
    serg_encode,
    vadim_encod,
    alina_encod,
]
known_face_names = [
    'Vitya',
    'Pasha',
    'Sergey',
    'Vadim',
    'Alina',
]

from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QApplication

AI_mod = False
Control_state = False
Face_list = [False, False, False, False, False, False]
ButtonState = ['0', '0', '0', '0', '0', '0', '0', '0']

server_socket = socket.socket()
server_socket.bind(('', 8485))
server_socket.listen(10)

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi(main_route+'ui/untitled.ui', self)

        self.button = self.findChild(QtWidgets.QPushButton, 'pushButton')
        self.button.clicked.connect(self.continue1)

        self.button1 = self.findChild(QtWidgets.QPushButton, 'pushButton_2')
        self.button1.clicked.connect(self.continue3)

        self.button2 = self.findChild(QtWidgets.QPushButton, 'pushButton_4')
        self.button2.clicked.connect(self.continue2)

        self.show()

    def continue1(self):
        self.close()
        self.next = Rule()

    def continue2(self):
        self.close()
        self.next = Second()

    def continue3(self):
        self.close()
        self.next = Settings()


class Settings(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(main_route+'ui/settings.ui', self)
        self.show()

    def keyPressEvent(self, e):
        if e.key() in [QtCore.Qt.Key_Escape]:
            self.close()
            self.next = Ui()


class Second(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi(main_route+'ui/names.ui', self)

        self.show()

    def keyPressEvent(self, e):
        if e.key() in [QtCore.Qt.Key_Escape]:
            self.close()
            self.next = Ui()


class FrameGrabber(QtCore.QThread):
    def __init__(self, parent=None):
        super(FrameGrabber, self).__init__(parent)

    signal = QtCore.pyqtSignal(QtGui.QImage)
    signal2 = QtCore.pyqtSignal(list)

    def run(self):
        global server_socket
        print("Listening")
        conn, addr = server_socket.accept()
        data = b""
        payload_size = struct.calcsize(">L")
        print("payload_size: {}".format(payload_size))
        face_locations = []
        face_names = []
        process_this_frame = True
        with sess:
            while True:
                data += conn.recv(4096)

                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack(">L", packed_msg_size)[0]
                if msg_size > 100000:
                    data = b''
                    continue
                while len(data) < msg_size:
                    data += conn.recv(4096)
                frame_data = data[:msg_size]
                frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
                frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

                if AI_mod:
                    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                    rgb_small_frame = small_frame[:, :, ::-1]


                    if process_this_frame:
                        # Find all the faces and face encodings in the current frame of video
                        face_locations = face_recognition.face_locations(rgb_small_frame)
                        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                        if not face_encodings:
                            self.signal2.emit([False])
                        face_names = []
                        for face_encoding in face_encodings:
                            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                            name = "Unknown"
                            # Or instead, use the known face with the smallest distance to the new face
                            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                            best_match_index = np.argmin(face_distances)
                            if matches[best_match_index]:
                                name = known_face_names[best_match_index]
                                self.signal2.emit([True])

                            face_names.append(name)


                    process_this_frame = not process_this_frame

                    # Display the results
                    for (top, right, bottom, left), name in zip(face_locations, face_names):
                        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                        top *= 4
                        right *= 4
                        bottom *= 4
                        left *= 4

                        # Draw a box around the face
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                        # Draw a label with a name below the face
                        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                        font = cv2.FONT_HERSHEY_DUPLEX
                        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
                self.signal.emit(image)
                data = b""


class Rule(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(main_route+'ui/rule.ui', self)

        self.button = self.findChild(QtWidgets.QPushButton, 'pushButton_3')
        self.button.clicked.connect(self.wasd)

        self.buttonAI = self.findChild(QtWidgets.QPushButton, 'pushButton_2')
        self.buttonAI.clicked.connect(self.ai_control)

        self.button_control = self.findChild(QtWidgets.QPushButton, 'pushButton_4')
        self.button_control.clicked.connect(self.control)

        self.check_box_control = self.findChild(QtWidgets.QCheckBox, 'checkBox_8')

        self.MainWindow = self.findChild(QtWidgets.QMainWindow, 'MainWindow')
        self.webCamDisplay = self.findChild(QtWidgets.QLabel, 'label')
        self.webCamDisplay.setFrameShape(QtWidgets.QFrame.Box)

        self.grabber = FrameGrabber()
        self.grabber.signal.connect(self.updateFrame)
        self.grabber.signal2.connect(self.updateBox)
        self.grabber.start()

        self.TFGH = [70, 71, 72, 84]

        self.check = self.findChild(QtWidgets.QCheckBox, 'checkBox_2')

        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)
        self.show()

    def ai_control(self):
        global AI_mod
        AI_mod = not AI_mod

    def control(self):
        global Control_state
        self.check_box_control.setChecked(not Control_state)
        Control_state = not Control_state

    def wasd(self):
        self.close()
        self.next = Awsd()

    @QtCore.pyqtSlot(QtGui.QImage)
    def updateFrame(self, image):
        self.webCamDisplay.setPixmap(QtGui.QPixmap.fromImage(image).scaledToWidth(700))

    @QtCore.pyqtSlot(list)
    def updateBox(self, state):
        if True in state:
            print('est true')
        else:
            print(state)

    def keyPressEvent(self, e):
        global Control_state
        global ButtonState
        if e.key() in [QtCore.Qt.Key_Escape]:
            self.close()
            self.next = Ui()
        if Control_state:
            if e.key() in self.TFGH:
                ButtonState[self.TFGH.index(e.key())] = '1'
                self.send_key(key=e.key())

    def keyReleaseEvent(self, e):
        global Control_state
        global ButtonState
        if Control_state:
            if e.key() in self.TFGH:
                ButtonState[self.TFGH.index(e.key())] = '0'

    def send_key(self, key):
        global ButtonState
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('192.168.43.205', 8585))
        client_socket.sendall(''.join(ButtonState).encode())


class Awsd(QtWidgets.QMainWindow):
    def __init__(self):
        super(Awsd, self).__init__()
        uic.loadUi(main_route+'ui/wasd.ui', self)
        self.show()

    def keyPressEvent(self, e):
        if e.key() in [QtCore.Qt.Key_Escape]:
            self.close()
            self.next = Ui()


app = QApplication(sys.argv)
window = Ui()
sys.exit(app.exec_())
