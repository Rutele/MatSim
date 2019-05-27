#Doped not finished

import json
import numpy as np
from matplotlib import pyplot as plt


class Material(object):

    def __init__(self, name='empty', typ=np.nan, mb_const=np.nan, el_mb_const=np.nan, ho_mb_const=np.nan, eg=np.nan, s0=np.nan,
                 me=np.nan, mh=np.nan, d0=np.nan, ea=np.nan, k=np.nan, n=np.nan, nc=np.nan, nv=np.nan):
        """
        :param name: Name of material
        :param typ: Type of material

        Electrical:
        :param mb_const: Mobility constant [m**2/(V*s*K)]
        :param el_mb_const: Electron mobility constant [-]
        :param ho_mb_const: Hole mobility constant [-]
        :param eg: Energy gap [eV]
        :param s0: Conductivity constant [S/m]
        :param me: effective mass of electrons [kg]
        :param mh: effective mass of holes [kg]
        :param d0: maximal diffusion coefficient [m*2/s]
        :param ea: activation energy [J]
        :param nc: effective density of states in conduction band [m**-3]
        :param nv: effective density of states in valence band [m**-3]

        Optical:
        :param k: Extinction coefficient
        :param n: Refractive index

        Thermal:
        """

        super().__init__()

    #initial conditions:

        #for electrical:
        if eg <= 0:
            print('Energy gap has to be positive!')
        elif ea <= 0:
            print('Activation energy has to be positive!')

        #for optical:
        elif n <= 0:
            print('Refractive index has to be positive!')

        #for thermal

        self.name = name
        self.type = typ

        self.attributes = {'Electrical':
                               {'Mobility constant': mb_const, 'Electron mobility constant': el_mb_const,
                                'Hole mobility constant': ho_mb_const, 'Energy gap': eg, 'Constant conductivity': s0,
                                'Effective mass of electrons': me, 'Effective mass of holes': mh,
                                'Maximal diffusion coefficient': d0, 'Activation energy': ea, 'Nc': nc, 'Nv': nv},

                           'Optical':
                               {'Extinction coefficient': k,'Refractive index': n},

                           'Thermal':
                               {}
                           }
        self.kb = 1.381e-23     #boltzmann constant [m**2 * kg / (s**2 * K)]
        self.e = 1.60217662e-19 #charge of the electron [C]
        self.R = 8.31446        #gas constant [J/(mol*K)]
        self.h = 6.62607004e-34 #planck constant [m**2 * kg / s]

    def __str__(self):
        return "Name of the material: " + str(self.name) + "\nAttributes are:\n" + str(self.attributes)

    def save(self, loc):
        # file_name = '.'.join([self.name, 'json'])
        with open(loc, 'w') as outfile:
            json.dump({'name': self.name, 'type': self.type, 'attributes': self.attributes}, outfile, indent=4)

    def load(self, loc):
        with open(loc, 'r') as source:
            data = json.load(source)
            self.name = data['name']
            self.type = data['type']
            self.attributes = data['attributes']

    def mobility_of_electrons(self, t):
        """
        type: electrical model
        :param t: temperature
        :return: value of moblity of electrons
        """

    def mobility_of_holes(self, t):
        """
        type: electrical model
        :param t: temperature
        :return: value of the mobility of electrons
        """

    def electrical_conductivity(self, t):
        """
        type: electrical model
        :param t: temperature
        :return: Electrical conductivity
        """

    def concentration_of_carriers(self, t, constants=False):
        """
        type: electrical model
        :param t: temperature
        :param constants: True/False, Default is False, True to use constant values of Nc and Nv which are predefined
        :return: concentration of carriers
        """

    def diffusion_coefficient(self, t):
        """
        type: electrical model
        :param t: temperature
        :return: diffusion coefficient
        """

    def Nc(self, t):
        """
        type: electrical model
        :param t: temperature
        :return: effective density of states for electrons
        """

    def Nv(self, t):
        """
        type: electrical model
        :param t: temperature
        :return: effective density of states for holes
        """

    def absorption(self, lam):
        """
        type: optical model
        :param lam: wavelength
        :return: absorption
        """
        return 4 * np.pi * self.attributes['Optical']['Extinction coefficient']/lam * 1e7

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

        elif param == 'Nc':
            t0 = boundary[0]
            tk = boundary[1]

            x = np.linspace(t0, tk, nt)
            y = self.Nc(x)

            xlabel = 'Temperature [K]'
            ylabel = 'Nc [m**-3]'

        elif param == 'Nc':
            t0 = boundary[0]
            tk = boundary[1]

            x = np.linspace(t0, tk, nt)
            y = self.Nv(x)

            xlabel = 'Temperature [K]'
            ylabel = 'Nc [m**-3]'

        elif param == 'Absorption':
            t0 = boundary[0]
            tk = boundary[1]

            x = np.linspace(t0, tk, nt)
            y = self.absorption(x)

            xlabel = 'Wavelength [nm]'
            ylabel = 'Absorption [1/cm]'

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


