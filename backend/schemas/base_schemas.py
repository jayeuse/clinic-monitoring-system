from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")

class GenericResponse(BaseModel, Generic[T]):
    success:bool = True
    message: str
    data: Optional[T] = None