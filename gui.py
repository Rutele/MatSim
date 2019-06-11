from PyQt5 import uic, QtWidgets
import os
import sys
import material
from copy import copy


class MainWindow(object):

    window = None
    _material = None
    mod_material = None
    _file = None
    _current_path = None
    message = None

    def __init__(self, path):
        #Initial data setup
        self._material = material.Material('', {})
        self.mod_material = material.Material('', {})
        self._current_path = path
        self.message = QtWidgets.QMessageBox()

        #Loading the GUI file from Qt Designer
        self.window = uic.loadUi(os.path.join(self._current_path, "GuiFiles/MainWindowAlternate.ui"))

        #Signals' actions assigments
        self.window.actionLoad.triggered.connect(self.file_open)
        self.window.actionSave.triggered.connect(self.file_save)
        self.window.actionSave_as.triggered.connect(self.file_save_as)
        self.window.actionPlot.triggered.connect(self.plot_menu)
        self.window.actionCreate.triggered.connect(self.create_menu)
        self.window.attributesBox.activated.connect(self.update_value)
        self.window.actionClose.triggered.connect(sys.exit)
        self.window.valueEdit.editingFinished.connect(self.update_material_value)

        #Showing the window
        self.window.show()

    def file_open(self):
        self._file = QtWidgets.QFileDialog.getOpenFileName(self.window, 'Open File', '', "JSON (*.json)")
        if self._file == ('', ''):
            pass
        else:
            self._material.load(self._file[0])
            self.mod_material = copy(self._material)
            self.window.attributesBox.clear()
            self.set_disp_vals_combo()
            self.update_value()
            self.update_window_name()

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

    def update_window_name(self):
        self.window.setWindowTitle(self._material.name)

    def set_disp_vals_combo(self):
        for key in self._material.attributes.keys():
            for attribute in self._material.attributes[key]:
                self.window.attributesBox.addItem(attribute)

    def update_value(self):
        for key in self._material.attributes.keys():
            if self.window.attributesBox.currentText() in self._material.attributes[key]:
                self.window.valueEdit.setText(str(self._material.attributes[key][self.window.attributesBox.currentText()]))

    def update_material_value(self):
        for key in self.mod_material.attributes.keys():
            if self.window.attributesBox.currentText() in self.mod_material.attributes[key]:
                self.mod_material.attributes[key][self.window.attributesBox.currentText()] = float(self.window.valueEdit.text())

    def plot_menu(self):
        plotting_window = PlotWindow(self.mod_material, self._current_path)
        plotting_window.window.exec()

    def create_menu(self):
        creation_window = CreateWindow(self._current_path)
        creation_window.window.exec()
        creation_window.window.result()
        if creation_window.window.result() == 0:
            pass
        elif creation_window.window.result() == 1:
            self._material = material.Material(name=creation_window.name, type=creation_window.type)
            self.set_disp_vals()
            self.update_window_name()


