import os
import sys
from PyQt5 import QtWidgets
import gui
import material
import json
import  Databse

#Current path directory
dir_path = os.path.dirname(os.path.realpath(__file__))

materials_path = dir_path + '\materials'


'''
obj1 = material.Material('Dupa', {'Nigga': 2, 'Gowno': 6})
obj1.save(materials_path + '\{}'.format(obj1.name) + '.json')
obj1.load(materials_path + '\{}'.format(obj1.name) + '.json')
'''

'''
#GUI
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = gui.MainWindow(dir_path)
    sys.exit(app.exec_())
'''

'''
d = Databse.Database(materials_path)
d.load()
d.path = dir_path + '\{}'.format('materials')
d.save()
'''
