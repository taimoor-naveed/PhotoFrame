from PyQt5.QtGui import QPixmap, QBrush, QColor, QTransform
from PyQt5.QtCore import Qt, pyqtSignal, QRectF, QTimeLine, QRect
    
class TransitionManager:
    def __init__(self, pixmapItem1, pixmapItem2):
        self.pixmapItem1 = pixmapItem1
        self.pixmapItem2 = pixmapItem2
        self.timeLine = QTimeLine()
        self.timeLine.valueChanged.connect(self.animationProgressed)
        self.timeLine.finished.connect(self.animationFinished)
        self.timeLine.setUpdateInterval(1000 / 60)
        self.timeLine.setCurveShape(QTimeLine.LinearCurve)

    def animationProgressed(self, value):
        raise NotImplementedError("Subclass must implement this method")

    def animationFinished(self):
        raise NotImplementedError("Subclass must implement this method")

    def displayImage(self, fileName, trigger, direction):
        raise NotImplementedError("Subclass must implement this method")
