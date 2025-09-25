from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False)
    user_email = Column(String, unique=True, index=True)
    age = Column(Integer)
    ZIP = Column(String)
    recommendations = Column(String) 
