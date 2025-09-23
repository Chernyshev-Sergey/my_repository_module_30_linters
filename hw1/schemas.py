from pydantic import BaseModel


class RecipeBook(BaseModel):
    name_of_the_dish: str
    cooking_time_in_minutes: str
    list_of_ingredients: str
    description: str
    number_of_views: int


class RecipeBookIn(RecipeBook):
    pass


class RecipeBookOut(RecipeBook):
    id: int

    class Config:
        from_attributes = True


class RecipeBookId(BaseModel):
    name_of_the_dish: str
    cooking_time_in_minutes: str
    list_of_ingredients: str
    description: str


class RecipeBookList(BaseModel):
    id: int
    name_of_the_dish: str
    cooking_time_in_minutes: str
    number_of_views: int
