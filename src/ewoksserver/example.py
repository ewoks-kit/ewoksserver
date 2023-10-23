"""
uvicorn ewoksserver.example:app --reload
"""


from typing import Union
from fastapi import FastAPI, Path, Query, Body, HTTPException
from pydantic import BaseModel, Field
from typing_extensions import Annotated

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

app = FastAPI(
    contact={
        "name": "ESRF - DAU",
        "url": "https://gitlab.esrf.fr/workflow/ewoks/ewoksserver/issues",
    },
    license_info={
        "name": "MIT",
        "identifier": "MIT",
    },
    openapi_tags=tags_metadata,
)


class Item(BaseModel):
    name: str
    description: Union[str, None] = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: Union[float, None] = None


class User(BaseModel):
    username: str
    full_name: Union[str, None] = None


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post(
    "/{pathparam}",
    summary="Summary of end-point",
    tags=["category"],
    response_description="Description of the return type",
    responses={404: {"description": "Item not found"}},
)
def root2(
    pathparam: Annotated[str, Path(title="Path parameter", description="")],
    queryparam: Annotated[
        Union[str, None], Query(title="Query parameter", description="")
    ] = None,
    item: Annotated[
        Union[Item, None], Body(title="Body parameter", description="")
    ] = None,
    user: Annotated[
        Union[User, None], Body(title="Body parameter", description="")
    ] = None,
):
    """
    Docs of end-point
    """
    raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Hello World"}
