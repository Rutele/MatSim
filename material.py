import json
import os
import math
import numpy as np


class Material(object):

    def __init__(self, name, mb_const=np.nan, el_mb_const=np.nan, ho_mb_const=np.nan, Eg=np.nan, s0=np.nan):
        """
        :param name: Name of material
        :param mb_const: Mobility constant
        :param el_mb_const: Electron mobility constant
        :param ho_mb_const: Hole mobility constant
        :param Eg: Energy gap
        :param s0: Conductivity constant
        """

        self.name = name
        self.attributes = {'Mobility constant': mb_const, 'Electron mobility constant': el_mb_const,
                           'Hole mobility constant': ho_mb_const, 'Energy gap': Eg, 'Constant conductivity': s0}
        self.kb = 1.381e-23

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
        :return: value of moblity of electrons
        """

        return self.attributes['Mobility constant'] * t ** self.attributes['Hole mobility constant']

    def electrical_conductivity(self, t):
        """
        type: electrical model
        :param t: temperature
        :return: Logarithm of electrical conductivity
        """

        return math.log(self.attributes['Constant conductivity']) + (-self.attributes['Energy gap']/(2 * self.kb * t))


    @property
    def attributes_keys(self):
        return list(self.attributes.keys())
