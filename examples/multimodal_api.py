from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from apibrain import APIBrain, capability
from typing import Optional, List

class ImageAnalysisResponse(BaseModel):
    objects: List[str]
    confidence: float
    tags: List[str]

class TextAnalysisResponse(BaseModel):
    sentiment: str
    score: float
    entities: List[str]

app = FastAPI(title="Multimodal API Example")
apibrain = APIBrain()

@capability(
    name="analyze_image",
    description="Analisa uma imagem e retorna objetos detectados",
    apibrain=apibrain
)
@app.post("/image/analyze")
async def analyze_image(file: UploadFile = File(...)) -> ImageAnalysisResponse:
    # Simulação de análise
    return ImageAnalysisResponse(
        objects=["pessoa", "carro"],
        confidence=0.95,
        tags=["outdoor", "dia"]
    )

@capability(
    name="analyze_text",
    description="Analisa texto para sentimento e entidades",
    apibrain=apibrain
)
@app.post("/text/analyze")
async def analyze_text(text: str) -> TextAnalysisResponse:
    return TextAnalysisResponse(
        sentiment="positivo",
        score=0.8,
        entities=["produto", "empresa"]
    )

apibrain.enable(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 