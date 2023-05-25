import os
import pyslha

def extract_m1_m2_mu(file_path):
     
     data = pyslha.read(file_path)

     m1 = data.blocks['EXTPAR'][1]
     m2 = data.blocks['EXTPAR'][2]
     mu = data.blocks['EXTPAR'][23]

     result = {
          'M_1(MX)': m1,
          'M_2(MX)': m2,
          'mu(MX)' : mu
     }

     return m1,m2,mu

def extract_N1_N2_C1(file_path):
     
     data = pyslha.read(file_path)

     N1 = data.blocks['MASS'][1000022]
     N2 = data.blocks['MASS'][1000023]
     C1 = data.blocks['MASS'][1000024]
     C2 = data.blocks['MASS'][1000037]
     
     return N1,N2,C1,C2

folder = 'output_dir'

def extract_cross_section(file):

    with open(file, 'r') as f:
        data = f.readlines()
    
    
    if data[-1].startswith(' #no_cross-section\n'):
        return None

    

    result = {}
    for i in range(len(data)):
        line = data[i]
        if line.startswith('XSECTION'):

            particle_1 = line.split(' ')[-4]
            particle_2 = line.split(' ')[-5]
            LO = data[i+1].split(' ')[-2]
            NLO = data[i+2].split(' ')[-2]
            result[(particle_1, particle_2)] = (LO,NLO)
    return result
            
def create_cross_section(folder):
    folder_list = os.listdir(folder)
    liste = []
    for file in folder_list:
        file_path = os.path.join('output_dir', file)
        m1,m2,mu = extract_m1_m2_mu(file_path)
        N1,N2,C1,C2 = extract_N1_N2_C1(file_path)
        resu = extract_cross_section(file_path)
        liste.append((m1,m2,mu,N1,N2,C1,C2, resu))
    return liste


print(create_cross_section(folder)[1])