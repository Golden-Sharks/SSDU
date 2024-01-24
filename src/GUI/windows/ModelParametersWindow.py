import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as guy
import src.GUI.windows.style as st


class ModelParametersWindow(qtw.QWidget):
    __mainWindow = 0
    __isHidden = False
    __state = "DQN"

    def __init__(self, mainWindow):
        super().__init__()
        self.__mainWindow = mainWindow
        self.setWindowFlags(qtc.Qt.FramelessWindowHint)
        self.__getRightLocation()
        self.setFixedHeight(50)
        self.setFixedWidth(300)
        self.setLayout(self.__getMenuDeroulant())
        self.setPalette(st.getPalette())

    def __getMenuDeroulant(self):
        layout = qtw.QVBoxLayout()
        menu = qtw.QComboBox()
        self.__layoutParams = qtw.QVBoxLayout()
        self.__getFrames()
        menu.addItems(["DQN", "PPO"])
        menu.currentTextChanged.connect(lambda: self.__switchModel())
        layout.addWidget(menu)
        layout.addLayout(self.__layoutParams)
        return layout

    def __switchModel(self):
        if self.__state == "POO":
            self.__framePOO.hide()
            self.__frameDQN.show()
            self.__state = "DQN"
        else:
            self.__frameDQN.hide()
            self.__framePOO.show()
            self.__state = "POO"


    def __getFrames(self):
        x = self.geometry().left()
        y = 125
        self.__framePOO = qtw.QFrame()
        self.__framePOO.setPalette(st.getPalette())
        self.__framePOO.setFixedWidth(300)
        self.__framePOO.setWindowFlags(qtc.Qt.FramelessWindowHint)
        self.__framePOO.move(x, y)
        self.__framePOO.setStyleSheet(st.full_stylesheet())
        self.__frameDQN = qtw.QFrame()
        self.__frameDQN.setPalette(st.getPalette())
        self.__frameDQN.setFixedWidth(300)
        self.__frameDQN.move(x, y)
        self.__frameDQN.setWindowFlags(qtc.Qt.FramelessWindowHint)
        self.__frameDQN.setMaximumWidth(300)
        self.__frameDQN.setStyleSheet(st.full_stylesheet())
        self.__framePOO.setLayout(self.__getParams_POO())
        self.__frameDQN.setLayout(self.__getParams_DQN())
        self.__framePOO.hide()
        return

    def __getParams_POO(self):
        mainLayout = qtw.QVBoxLayout()
        params = qtw.QVBoxLayout()
        hyper_params = qtw.QVBoxLayout()

        self.__tensorboard_name_POO = qtw.QLineEdit(self)
        self.__tensorboard_name_POO.setPlaceholderText("nom du tensorboard : string")
        params.addWidget(self.__tensorboard_name_POO)
        self.__policy_POO = qtw.QComboBox()
        self.__policy_POO.addItems(["MlpPolicy", "CnnPolicy", "MultiInputPolicy"])
        params.addWidget(self.__policy_POO)
        self.__n_epochs_POO = qtw.QLineEdit(self)
        self.__n_epochs_POO.setPlaceholderText("n_epochs : int")
        params.addWidget(self.__n_epochs_POO)
        self.__n_steps_POO = qtw.QLineEdit(self)
        self.__n_steps_POO.setPlaceholderText("n_steps : int")
        params.addWidget(self.__n_steps_POO)

        self.__learning_rate_POO = qtw.QLineEdit(self)
        self.__learning_rate_POO.setPlaceholderText("learning rate : float")
        params.addWidget(self.__learning_rate_POO)
        self.__gamma_POO = qtw.QLineEdit(self)
        self.__gamma_POO.setPlaceholderText("gamma : float")
        params.addWidget(self.__gamma_POO)
        self.__gae_lambda_POO = qtw.QLineEdit(self)
        self.__gae_lambda_POO.setPlaceholderText("gae_lambda : float")
        params.addWidget(self.__gae_lambda_POO)

        mainLayout.addLayout(params)
        mainLayout.addLayout(hyper_params)
        return mainLayout

    def __getParams_DQN(self):
        mainLayout = qtw.QVBoxLayout()
        params = qtw.QVBoxLayout()
        hyper_params = qtw.QVBoxLayout()
        self.__buffer_size_DQN = qtw.QLineEdit(self)
        self.__buffer_size_DQN.setPlaceholderText("buffer size : int")
        params.addWidget(self.__buffer_size_DQN)
        self.__tensorboard_name_DQN = qtw.QLineEdit(self)
        self.__tensorboard_name_DQN.setPlaceholderText("nom du tensorboard : string")
        params.addWidget(self.__tensorboard_name_DQN)
        self.__total_timesteps_DQN = qtw.QLineEdit(self)
        self.__total_timesteps_DQN.setPlaceholderText("timesteps total : int")
        params.addWidget(self.__total_timesteps_DQN)

        self.__policy_DQN = qtw.QComboBox()
        self.__policy_DQN.addItems(["MlpPolicy", "CnnPolicy", "MultiInputPolicy"])
        hyper_params.addWidget(self.__policy_DQN)
        self.__tauLabel = qtw.QLabel("tau : 1.0000")
        self.__tauLabel.setStyleSheet("QLabel {color: "+st.white+";}")
        layoutTAU = qtw.QHBoxLayout()
        self.__tau_DQN = qtw.QSlider(qtc.Qt.Horizontal)
        self.__tau_DQN.setMaximum(10000)
        self.__tau_DQN.setMinimum(0)
        self.__tau_DQN.setValue(10000)
        self.__tau_DQN.valueChanged.connect(lambda: self.__updateTauLabel())
        layoutTAU.addWidget(self.__tau_DQN)
        layoutTAU.addWidget(self.__tauLabel)
        hyper_params.addLayout(layoutTAU)
        self.__gamma_DQN = qtw.QLineEdit(self)
        self.__gamma_DQN.setPlaceholderText("gamma : float")
        hyper_params.addWidget(self.__gamma_DQN)
        self.__trainingStart_DQN = qtw.QLineEdit(self)
        self.__trainingStart_DQN.setPlaceholderText("trainingStart : int")
        hyper_params.addWidget(self.__trainingStart_DQN)

        mainLayout.addLayout(params)
        mainLayout.addLayout(hyper_params)
        return mainLayout

    def __updateTauLabel(self):
        label = "tau : " + str(self.__tau_DQN.value()/10000)
        while len(label)<12:
            label = label + "0"
        self.__tauLabel.setText(label)

    def __saveCurrentDico(self):
        dico = {}
        if self.__state == "POO":
            dico["model"] = "PPO"
            dico["tensorboard_name"] = self.__tensorboard_name_DQN.text() if self.__tensorboard_name_DQN.text() != "" else "requin"
            dico["policy"] = self.__policy_POO.currentText()
            dico["n_epochs"] = int(self.__n_epochs_POO.text()) if self.__n_epochs_POO.text() != "" else 10
            dico["n_steps"] = int(self.__n_steps_POO.text()) if self.__n_steps_POO.text() != "" else 2048
            dico["learning_rate"] = float(self.__learning_rate_POO.text()) if self.__learning_rate_POO.text() != "" else 0.0003
            dico["gamma"] = float(self.__gamma_POO.text()) if self.__gamma_POO.text() != "" else 0.99
            dico["gae_lambda"] = float(self.__gae_lambda_POO.text()) if self.__gae_lambda_POO.text() != "" else 0.95
        else:
            dico["model"] = "DQN"
            dico["buffer_size"] = int(self.__buffer_size_DQN.text()) if self.__buffer_size_DQN.text() != "" else 5000
            dico["tensorboard_name"] = self.__tensorboard_name_DQN.text() if self.__tensorboard_name_DQN.text() != "" else "requin"
            dico["total_timesteps"] = int(self.__total_timesteps_DQN.text()) if self.__total_timesteps_DQN.text() != "" else 1000
            dico["policy"] = self.__policy_DQN.currentText()
            dico["tau"] = self.__tau_DQN.value()/10000
            dico["gamma"] = float(self.__gamma_DQN.text()) if self.__gamma_DQN.text() != "" else 0.99
            dico["trainingStart"] = int(self.__trainingStart_DQN.text()) if self.__trainingStart_DQN.text() != "" else 100
        return dico

    def __getRightLocation(self):
        ag = qtw.QDesktopWidget().availableGeometry()
        widget = self.geometry()
        x = ag.width() // 2 - widget.width() // 2 + 170
        y = 75
        self.move(x, y)
        return

    def keyPressEvent(self, a0: guy.QKeyEvent):
        if a0.key() == qtc.Qt.Key_Escape:
            self.__mainWindow.closeAllWindows()
        return

    def hide(self):
        self.__frameDQN.hide()
        self.__framePOO.hide()
        super().hide()
        return

    def close(self):
        self.__frameDQN.close()
        self.__framePOO.close()
        super().close()
        return

    def show(self):
        if self.__state == "POO":
            self.__framePOO.show()
        else:
            self.__frameDQN.show()
        super().show()
        return

    def gatherDatas(self):
        return {"model": self.__saveCurrentDico()}
