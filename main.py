import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from MainWindow import MainWindow

DEFAULT_SLIDE_SHOW_TIMEOUT = 5000

FULLSCREEN = True

PATH = r'/home/pi/PhotoFrame'
# PATH = r'/Users/taimoor/photo_frame/PhotoFrame'


if __name__ == '__main__':
    app = QApplication(sys.argv)
    if FULLSCREEN:
        QApplication.setOverrideCursor(Qt.BlankCursor)
    mainWindow = MainWindow(PATH, DEFAULT_SLIDE_SHOW_TIMEOUT, FULLSCREEN)
    mainWindow.show()
    sys.exit(app.exec_())