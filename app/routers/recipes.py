from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.post("/", response_model=schemas.Recipe, status_code=201)
def create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    return crud.create_recipe(db, recipe)


@router.get("/", response_model=list[schemas.Recipe])
def list_recipes(
    skip: int = 0,
    limit: int = Query(default=20, le=100),
    ingredient: str | None = None,
    db: Session = Depends(get_db),
):
    return crud.list_recipes(db, skip=skip, limit=limit, ingredient=ingredient)


@router.get("/{recipe_id}", response_model=schemas.Recipe)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = crud.get_recipe(db, recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.patch("/{recipe_id}", response_model=schemas.Recipe)
def update_recipe(
    recipe_id: int, updates: schemas.RecipeUpdate, db: Session = Depends(get_db)
):
    recipe = crud.update_recipe(db, recipe_id, updates)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.delete("/{recipe_id}", status_code=204)
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_recipe(db, recipe_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Recipe not found")
