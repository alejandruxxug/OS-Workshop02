"""Pydantic validation models for the items API. All inherit from BaseModel."""

from datetime import datetime
from pydantic import BaseModel


class ItemBase(BaseModel):
    """Base item fields for request validation."""

    name: str
    price: float


class ItemSchema(BaseModel):
    """Full item schema including id and created_at for responses."""

    id: int
    name: str
    price: float
    created_at: datetime


# POST endpoint validation
class PostItemRequest(BaseModel):
    """Request validator for POST /items."""

    items: list[ItemBase]


class PostItemResponse(BaseModel):
    """Response validator for POST /items."""

    items: list[ItemSchema]


# GET endpoint validation
class GetItemsRequest(BaseModel):
    """Request validator for GET /items query params."""

    limit: int | None = None
    offset: int | None = None


class GetItemsResponse(BaseModel):
    """Response validator for GET /items."""

    items: list[ItemSchema]
