import json
import numpy as np
from matplotlib import pyplot as plt


class Material(object):

    def __init__(self, name='empty', mb_const=np.nan, el_mb_const=np.nan, ho_mb_const=np.nan, eg=np.nan, s0=np.nan,
                 nc=np.nan, nv=np.nan, d0=np.nan, ea=np.nan):
        """
        :param name: Name of material
        :param mb_const: Mobility constant [m**2/(V*s*K)]
        :param el_mb_const: Electron mobility constant [-]
        :param ho_mb_const: Hole mobility constant [-]
        :param eg: Energy gap [eV]
        :param s0: Conductivity constant [S/m]
        :param nc: effective density of states in conduction band [m**-3]
        :param nv: effective density of states in valence band [m**-3]
        :param d0: maximal diffusion coefficient [m*2/s]
        :param ea: activation energy [J]
        """

        self.name = name
        self.attributes = {'Mobility constant': mb_const, 'Electron mobility constant': el_mb_const,
                           'Hole mobility constant': ho_mb_const, 'Energy gap': eg, 'Constant conductivity': s0,
                           'Nc': nc, 'Nv': nv, 'Maximal diffusion coefficient': d0, 'Activation energy': ea}
        self.kb = 1.381e-23     #boltzmann cosnatnt
        self.e = 1.60217662e-19 #charge of the electron
        self.R = 8.31446        #gas constant [J/(mol*K)]


    def __str__(self):
        return "Name of the material: " + str(self.name) + "\nAttributes are:\n" + str(self.attributes)

    def save(self, loc):
        # file_name = '.'.join([self.name, 'json'])
        with open(loc, 'w') as outfile:
            json.dump({'name': self.name,'attributes': self.attributes}, outfile, indent=4)

    def load(self, loc):
        with open(loc, 'r') as source:
            data = json.load(source)
            self.name = data['name']
            self.attributes = data['attributes']

    def mobility_of_electrons(self, t):
        """
        type: electrical model
        :param t: temperature
        :return: value of moblity of electrons
        """

        return self.attributes['Mobility constant'] * t ** self.attributes['Electron mobility constant']

    def mobility_of_holes(self, t):
        """
        type: electrical model
        :param t: temperature
        :return: value of the mobility of electrons
        """

        return self.attributes['Mobility constant'] * t ** self.attributes['Hole mobility constant']

    def electrical_conductivity(self, t):
        """
        type: electrical model
        :param t: temperature
        :return: Electrical conductivity
        """

        return self.attributes['Constant conductivity'] + np.exp(-self.attributes['Energy gap'] * self.e/(2 * self.kb * t))

    def concentration_of_carriers(self, t):
        """
        :param t: temperature
        :return:
        """
        return (self.attributes['Nv'] * self.attributes['Nc'])**0.5 * np.exp(-self.attributes['Energy gap'] *
                                                                             self.e/(2 * self.kb * t))
    def diffusion_coefficient(self, t):
        """
        :param t:
        :return:
        """
        return self.attributes['D0'] * np.exp(-self.attributes['Activation energy']/(self.R * t))


    def plot(self, param,  boundary, nt=1000):
        """
        :param param: parameter to plot
        :param boundary: boundary of x as a tuple
        :param nt: number of points between boundary
        :return: plot
        """
        if param == 'Mobility of electrons':
            t0 = boundary[0]
            tk = boundary[1]

            x = np.linspace(t0, tk, nt)
            y = self.mobility_of_electrons(x)

            xlabel = 'Temperature [K]'
            ylabel = 'Mobility of electrons [m**2/(V*s)]'

        elif param == 'Mobility of holes':
            t0 = boundary[0]
            tk = boundary[1]

            x = np.linspace(t0, tk, nt)
            y = self.mobility_of_holes(x)

            xlabel = 'Temperature [K]'
            ylabel = 'Mobility of holes [m**2/(V*s)]'

        elif param == 'Electrical conductivity':
            t0 = boundary[0]
            tk = boundary[1]

            x = np.linspace(t0, tk, nt)
            y = self.electrical_conductivity(x)

            xlabel = 'Temperature [K]'
            ylabel = 'Electrical conductivity'

        elif param == 'Concentration of carriers':
            t0 = boundary[0]
            tk = boundary[1]

            x = np.linspace(t0, tk, nt)
            y = self.concentration_of_carriers(x)

            xlabel = 'Temperature [K]'
            ylabel = 'Concentration of carriers [m**-3]'

        elif param == 'Diffusion coefficient':
            t0 = boundary[0]
            tk = boundary[1]

            x = np.linspace(t0, tk, nt)
            y = self.diffusion_coefficient(x)

            xlabel = 'Temperature [K]'
            ylabel = 'Diffusion coefficient [m**2/s]'

        else:
            return

        plt.figure()
        plt.plot(x, y, '-b')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

    @property
    def attributes_keys(self):
        return list(self.attributes.keys())
