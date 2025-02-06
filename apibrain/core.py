from typing import List, Dict, Any, Optional, Callable
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .config import APIBrainConfig
import json
from fastapi.middleware.cors import CORSMiddleware
from functools import lru_cache

class APIBrain:
    def __init__(self, config: Optional[APIBrainConfig] = None):
        self.config = config or APIBrainConfig()
        self.capabilities: List[Dict[str, Any]] = []
        self._cache = {}
    
    @lru_cache(maxsize=128)
    def get_capability_schema(self, name: str) -> Dict[str, Any]:
        """Retorna schema cacheado de uma capacidade"""
        return next((c for c in self.capabilities if c["name"] == name), {})
    
    def register_capability(self, capability_meta: Dict[str, Any]):
        """Registra uma nova capacidade"""
        self.capabilities.append(capability_meta)
        self._cache.clear()  # Limpa cache ao registrar nova capacidade
    
    def enable(self, app: FastAPI):
        """Habilita o APIBrain em uma aplicação FastAPI"""
        # Adiciona middleware UTF-8
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        @app.get("/discover", tags=["APIBrain"])
        async def discover():
            return JSONResponse(
                content={"capabilities": self.capabilities},
                headers={"Content-Type": "application/json; charset=utf-8"}
            )
        
        # Modifica o OpenAPI schema
        original_openapi = app.openapi
        def custom_openapi():
            if app.openapi_schema:
                return app.openapi_schema
            
            openapi_schema = original_openapi()
            openapi_schema["x-apibrain-context"] = {
                "description": self.config.description,
                "version": self.config.version,
                "capabilities": self.capabilities
            }
            
            app.openapi_schema = openapi_schema
            return app.openapi_schema
        
        app.openapi = custom_openapi 