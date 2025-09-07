from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class BaseEntitySchema(BaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime

class ResponseSchema(BaseSchema):
    message: str
    success: bool = True

class ErrorSchema(BaseSchema):
    message: str
    success: bool = False
    error_code: Optional[str] = None