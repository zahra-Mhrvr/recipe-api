from sqlalchemy.orm import Session

from app import models, schemas


def _to_db_ingredients(ingredients: list[str]) -> str:
    return ", ".join(i.strip() for i in ingredients)


def _from_db_ingredients(ingredients: str) -> list[str]:
    return [i.strip() for i in ingredients.split(",") if i.strip()]


def _to_schema(recipe: models.Recipe) -> schemas.Recipe:
    return schemas.Recipe(
        id=recipe.id,
        title=recipe.title,
        ingredients=_from_db_ingredients(recipe.ingredients),
        instructions=recipe.instructions,
        prep_minutes=recipe.prep_minutes,
        servings=recipe.servings,
    )


def create_recipe(db: Session, recipe: schemas.RecipeCreate) -> schemas.Recipe:
    db_recipe = models.Recipe(
        title=recipe.title,
        ingredients=_to_db_ingredients(recipe.ingredients),
        instructions=recipe.instructions,
        prep_minutes=recipe.prep_minutes,
        servings=recipe.servings,
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return _to_schema(db_recipe)


def get_recipe(db: Session, recipe_id: int) -> schemas.Recipe | None:
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    return _to_schema(db_recipe) if db_recipe else None


def list_recipes(
    db: Session, skip: int = 0, limit: int = 20, ingredient: str | None = None
) -> list[schemas.Recipe]:
    query = db.query(models.Recipe)
    if ingredient:
        query = query.filter(models.Recipe.ingredients.ilike(f"%{ingredient}%"))
    db_recipes = query.offset(skip).limit(limit).all()
    return [_to_schema(r) for r in db_recipes]


def update_recipe(
    db: Session, recipe_id: int, updates: schemas.RecipeUpdate
) -> schemas.Recipe | None:
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not db_recipe:
        return None

    data = updates.model_dump(exclude_unset=True)
    if "ingredients" in data:
        data["ingredients"] = _to_db_ingredients(data["ingredients"])

    for field, value in data.items():
        setattr(db_recipe, field, value)

    db.commit()
    db.refresh(db_recipe)
    return _to_schema(db_recipe)


def delete_recipe(db: Session, recipe_id: int) -> bool:
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not db_recipe:
        return False
    db.delete(db_recipe)
    db.commit()
    return True
