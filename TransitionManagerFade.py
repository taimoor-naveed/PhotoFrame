from PyQt5.QtGui import QPixmap, QBrush, QColor, QTransform
from PyQt5.QtCore import Qt, pyqtSignal, QRectF, QTimeLine, QRect

from TransitionManager import TransitionManager

class TransitionManagerFade(TransitionManager):
    def __init__(self, pixmapItem1, pixmapItem2):
        super().__init__(pixmapItem1, pixmapItem2)
        
    def animationProgressed(self, value):
        self.pixmapItem2.setOpacity(value)
        self.pixmapItem1.setOpacity(1 - value)

    def animationFinished(self):
        self.pixmapItem1.setPixmap(self.pixmapItem2.pixmap())
        self.pixmapItem1.setOpacity(1)

    def displayImage(self, fileName, trigger, direction=None):
        if fileName:
            pixmap = QPixmap(fileName)
            
            pixmap = pixmap.copy(QRect((pixmap.width() - 1024) / 2, (pixmap.height() - 600) / 2, 1024, 600))
            
            self.pixmapItem2.setOpacity(0)
            self.pixmapItem2.setPixmap(pixmap)

            if trigger:
                self.timeLine.setDuration(500)
            else:
                self.timeLine.setDuration(2000)

            self.timeLine.start()
