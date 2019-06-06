import os
import json


class Function(object):

    def __init__(self, funcs, attributes, type_, dir_=os.path.dirname(os.path.realpath(__file__))+'/func.py'):
        """
        :param funcs: functions in form {'name': ['variables', 'function' ]
        :param attributes: used constants in form of the dictionary {'simulation': [value_name]} !!don't use spaces
        :param type_: type of the material
        :param dir_: directory of the imported code
        """

        self.funcs = funcs
        self.attributes = attributes
        self.type = type_
        self.dir = dir_

    def import_(self):
        with open(self.dir, 'w') as file:
            #imported functions
            file.write('import numpy as np\nfrom matplotlib import pyplot as plt\n\n')

            #class definition
            file.write('class Material(object):\n\n')

            #__init__
            ##__init__ input
            var = [x for sublist in self.attributes.values() for x in sublist]
            input_ = str([s + '=np.nan' for s in var]).replace("[", "").replace("]", "").replace("'", "")
            ##__init__ definition
            file.write("\tdef __init__(self, name='empty', " + input_ +'):\n')
            ##__init__ class variables definition
            file.write('\t\tself.name = name\n')
            ###atributes
            attributes_keys = list(self.attributes.keys())
            attributes_values = list(self.attributes.values())

            values = []
            for i in range(len(attributes_values)):
                values.append(["'" + x + "'" + ':{}'.format(x) for x in attributes_values[i]])


            dicts = []
            for j in range(len(attributes_keys)):
                dicts.append({attributes_keys[j]: values[j]})
            attributes = {k:v for d in dicts for k,v in d.items()}

            attributes = str(attributes).replace('[', '{').replace(']', '}')
            attributes_string = str(attributes). replace('"', '')
            file.write('\t\tself.attributes = {}\n\n'.format(attributes_string))

            #functions definition
            for key in self.funcs:
                file.write('\tdef {}(self, {}):\n'.format(key, self.funcs[key][0]))
                file.write('\t\treturn {}\n\n'.format(self.funcs[key][1]))

            #plot definition
            file.write('\tdef plot(self, param,  boundary, nt=1000, file=None):\n\n')
            func_names = list(self.funcs.keys())
            inputnames = list(self.funcs.values())

            for k in range(len(func_names)):
                if k != 0:
                    file.write('\t\telif param == "{}":\n'.format(func_names[k]))
                elif k == 0:
                    file.write('\t\tif param == "{}":\n'.format(func_names[k]))
                file.write('\t\t\tx0 = boundary[0]\n')
                file.write('\t\t\txk = boundary[1]\n')
                file.write('\t\t\tx = np.linspace(x0, xk, nt)\n')
                file.write('\t\t\ty = self.{}(x)\n'.format(func_names[k]))
                file.write('\t\t\txlabel = "{}"\n'.format(inputnames[k]))
                file.write('\t\t\tylabel = "{}"\n\n'.format(func_names[k]))


            file.write("\t\telse:\n\t\t\treturn\n\n")

            file.write('\t\tif file is None:\n')
            file.write("\t\t\tplt.plot(x, y, '-b')\n")
            file.write("\t\t\tplt.xlabel(xlabel)\n")
            file.write("\t\t\tplt.ylabel(ylabel)\n")
            file.write("\t\t\tplt.show()\n")

            file.write('\t\telse:\n')
            file.write("\t\t\twith open(file, 'w') as outfile:\n")
            file.write("\t\t\t\tfor i in range(x.size):\n")
            file.write("\t\t\t\t\ttxt1 = str(x[i])\n")
            file.write("\t\t\t\t\ttxt2 = str(y[i])\n")
            file.write('\t\t\t\t\toutfile.write("{}' + '\ '.replace(' ', '') + 't' + '{}' + '\ '.replace(' ', '') + 'n' + '".format(txt1, txt2))\n')

            #property
            file.write('\n\t@property')
            file.write('\n\tdef attributes_keys(self):\n')
            file.write('\t\treturn list(self.attributes.keys())\n\n')

    def save(self, loc):
        with open(loc, 'w') as outfile:
            json.dump(self.funcs, outfile, indent=4)

    def load(self, loc):
        with open(loc, 'r') as source:
            self.funcs = json.load(source)


