from app.repositories.base import RepoBase
from app.models.category import Category
from app.schemas import CategoryCreate, CategoryUpdate


class CategoryRepo(RepoBase[Category, CategoryCreate, CategoryUpdate]):
    pass


category = CategoryRepo(Category)