class IntrinsicSemiconductor(Material):

    def __init__(self, name='empty', mb_const=np.nan, el_mb_const=np.nan, ho_mb_const=np.nan, eg=np.nan, s0=np.nan,
                 me=np.nan, mh=np.nan, d0=np.nan, ea=np.nan, k=np.nan, n=np.nan, nc=np.nan, nv=np.nan):
        """
        :param name: Name of material

        Electrical:
        :param mb_const: Mobility constant [m**2/(V*s*K)]
        :param el_mb_const: Electron mobility constant [-]
        :param ho_mb_const: Hole mobility constant [-]
        :param eg: Energy gap [eV]
        :param s0: Conductivity constant [S/m]
        :param me: effective mass of electrons [kg]
        :param mh: effective mass of holes [kg]
        :param d0: maximal diffusion coefficient [m*2/s]
        :param ea: activation energy [J]
        :param nc: effective density of states in conduction band [m**-3]
        :param nv: effective density of states in valence band [m**-3]

        Optical:
        :param k: Extinction coefficient
        :param n: Refractive index

        Thermal:
        """
        typ = 'Intrinsic Semiconductor'

        super().__init__(name, typ, mb_const, el_mb_const, ho_mb_const, eg, s0,
                 me, mh, d0, ea, k, n, nc, nv)


    def mobility_of_electrons(self, t):
        """
        type: electrical model
        :param t: temperature
        :return: value of moblity of electrons
        """

        return self.attributes['Electrical']['Mobility constant'] * t ** self.attributes['Electrical']['Electron mobility constant']

    def mobility_of_holes(self, t):
        """
        type: electrical model
        :param t: temperature
        :return: value of the mobility of electrons
        """

        return self.attributes['Electrical']['Mobility constant'] * t ** self.attributes['Electrical']['Hole mobility constant']

    def electrical_conductivity(self, t):
        """
        type: electrical model
        :param t: temperature
        :return: Electrical conductivity
        """

        return self.attributes['Electrical']['Constant conductivity'] + np.exp(-self.attributes['Electrical']['Energy gap'] * self.e/(2 * self.kb * t))

    def concentration_of_carriers(self, t, constants=False):
        """
        type: electrical model
        :param t: temperature
        :param constants: True/False, Default is False, True to use constant values of Nc and Nv which are predefined in attributes
        :return: concentration of carriers
        """
        if not constants:
            return (self.Nv(t) * self.Nc(t))**0.5 * np.exp(-self.attributes['Electrical']['Energy gap'] *
                                                                             self.e/(2 * self.kb * t))
        if constants:
            return (self.attributes['Electrical']['Nv'] * self.attributes['Electrical']['Nc'])**0.5 * \
                   np.exp(-self.attributes['Electrical']['Energy gap'] * self.e/(2 * self.kb * t))
    def diffusion_coefficient(self, t):
        """
        type: electrical model
        :param t:
        :return:
        """
        return self.attributes['Electrical']['D0'] * np.exp(-self.attributes['Electrical']['Activation energy']/(self.R * t))

    def Nc(self, t):
        """
        type: electrical model
        :param t: temperature
        :return: effective density of states for electrons
        """
        return 2 * (2 * np.pi * self.attributes['Electrical']['Effective mass of electrons'] * t/self.h**2)**1.5

    def Nv(self, t):
        """
        type: electrical model
        :param t: temperature
        :return: effective density of states for holes
        """
        return 2 * (2 * np.pi * self.attributes['Electrical']['Effective mass of holes'] * t / self.h ** 2) ** 1.5

