from typing import Optional
from pydantic import BaseModel
from typing import TypeVar, Generic
T = TypeVar("T")

class GenericResponse(BaseModel, Generic[T]):
    success:bool = True
    message: str
    data: Optional[T] = None