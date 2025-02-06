from functools import wraps
from typing import Callable, Dict, Any, get_type_hints
from .core import APIBrain
import inspect

def _get_simple_schema(type_hint: Any) -> Dict[str, Any]:
    """Retorna schema simples para tipos básicos"""
    if type_hint == str:
        return {"type": "string"}
    elif type_hint == int:
        return {"type": "integer"}
    elif type_hint == float:
        return {"type": "number"}
    elif type_hint == bool:
        return {"type": "boolean"}
    elif hasattr(type_hint, 'schema'):  # Pydantic model
        return type_hint.schema()
    return {"type": "string"}  # fallback

def capability(name: str, description: str, apibrain: APIBrain):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        
        # Extrai tipos e parâmetros
        hints = get_type_hints(func)
        params = inspect.signature(func).parameters
        
        # Schema de entrada
        properties = {}
        for param_name, param in params.items():
            if param_name in hints:
                param_type = hints[param_name]
                properties[param_name] = _get_simple_schema(param_type)
        
        input_schema = {
            "type": "object",
            "properties": properties
        }
        
        # Schema de saída
        return_type = hints.get('return')
        output_schema = _get_simple_schema(return_type) if return_type else {}
        
        # Registra capacidade
        capability_meta = {
            "name": name,
            "description": description,
            "input_schema": input_schema,
            "output_schema": output_schema
        }
        
        apibrain.register_capability(capability_meta)
        return wrapper
    return decorator 