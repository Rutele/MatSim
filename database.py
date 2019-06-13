import os
import material


class Database(object):

    data_path = None
    file_path = None
    tmp_material = None
    loaded_materials = [[]]

    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__), "materials")
        self.file_path = None
        self.tmp_material = material.Material()
        self.loaded_materials = []

    def load_db(self):
        for file in os.listdir(self.data_path):
            self.file_path = os.path.join(self.data_path, file)
            self.tmp_material.load(loc=self.file_path)
            self.loaded_materials.append([self.tmp_material.name, self.file_path])
