from pydantic import BaseModel

# from decimal import Decimal


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    id: int
    username: str
    role: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


class ProductUpdateInput(BaseModel):
    price: float


class Customer(BaseModel):
    username: str
    full_name: str


class Order(BaseModel):
    customer_id: int
    customer: Customer


class OrderInput(BaseModel):
    product_id: int
    quantity: int
    discount: float | None = 0
    email: str | None = None
