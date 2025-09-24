from typing import List


import models
import schemas
from database import session
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import update
from sqlalchemy.future import select

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.post("/recipes", response_model=schemas.RecipeBookOut)
async def recipe_book_post(book: schemas.RecipeBookIn) -> models.RecipeBook:
    new_recipe = models.RecipeBook(**book.model_dump())
    async with session.begin():
        session.add(new_recipe)
    await session.commit()
    return new_recipe


@router.get("/recipes", response_model=List[schemas.RecipeBookList])
async def recipe_book_get():
    response = await session.execute(
        select(models.RecipeBook).order_by(
            models.RecipeBook.number_of_views.desc(),
            models.RecipeBook.cooking_time_in_minutes.desc(),
        )
    )
    return response.scalars().all()


@router.get("/recipes/{recipe_id}", response_model=schemas.RecipeBookId)
async def recipe_details(recipe_id: int) -> models.RecipeBook:
    response = await session.execute(
        select(models.RecipeBook).filter(models.RecipeBook.id == recipe_id)
    )
    out_res = response.scalars().one()
    await session.execute(
        update(models.RecipeBook)
        .where(models.RecipeBook.id == recipe_id)
        .values(number_of_views=out_res.number_of_views + 1)
    )
    await session.commit()
    return out_res


@router.get("/recipes_in_html", response_class=HTMLResponse)
async def recipe_book_get_html(request: Request):
    response = await session.execute(
        select(models.RecipeBook).order_by(
            models.RecipeBook.number_of_views.desc(),
            models.RecipeBook.cooking_time_in_minutes.desc(),
        )
    )
    recipes = response.scalars().all()
    return templates.TemplateResponse(
        "recipe_book.html", {"request": request, "recipes": recipes}
    )


@router.get("/recipes_in_html/{recipe_id}", response_class=HTMLResponse)
async def recipe_details_html(recipe_id: int, request: Request):
    response = await session.execute(
        select(models.RecipeBook).filter(models.RecipeBook.id == recipe_id)
    )
    recipe = response.scalars().one()
    await session.execute(
        update(models.RecipeBook)
        .where(models.RecipeBook.id == recipe_id)
        .values(number_of_views=recipe.number_of_views + 1)
    )
    await session.commit()
    return templates.TemplateResponse(
        "recipe_details.html", {"request": request, "recipe": recipe}
    )
