from typing import List
from pydantic import BaseModel, ConfigDict, Field


class RecipeBase(BaseModel):
    title: str
    ingredients: List[str]
    instructions: str
    prep_minutes: int = Field(default=0, ge=0)
    servings: int = Field(default=1, ge=1)


class RecipeCreate(RecipeBase):
    pass


class RecipeUpdate(BaseModel):
    title: str | None = None
    ingredients: List[str] | None = None
    instructions: str | None = None
    prep_minutes: int | None = None
    servings: int | None = None


class Recipe(RecipeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
