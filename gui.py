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
        self.window = uic.loadUi(os.path.join(self._current_path, "GuiFiles/MainWindow.ui"))

        #Signals' actions assigments
        self.window.actionLoad.triggered.connect(self.file_open)
        self.window.actionSave.triggered.connect(self.file_save)
        self.window.actionSave_as.triggered.connect(self.file_save_as)
        self.window.actionPlot.triggered.connect(self.plot_menu)
        self.window.actionCreate.triggered.connect(self.create_menu)

        #Showing the window
        self.window.show()

    def file_open(self):
        self._file = QtWidgets.QFileDialog.getOpenFileName(self.window, 'Open File', '', "JSON (*.json)")
        if self._file == ('', ''):
            pass
        else:
            self._material.load(self._file[0])
            self.set_disp_vals()

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

    def set_disp_vals(self):
        """
        This function is setting up the displayed values of the loaded/edited material
        """
        self.window.MobConst.setText(str(self._material.attributes['Electrical']['Mobility constant']))
        self.window.ConstCond.setText(str(self._material.attributes['Electrical']['Constant conductivity']))
        self.window.Eg.setText(str(self._material.attributes['Electrical']['Energy gap']))
        self.window.ElecMobConst.setText(str(self._material.attributes['Electrical']['Electron mobility constant']))
        self.window.HoleMobConst.setText(str(self._material.attributes['Electrical']['Hole mobility constant']))

    def plot_menu(self):
        self.plotting_window = PlotWindow(self._material, self._current_path)
        self.plotting_window.window.exec()

    def create_menu(self):
        self.creation_window = CreateWindow(self._current_path)
        self.creation_window.window.exec()
        self.creation_window.window.result()
        if self.creation_window.window.result() == 0:
            pass
        elif self.creation_window.window.result() == 1:
            self._material = material.Material(name=self.creation_window.name, type=self.creation_window.type)
            print(self._material)
            self.set_disp_vals()
            self.update_window_name()


class PlotWindow(QtWidgets.QDialog):
    def __init__(self, mat, path):
        super().__init__()
        self._current_mat = mat
        self.window = uic.loadUi(os.path.join(path, "GuiFiles/PlotWindow.ui"))
        self.window.PlotBtn.clicked.connect(self.plot)

    def plot(self):
        tp = float(self.window.Start.text())
        tk = float(self.window.End.text())
        nt = int(self.window.Points.text())
        param = self.window.ParamList.currentText()
        self._current_mat.plot(str(param), (tp, tk), nt)


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
