from pydantic import BaseModel
from typing import Optional

class ReadUserDTO(BaseModel):
    id: int
    name: str
    email: str
    model_config = {
        "from_attributes": True
    }

class CreateUserDTO(BaseModel):
    name: str
    email: str
    password: str

class UpdateUserDTO(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None