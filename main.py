import material
import os



dir_path = os.path.dirname(os.path.realpath(__file__))

obj1 = material.Material("GaAs", {'therm_conduct': 0, 'eg': 0})

obj1.load_material(dir_path, 'test.json')
print(obj1)

