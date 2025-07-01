from pydantic import BaseModel, Field
from typing import Dict, List, Literal, Optional, Union


# Represents a single property inside "properties"
class Property(BaseModel):
    type: Literal["string", "boolean", "number", "integer", "object", "array"]
    description: Optional[str] = None


# Represents the full "params" schema
class ParamsSchema(BaseModel):
    type: Literal["object"] = "object"
    properties: Dict[str, Property]
    required: List[str]


# Final tool spec model
class ToolSpec(BaseModel):
    name: str
    description: str
    method: Literal["GET", "POST", "PUT", "DELETE"]
    endpoint: str
    params: ParamsSchema


class User(BaseModel):
    name: str
    email: str
    password: str
