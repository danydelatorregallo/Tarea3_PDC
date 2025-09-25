import os
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Depends, Header, status
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, JSON, select
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# Cargar variables de entorno 
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Configuración de la base de datos
DATABASE_URL = "sqlite:///./users.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#Iniciar app
app = FastAPI(title="User API", version="1.0")

#crear tablas
Base.metadata.create_all(bind=engine)

# Modelo SQLAlchemy
class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False)
    user_email = Column(String, unique=True, index=True, nullable=False)
    age = Column(Integer, nullable=True)
    recommendations = Column(JSON, nullable=True)
    ZIP = Column(String, nullable=True)

# Pydantic schemas
class UserCreate(BaseModel):
    user_name: str
    user_id: int
    user_email: EmailStr
    age: Optional[int] = None
    recommendations: List[str] = []
    ZIP: Optional[str] = None

class UserUpdate(BaseModel):
    user_name: Optional[str] = None
    user_email: Optional[EmailStr] = None
    age: Optional[int] = None
    recommendations: Optional[List[str]] = None
    ZIP:Optional[str] = None

class  UserResponse(BaseModel):
    user_id: int
    user_name: str
    user_email: EmailStr
    age: Optional[int]
    recommendations: Optional[List[str]]
    ZIP: Optional[str]

    class Config:
        orm_mode = True

# Dependencias DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key")
    
# FastAPI app
app = FastAPI(title="User API", version="1.0")

@app.post("/api/v1/users/{user_id}", response_model=UserResponse, dependencies=[Depends(verify_api_key)])
def create_user(user: UserCreate, db: Session = Depends(get_db)): #email duplicado
    if db.execute(select(User).where(User.user_email == user.user_email)).scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Email already exists")
    
    if db.get(User, user.user_id): #verifica user_id duplicado
        raise HTTPException(status_code=409, detail="User ID already exists")
    
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.put("/api/v1/users/{user_id}", response_model=UserResponse, dependencies=[Depends(verify_api_key)])
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/api/v1/users/{user_id}", response_model=UserResponse, dependencies=[Depends(verify_api_key)])
def get_user(user_id: int, db:Session = Depends(get_db)):
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/api/v1/users/{user_id}", dependencies=[Depends(verify_api_key)])
def delete_user(user_id: int, db: Session= Depends(get_db)):
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"status": f"User {user_id} deleted"}