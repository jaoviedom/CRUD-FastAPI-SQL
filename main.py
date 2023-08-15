from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class UserBase(BaseModel):
  name: str
  age: int
  status: str

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user:UserBase, db: db_dependency):
  db_user = models.User(**user.dict())
  db.add(db_user)
  db.commit()

@app.get("/users/", status_code=status.HTTP_200_OK)
async def read_users(db: db_dependency):
  users = db.query(models.User).all()
  return users