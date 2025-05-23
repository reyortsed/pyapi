
from typing import Any
from pydantic import BaseModel

def update_model_from_dto(dto: BaseModel, model: Any) -> Any:
    updates = dto.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(model, key, value)
    return model
