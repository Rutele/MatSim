import os
import sys
from PyQt5 import QtWidgets
import gui

#Current path directory
dir_path = os.path.dirname(os.path.realpath(__file__))

"""
obj1 = material.Material(0, 0)
obj1.load_material(dir_path, "test.json")
print(obj1)
"""

#GUI
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = gui.MainWindow(dir_path)
    sys.exit(app.exec_())
