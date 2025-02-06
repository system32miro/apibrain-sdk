import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apibrain import APIBrain, capability, APIBrainConfig

def test_apibrain_initialization():
    """Testa se o SDK inicializa corretamente"""
    app = FastAPI()
    apibrain = APIBrain()
    apibrain.enable(app)
    
    client = TestClient(app)
    
    # Testa endpoint /discover
    response = client.get("/discover")
    assert response.status_code == 200
    assert "capabilities" in response.json()
    
    # Testa OpenAPI Schema
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "x-apibrain-context" in response.json()

def test_capability_decorator():
    """Testa se o decorador @capability funciona"""
    app = FastAPI()
    apibrain = APIBrain()
    
    @capability(
        name="test_endpoint",
        description="Endpoint de teste",
        apibrain=apibrain  # Passa a instância
    )
    @app.get("/test")
    async def test_endpoint():
        return {"status": "ok"}
    
    apibrain.enable(app)
    client = TestClient(app)
    
    # Verifica se a capacidade foi registrada
    response = client.get("/discover")
    capabilities = response.json()["capabilities"]
    assert len(capabilities) == 1
    assert capabilities[0]["name"] == "test_endpoint"

def test_config_customization():
    """Testa se as configurações são aplicadas corretamente"""
    app = FastAPI()
    config = APIBrainConfig(
        description="API de teste",
        version="2.0.0"
    )
    apibrain = APIBrain(config=config)
    apibrain.enable(app)
    
    client = TestClient(app)
    response = client.get("/openapi.json")
    context = response.json()["x-apibrain-context"]
    assert context["description"] == "API de teste" 