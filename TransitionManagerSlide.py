from PyQt5.QtGui import QPixmap, QBrush, QColor, QTransform
from PyQt5.QtCore import Qt, pyqtSignal, QRectF, QTimeLine, QRect

from TransitionManager import TransitionManager

class TransitionManagerSlide(TransitionManager):
    def __init__(self, pixmapItem1, pixmapItem2):
        super().__init__(pixmapItem1, pixmapItem2)

        self.width = 1024
        self.direction = None

    def animationProgressed(self, value):
        if self.direction == 1:
            self.pixmapItem2.setOffset(-self.width + self.width * value, 0)
            self.pixmapItem1.setOffset(self.width * value, 0)
        else:
            self.pixmapItem2.setOffset(self.width - self.width * value, 0)
            self.pixmapItem1.setOffset(-(self.width * value), 0)
            pass

    def animationFinished(self):
        self.pixmapItem1.setPixmap(self.pixmapItem2.pixmap())
        self.pixmapItem1.setOffset(0, 0)

    def displayImage(self, fileName, trigger, direction):
        if fileName:
            pixmap = QPixmap(fileName)
            pixmap = pixmap.copy(QRect((pixmap.width() - 1024) / 2, (pixmap.height() - 600) / 2, 1024, 600))
            
            self.direction = direction

            if self.direction == 1:               
                self.pixmapItem2.setOffset(-self.width, 0)    
            else:
                self.pixmapItem2.setOffset(self.width, 0)    

            self.pixmapItem2.setPixmap(pixmap)
            
            self.timeLine.setDuration(500)

            self.timeLine.start()
