import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as guy
import numpy as np
from mss import mss
from PIL import Image
from pynput import mouse
import src.GUI.windows.style as st


class ResizeWindow(qtw.QWidget):
    __isHidden = False

    def __init__(self, mainWindow):
        super().__init__()
        self.__frameGO = qtw.QFrame()
        self.__forGameOver = False
        self.__dicoNormal = {"top": 0, "left": 0, "width": 1920, "height": 1080, "mon": 1}
        self.__dicoGO = {"top": 0, "left": 0, "width": 1920, "height": 1080, "mon": 1}
        self.__mss = mss()
        self.__label = qtw.QLabel(self)
        self.__mainWindow = mainWindow
        self.setWindowFlags(qtc.Qt.FramelessWindowHint)
        self.__getRightLocation()
        self.setLayout(self.__getContent())
        self.__setGoWindow()
        self.setFixedHeight(310)
        self.setFixedWidth(300)
        self.setPalette(st.getPalette())
        self.setStyleSheet(st.full_stylesheet())
        self.__listener = mouse.Listener(on_move=self.__on_move)
        return

    def __on_move(self, x, y):
        text = "Mouse coordinates ; X:" + str(x) + ", Y:" + str(y)
        self.__mouseCoord.setText(text)
        return

    def __setGoWindow(self):
        x = self.geometry().left()
        y = 375
        self.__frameGO.setPalette(st.getPalette())
        self.__frameGO.setFixedWidth(300)
        self.__frameGO.setWindowFlags(qtc.Qt.FramelessWindowHint)
        self.__frameGO.move(x, y)
        self.__frameGO.setStyleSheet(st.full_stylesheet())

        mainLayout = qtw.QVBoxLayout()
        self.__mouseCoord = qtw.QLabel()
        mainLayout.addWidget(self.__mouseCoord)
        coordonnees = qtw.QHBoxLayout()
        self.__X = qtw.QLineEdit(self)
        self.__X.setPlaceholderText("replay btn : X")
        coordonnees.addWidget(self.__X)
        self.__Y = qtw.QLineEdit(self)
        self.__Y.setPlaceholderText("replay btn : Y")
        coordonnees.addWidget(self.__Y)
        mainLayout.addLayout(coordonnees)
        self.__Go_text = qtw.QLineEdit(self)
        self.__Go_text.setPlaceholderText("Game Over text")
        mainLayout.addWidget(self.__Go_text)
        self.__frameGO.setLayout(mainLayout)
        self.__frameGO.hide()
        return

    def __getRightLocation(self):
        """
        Place la fenêtre au bon endroit sur l'écran
        """
        ag = qtw.QDesktopWidget().availableGeometry()
        widget = self.geometry()
        x = ag.width() // 2 - widget.width() // 2 + 60
        y = 75
        self.move(x, y)
        return

    def __getContent(self):
        """
        Rempli la fenêtre avec son contenu
        """
        mainLayout = qtw.QVBoxLayout()

        self.__stateOfWindow = qtw.QComboBox()
        self.__stateOfWindow.addItems(["Play Window", "GameOver Window"])
        mainLayout.addWidget(self.__stateOfWindow)
        self.__stateOfWindow.currentTextChanged.connect(lambda: self.__switchPurpose())

        self.__mon = qtw.QLineEdit(self)
        self.__mon.setPlaceholderText("monitor")
        self.__mon.setToolTip("Numero of the monitor (starting at 1)")
        self.__mon.setMaximumWidth(50)
        mainLayout.addWidget(self.__mon)

        layout = qtw.QHBoxLayout()
        self.__top = qtw.QLineEdit(self)
        self.__top.setPlaceholderText("top coordinate")
        self.__top.setToolTip("Top Coordinate (0 is the higher)")
        layout.addWidget(self.__top)
        self.__width = qtw.QLineEdit(self)
        self.__width.setPlaceholderText("width of screen")
        self.__width.setToolTip("Width of the screenshot (in pixel)")
        layout.addWidget(self.__width)
        mainLayout.addLayout(layout)

        layout2 = qtw.QHBoxLayout()
        self.__left = qtw.QLineEdit(self)
        self.__left.setPlaceholderText("left coordinate")
        self.__left.setToolTip("Left Coordinate (0 is the left edge of yout screen)")
        layout2.addWidget(self.__left)
        self.__height = qtw.QLineEdit(self)
        self.__height.setPlaceholderText("height of screen")
        self.__height.setToolTip("Height of the screenshot (in pixel)")
        layout2.addWidget(self.__height)
        mainLayout.addLayout(layout2)

        self.__takeScreenshot(True)

        pixmap = guy.QPixmap('icons/screenshot.jpeg')
        ratio = pixmap.width() / pixmap.height()
        self.__label.setFixedWidth(275)
        self.__label.setMaximumHeight(275 / ratio)

        self.__label.setPixmap(pixmap)
        self.__label.setScaledContents(True)
        mainLayout.addWidget(self.__label)

        vbox = qtw.QVBoxLayout()
        btnValidate = qtw.QPushButton("Validate")
        btnValidate.setMinimumSize(100, 25)
        btnValidate.setToolTip("Take a screenshot with the specified dimension")
        btnValidate.clicked.connect(lambda: self.__takeScreenshot(False))
        vbox.addWidget(btnValidate)
        vbox.setAlignment(qtc.Qt.AlignCenter)
        mainLayout.addLayout(vbox)

        return mainLayout

    def __getCurrentDico(self):
        """
        Récupère et retourne les coordonnées affichées
        sur la fenêtre
        """
        mon = int(self.__mon.text()) if self.__mon.text() != "" else 1
        top = int(self.__top.text()) if self.__top.text() != "" else 0
        left = int(self.__left.text()) if self.__left.text() != "" else 0
        ag = qtw.QDesktopWidget().availableGeometry()
        width = int(self.__width.text()) if self.__width.text() != "" else ag.width()-left
        height = int(self.__height.text()) if self.__height.text() != "" else ag.height()-top

        nbMonitors = len(self.__mss.monitors) - 1
        if mon > nbMonitors:
            mon = nbMonitors
        capture_dic = {'top': top, 'left': left, 'width': width, 'height': height, 'mon': mon}
        return capture_dic

    def __takeScreenshot(self, isInit):
        """
        Prend un screenshot de l'écran
        """
        currentDico = self.__getCurrentDico()
        self.__mainWindow.hide()
        self.hide()
        captureDico = self.__getCaptureDico(currentDico)
        image = np.array(self.__mss.grab(captureDico))[:, :, :3].astype(np.uint8)
        self.__mainWindow.show()
        self.show()
        im = Image.fromarray(image)
        im.save("icons/screenshot.jpeg")
        pixmap = guy.QPixmap('icons/screenshot.jpeg')
        self.__label.clear()
        self.__label.setPixmap(pixmap)
        ratio = pixmap.width() / pixmap.height()
        if pixmap.width() > pixmap.height():
            self.__label.setMinimumSize(275, 275 / ratio)
            self.__label.setMaximumSize(275, 275 / ratio)
        else:
            self.__label.setMinimumSize(275 * ratio, 275)
            self.__label.setMaximumSize(275 * ratio, 275)

        if isInit:
            self.hide()
        return

    def __getCaptureDico(self, currentDico):
        monitor_number = currentDico.get('mon')
        mon = self.__mss.monitors[monitor_number]

        capture_dic = {'top': mon['top'] + currentDico.get('top'),
                       'left': mon['left'] + currentDico.get('left'),
                       'width': currentDico.get('width'),
                       'height': currentDico.get('height'),
                       'mon': monitor_number}
        return capture_dic

    def keyPressEvent(self, a0: guy.QKeyEvent):
        if a0.key() == qtc.Qt.Key_Escape:
            self.__mainWindow.closeAllWindows()
        return

    def gatherDatas(self):
        """
        Retourne les deux coordonnées de l'écran de jeu et de game over
        """
        dico = {}
        dicoGo = []
        if self.__forGameOver:
            dico["capture"] = self.__dicoNormal
            dicoGo.append(self.__getCurrentDico())
        else:
            dico["capture"] = self.__getCurrentDico()
            dicoGo.append(self.__dicoGO)
        text = self.__Go_text.text() if self.__Go_text.text() != "" else "Game Over"
        dicoGo.append(text)
        ag = qtw.QDesktopWidget().availableGeometry()
        X = int(self.__X.text()) if self.__X.text() != "" else int(ag.width() / 2)
        Y = int(self.__Y.text()) if self.__Y.text() != "" else int(ag.height() / 2)
        dicoGo.append((X, Y))
        dico["gameOver"] = dicoGo
        return dico

    def __switchPurpose(self):
        """
        Change le mode de "jeu" à "game over"
        """
        if self.__forGameOver:
            self.__dicoGO = self.__getCurrentDico()
            ref = self.__dicoNormal
            self.__frameGO.hide()
            self.__listener.stop()
        else:
            self.__dicoNormal = self.__getCurrentDico()
            ref = self.__dicoGO
            self.__frameGO.show()
            self.__listener.start()

        self.__top.setText(str(ref["top"]))
        self.__left.setText(str(ref["left"]))
        self.__width.setText(str(ref["width"]))
        self.__height.setText(str(ref["height"]))
        self.__mon.setText(str(ref["mon"]))

        self.__forGameOver = not self.__forGameOver
        return

    def hide(self):
        try:
            self.__frameGO.hide()
            super().hide()
        except Exception as e:
                print(e)
        return

    def close(self):
        try:
            self.__frameGO.close()
        except Exception as e:
                print(e)
        super().close()
        return

    def show(self):
        if self.__forGameOver:
            self.__frameGO.show()
        super().show()
        return
