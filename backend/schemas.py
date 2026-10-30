"""Contrato de entrada y salida del endpoint de inferencia."""
import math
from typing import Annotated

from pydantic import BaseModel, Field, model_validator

from backend.predictor import FEATURES


class Transaction(BaseModel):
    # Se mantiene la interfaz exacta Time, V1..V28, Amount del dataset original.
    features: dict[str, Annotated[float, Field(allow_inf_nan=False)]]

    @model_validator(mode='after')
    def validate_features(self):
        keys = set(self.features)
        required = set(FEATURES)
        if keys != required:
            missing = sorted(required - keys)
            extra = sorted(keys - required)
            raise ValueError(f'Variables incorrectas. Faltantes: {missing}; adicionales: {extra}')
        if self.features['Time'] < 0 or self.features['Amount'] < 0:
            raise ValueError('Time y Amount deben ser no negativos.')
        if not all(math.isfinite(v) for v in self.features.values()):
            raise ValueError('Todas las variables deben ser números finitos.')
        return self


class Prediction(BaseModel):
    probabilidad_fraude: float
    clasificacion: int
    resultado: str
    umbral: float
