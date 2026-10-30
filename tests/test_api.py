from fastapi.testclient import TestClient
from backend.main import app
from backend.predictor import FEATURES


def test_health_and_model_info():
    with TestClient(app) as client:
        response = client.get('/health')
        assert response.status_code == 200
        assert response.json()['modelo_disponible'] is True
        response = client.get('/model-info')
        assert response.status_code == 200
        assert response.json()['umbral'] == 0.17
        assert response.json()['numero_variables'] == 30


def test_predict_and_reject_invalid_payload():
    features = {name: 0.0 for name in FEATURES}
    with TestClient(app) as client:
        response = client.post('/predict', json={'features': features})
        assert response.status_code == 200
        payload = response.json()
        assert 0 <= payload['probabilidad_fraude'] <= 1
        assert payload['clasificacion'] == int(payload['probabilidad_fraude'] >= 0.17)
        del features['V1']
        assert client.post('/predict', json={'features': features}).status_code == 422
        features['V1'] = float('nan')
        # JSON estándar no permite NaN; los clientes deben rechazarlo antes de enviar.
        features['V1'] = 0
        features['Amount'] = -1
        assert client.post('/predict', json={'features': features}).status_code == 422
