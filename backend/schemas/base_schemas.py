from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")

class PaginationMeta(BaseModel):
    total_records: int
    current_page: int
    total_pages: int
    next_page: Optional[int]
    prev_page: Optional[int]

class GenericResponse(BaseModel, Generic[T]):
    success:bool = True
    message: str
    data: Optional[T] = None
    meta: Optional[PaginationMeta] = None