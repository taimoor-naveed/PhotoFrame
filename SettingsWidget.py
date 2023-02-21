from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QLabel, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap, QFont, QBrush, QColor
from PyQt5.QtCore import Qt, QTimer

class SettingsWidget(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.slideShowTimeout = None

        self.setBackgroundBrush(QBrush(QColor(128, 128, 128)))

        self.okButton = QPushButton('Ok')
        self.cancelButton = QPushButton('Cancel')

        self.buttonLeft = QPushButton('<')
        self.buttonLeft.clicked.connect(self.leftButtonClicked)

        self.timeOutLabel = QLabel()
        self.timeOutLabel.setStyleSheet('border-radius: 25px;border: 1px solid black;')
        self.timeOutLabel.setAlignment(Qt.AlignCenter)

        self.buttonRight = QPushButton('>')
        self.buttonRight.clicked.connect(self.rightButtonClicked)


        hLayout1 = QHBoxLayout()
        hLayout1.addWidget(self.buttonLeft)
        hLayout1.addWidget(self.timeOutLabel)
        hLayout1.addWidget(self.buttonRight)


        hLayout2 = QHBoxLayout()
        hLayout2.addWidget(self.okButton)
        hLayout2.addWidget(self.cancelButton)

        layout = QVBoxLayout()
        layout.addLayout(hLayout1)
        layout.addLayout(hLayout2)

        self.setLayout(layout)

        self.hide()

    def updateTimeOutLabel(self):
        self.timeOutLabel.setText(str(int(self.slideShowTimeout / 1000)))

    def rightButtonClicked(self):
        if self.slideShowTimeout < 99000:
            self.slideShowTimeout = self.slideShowTimeout + 1000
            self.updateTimeOutLabel()

    def leftButtonClicked(self):
        if self.slideShowTimeout > 5000:
            self.slideShowTimeout = self.slideShowTimeout - 1000
            self.updateTimeOutLabel()

    def show(self):
        font = self.timeOutLabel.font()
        font.setWeight(QFont.Bold)

        font.setPixelSize(60)
        self.timeOutLabel.setFont(font)

        font.setPixelSize(80)
        self.buttonRight.setFont(font)
        self.buttonLeft.setFont(font)

        font.setPixelSize(35)
        self.okButton.setFont(font)
        self.cancelButton.setFont(font)

        self.updateTimeOutLabel()

        self.buttonLeft.setFixedHeight(self.height() / 2)
        self.timeOutLabel.setFixedHeight(self.height() / 2)
        self.buttonRight.setFixedHeight(self.height() / 2)

        self.okButton.setFixedHeight(self.height() / 4)
        self.cancelButton.setFixedHeight(self.height() / 4)

        super().show()

