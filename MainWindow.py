import os
import pickle
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from SettingsWidget import SettingsWidget
from FileManager import FileManager
from Canvas import Canvas

settingsFile = 'settings.pkl'

class MainWindow(QMainWindow):
    def __init__(self, PATH, DEFAULT_SLIDE_SHOW_TIMEOUT, FULLSCREEN):
        super().__init__()

        if os.path.exists(settingsFile):
            with open(settingsFile, 'rb') as f:
                DEFAULT_SLIDE_SHOW_TIMEOUT = pickle.load(f)

        self.first = 1
        self.slideShowTimerTimeOut = DEFAULT_SLIDE_SHOW_TIMEOUT

        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)

        if FULLSCREEN:
            self.showFullScreen()
        else:
            self.setFixedSize(1024, 600)

        self.settingsWidget = SettingsWidget()
        self.settingsWidget.okButton.clicked.connect(self.slideShowTimerTimeOutUpdated)
        self.settingsWidget.cancelButton.clicked.connect(self.hideSettingsWidget)

        self.canvas = Canvas(self.settingsWidget)
        self.canvas.mouseClickedRight.connect(self.nextPhotoClicked)
        self.canvas.mouseClickedLeft.connect(self.previousPhotoClicked)
        self.canvas.mouseClickedCenter.connect(self.showSettingsWidget)

        self.setCentralWidget(self.canvas)

        self.fileManager = FileManager(PATH)

        self.slideShowTimer = QTimer()
        self.slideShowTimer.timeout.connect(self.slideShowTimerTimedOut)
        self.slideShowTimer.start(1000)

    def slideShowTimerTimeOutUpdated(self):
        self.slideShowTimerTimeOut = self.settingsWidget.slideShowTimeout

        with open(settingsFile, 'wb') as f:
            pickle.dump(self.slideShowTimerTimeOut, f)

        self.hideSettingsWidget()

    def showSettingsWidget(self):

        self.slideShowTimer.stop()
        self.settingsWidget.setFixedSize(self.width() / 3, self.height() / 3)
        self.settingsWidget.slideShowTimeout = self.slideShowTimerTimeOut
        self.settingsWidget.show()

    def hideSettingsWidget(self):
        self.slideShowTimer.start(self.slideShowTimerTimeOut)
        self.settingsWidget.hide()

    def slideShowTimerTimedOut(self):
        if self.first:
            fileName = self.fileManager.getFirstFile()
            self.first = 0
            self.slideShowTimer.start(self.slideShowTimerTimeOut)
        else:
            fileName = self.fileManager.getNextFile()

        self.canvas.displayImage(fileName, 0)

    def nextPhotoClicked(self):
        fileName = self.fileManager.getNextFile()
        self.canvas.displayImage(fileName, 1)
        self.slideShowTimer.start(self.slideShowTimerTimeOut)

    def previousPhotoClicked(self):
        fileName = self.fileManager.getPreviousFile()
        self.canvas.displayImage(fileName, 1)
        self.slideShowTimer.start(self.slideShowTimerTimeOut)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            if self.fileManager.fileEventQueue.qsize():
                buttonReply = QMessageBox.question(self, 'Warning', "New added photos are still being processed. Do you want to exit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if buttonReply == QMessageBox.Yes:
                    self.fileManager.stop()
                    QApplication.quit()
            else:

                self.fileManager.stop()
                QApplication.quit()
