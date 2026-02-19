# extra models

## multiple models

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()

class UserInMultipleModels(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None
    
class UserOutMultipleModels(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None
    
class UserInDBMultipleModels(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: str | None = None
    
def fake_password_hasher_multi(raw_password: str):
    return "supersecret" + raw_password

def fake_save_user_multi(user_in: UserInMultipleModels):
    hashed_password = fake_password_hasher_multi(user_in.password)
    user_in_db = UserInDBMultipleModels(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    print(user_in_db)
    return user_in_db

@app.post("/user/", response_model=UserOutMultipleModels)
async def create_user_multi(user_in: UserInMultipleModels):
    user_saved = fake_save_user_multi(user_in)
    return user_saved


## reduce duplicate

class UserBaseReduceDuplicate(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None
    
class UserInReduceDuplicate(UserBaseReduceDuplicate):
    password: str
    
class UserOutReduceDuplicate(UserBaseReduceDuplicate):
    pass

class UserInDBReduceDuplicate(UserBaseReduceDuplicate):
    hashed_password: str
    
def fake_password_hasher_reduce_duplicate(raw_password: str):
    return "supersecret" + raw_password

def fake_save_user_reduce_duplicate(user_in: UserInReduceDuplicate):
    hashed_password = fake_password_hasher_reduce_duplicate(user_in.password)
    user_in_db = UserInDBReduceDuplicate(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    print(user_in_db)
    return user_in_db

@app.post("/user/reduce_duplicate", response_model=UserOutReduceDuplicate)
async def create_user_reduce_duplicate(user_in: UserInReduceDuplicate):
    user_saved = fake_save_user_reduce_duplicate(user_in)
    return user_saved


## union of anyOf

class BaseItem(BaseModel):
    description: str
    type: str
    
class CarItem(BaseItem):
    type: str = "car"
    
class PlaneItem(BaseItem):
    type: str = "plane"
    size: int
    
items = {
    "item1": {
        "description": "A car item",
        "type": "car"
    },
    "item2": {
        "description": "A plane item",
        "type": "plane",
        "size": 5
    }
}

@app.get("/items/{item_id}", response_model=PlaneItem | CarItem)
async def read_item(item_id: str):
    return items[item_id]


## list of models
class Item(BaseModel):
    name: str
    description: str | None = None
    
items_list = [
    {"name": "item1", "description": "The first item"},
    {"name": "item2", "description": "The second item"},
    {"name": "item3", "description": "The third item"},
]

@app.get("/items/", response_model=list[Item])
async def read_items():
    return items_list


# response with arbitrary dict
@app.get("/arbitrary_dict/", response_model=dict[str, int])
async def read_arbitrary_dict():
    return {"key1": 1, "key2": 2, "key3": 3}