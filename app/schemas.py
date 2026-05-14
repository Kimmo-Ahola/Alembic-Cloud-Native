# i schemas lägger vi till pydantic
# detta är API-datamodeller
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ErrorResponse(BaseModel):
    detail: str = Field(examples=["Task 42 not found"])


"""
Modeller för category med pydantic
"""


class CategoryBase(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100,  # ska egentligen matcha databasen, eller ska helst göra det
        description="Category name, must be unique",
        examples=["Work", "Home"],
    )

    ConfigDict(
        from_attributes=True, 
        str_strip_whitespace=True, 
        extra="forbid"
    )


class CategoryCreate(CategoryBase):
    pass


# kan vara patch så vi vill ha optional
class CategoryUpdate(BaseModel):
    name: str | None = Field(
        min_length=1,
        max_length=100,  # ska egentligen matcha databasen, eller ska helst göra det
        description="Optional. Omit to leave unchanged",
    )


class CategoryRead(CategoryBase):
    category_id: int # måste heta samma som kolumnen eftersom de är kopplade

    model_config = ConfigDict(from_attributes=True)


class TaskBase(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=255,
        description="Readable content of a Task model",
        examples=["Buy milk", "Do your homework", "Send in report"],
    )
    description: str | None = None

    category_id: int | None = Field(
        default=None,
        description="Id of the category. Optional",
        examples=[1]
    )


class TaskCreate(TaskBase):  # i POST
    pass


class TaskUpdate(BaseModel):  # i PUT/PATCH
    """Partial update. Only the included fields will be changed."""

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="New title. Omit to leave unchanged.",
    )
    description: str | None = None
    done: bool | None = None

    category_id: int | None = None


class TaskRead(TaskBase):  # i GET
    id: int
    done: bool
    created_at: datetime

    category: CategoryRead | None = None

    model_config = ConfigDict(
        from_attributes=True,
        frozen=True,  # readonly, immutable, kan inte ändras efteråt
        extra="forbid",  # denna förbjuder extra fält i body med felkod 422. Mer användbar i POST/PUT/PATCH
        str_strip_whitespace=True,
    )


# task.id - funkar pga ConfigDict ovan
# task["id"] - funkar inte pga ConfigDict ovan
