from typing import Union
import redis
from fastapi import FastAPI
import os
from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI, status
from pydantic import BaseModel
from fastapi.exceptions import HTTPException


# from flask_caching import Cache
app = FastAPI()
redis_cli = redis.Redis(host='redis-18057.c14.us-east-1-3.ec2.redns.redis-cloud.com', port=18057, password='utgvvXEMTVMuMdIhHcWVZmKS31UeJwqN')
# Initialize Flask-Caching with Redis
# cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_HOST': redis_client})
# cache.init_app(app)

class Item(BaseModel):
    name: str
    
@app.get("/")
def read_root():
    return {"Hello": "World1"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
#async def create_item(item: Item):
# 新增 item 至 Redis
@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(item):
    # Add item to the Redis list
    # redis_cli.rpush("items", item.name)
    print(item.name)
    redis_cli.set('md',item)
    return {"message": "Item added successfully"}

# 取得 Redis 內的所有 items
@app.get("/items/", status_code=status.HTTP_200_OK)
async def get_items():
    # Retrieve items from the Redis list
    # items = redis_cli.lrange("items", 0, -1)
    redis_cli.get('md',item.name)
    return {"items": items}

# 刪除 Redis 內的特定 item
@app.delete("/items/{item_name}", status_code=status.HTTP_200_OK)
async def delete_item(item_name: str):
    # Delete a specific item from the Redis list
    if item_name not in redis_cli.lrange("items", 0, -1):
        raise HTTPException(status_code=404, detail="Item not found")
    redis_cli.lrem("items", 0, item_name)
    return {"message": f"Item '{item_name}' deleted successfully"}
