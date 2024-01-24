import PyQt5.QtGui as guy

black = "#2B2B2B"
green = "#074925"
white = "#E6E6E6"
gray = "#7D7D7D"


def getPalette():
    palette = guy.QPalette()
    palette.setColor(guy.QPalette.Window, guy.QColor(black))
    palette.setColor(guy.QPalette.WindowText, guy.QColor(white))
    palette.setColor(guy.QPalette.Base, guy.QColor(gray))
    palette.setColor(guy.QPalette.Text, guy.QColor(green))
    palette.setColor(guy.QPalette.Button, guy.QColor(gray))
    palette.setColor(guy.QPalette.ButtonText, guy.QColor(green))
    return palette


def linedit_stylesheet():
    stylesheet = "QLineEdit{border-radius:4px;}"
    return stylesheet


def button_stylesheet():
    stylesheet = "QPushButton{background-color:" + green + ";color:" + white + ";border-radius:8px;}"
    return stylesheet


def checkbox_stylesheet():
    stylesheet = "QCheckBox{color:" + white + "}"
    return stylesheet


def combobox_stylesheet():
    stylesheet = ""
    return stylesheet


def label_stylesheet():
    stylesheet = "QLabel{color:" + white + "}"
    return stylesheet


def full_stylesheet():
    return linedit_stylesheet() + button_stylesheet() + checkbox_stylesheet() + combobox_stylesheet() + label_stylesheet()
