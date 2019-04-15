import material
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)

obj1 = material.Material("GaAs", {'therm_conduct': 0, 'eg': 0})
print(obj1.attributes['therm_conduct'])
obj1.dump_attributes(dir_path)
