from pydantic import BaseModel


class RecipeIn(BaseModel):
    name: str
    cooking_time: int
    ingredients: str
    description: str


class RecipeOut(RecipeIn):
    id: int


class RecipeInfoPydentic(BaseModel):
    id: int
    name: str
    count_views: int
    cooking_time: int
