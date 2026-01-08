from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    name: str
    description: str = None

items_db = []

@app.get("/")
def read_root():
    env = os.getenv("ENV", "local")
    return {"message": "Hello World", "environment": env}

@app.get("/api/items")
def get_items():
    print("hello alaa and reem")
    print("hiiii")
    print("hello alaa and reem")
    return {"items": items_db}

@app.post("/api/items")
def create_item(item: Item):
    items_db.append(item.dict())
    return {"message": "Item created", "item": item}

@app.get("/api/items/{item_id}")
def get_item(item_id: int):
    if item_id < len(items_db):
        return items_db[item_id]
    return {"error": "Item not found"}
