from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from schemas import (
    User,
    UserInDB,
    Token,
    TokenData,
    ProductUpdateInput,
    Order,
    OrderInput,
)

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db = {
    "sayed": {
        "id": 1,
        "username": "sayed",
        "full_name": "Ahmed Abd Elgawad",
        "email": "sayed@example.com",
        # password="g=z%UY334FzY"
        "hashed_password": "$2b$12$xIJZShyOKuTSBdIPPyZpkOr8vJmK0laSucSsFcY1yjixw5u3pnngu",
        "role": "admin",
        "disabled": False,
    },
    "reda": {
        "id": 2,
        "username": "reda",
        "full_name": "Reda Elmesery",
        "email": "reda@example.com",
        # password="KA5=u33|@]8t"
        "hashed_password": "$2b$12$EKeRgu1rSAeOczp1dLAebOSbReMcTR1P0qTYVCiU5M.FgUAI1d3Ay",
        "role": "customer",
        "disabled": False,
    },
    "ibrahim": {
        "id": 3,
        "username": "ibrahim",
        "full_name": "Ibrahim Nour",
        "email": "ibrahim@example.com",
        # password=",@3#62S&#'tp"
        "hashed_password": "$2b$12$xMiVL2TMo0vLmPdV3ltde.9KTVecVE5R9EnIGK5V6CroyQ/CEBazK",
        "role": "customer",
        "disabled": False,
    },
}


fake_order_db = [
    {
        "customer_id": "2",
        "customer": {
            "username": "reda",
            "full_name": "Reda Elmesery",
        },
    },
    {
        "customer_id": "3",
        "customer": {
            "username": "ibrahim",
            "full_name": "Ibrahim Nour",
        },
    },
]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def only_admin_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    if current_user.role != "admin":
        raise HTTPException(status_code=400, detail="Not Allowed user")
    return current_user


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]


@app.post("/products/{product_id}")
async def update_product(
    product_id: int,
    product_input: ProductUpdateInput,
    current_user: Annotated[User, Depends(only_admin_user)],
):
    # should be avalible for onlyy admin users
    # function level
    product = {
        "id": product_id,
        "name": "product1",
    }
    product.update(product_input)
    return product


def get_all_orders():
    return fake_order_db


def get_user_orders(user_id: int):
    return [order for order in fake_order_db if int(order["customer_id"]) == user_id]


@app.get("/orders/", response_model=list[Order])
async def read_user_orders(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    # customer should get his orders only not all orders
    # object level
    if current_user.role == "admin":
        return get_all_orders()
    else:
        return get_user_orders(current_user.id)


@app.post("/orders/")
async def create_order(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    # customer can place order but can't use discount property
    # property level
    return {}
