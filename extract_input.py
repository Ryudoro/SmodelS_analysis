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