from PyQt5 import uic, QtWidgets
import os
import sys
import material
import database
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
        self.window.actionMaterial_database.triggered.connect(self.database_menu)
        self.window.attributesBox.activated.connect(self.update_value)
        self.window.actionClose.triggered.connect(sys.exit)
        self.window.valueEdit.returnPressed.connect(self.check_input)

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
            self.mod_material.save(self._file[0])

    def file_save_as(self):
        self._file = QtWidgets.QFileDialog.getSaveFileName(self.window, 'Save File', '', 'JSON (*.json)')
        if self._file == ('', ''):
            pass
        else:
            self.mod_material.save(self._file[0])

    def update_window_name(self):
        self.window.setWindowTitle("MatSim - {}".format(self._material.name))

    def set_disp_vals_combo(self):
        for key in self._material.attributes.keys():
            for attribute in self._material.attributes[key]:
                self.window.attributesBox.addItem(attribute)

    def update_value(self):
        for key in self._material.attributes.keys():
            if self.window.attributesBox.currentText() in self._material.attributes[key]:
                self.window.valueEdit.setText(str(self._material.attributes[key][self.window.attributesBox.currentText()]))
                self.update_unit()

    def update_material_value(self):
        for key in self.mod_material.attributes.keys():
            if self.window.attributesBox.currentText() in self.mod_material.attributes[key]:
                self.mod_material.attributes[key][self.window.attributesBox.currentText()] = float(self.window.valueEdit.text())

    def check_input(self):
        try:
            if self.window.attributesBox.currentText() == "Refractive index" and float(self.window.valueEdit.text()) <= 0:
                self.message.setIcon(QtWidgets.QMessageBox.Warning)
                self.message.setWindowTitle("Incorrect values")
                self.message.setText("Refractive index can't be negative.")
                self.message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                self.message.exec()
            elif self.window.attributesBox.currentText() == "Energy gap" and float(self.window.valueEdit.text()) <= 0:
                self.message.setIcon(QtWidgets.QMessageBox.Warning)
                self.message.setWindowTitle("Incorrect values")
                self.message.setText("Energy gap can't be smaller or equal to zero")
                self.message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                self.message.exec()
            elif self.window.attributesBox.currentText() == "Activation energy" and float(self.window.valueEdit.text()) <= 0:
                self.message.setIcon(QtWidgets.QMessageBox.Warning)
                self.message.setWindowTitle("Incorrect values")
                self.message.setText("Activation energy can't be smaller or equal to zero")
                self.message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                self.message.exec()
            elif float(self.window.valueEdit.text()) == 0:
                self.message.setIcon(QtWidgets.QMessageBox.Warning)
                self.message.setWindowTitle("Incorrect values")
                self.message.setText("Please enter non zero value")
                self.message.setStandardButtons(QtWidgets.QMessageBox.Ok)
                self.message.exec()
            else:
                self.update_material_value()
        except ValueError:
            self.message.setIcon(QtWidgets.QMessageBox.Warning)
            self.message.setWindowTitle("Incorrect values")
            self.message.setText("Please enter a number.")
            self.message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.message.exec()

    def update_unit(self):
        if self.window.attributesBox.currentText() == "Energy gap":
            self.window.unitLabel.setText("[eV]")
        elif self.window.attributesBox.currentText() == "Effective mass of electrons" or self.window.attributesBox.currentText() == "Effective mass of holes":
            self.window.unitLabel.setText("[kg]")
        elif self.window.attributesBox.currentText() == "Conductivity constant":
            self.window.unitLabel.setText("[S/m]")
        elif self.window.attributesBox.currentText() == "Mobility constant":
            self.window.unitLabel.setText("[m**2/(V*s*K)]")
        elif self.window.attributesBox.currentText() == "Maximal diffusion coefficient":
            self.window.unitLabel.setText("[m**2/s]")
        elif self.window.attributesBox.currentText() == "Activation energy":
            self.window.unitLabel.setText("[J]")
        elif self.window.attributesBox.currentText() == "Nc" or self.window.attributesBox.currentText() == "Nv":
            self.window.unitLabel.setText("[m**-3]")
        else:
            self.window.unitLabel.setText("")

    def plot_menu(self):
        if self._material.name == '':
            self.message.setIcon(QtWidgets.QMessageBox.Warning)
            self.message.setWindowTitle("No material")
            self.message.setText("No material loaded. Please load a material first.")
            self.message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.message.exec()
        else:
            plotting_window = PlotWindow(self.mod_material, self._current_path)
            plotting_window.window.exec()

    def create_menu(self):
        creation_window = CreateWindow(self._current_path)
        creation_window.window.exec()
        if creation_window.window.result() == 0:
            pass
        elif creation_window.window.result() == 1:
            self._material = material.Material(name=creation_window.name, typ=creation_window.type)
            self.mod_material = self._material
            self.set_disp_vals_combo()
            self.update_window_name()

    def database_menu(self):
        database_window = DatabaseWindow(self._current_path)
        database_window.window.exec()
        if database_window.window.result() == 1:
            self._material.load(loc=database_window.material_to_load)
            self.mod_material = copy(self._material)
            self.window.attributesBox.clear()
            self.set_disp_vals_combo()
            self.update_value()
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
                elif float(self.window.PointsLam.text()) <= 0:
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
                elif float(self.window.Points.text()) <= 0:
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
        except TypeError:
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
            nt = float(self.window.PointsLam.text())
        else:
            tp = float(self.window.Start.text())
            tk = float(self.window.End.text())
            nt = float(self.window.Points.text())
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
        self.type = "Intrinsic semiconductor"
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


class DatabaseWindow(QtWidgets.QDialog):

    db = None
    message = None
    material_to_load = None

    def __init__(self, path):
        super().__init__()
        self.material_to_load = None
        self.db = database.Database()
        self.db.load_db()
        self.message = QtWidgets.QMessageBox()
        self.window = uic.loadUi(os.path.join(path, "GuiFiles/Database.ui"))
        self.window.cancelBtn.clicked.connect(self.window.reject)
        self.window.loadBtn.clicked.connect(self.load)
        self.update_box()

    def update_box(self):
        for entry in self.db.loaded_materials:
            self.window.materialBox.addItem(entry[0])

    def load(self):
        if not self.db.loaded_materials:
            self.message.setIcon(QtWidgets.QMessageBox.Warning)
            self.message.setWindowTitle("No materials")
            self.message.setText("No material was chosen or no materials were found.")
            self.message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.message.exec()
        else:
            for mat in self.db.loaded_materials:
                if mat[0] == self.window.materialBox.currentText():
                    self.material_to_load = mat[1]
                    self.window.accept()
