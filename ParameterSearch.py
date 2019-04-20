import json
import os
import material as m


def load(path):
    entries = os.listdir(path)

    entries = [e for e in entries if '.json' in e]

    objects = []

    for elem in entries:
        with open(elem, 'r') as f:
            file = json.load(f)
            objects.append(m.Material(file[1],file[0]))

    return objects
