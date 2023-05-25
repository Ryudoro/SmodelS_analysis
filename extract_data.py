import importlib.util
import os
import pandas as pd
    

def check_warning(liste):
    liste_without_warn = []
    for elem in liste:
        elem2 = elem['OutputStatus']
        if elem2['warnings'].startswith("Error"):
            continue
        liste_without_warn.append(elem)
    return liste_without_warn
        



def extract_data(folder):
    data_filenames = [filename for filename in os.listdir(folder) if filename.endswith('.slha.py')]
    liste = []
    for data_filename in data_filenames:
        file_path = os.path.join(folder, data_filename)
        spec = importlib.util.spec_from_file_location("module.name", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
            
        smodelsOutput = getattr(module, 'smodelsOutput')
        liste.append(smodelsOutput)
    return liste

def data_to_df(liste, input):
    liste_without_warning = check_warning(liste)
    ExptRes = [x['ExptRes'] for x in liste_without_warning]
    i = 0
    for Expt in ExptRes:
        for data in Expt:
            data['input_param'] = input[i]
        i+=1
    all_Res = [item for sublist in ExptRes for item in sublist]
    df = pd.DataFrame(all_Res)
    return df

def extract_data_input(liste):
    liste_without_warning = check_warning(liste)
    liste_input = [elem['OutputStatus']['input file'] for elem in liste_without_warning]
    return liste_input
    
def main_extract(output_folder):
    folder = output_folder
    liste = extract_data(output_folder)
    input = extract_data_input(liste)
    df = data_to_df(liste, input)
    
    return df,input