class PlotWindow(QtWidgets.QDialog):

    message = None
    isLam = None

    def __init__(self, mat, path):
        super().__init__()
        self._current_mat = mat
        self.message = QtWidgets.QMessageBox()
        self.window = uic.loadUi(os.path.join(path, "GuiFiles/PlotWindow.ui"))
        self.window.PlotBtn.clicked.connect(self.plot)
        self.window.CancelBtn.clicked.connect(self.window.reject)
        self.window.ExportToTXTBtn.clicked.connect(self.export_data)
        self.window.ParamList.currentIndexChanged.connect(self.disable_edit)
        self.disable_edit()
        self.isLam = False

    def plot(self):
        try:
            if self.isLam:
                if float(self.window.StartLam.text()) > float(self.window.EndLam.text()):
                    self.message.setIcon(QtWidgets.QMessageBox.Warning)
                    self.message.setWindowTitle("Incorrect values")
                    self.message.setText("Starting point can not be larger than the ending point.")
                    self.message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    self.message.exec()
                elif float(self.window.StartLam.text()) < 0 or float(self.window.EndLam.text()) < 0:
                    self.message.setIcon(QtWidgets.QMessageBox.Warning)
                    self.message.setWindowTitle("Incorrect values")
                    self.message.setText("Range can not have negative values.")
                    self.message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    self.message.exec()
                elif int(self.window.PointsLam.text()) <= 0:
                    self.message.setIcon(QtWidgets.QMessageBox.Warning)
                    self.message.setWindowTitle("Incorrect values")
                    self.message.setText("Step has to be non-zero, positive value.")
                    self.message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    self.message.exec()
                else:
                    tp = float(self.window.StartLam.text())
                    tk = float(self.window.EndLam.text())
                    nt = float(self.window.PointsLam.text())
                    param = self.window.ParamList.currentText()
                    self._current_mat.plot(str(param), (tp, tk), nt)
            elif not self.isLam:
                if float(self.window.Start.text()) > float(self.window.End.text()):
                    self.message.setIcon(QtWidgets.QMessageBox.Warning)
                    self.message.setWindowTitle("Incorrect values")
                    self.message.setText("Starting point can not be larger than the ending point.")
                    self.message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    self.message.exec()
                elif float(self.window.Start.text()) < 0 or float(self.window.End.text()) < 0:
                    self.message.setIcon(QtWidgets.QMessageBox.Warning)
                    self.message.setWindowTitle("Incorrect values")
                    self.message.setText("Range can not have negative values.")
                    self.message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    self.message.exec()
                elif int(self.window.Points.text()) <= 0:
                    self.message.setIcon(QtWidgets.QMessageBox.Warning)
                    self.message.setWindowTitle("Incorrect values")
                    self.message.setText("Step has to be non-zero, positive value.")
                    self.message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    self.message.exec()
                else:
                    tp = float(self.window.Start.text())
                    tk = float(self.window.End.text())
                    nt = float(self.window.Points.text())
                    param = self.window.ParamList.currentText()
                    self._current_mat.plot(str(param), (tp, tk), nt)
        except ValueError:
            self.message.setIcon(QtWidgets.QMessageBox.Warning)
            self.message.setWindowTitle("Incorrect values")
            self.message.setText("Please enter a number.")
            self.message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.message.exec()

    def export_data(self):
        file = QtWidgets.QFileDialog.getSaveFileName(self.window, 'Export to TXT', '', 'TXT (*.txt)')
        if self.window.ParamList.currentText() == "Absorption":
            tp = float(self.window.StartLam.text())
            tk = float(self.window.EndLam.text())
            nt = int(self.window.PointsLam.text())
        else:
            tp = float(self.window.Start.text())
            tk = float(self.window.End.text())
            nt = int(self.window.Points.text())
        param = self.window.ParamList.currentText()
        self._current_mat.plot(str(param), (tp, tk), nt, file[0])

    def disable_edit(self):
        if self.window.ParamList.currentText() == "Absorption":
            self.window.Start.setDisabled(True)
            self.window.End.setDisabled(True)
            self.window.Points.setDisabled(True)
            self.window.StartLam.setDisabled(False)
            self.window.EndLam.setDisabled(False)
            self.window.PointsLam.setDisabled(False)
            self.isLam = True
        else:
            self.window.Start.setDisabled(False)
            self.window.End.setDisabled(False)
            self.window.Points.setDisabled(False)
            self.window.StartLam.setDisabled(True)
            self.window.EndLam.setDisabled(True)
            self.window.PointsLam.setDisabled(True)
            self.isLam = False


class CreateWindow(QtWidgets.QDialog):
    name = None
    type = None

    def __init__(self, path):
        super().__init__()
        self.name = "empty"
        self.type = "none"
        self.window = uic.loadUi(os.path.join(path, "GuiFiles/CreateMaterial.ui"))
        self.window.cancelButton.clicked.connect(self.window.reject)
        self.window.createButton.clicked.connect(self.accept_form)
        self.window.radioIntrinsic.toggled.connect(self.set_type_intrinsic)
        self.window.radioDoped.toggled.connect(self.set_type_doped)

    def accept_form(self):
        self.name = self.window.nameEdit.text()
        self.window.accept()

    def set_type_intrinsic(self):
        self.type = "Intrinsic Semiconductor"

    def set_type_doped(self):
        self.type = "Doped Semiconductor"
