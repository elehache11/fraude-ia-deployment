"""Inferencia reutilizando el modelo final de la Actividad 6."""
import csv
import os
from pathlib import Path

import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = Path(os.getenv('MODEL_PATH', str(ROOT / 'model' / 'modelo_final_Random_Forest.joblib')))
THRESHOLD_PATH = Path(os.getenv('THRESHOLD_PATH', str(ROOT / 'model' / 'umbrales_seleccionados.csv')))
FEATURES = ['Time'] + [f'V{i}' for i in range(1, 29)] + ['Amount']


class FraudPredictor:
    def __init__(self):
        self.model = joblib.load(MODEL_PATH)  # Sólo archivos propios o de confianza.
        if list(self.model.feature_names_in_) != FEATURES:
            raise ValueError('El orden de variables del modelo no coincide con el contrato de la API.')
        if list(self.model.classes_) != [0, 1]:
            raise ValueError('Las clases del modelo no son [0, 1].')
        with THRESHOLD_PATH.open(newline='', encoding='utf-8-sig') as file:
            matches = [row for row in csv.DictReader(file) if row['Modelo'] == 'Random_Forest']
        if len(matches) != 1:
            raise ValueError('Debe existir exactamente un umbral para Random_Forest.')
        self.threshold = float(matches[0]['Umbral'])
        if not 0 < self.threshold < 1:
            raise ValueError('Umbral fuera del intervalo (0, 1).')

    def predict(self, values: dict[str, float]):
        frame = pd.DataFrame([[values[name] for name in FEATURES]], columns=FEATURES)
        probability = float(self.model.predict_proba(frame)[0, 1])
        classification = int(probability >= self.threshold)
        return {
            'probabilidad_fraude': round(probability, 6),
            'clasificacion': classification,
            'resultado': 'Fraude potencial' if classification else 'Transacción legítima',
            'umbral': self.threshold,
        }
