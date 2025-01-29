from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import select, update
from sqlalchemy.exc import InvalidRequestError

from database import engine, session
from models_db import Base, RecipeDB, RecipesInfoDB
from models_routes import RecipeIn, RecipeInfoPydentic, RecipeOut


async def create_db():
    """Создает базу данных если ее нет"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db()
    yield


async def inc_counter(recipe_id: int):
    """Увеличивает параметр count_views на 1 из таблицы RecipesInfoDB"""
    await session.execute(
        update(RecipesInfoDB)
        .where(RecipesInfoDB.id == recipe_id)
        .values(count_views=RecipesInfoDB.count_views + 1)
    )
    await session.commit()


app = FastAPI(lifespan=lifespan)


@app.get("/recipes")
async def recipes_all() -> list[RecipeInfoPydentic]:
    """Получить все рецепт и вернуть их"""
    async with session.begin():
        result = await session.execute(
            select(RecipesInfoDB).order_by(
                RecipesInfoDB.count_views.desc(), RecipesInfoDB.cooking_time.desc()
            )
        )
        all_recipes = result.scalars().all()
        response = [RecipeInfoPydentic(**recipe.__dict__) for recipe in all_recipes]
        return response


@app.get("/recipes/{recipe_id}")
async def recipe_by_id(recipe_id: int) -> RecipeOut | None:
    """получить рецепт вернуть его, увеличить счетчик на 1"""
    result = await session.execute(select(RecipeDB).where(RecipeDB.id == recipe_id))
    recipe = result.scalar()

    if recipe:
        await inc_counter(recipe_id)
        recipe = RecipeOut(**recipe.__dict__)

    return recipe


@app.post("/recipes", status_code=201)
async def recipe_add(recipe: RecipeIn) -> RecipeOut:
    """Добавить рецепт"""
    new_recipe = RecipeDB(**recipe.model_dump())

    recipe_info = RecipesInfoDB(
        name=new_recipe.name, count_views=0, cooking_time=new_recipe.cooking_time
    )

    await session.commit()
    async with session.begin():
        new_recipe.info.append(recipe_info)
        session.add(new_recipe)

    return RecipeOut(**new_recipe.__dict__)
