from fastapi import FastAPI, Body
from pydantic import BaseModel
from apibrain import APIBrain, capability, APIBrainConfig
from typing import List, Optional

# Models
class WeatherResponse(BaseModel):
    temperature: float
    condition: str
    humidity: Optional[float] = None

class CalculationRequest(BaseModel):
    a: float
    b: float
    operation: str = "sum"

class CalculationResponse(BaseModel):
    result: float
    operation: str

# Configurar API
app = FastAPI(title="Test API")
config = APIBrainConfig(
    description="API de teste do APIBrain SDK",
    version="1.0.0"
)
apibrain = APIBrain(config=config)

# Endpoints
@capability(
    name="get_weather",
    description="Previsão do tempo por cidade",
    apibrain=apibrain
)
@app.get("/weather/{city}")
async def get_weather(city: str, detailed: bool = False) -> WeatherResponse:
    """Retorna previsão do tempo para uma cidade"""
    return WeatherResponse(
        temperature=22.5,
        condition="Ensolarado",
        humidity=65.0 if detailed else None
    )

@capability(
    name="calculate",
    description="Realiza operações matemáticas",
    apibrain=apibrain
)
@app.post("/calculate")
async def calculate(request: CalculationRequest) -> CalculationResponse:
    """Realiza cálculos matemáticos"""
    operations = {
        "sum": lambda x, y: x + y,
        "multiply": lambda x, y: x * y
    }
    result = operations[request.operation](request.a, request.b)
    return CalculationResponse(result=result, operation=request.operation)

# Habilitar APIBrain
apibrain.enable(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 