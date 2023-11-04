'''
wormvolution_layouts.py

Author: Elijah Theander
Project: Wormvolution Python Edition

Date Created: November 2, 2023

'''
#Python STL
import sys
import os


#Third Party Packages

from PyQt5.QtCore import(
    Qt,
    QSize,
    QRect,
    pyqtSignal
)

from PyQt5.QtGui import(
    QIcon,
    QFont,
    QPixmap,
    QColor,
    QImage
)

from PyQt5.QtWidgets import(
    QWidget,
    QLabel,
    QApplication,
    QMainWindow
)


class BoardLayout(QLabel):

    def __init__(self,parent, boardSize):
        super(BoardLayout,self).__init__(parent)

        self.setMinimumSize(QSize(80,80))

        self.setText('Hello')

        self.pixelSize = int(900/boardSize)

        self.boardSize = boardSize

        side = self.pixelSize * self.boardSize

        self.canvas = QImage(side,side,QImage.Format_ARGB32)



        self.canvas.fill(Qt.black)
        self.paint_image()


    def get_preferred_size(self):
        size = self.canvas.size()

        height = size.height()
        width = size.width() 
        return [height,width]
    
    def fill_canvas(self, color):

        self.canvas.fill(color)

    def draw_point(self,point,color):
        x = point[0]
        y = point[1]

        for i in range((x*self.pixelSize),(self.pixelSize * (x+1))):

            for j in range((y* self.pixelSize), (self.pixelSize * (y +1))):
                self.canvas.setPixelColor(i,j,color)

        self.paint_image()

    def erase_point(self, point):

        self.draw(point, Qt.black)

    def paint_image(self):
        self.setPixmap(QPixmap.fromImage(self.canvas))
                                           

def main():
    app = QApplication(sys.argv)

    window = QMainWindow()

    window.setMinimumSize(1920,1080)

    central_widget = QWidget()

    window.setCentralWidget(central_widget)

    board = BoardLayout(central_widget,100)

    board.move(100,100)

    board.draw_point([10,10], Qt.red)

    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()