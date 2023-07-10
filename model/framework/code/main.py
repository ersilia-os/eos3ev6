# imports
import os
import csv
import sys
import numpy as np
from rdkit import Chem

# current file directory
root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(root, ".."))

from predictors.cyp450.cyp450_predictor import CYP450Predictor

# parse arguments
input_file = sys.argv[1]
output_file = sys.argv[2]

# my model
def my_model(smiles_list):
    mols = [Chem.MolFromSmiles(smi) for smi in smiles_list]
    kek_mols = []
    for mol in mols:
        if mol is not None:
            Chem.Kekulize(mol)
        kek_mols += [mol]
    
    cyp = CYP450Predictor(np.asarray(kek_mols))
    preds = cyp.get_predictions()

    return preds

# read SMILES from .csv file, assuming one column with header
with open(input_file, "r") as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    smiles_list = [r[0] for r in reader]

print(smiles_list)
# run modeler
outputs = my_model(smiles_list)

# write output in a .csv file

outputs.to_csv(output_file, index=False)
