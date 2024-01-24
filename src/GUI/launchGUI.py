import sys
from pathlib import Path

import PyQt5.QtWidgets as pqt
from src.GUI.windows import MainWindow as mw


def launch():
    import os
    print(os.getcwd())
    app = pqt.QApplication(sys.argv)
    window = mw.MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    launch()
