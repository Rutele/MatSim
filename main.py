import os
import sys
from PyQt5 import QtWidgets
import gui

dir_path = os.path.dirname(os.path.realpath(__file__))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = gui.MainWindow(dir_path)
    sys.exit(app.exec_())

