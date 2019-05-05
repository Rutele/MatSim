import json
import os


class Material(object):

    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes

    def __str__(self):
        return "Name of the material: " + str(self.name) + "\nAttributes are:\n" + str(self.attributes)

    def save(self, loc):
        # file_name = '.'.join([self.name, 'json'])
        with open(loc, 'w') as outfile:
            json.dump((self.attributes, self.name), outfile, indent=4)

    def load(self, loc):
        with open(loc, 'r') as source:
            data = json.load(source)
            self.name = data['name']
            self.attributes = data['attributes']

    @property
    def attributes_keys(self):
        return list(self.attributes.keys())
