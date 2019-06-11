import os
import sys
from PyQt5 import QtWidgets
import gui
import material
import json
import Databse


#Current path directory
dir_path = os.path.dirname(os.path.realpath(__file__))

materials_path = dir_path + '\materials' + '\Ge.json'

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = gui.MainWindow(dir_path)
    sys.exit(app.exec_())

'''
d = Databse.Database(materials_path)
d.load()
d.plot('Electrical conductivity', (1, 20))
d.path = d.entries[1]
d.load()
d.plot('Electrical conductivity', (1, 20))

func = {'multiplication': ['T', 'T*2'], 'division': ['T', 'T/2']}
attributes = {'Thermal': ['Energy_gap', 'Mobility'],
         'Optical': ['Refractive_index', 'Extinction_coefficient'],
         'Electrical': ['Activation_energy', 'Nc', 'Nv']
         }
type_ = 'Semiconductor'
res = function.Function(func, attributes, type_)
res.import_()
res.save(dir_path + '/fun.json')
'''