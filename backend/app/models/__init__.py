from .category import categories as categories_table, Category as CategoryModel
from .customer import customers as customers_table, Customer as CustomerModel
from .item import items as items_table, Item as ItemModel
from .order import orders as orders_table, order_items as order_item_table, Order as OrderModel, OrderItem as OrderItemModel
from .discount import discount as discount_table, Discount as DiscountModel
from .user import users as users_table, User as UserModel
from .user import roles as roles_table, Role as RoleModel