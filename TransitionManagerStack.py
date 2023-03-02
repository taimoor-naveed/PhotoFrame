from PyQt5.QtGui import QPixmap, QBrush, QColor, QTransform
from PyQt5.QtCore import Qt, pyqtSignal, QRectF, QTimeLine, QRect

from TransitionManager import TransitionManager

class TransitionManagerStack(TransitionManager):
    def __init__(self, pixmapItem1, pixmapItem2):
        super().__init__(pixmapItem1, pixmapItem2)

        self.width = 1024
        self.direction = None        

    def animationProgressed(self, value):
        if self.direction == 1:
            self.pixmapItem2.setOffset(-self.width + self.width * value, 0)
        else:
            self.pixmapItem1.setOffset(-(self.width * value), 0)

    def bringPixmap1ToFront(self):
        self.pixmapItem1.setZValue(2)
        self.pixmapItem2.setZValue(1) 

    def bringPixmap2ToFront(self):
        self.pixmapItem1.setZValue(1)
        self.pixmapItem2.setZValue(2)

    def animationFinished(self):
        self.pixmapItem1.setPixmap(self.pixmapItem2.pixmap())
        self.bringPixmap1ToFront()

    def displayImage(self, fileName, trigger, direction):
        if fileName:
            pixmap = QPixmap(fileName)
            pixmap = pixmap.copy(QRect((pixmap.width() - 1024) / 2, (pixmap.height() - 600) / 2, 1024, 600))
            
            self.direction = direction

            if self.direction == 1:           
                self.pixmapItem1.setOffset(0, 0)
                self.pixmapItem2.setOffset(-self.width, 0)
                self.bringPixmap2ToFront()   
            else:
                self.pixmapItem2.setOffset(0, 0)    
                self.bringPixmap1ToFront()

            self.pixmapItem2.setPixmap(pixmap)

            self.timeLine.setDuration(500)

            self.timeLine.start()
