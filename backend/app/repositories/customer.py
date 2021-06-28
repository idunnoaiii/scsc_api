from app.repositories.base import RepoBase
from app.models.customer import Customer
from app.schemas import CategoryCreate, CategoryUpdate


class CustomerRepo(RepoBase[Customer, CategoryCreate, CategoryUpdate]):
    pass


customer = CustomerRepo(Customer)