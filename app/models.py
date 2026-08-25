from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    ingredients = Column(Text, nullable=False)  # comma separated, keeping it simple
    instructions = Column(Text, nullable=False)
    prep_minutes = Column(Integer, default=0)
    servings = Column(Integer, default=1)
