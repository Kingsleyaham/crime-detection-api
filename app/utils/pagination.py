from typing import TypeVar, Generic

from pydantic import BaseModel, Field
from sqlmodel import Session, select, func

ModelType = TypeVar('ModelType')
ResponseType = TypeVar('ResponseType', bound=BaseModel)


class Pagination(BaseModel, Generic[ResponseType]):
    """Pagination response"""
    data: list[ResponseType]
    total: int
    page: int
    size: int


def paginate(session: Session, model: type[ModelType], response_model: type[ResponseType],
             page: int = Field(default=1, ge=1), size: int = Field(default=20, ge=1, le=100)) -> Pagination[ModelType]:
    """
    Pagination helper function with query parameter support
    Args:
        session: Database session
        model: SQLModel to query
        response_model: Pydantic response model
        page: Current page number (default 1)
        size: Number of items per page (default 10, max 100)
    """
    offset = (page - 1) * size
    total = session.exec(select(func.count()).select_from(model)).one()

    query = select(model).offset(offset).limit(size)
    results = session.exec(query).all()

    data = [response_model.model_validate(data) for data in results]

    return Pagination(data=data, total=total, page=page, size=size)
