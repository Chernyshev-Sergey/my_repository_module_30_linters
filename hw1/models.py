from database import Base
from sqlalchemy import Column, Integer, String


class RecipeBook(Base):
    __tablename__ = "RecipeBook"
    id = Column(Integer, primary_key=True, index=True)
    name_of_the_dish = Column(String, index=True)
    list_of_ingredients = Column(String, index=True)
    description = Column(String, index=True)
    cooking_time_in_minutes = Column(String, index=True)
    number_of_views = Column(Integer, index=True)
