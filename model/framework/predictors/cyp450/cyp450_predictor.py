import pandas as pd
import numpy as np
from numpy import array
from typing import Tuple
from ..features.morgan_fp import MorganFPGenerator
from ..utilities.utilities import get_processed_smi
from rdkit import Chem
from ..features.rdkit_descriptors import RDKitDescriptorsGenerator
from ..cyp450 import cyp450_models_dict
import csv

class CYP450Predictor:
    """
    Makes CYP450 predictions

    Attributes:
        df (DataFrame): DataFrame containing column with smiles
        smiles_column_index (int): index of column containing smiles
        predictions_df (DataFrame): DataFrame hosting all predictions
    """

    _columns_dict = {
        'CYP3A4_inhib': {
            'order': 1,
            'description': 'CYP3A4 inhibitor',
            'isSmilesColumn': False
        },
        'CYP3A4_subs': {
            'order': 2,
            'description': 'CYP3A4 substrate',
            'isSmilesColumn': False
        }
    }

    def __init__(self, kekule_mols: array = None, rdkit_descriptors_matrix: array = None, morgan_fp_matrix: array = None, smiles: array = None):
        """
        Constructor for RLMPredictior class

        Parameters:
            kekule_mols (array): n x 1 array of RDKit molecule objects kekulized
            rdkit_descriptors_matrix (array): optional numpy array of rdkit descriptors for each molecule,
            morgan_fp_matrix (array): optional numpy array of morgan fingerprints for each molecule,
            smiles (array): optional n x 1 array of SMILES used to record raw predictions in raw_predictions_df property
        """

        self.kekule_mols = kekule_mols

        # create dataframe to be filled with predictions
        columns = self._columns_dict.keys()
        self.predictions_df = pd.DataFrame(columns=columns)
        self.raw_predictions_df = pd.DataFrame()

        if len(self.kekule_mols) == 0:
            raise ValueError('Please provide valid smiles')


        if morgan_fp_matrix is None:
            # generate morgan fingerprints
            morgan_fp_generator = MorganFPGenerator(self.kekule_mols)
            self.morgan_fp_matrix = morgan_fp_generator.get_morgan_features()
        else:
            self.morgan_fp_matrix = morgan_fp_matrix

        if rdkit_descriptors_matrix is None:
            # generate rdkit descriptors
            rdkit_descriptors_generator = RDKitDescriptorsGenerator(self.kekule_mols)
            self.rdkit_desc_matrix = rdkit_descriptors_generator.get_rdkit_descriptors(['MolLogP', 'TPSA', 'ExactMolWt', 'NumHDonors', 'NumHAcceptors'])
        else:
            self.rdkit_desc_matrix = rdkit_descriptors_matrix

        self.smiles = smiles

        self.has_errors = False
        self.model_errors = []

    def get_predictions(self):

        features = np.append(self.morgan_fp_matrix, self.rdkit_desc_matrix, axis=1)

        for model_name in cyp450_models_dict.keys():
            print(model_name)
            error_threshold_length = len(self.predictions_df.index)
            models = cyp450_models_dict[model_name]
            print(models)
            if len(models) == 0:
                print(model_name, "did not work")
                continue     
            model_has_error = False
            probs_matrix = np.ma.empty((64, features.shape[0]))
            probs_matrix.mask = True
            for model_number in range(0, 64):
                probs = models[f'model_{model_number}'].predict_proba(features)
                probs_matrix[model_number, :probs.shape[0]] = probs.T[1]
                if model_has_error == False and error_threshold_length > len(probs):
                    model_has_error = True

            mean_probs = probs_matrix.mean(axis=0)
            response_dict = {
                "mean_probs": mean_probs,
                "model_has_error": model_has_error
            }
            print(response_dict)

            self.predictions_df[f'{model_name}'] = pd.Series(np.around(mean_probs, 3))
            
        return self.predictions_df

    def _error_callback(self, error):
        print(error)

    def _get_model_predictions(self, request_queue, response_queue):
        params_dict = request_queue.get()

        model_name = params_dict['model_name']
        features = params_dict['features']
        error_threshold_length = params_dict['error_threshold_length']
        models = cyp450_models_dict[model_name]
        model_has_error = False
        probs_matrix = np.ma.empty((64, features.shape[0]))
        probs_matrix.mask = True
        for model_number in range(0, 64):
            probs = models[f'model_{model_number}'].predict_proba(features)
            probs_matrix[model_number, :probs.shape[0]] = probs.T[1]
            if model_has_error == False and error_threshold_length > len(probs):
                model_has_error = True

        mean_probs = probs_matrix.mean(axis=0)
        response_dict = {
            "mean_probs": mean_probs,
            "model_has_error": model_has_error
        }
        response_queue.put(response_dict)
        return None

    def get_errors(self):
        return {
            'model_errors': self.model_errors
        }

    def columns_dict(self):
        return self._columns_dict.copy()

    def record_predictions(self, file_path):
        if len(self.raw_predictions_df.index) > 0:
            with open(file_path, 'a') as fw:
                rows = self.raw_predictions_df.values.tolist()
                cw = csv.writer(fw)
                cw.writerows(rows)
