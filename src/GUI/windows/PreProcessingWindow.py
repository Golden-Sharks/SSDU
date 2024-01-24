import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as guy
import src.GUI.windows.style as st

class PreProcessingWindow(qtw.QWidget):
    __mainWindow = 0
    __isHidden = False

    def __init__(self, mainWindow):
        super().__init__()
        self.__dico = {"preprocessing": False, "resize": (800, 450), "grayscale": False}
        self.__mainWindow = mainWindow
        self.setWindowFlags(qtc.Qt.FramelessWindowHint)
        self.__getRightLocation()
        self.setFixedHeight(50)
        self.setFixedWidth(300)
        self.setLayout(self.__getLayout())
        self.setPalette(st.getPalette())
        self.setStyleSheet(st.full_stylesheet())

    def __getLayout(self):
        mainLayout = qtw.QVBoxLayout()
        self.__frame = qtw.QFrame()
        self.__frame.setPalette(st.getPalette())
        self.__frame.setMinimumWidth(300)
        otherLayout = qtw.QVBoxLayout()
        self.__preprocessing = qtw.QCheckBox('Use preprocessing')
        self.__preprocessing.stateChanged.connect(self.__hideAndSeek)
        mainLayout.addWidget(self.__preprocessing)
        self.__grayscale = qtw.QCheckBox('image in black & white')
        otherLayout.addWidget(self.__grayscale)
        resizeLayout = qtw.QHBoxLayout()
        self.__resizeW = qtw.QLineEdit(self)
        self.__resizeW.setPlaceholderText("new width")
        self.__resizeW.setToolTip("Resize the image with this new width")
        self.__resizeH = qtw.QLineEdit(self)
        self.__resizeH.setPlaceholderText("new height")
        self.__resizeH.setToolTip("Resize the image with this new height")
        resizeLayout.addWidget(self.__resizeW)
        resizeLayout.addWidget(self.__resizeH)
        otherLayout.addLayout(resizeLayout)
        self.__getRightSubLocation()
        self.__frame.setLayout(otherLayout)
        self.__frame.setStyleSheet(st.full_stylesheet())
        return mainLayout

    def __hideAndSeek(self):
        self.__frame.setVisible(self.__preprocessing.isChecked())

    def __getRightLocation(self):
        ag = qtw.QDesktopWidget().availableGeometry()
        widget = self.geometry()
        x = ag.width() // 2 - widget.width() // 2 + 230
        y = 75
        self.move(x, y)
        return

    def __getRightSubLocation(self):
        self.__frame.setWindowFlags(qtc.Qt.FramelessWindowHint)
        self.__frame.setMaximumWidth(300)
        x = self.geometry().left()
        y = 125
        self.__frame.move(x, y)
        return

    def keyPressEvent(self, a0: guy.QKeyEvent):
        if a0.key() == qtc.Qt.Key_Escape:
            self.__mainWindow.closeAllWindows()
        return

    def __fillInDico(self):
        if self.__preprocessing.isChecked():
            self.__dico["grayscale"] = self.__grayscale.isChecked()
            width = int(self.__resizeW.text()) if self.__resizeW.text() != "" else 21
            height = int(self.__resizeH.text()) if self.__resizeH.text() != "" else 21
            self.__dico["resize"] = (width, height)

    def gatherDatas(self):
        self.__fillInDico()
        dico = {"preprocessing": self.__dico}
        return dico

    def hide(self):
        self.__frame.hide()
        super().hide()
        return

    def close(self):
        self.__frame.close()
        super().close()
        return
