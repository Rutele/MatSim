import json
import os


class Material(object):

    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes
        self.file_name = 'material.json'

    def __str__(self):
        return "Name of the material: " + str(self.name) + "\nAttributes are:\n" + str(self.attributes)

    def dump_attributes(self, loc):
        with open(os.path.join(loc, self.file_name), 'w') as outfile:
            json.dump((self.attributes, self.name), outfile, indent = 4)

