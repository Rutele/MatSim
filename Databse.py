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
            with open(elem, 'r') as f:
                file = json.load(f)
                objects.append(m.Material(file[1],file[0]))

        self.objects = objects

    def save(self):
        '''
        :return: saves database
        '''

        for i in range(len(self.objects)):
            self.objects[i].save_material(self.path)

