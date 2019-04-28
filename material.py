import json
import os


class Material(object):

    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes

    def __str__(self):
        return "Name of the material: " + str(self.name) + "\nAttributes are:\n" + str(self.attributes)

    def save_material(self, loc):
        file_name = '.'.join([self.name, 'json'])
        with open(os.path.join(loc, file_name), 'w') as outfile:
            json.dump((self.attributes, self.name), outfile, indent=4)

    def load_material(self, loc, file_name):
        with open(os.path.join(loc, file_name), 'r') as source:
            data = json.load(source)
            self.name = data['material_name']
            self.attributes = data['attributes']
