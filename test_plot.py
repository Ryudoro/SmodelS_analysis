import pyslha
import os
import numpy as np
import matplotlib.pyplot as plt
import importlib.util

def read_slha(file_path):
    data = pyslha.read(file_path)
    M_2 = data.blocks['EXTPAR'][2]
    mu = data.blocks['EXTPAR'][23]

    return M_2,mu

def read_py(file_path):
    spec = importlib.util.spec_from_file_location("smodels_output", file_path)
    smodels_output = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(smodels_output)

    r = 0
    for res in smodels_output.smodelsOutput['ExptRes']:
        if 'r' in res:
            r = res['r']
            break

    return r
        
def extract_data(smomodel_file_path, slha_file_path, py_file_path):
    M_2, mu = read_slha(slha_file_path)
    r = read_py(py_file_path)

    return M_2, mu, r

data = []
folder = 'smodels/outpute'
files = os.listdir(folder)

for file in files:
    if file.endswith('.smodels'):
        file_path = os.path.join(folder, file)
        input_file_path = os.path.join('smodels/inpute', file.replace('.smodels', ''))
        py_file_path = os.path.join(folder, file.replace('.smodels', '.py'))
        print(py_file_path)
        if os.path.exists(input_file_path) and os.path.exists(py_file_path):
            print('a')
            data.append(extract_data(file_path, input_file_path, py_file_path))

print(data)
data = np.array(data)

M_2, mu, r = data[:,0], data[:,1], data[:,2]

plt.scatter(M_2,mu, c=r)