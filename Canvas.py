from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGridLayout
from PyQt5.QtGui import QPixmap, QBrush, QColor
from PyQt5.QtCore import Qt, pyqtSignal, QRectF, QTimeLine
from TransitionManager import TransitionManager
import math


def distance(p1, p2):
    return math.sqrt(math.pow(p2[1] - p1[1], 2) + math.pow(p2[0] - p1[0], 2))


class Canvas(QGraphicsView):

    mouseClickedLeft = pyqtSignal()
    mouseClickedRight = pyqtSignal()
    mouseClickedCenter = pyqtSignal()

    def __init__(self, settingsWidget):
        super().__init__()

        self.settingsWidget = settingsWidget

        self.setObjectName("CentralWidget");
        self.setStyleSheet('QGraphicsView#CentralWidget { border: 0px}')

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setBackgroundBrush(QBrush(QColor(0, 0, 0)))

        self.pixmapItem1 = QGraphicsPixmapItem()
        self.pixmapItem2 = QGraphicsPixmapItem()

        self.scene = QGraphicsScene()
        self.scene.addItem(self.pixmapItem1)
        self.scene.addItem(self.pixmapItem2)
        self.setScene(self.scene)

        self.transitionManager = TransitionManager(self.pixmapItem1, self.pixmapItem2)

        self.mousePressLocation = None

        layout = QGridLayout()
        layout.addWidget(self.settingsWidget, 0, 0)

        self.setLayout(layout)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and not self.settingsWidget.isVisible() and self.transitionManager.timeLine.state() != QTimeLine.Running:
            currentMouseLocation = (event.x(), event.y())

            if distance(self.mousePressLocation, currentMouseLocation) < 5:
                if event.x() < self.width() * 1 / 3:
                    self.mouseClickedLeft.emit()
                elif event.x() > self.width() * 2 / 3:
                    self.mouseClickedRight.emit()
                else:
                    self.mouseClickedCenter.emit()

        super().mouseReleaseEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not self.settingsWidget.isVisible():
            self.mousePressLocation = (event.x(), event.y())
            super().mousePressEvent(event)

    def displayImage(self, fileName, trigger):
        self.setSceneRect(QRectF(0, 0, self.width(), self.height()))
        self.transitionManager.displayImage(fileName, trigger)

