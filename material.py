#Doped not finished

import json
import numpy as np
from matplotlib import pyplot as plt


class Material(object):

    def __init__(self, name='empty', typ=np.nan, mb_const=np.nan, el_mb_const=np.nan, ho_mb_const=np.nan, eg=np.nan,
                 s0=np.nan, me=np.nan, mh=np.nan, d0=np.nan, ea=np.nan, k=np.nan, n=np.nan, nc=np.nan, nv=np.nan,
                 nd=np.nan, ei=np.nan, ta=np.nan, tb=np.nan, conditions=True, atr_dict=None):
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
		:param nd: effective density of states in donor band [m**-3]
		:param ei: Intrinsic Fermi level [eV]

        Optical:
        :param k: Extinction coefficient
        :param n: Refractive index

        Thermal:
        :param ta: Thermal conductivity multiplication constant
        :param tb: Thermal conductivity exponent constant

        Other:
        :param conditions: True/False, Whether check or not condition for attributes (default True)
        """

        super().__init__()

        # initial conditions:
        if conditions:
            # for electrical:
            if eg <= 0:
                print('Energy gap has to be positive!')
            elif ea <= 0:
                print('Activation energy has to be positive!')

            # for optical:
            elif n <= 0:
                print('Refractive index has to be positive!')

        self.name = name
        self.type = typ

        if atr_dict is not None:
            self.attributes = atr_dict
        else:
            self.attributes = {'Electrical':
                                   {'Mobility constant': mb_const, 'Electron mobility constant': el_mb_const,
                                    'Hole mobility constant': ho_mb_const, 'Energy gap': eg, 'Constant conductivity': s0,
                                    'Effective mass of electrons': me, 'Effective mass of holes': mh,
                                    'Maximal diffusion coefficient': d0, 'Activation energy': ea, 'Nc': nc, 'Nv': nv,
									'Nd':nd, 'Ei':ei},

                               'Optical':
                                   {'Extinction coefficient': k,'Refractive index': n},

                               'Thermal':
                                   {'A': ta, 'B': tb}
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
        :return: value of mobility of electrons
        """

        if self.type == 'Intrinsic Semiconductor':
            return self.attributes['Electrical']['Mobility constant'] * t ** self.attributes['Electrical'][
                'Electron mobility constant']
        elif self.type == 'Doped Semiconductor':
            #to be changed
            return self.attributes['Electrical']['Mobility constant'] * t ** self.attributes['Electrical'][
                'Electron mobility constant']

    def mobility_of_holes(self, t):
        """
        type: electrical model
        :param t: temperature
        :return: value of the mobility of electrons
        """

        if self.type == 'Intrinsic Semiconductor':
            return self.attributes['Electrical']['Mobility constant'] * t ** self.attributes['Electrical']['Hole mobility constant']

        elif self.type == 'Doped Semiconductor':
            #to be changed
            return self.attributes['Electrical']['Mobility constant'] * t ** self.attributes['Electrical'][
                'Hole mobility constant']

    def electrical_conductivity(self, t, constants=False):
        """
        type: electrical model
        :param t: temperature
        :param constants: True/False If Nc/Nv is constant or not
        :return: Electrical conductivity
        """
        if self.type == 'Intrinsic Semiconductor':
            return self.attributes['Electrical']['Conductivity constant'] + np.exp(
                -self.attributes['Electrical']['Energy gap'] * self.e / (2 * self.kb * t))
        elif self.type == 'Doped Semiconductor':
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
                return self.e * mi * (self.attributes['Electrical']['Nd'] * n) ** 0.5 * np.exp(
                    -self.attributes['Electrical']['Ionisation Energy'] / (2 * self.kb * t))
            elif 100 <= t <= 500:
                return self.e * mi * self.attributes['Electrical']['Nd']
            elif t > 500:
                return self.attributes['Electrical']['Conductivity constant'] + np.exp(
                    -self.attributes['Electrical']['Energy gap'] * self.e / (2 * self.kb * t))

    def concentration_of_carriers(self, t, constants=False, type_='n'):
        """
        type: electrical model
        :param t: temperature
        :param constants: True/False, Default is False, True to use constant values of Nc and Nv which are predefined
		:param type_: which type of carriers can be p or n, default n
        :return: concentration of carriers
        """
        if self.type == 'Intrinsic Semiconductor':
            if not constants:
                return (self.Nv(t) * self.Nc(t)) ** 0.5 * np.exp(-self.attributes['Electrical']['Energy gap'] *
                                                                 self.e / (2 * self.kb * t))
            if constants:
                return (self.attributes['Electrical']['Nv'] * self.attributes['Electrical']['Nc']) ** 0.5 * \
						np.exp(-self.attributes['Electrical']['Energy gap'] * self.e / (2 * self.kb * t))

        elif self.type == 'Doped Semiconductor':
            if not constants:
                nc = self.Nc(t)
                nv = self.Nv(t)
            elif constants:
                nc = self.attributes['Electrical']['Nc']
                nv = self.attributes['Electrical']['Nv']
            
            if type_ == 'n':
                nx=nc
            elif type_ == 'p':
                nx=nv	
			
            if t < 100:
                return (self.attributes['Electrical']['Nd']*nx/2)**0.5 * np.exp(-self.attributes['Electrical']['Ei'] * self.e/(2*self.kb*t))
            elif 100 <= t <= 500:
                return self.attributes['Electrical']['Nd']
            elif t >= 500:
                return (nv * nc) ** 0.5 * np.exp(-self.attributes['Electrical']['Energy gap'] * self.e / (2 * self.kb * t))
			

    def diffusion_coefficient(self, t):
        """
        type: electrical model
        :param t: temperature
        :return: diffusion coefficient
        """
        if self.type == 'Intrinsic Semiconductor':
            return self.attributes['Electrical']['D0'] * np.exp(
                -self.attributes['Electrical']['Activation energy'] / (self.R * t))

        elif self.type == 'Doped Semiconductor':
            #to be chaned
            return self.attributes['Electrical']['D0'] * np.exp(
                -self.attributes['Electrical']['Activation energy'] / (self.R * t))

    def Nc(self, t):
        """
        type: electrical model
        :param t: temperature
        :return: effective density of states for electrons
        """
        if self.type == 'Intrinsic Semiconductor':
            return 2 * (2 * np.pi * self.attributes['Electrical'][
                'Effective mass of electrons'] * t / self.h ** 2) ** 1.5

        elif self.type == 'Doped Semiconductor':
            #to be chaned
            return 2 * (2 * np.pi * self.attributes['Electrical'][
                'Effective mass of electrons'] * t / self.h ** 2) ** 1.5

    def Nv(self, t):
        """
        type: electrical model
        :param t: temperature
        :return: effective density of states for holes
        """
        if self.type == 'Intrinsic Semiconductor':
            return 2 * (2 * np.pi * self.attributes['Electrical']['Effective mass of holes'] * t / self.h ** 2) ** 1.5

        elif self.type == 'Doped Semiconductor':
            #to be changed
            return 2 * (2 * np.pi * self.attributes['Electrical']['Effective mass of holes'] * t / self.h ** 2) ** 1.5

    def absorption(self, lam):
        """
        type: optical model
        :param lam: wavelength
        :return: absorption
        """
        return 4 * np.pi * self.attributes['Optical']['Extinction coefficient']/lam * 1e7
    
    def thermal_conductivity(self, t):
        """
        type: thermal model
        :param t: temperature
        :return: thermal conductivity [W/(m*K)]
        """
        return self.attributes['Thermal']['A'] * (300/t)**self.attributes['Thermal']['B']

    def plot(self, param,  boundary, nt=1000, file=None):
        """
        :param param: parameter to plot
        :param boundary: boundary of x as a tuple
        :param nt: number of points between boundary
        :param file: file location used for exporting the data to text file
        :return: plot
        """
        if param == 'Mobility of electrons':
            t0 = boundary[0]
            tk = boundary[1]

            x = np.linspace(t0, tk, (tk-t0)/nt)
            y = self.mobility_of_electrons(x)

            xlabel = 'Temperature [K]'
            ylabel = 'Mobility of electrons [m**2/(V*s)]'

        elif param == 'Mobility of holes':
            t0 = boundary[0]
            tk = boundary[1]

            x = np.linspace(t0, tk, (tk-t0)/nt)
            y = self.mobility_of_holes(x)

            xlabel = 'Temperature [K]'
            ylabel = 'Mobility of holes [m**2/(V*s)]'

        elif param == 'Electrical conductivity':
            t0 = boundary[0]
            tk = boundary[1]

            x = np.linspace(t0, tk, (tk-t0)/nt)
            y = self.electrical_conductivity(x)

            xlabel = 'Temperature [K]'
            ylabel = 'Electrical conductivity'

        elif param == 'Concentration of carriers':
            t0 = boundary[0]
            tk = boundary[1]

            x = np.linspace(t0, tk, (tk-t0)/nt)
            y = self.concentration_of_carriers(x)

            xlabel = 'Temperature [K]'
            ylabel = 'Concentration of carriers [m**-3]'

        elif param == 'Diffusion coefficient':
            t0 = boundary[0]
            tk = boundary[1]

            x = np.linspace(t0, tk, (tk-t0)/nt)
            y = self.diffusion_coefficient(x)

            xlabel = 'Temperature [K]'
            ylabel = 'Diffusion coefficient [m**2/s]'

        elif param == 'Nc':
            t0 = boundary[0]
            tk = boundary[1]

            x = np.linspace(t0, tk, (tk-t0)/nt)
            y = self.Nc(x)

            xlabel = 'Temperature [K]'
            ylabel = 'Nc [m**-3]'

        elif param == 'Nc':
            t0 = boundary[0]
            tk = boundary[1]

            x = np.linspace(t0, tk, (tk-t0)/nt)
            y = self.Nv(x)

            xlabel = 'Temperature [K]'
            ylabel = 'Nc [m**-3]'

        elif param == 'Absorption':
            t0 = boundary[0]
            tk = boundary[1]

            x = np.linspace(t0, tk, (tk-t0)/nt)
            y = self.absorption(x)

            xlabel = 'Wavelength [nm]'
            ylabel = 'Absorption [1/cm]'

        elif param == 'Thermal conductivity':
            t0 = boundary[0]
            tk = boundary[1]

            x = np.linspace(t0, tk, (tk-t0)/nt)
            y = self.thermal_conductivity(x)

            ylabel = 'Thermal conductivity [W/(m*K)]'
            xlabel = 'Temperature [K]'

        else:
            return

        if file is None:
            plt.figure()
            plt.plot(x, y, '-b')
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.show()
        else:
            if param == "Absorption":
                fun_var = "Wavelength [nm]"
            else:
                fun_var = "Temperature [K]"
            with open(file, 'w') as outfile:
                outfile.write("#{}  {}\n".format(param, fun_var))
                for i in range(x.size):
                    txt1 = str(x[i])
                    txt2 = str(y[i])
                    outfile.write("{}\t{}\n".format(txt1, txt2))

    @property
    def attributes_keys(self):
        return list(self.attributes.keys())
