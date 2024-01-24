import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
from pynput import keyboard
import src.GUI.windows.style as st


class InputsWindow(qtw.QWidget):
    __listOfKey = {}

    def __init__(self, mainWindow):
        super().__init__()
        self.__mainWindow = mainWindow
        widget = qtw.QWidget()
        self.setWindowFlags(qtc.Qt.FramelessWindowHint)
        self.__getContent()
        listener = keyboard.Listener(on_release=self.on_release)
        listener.start()
        widget.setGeometry(50, 50, 320, 200)
        self.setPalette(st.getPalette())

    def on_release(self, key):
        self.__updateList(format(key), False)

    def __getContent(self):
        mainLayout = qtw.QVBoxLayout()
        layout = qtw.QHBoxLayout()
        textBox = qtw.QLabel()
        textBox.setText("Saisissez les inputs")
        self.__button = qtw.QPushButton("reset")
        self.__button.setStyleSheet(st.button_stylesheet())
        self.__button.setToolTip("Reset the input list")
        self.__button.clicked.connect(lambda: (self.__updateList("reset", True)))
        self.__button.installEventFilter(self)
        layout.addWidget(textBox)
        layout.addWidget(self.__button)
        mainLayout.addLayout(layout)
        self.__listView = qtw.QListWidget()
        self.__listView.setFocus()
        mainLayout.addWidget(self.__listView)
        self.setLayout(mainLayout)
        self.setFixedHeight(400)
        self.setFixedWidth(300)
        self.__getRightLocation()

    def eventFilter(self, obj, event):
        if obj is self.__button and event.type() == qtc.QEvent.KeyPress:
            return True
        return super().eventFilter(obj, event)

    def __getRightLocation(self):
        ag = qtw.QDesktopWidget().availableGeometry()
        widget = self.geometry()
        x = ag.width() // 2 - widget.width() // 2 - 50
        y = 75
        self.move(x, y)
        return

    def __updateList(self, key, reset):
        try:
            if not self.isVisible():
                return
            if key[0] == '\'':
                key = key[1]
            else :
                i=4
                newKey = ""
                while i<len(key):
                    newKey = newKey + key[i]
                    i+=1
                key = newKey
            if reset:
                self.__listOfKey.clear()
                self.__listView.clear()
                return

            i = 0
            while i < len(self.__listOfKey):
                if key == self.__listOfKey[i]:
                    return
                i += 1

            if key != "esc":
                self.__listOfKey[len(self.__listOfKey)] = key
                self.__listView.addItem(key)
                self.__listView.repaint()
        except RuntimeError:
            print("input windows has been brutally deleted")
        return

    def gatherDatas(self):
        dico = {"Inputs": self.__listOfKey}
        return dico

