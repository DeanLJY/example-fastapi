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

# 新增 item 至 Redis
@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    # Add item to the Redis list
    redis_cli.rpush("items", item.name)
    return {"message": "Item added successfully"}
