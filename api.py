"""Items API with POST and GET endpoints, using dedicated validation classes per endpoint."""

from fastapi import Depends, FastAPI, Query

from database import get_items, init_db, insert_items
from models import GetItemsRequest, GetItemsResponse, PostItemRequest, PostItemResponse

app = FastAPI()


def get_items_query(
    limit: int | None = Query(None, description="Max number of items to return"),
    offset: int | None = Query(None, description="Number of items to skip"),
) -> GetItemsRequest:
    """Dependency that validates GET query params via GetItemsRequest."""
    return GetItemsRequest(limit=limit, offset=offset)


@app.on_event("startup")
def startup() -> None:
    """Initialize the database on startup."""
    init_db()


@app.post("/items", response_model=PostItemResponse)
def post_items(body: PostItemRequest) -> PostItemResponse:
    """Add one or more items to the database. Validates request and response."""
    items_to_insert = [{"name": item.name, "price": item.price} for item in body.items]
    inserted = insert_items(items_to_insert)
    return PostItemResponse(items=inserted)


@app.get("/items", response_model=GetItemsResponse)
def get_items_endpoint(
    query: GetItemsRequest = Depends(get_items_query),
) -> GetItemsResponse:
    """Retrieve items from the database. Validates request and response."""
    items = get_items(limit=query.limit, offset=query.offset)
    return GetItemsResponse(items=items)
