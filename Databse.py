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
