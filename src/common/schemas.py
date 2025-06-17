import humps
from pydantic import BaseModel


class ErrorSchema(BaseModel):
    message: str


class ResponseSchema(BaseModel):
    class Config:
        extra = "allow"
        alias_generator = humps.camelize
        populate_by_name = True
