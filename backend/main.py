"""API local para evaluar una transacción con el Random Forest final."""
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from backend.predictor import FEATURES, FraudPredictor
from backend.schemas import Prediction, Transaction


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.predictor = FraudPredictor()  # Falla al iniciar si faltan artefactos.
    yield


app = FastAPI(title='API de detección de fraude', version='1.0.0', lifespan=lifespan)


@app.get('/health')
def health(request: Request):
    return {'estado': 'ok', 'modelo_disponible': request.app.state.predictor is not None}


@app.get('/model-info')
def model_info(request: Request):
    predictor = request.app.state.predictor
    return {'modelo': 'Random_Forest', 'variables': FEATURES, 'numero_variables': len(FEATURES),
            'umbral': predictor.threshold, 'clases': [0, 1]}


@app.post('/predict', response_model=Prediction)
def predict(transaction: Transaction, request: Request):
    return request.app.state.predictor.predict(transaction.features)
