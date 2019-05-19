import json
import os
import material as m
from matplotlib import pyplot as plt
import numpy as np


class Database(object):
    """
    Current material is save in self.objects[0]
    In self.entries are saved directories for other materials.
    """

    def __init__(self, path):
        """
        :param path: path of material
        """
        self.material = m.Material('None')
        self.entries = []
        self.path = path

    def load(self):
        """
        :return: Loaded material
        """

        self.material.load(self.path)

        path = self.path.rstrip('{}'.format(self.material.name + '.json'))

        entries = os.listdir(path)

        self.entries = [e for e in entries if '.json' in e]
        for i in range(len(self.entries)):
            self.entries[i] = path + '{}'.format(self.entries[i])


    def save(self):
        '''
        :return: saves current material
        '''
        if self.material.name != 'None':
            self.material.save(self.path)

    def plot(self, param,  boundary):
        """
        :param param: parameter to plot
        :param boundary: boundary of x as a tuple
        :return: plot
        """
        if param == 'Mobility of electrons':
            T0 = boundary[0]
            Tk = boundary[1]
            Nt = 1000

            x = np.linspace(T0, Tk, Nt)
            y = self.material.mobility_of_electrons(x)


            xlabel = 'Temperature [K]'
            ylabel = 'Mobility of electrons [m**2/(V*s)]'

        elif param == 'Mobility of holes':
            T0 = boundary[0]
            Tk = boundary[1]
            Nt = 1000

            x = np.linspace(T0, Tk, Nt)
            y = self.material.mobility_of_holes(x)


            xlabel = 'Temperature [K]'
            ylabel = 'Mobility of holes [m**2/(V*s)]'

        elif param == 'Electrical conductivity':
            T0 = boundary[0]
            Tk = boundary[1]
            Nt = 1000

            x = np.linspace(T0, Tk, Nt)
            y = self.material.electrical_conductivity(x)

            xlabel = 'Temperature [K]'
            ylabel = 'Logarithm of electrical conductivity'

        else:
            return

        plt.figure()
        plt.plot(x, y, '-b')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

