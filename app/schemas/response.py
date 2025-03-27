from typing import Optional,Any

from pydantic import BaseModel


class ResponseModel(BaseModel):
    success: bool = True
    data: Any | None = None
    message: str | None = None