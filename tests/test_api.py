from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200

def test_get_comedores():
    response = client.get("/comedores")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_validacion_ratio_viandas():
    payload = {
        "provincia": "Buenos Aires",
        "barrio_anonimo": "Barrio 99",
        "tipo_comedor": "Comunitario",
        "capacidad_viandas": 5000,
        "voluntarios": 2
    }
    response = client.post("/comedores", json=payload)
    assert response.status_code == 422 # Debe fallar por tu validador

def test_crear_comedor_valido():
    payload = {
        "provincia": "CABA",
        "barrio_anonimo": "Barrio 07",
        "tipo_comedor": "Comunitario",
        "capacidad_viandas": 150,
        "voluntarios": 5
    }
    response = client.post("/comedores", json=payload)
    assert response.status_code == 201
    assert response.json()["provincia"] == "CABA"