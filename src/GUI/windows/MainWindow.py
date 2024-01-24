import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as guy
import PyQt5.QtCore as qtc
import src.GUI.windows.style as st

from src.GUI.windows.InputsWindow import InputsWindow
from src.GUI.windows.ModelParametersWindow import ModelParametersWindow
from src.GUI.windows.PreProcessingWindow import PreProcessingWindow
from src.GUI.windows.ResizeWindow import ResizeWindow
from src.WebGameWrapper.WebGameTrainer import WebGameTrainer


class MainWindow(qtw.QWidget):
    __isStarted = False
    __subWindows = {}

    def __init__(self):
        super().__init__()
        self.setWindowFlags(qtc.Qt.FramelessWindowHint)
        self.__getSubWindows()
        layout = self.__getLayout()
        self.setLayout(layout)
        self.setFixedHeight(80)
        self.setFixedWidth(300)
        layout.setAlignment(qtc.Qt.AlignCenter)
        self.__getRightLocation()
        self.setPalette(st.getPalette())

    def keyPressEvent(self, a0: guy.QKeyEvent):
        """
        key listener ne se concentrant que sur la touche "échap" pour fermer l'application
        """
        if a0.key() == qtc.Qt.Key_Escape:
            self.closeAllWindows()
        return

    def closeAllWindows(self):
        """
        Ferme toutes les fenêtres de l'application, puis
        ferme la fenêtre principale et quitte l'application
        """
        i = 0
        while i < len(self.__subWindows):
            window = self.__subWindows[i]
            window.close()
            i += 1
        self.close()
        return

    def __getLayout(self):
        """
        Définit le layout principal de la fenêtre
        """
        layout = qtw.QHBoxLayout()
        layout.addWidget(self.__getButton(0, "Select the size of the game's window"))
        layout.addWidget(self.__getButton(1, "Select the differents inputs to play"))
        layout.addWidget(self.__getButton(2, "Set the model and his hyper-parameters"))
        layout.addWidget(self.__getButton(3, "Select the pre-processing of the images"))
        layout.addWidget(self.__getButton(4, "Start and stop the record"))
        return layout

    def __getButton(self, idButton, textTip):
        """
        Créé les différents boutons
        :param idButton: l'id du bouton à créer
        :param textTip: le texte qui apparait lorsque le bouton est survolé
        """
        button = qtw.QPushButton()
        button.setToolTip(textTip)
        if idButton == 0:
            button.setIcon(guy.QIcon('icons/resizeWindow.png'))
            button.clicked.connect(lambda: self.__hideAllSwitchOne(0))
        elif idButton == 1:
            button.setIcon(guy.QIcon('icons/inputs.png'))
            button.clicked.connect(lambda: self.__hideAllSwitchOne(1))
        elif idButton == 2:
            button.setIcon(guy.QIcon('icons/neuralNetwork.png'))
            button.clicked.connect(lambda: self.__hideAllSwitchOne(2))
        elif idButton == 3:
            button.setIcon(guy.QIcon('icons/preProcess.png'))
            button.clicked.connect(lambda: self.__hideAllSwitchOne(3))
        else:
            button.setIcon(guy.QIcon('icons/start.png'))
            button.clicked.connect(lambda: self.__switch(button))

        button.setFixedHeight(50)
        button.setFixedWidth(50)
        return button

    def __switch(self, button):
        """
        switch le mode de l'application entre start et stop
        """
        self.__hideAllSwitchOne(5)
        if (self.__isStarted):
            self.__stop(button)
        else:
            self.__start(button)
        self.__isStarted = ~self.__isStarted

    def __start(self, button):
        dico = self.__gatherDatas()
        self.__wgt = WebGameTrainer(dico)
        button.setIcon(guy.QIcon('icons/stop.png'))

    def __stop(self, button):
        self.__wgt.stop()
        button.setIcon(guy.QIcon('icons/start.png'))

    def __getSubWindows(self):
        """
        Créé les sous-fenêtres
        """
        self.__subWindows[0] = ResizeWindow(self)
        self.__subWindows[1] = InputsWindow(self)
        self.__subWindows[2] = ModelParametersWindow(self)
        self.__subWindows[3] = PreProcessingWindow(self)
        return

    def __hideAllSwitchOne(self, idToSwitch):
        """
        Cache toutes les sous-fenêtres ne correspondant pas à l'id
        et change la visibilité de celle correspondant
        """
        i = 0
        while i < len(self.__subWindows):
            window = self.__subWindows[i]
            if i == idToSwitch:
                if window.isHidden():
                    window.show()
                else:
                    window.hide()
            else:
                window.hide()
            i += 1
        return

    def __getRightLocation(self):
        """
        Déplace la fenêtre aux bonnes coordonnées sur l'écran
        """
        ag = qtw.QDesktopWidget().availableGeometry()
        widget = self.geometry()
        x = ag.width() // 2 - widget.width() // 2
        y = 0
        self.move(x, y)
        return

    def __gatherDatas(self):
        """
        Réunit les dictionnaires de toutes les sous-fenêtres et les affiches
        """
        dico = {}
        i = 0
        while i < len(self.__subWindows):
            window = self.__subWindows[i]
            dico.update(window.gatherDatas())
            i += 1
        print(dico)
        return dico
