from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    ...


class RecipeDB(Base):
    __tablename__ = 'recipes'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    cooking_time: Mapped[int]
    ingredients: Mapped[str]
    description: Mapped[str]

    def __repr__(self):
        return f'{self.id=} {self.name=}'


class RecipesInfoDB(Base):
    __tablename__ = 'all_recipes'
    id: Mapped[int] = mapped_column(ForeignKey('recipes.id'), primary_key=True)
    name: Mapped[str]
    count_views: Mapped[int]
    cooking_time: Mapped[int]

    recipe: Mapped["RecipeDB"] = relationship("RecipeDB", backref='info', uselist=False)

    def __repr__(self):
        return f'{self.name} {self.count_views}'
