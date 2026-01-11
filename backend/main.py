from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session
import os
from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base

# 1. Load Environment Variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Database Setup (SQLAlchemy)
# We check if DATABASE_URL exists to avoid errors if .env is missing
if not DATABASE_URL:
    raise ValueError("No DATABASE_URL found in .env file")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 3. Define the Database Table (Model)
class ItemModel(Base):
    __tablename__ = "items"
<<<<<<< HEAD
    print ("hellos")
=======
    print ("reem")
    
>>>>>>> 7ec9373b0b72914a070851beff3e3f4e2af649aa

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)

# Create the tables in the database automatically
Base.metadata.create_all(bind=engine)

# 4. Pydantic Models (Schemas)
# This is used for validation when sending/receiving data
class ItemCreate(BaseModel):
    name: str
    description: str = None

class ItemResponse(ItemCreate):
    id: int
    
    class Config:
        # This tells Pydantic to read data even if it's not a dict (it's an ORM object)
        orm_mode = True 

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 5. Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/api/items", response_model=list[ItemResponse])
def get_items(db: Session = Depends(get_db)):
    print("hello alaa and reem")
    print("hiiii")
    # Query the database
    items = db.query(ItemModel).all()
    return items

@app.post("/api/items", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    # Create a new database model instance
    db_item = ItemModel(name=item.name, description=item.description)
    
    # Add to session and commit
    db.add(db_item)
    db.commit()
    
    # Refresh to get the new ID assigned by the database
    db.refresh(db_item)
    return db_item

@app.get("/api/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    # Query for a specific item by ID
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return item