class DopedSemiconductor(Material):

    def __init__(self, name='empty', typ='n-type', mb_const=np.nan, el_mb_const=np.nan, ho_mb_const=np.nan, eg=np.nan, s0=np.nan,
                 me=np.nan, mh=np.nan, d0=np.nan, ea=np.nan, k=np.nan, n=np.nan, nc=np.nan, nv=np.nan, nd=np.nan, ei=np.nan):
        """
        :param name: Name of material
        :param typ: Type of doped semiconductor (n-type/p-type), default n-type

        Electrical:
        :param mb_const: Mobility constant [m**2/(V*s*K)]
        :param el_mb_const: Electron mobility constant [-]
        :param ho_mb_const: Hole mobility constant [-]
        :param eg: Energy gap [eV]
        :param s0: Conductivity constant [S/m]
        :param me: effective mass of electrons [kg]
        :param mh: effective mass of holes [kg]
        :param d0: maximal diffusion coefficient [m*2/s]
        :param ea: activation energy [J]
        :param nc: effective density of states in conduction band [m**-3]
        :param nv: effective density of states in valence band [m**-3]
        :param nd: Dopant concentration [m**-3]
        "param ei: Ionisation energy [eV]

        Optical:
        :param k: Extinction coefficient
        :param n: Refractive index

        Thermal:
        """
        typ = typ + ' semiconductor'

        super().__init__(name, typ, mb_const, el_mb_const, ho_mb_const, eg, s0,
                 me, mh, d0, ea, k, n, nc, nv)

        self.attributes['Electrical']['Nd'] = nd
        self.attributes['Electrical']['Ionisation energy'] = ei

    def mobility_of_electrons(self, t):
        # same as intrinsic
        """
        type: electrical model
        :param t: temperature
        :return: value of moblity of electrons
        """

        return self.attributes['Electrical']['Mobility constant'] * t ** self.attributes['Electrical']['Electron mobility constant']

    def mobility_of_holes(self, t):
        # same as intrinsic
        """
        type: electrical model
        :param t: temperature
        :return: value of the mobility of electrons
        """

        return self.attributes['Electrical']['Mobility constant'] * t ** self.attributes['Electrical']['Hole mobility constant']

    def electrical_conductivity(self, t, constants=False):
        """
        type: electrical model
        :param t: temperature
        :return: Electrical conductivity
        :param constants: True/False, Default is False, True to use constant values of Nc and Nv which are predefined in attributes
        """
        mi = np.nan
        n = np.nan
        if self.type == 'n-type semiconductor':
            mi = self.mobility_of_electrons(t)
            if constants:
                n = self.attributes['Electrical']['Nc']
            elif not constants:
                n = self.Nc(t)
        elif self.type == 'p-type semiconductor':
            mi = self.mobility_of_holes(t)
            if constants:
                n = self.attributes['Electrical']['Nv']
            elif not constants:
                n = self.Nv(t)


        if t < 100:
            return self.e * mi * (self.attributes['Electrical']['Nd'] * n)**0.5 * np.exp(-self.attributes['Electrical']['Ionisation Energy']/(2*self.kb*t))
        elif 100 <= t >= 500:
            return self.e * mi * self.attributes['Electrical']['Nd']
        elif t > 500:
            return self.attributes['Electrical']['Constant conductivity'] + np.exp(-self.attributes['Electrical']['Energy gap'] * self.e/(2 * self.kb * t))


    #DO IT
    def concentration_of_carriers(self, t, constants=False):
        # same as intrinsic
        """
        type: electrical model
        :param t: temperature
        :param constants: True/False, Default is False, True to use constant values of Nc and Nv which are predefined in attributes
        :return: concentration of carriers
        """
        if not constants:
            nc = self.Nc(t)
            nv = self.Nv(t)
        elif constants:
            nc = self.attributes['Electrical']['Nc']
            nv = self.attributes['Electrical']['Nv']

    def diffusion_coefficient(self, t):
        # same as intrinsic
        """
        type: electrical model
        :param t:
        :return:
        """
        return self.attributes['Electrical']['D0'] * np.exp(-self.attributes['Electrical']['Activation energy']/(self.R * t))

    def Nc(self, t):
        # same as intrinsic
        """
        type: electrical model
        :param t: temperature
        :return: effective density of states for electrons
        """
        return 2 * (2 * np.pi * self.attributes['Electrical']['Effective mass of electrons'] * t/self.h**2)**1.5

    def Nv(self, t):
        # same as intrinsic
        """
        type: electrical model
        :param t: temperature
        :return: effective density of states for holes
        """
        return 2 * (2 * np.pi * self.attributes['Electrical']['Effective mass of holes'] * t / self.h ** 2) ** 1.5

