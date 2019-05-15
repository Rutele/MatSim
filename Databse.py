import json
import os
import material as m


class Database(object):

    def __init__(self, path):
        self.objects = []
        self.path = path

    def load(self):
        '''
        :return: Data loaded from path
        '''
        entries = os.listdir(self.path)

        entries = [e for e in entries if '.json' in e]

        objects = []

        for elem in entries:
            loc = self.path + '\{}'.format(elem)
            material = m.Material(0, 0)
            material.load(loc)
            objects.append(material)

        self.objects = objects

    def save(self):
        '''
        :return: saves database
        '''

        for i in range(len(self.objects)):
            self.objects[i].save(self.path + "\{}".format(self.objects[i].name) + '.json')

