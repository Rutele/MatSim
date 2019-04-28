import material
import os
import Databse



dir_path = os.path.dirname(os.path.realpath(__file__))

obj1 = material.Material("GaAs", {'therm_conduct': 0, 'eg': 0})

db = Databse.Database(dir_path)
db.load()
print(db.objects[0])
db.objects[0].name = 'AAAAA'
db.save()

