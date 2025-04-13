# backend/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    configs = relationship("ClientConfig", back_populates="user")

class ClientConfig(Base):
    __tablename__ = "client_configs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    location = Column(String, index=True)
    private_key = Column(String)
    public_key = Column(String)
    assigned_ip = Column(String)
    config_text = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    
    user = relationship("User", back_populates="configs")

