import os

from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPixmap, QLinearGradient, QColor, QBrush
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QWidget, QApplication, QFileDialog, QHBoxLayout

from svgButton import SvgButton


class ImageView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.__aspectRatioMode = Qt.KeepAspectRatio
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.__scene = QGraphicsScene()
        self.__p = QPixmap()
        self.__item = ''
        self.setScene(self.__scene)

        self.__factor = 1.1  # Zoom factor

    def __initUi(self):
        self.__setControlWidget()

        # set mouse event
        # to make buttons appear and apply gradient
        # above the top of an image when you hover the mouse cursor over it
        self.setMouseTracking(True)
        self.__defaultBrush = self.foregroundBrush()
        gradient = QLinearGradient(QPointF(0, 0), QPointF(0, self.viewport().height()))
        gradient.setColorAt(0, QColor(0, 0, 0, 150))
        gradient.setColorAt(1, QColor(0, 0, 0, 0))
        self.__brush = QBrush(gradient)

        self.__controlWidget.setEnabled(False)

        self.setMinimumSize(150, 150)

    def __setControlWidget(self):
        # copy the image
        copyBtn = SvgButton()
        copyBtn.setIcon('ico/copy_light.svg')
        copyBtn.clicked.connect(self.__copy)

        # download the image
        saveBtn = SvgButton()
        saveBtn.setIcon('ico/save_light.svg')
        saveBtn.clicked.connect(self.__save)

        # zoom in
        zoomInBtn = SvgButton()
        zoomInBtn.setIcon('ico/add_light.svg')
        zoomInBtn.clicked.connect(self.__zoomIn)

        # zoom out
        zoomOutBtn = SvgButton()
        zoomOutBtn.setIcon('ico/delete_light.svg')
        zoomOutBtn.clicked.connect(self.__zoomOut)

        lay = QHBoxLayout()
        lay.addWidget(copyBtn)
        lay.addWidget(saveBtn)
        lay.addWidget(zoomInBtn)
        lay.addWidget(zoomOutBtn)

        self.__controlWidget = QWidget(self)
        self.__controlWidget.setLayout(lay)

        self.__controlWidget.hide()

    def __copy(self):
        QApplication.clipboard().setPixmap(self.__p)

    def __save(self):
        filename = QFileDialog.getSaveFileName(self, 'Save', os.path.expanduser('~'), 'Image file (*.png)')
        if filename[0]:
            filename = filename[0]
            self.__p.save(filename)

    def __zoomIn(self):
        self.scale(self.__factor, self.__factor)

    def __zoomOut(self):
        self.scale(1 / self.__factor, 1 / self.__factor)

    def setFilename(self, filename: str):
        # Clear the scene before adding a new image
        if self.__item:
            self.__scene.removeItem(self.__item)
        self.__scene.clear()

        self.__p = QPixmap(filename)
        self.__scene.setSceneRect(0, 0, self.__p.width(), self.__p.height())
        self.__item = self.__scene.addPixmap(self.__p)
        self.__item.setTransformationMode(Qt.SmoothTransformation)

        self.fitInView(self.__item, self.__aspectRatioMode)
        self.__controlWidget.setEnabled(True)

    def setAspectRatioMode(self, mode):
        self.__aspectRatioMode = mode

    def resizeEvent(self, e):
        if self.__item:
            self.fitInView(self.sceneRect(), self.__aspectRatioMode)
        return super().resizeEvent(e)

    def enterEvent(self, e):
        # Show the button when the mouse enters the view
        if self.__item:
            self.__controlWidget.move(self.rect().x(), self.rect().y())
            self.setForegroundBrush(self.__brush)
            self.__controlWidget.show()
        return super().enterEvent(e)

    def leaveEvent(self, e):
        # Hide the button when the mouse leaves the view
        self.__controlWidget.hide()
        self.setForegroundBrush(self.__defaultBrush)
        return super().leaveEvent(e)

    def wheelEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            # Check if Ctrl key is pressed
            if event.angleDelta().y() > 0:
                # Ctrl + wheel up, zoom in
                self.__zoomIn()
            else:
                # Ctrl + wheel down, zoom out
                self.__zoomOut()
            event.accept()  # Accept the event if Ctrl is pressed
        else:
            super().wheelEvent(event)  # Default behavior for other cases