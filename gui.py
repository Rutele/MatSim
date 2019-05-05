from PyQt5 import uic, QtWidgets
import os
import material


class MainWindow(object):

    window = None
    _material = None
    _file = None
    _current_path = None

    def __init__(self, path):
        #Initial data setup
        self._material = material.Material('', {})
        self._current_path = path

        #Loading the GUI file from Qt Designer
        self.window = uic.loadUi(os.path.join(self._current_path, "MainWindow.ui"))

        #Signals' actions assigments
        self.window.actionLoad.triggered.connect(self.file_open)
        self.window.actionSave.triggered.connect(self.file_save)
        self.window.actionSave_as.triggered.connect(self.file_save_as)
        self.window.comboBoxAtributes.activated.connect(self.show_attribute_value)

        #Showing the window
        self.window.show()

    def file_open(self):
        self._file = QtWidgets.QFileDialog.getOpenFileName(self.window, 'Open File', '', "JSON (*.json)")
        if self._file == ('', ''):
            pass
        else:
            self._material.load(self._file[0])
            print(self._material)
            #This takes care of inputing attributes names into the combobox
            for atr in self._material.attributes_keys:
                self.window.comboBoxAtributes.addItem(atr)
                self.window.setWindowTitle("Testing - " + self._material.name)

    def file_save(self):
        if not self._file:
            self.file_save_as()
        elif self._file == ('', ''):
            self.file_save_as()
        else:
            self._material.save(self._file[0])

    def file_save_as(self):
        self._file = QtWidgets.QFileDialog.getSaveFileName(self.window, 'Save File', '', 'JSON (*.json)')
        if self._file == ('', ''):
            pass
        else:
            self._material.save(self._file[0])

    def show_attribute_value(self):
        attr_val = self._material.attributes[self.window.comboBoxAtributes.currentText()]
        print(attr_val)
        self.window.lineEditAtrVal.setText(str(attr_val))
