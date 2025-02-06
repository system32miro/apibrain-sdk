from pydantic import BaseModel
from typing import Optional

class APIBrainConfig(BaseModel):
    description: str = "API compatível com APIBrain Standard"
    version: str = "1.0.0"
    base_url: Optional[str] = None 