from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    bio = Column(Text, nullable=True)
    avatar_url = Column(String(500), nullable=True)
    theme = Column(String(20), default="light")
    password = Column(String(100), nullable=True)  # Simple password protection
    
    links = relationship("Link", back_populates="user", cascade="all, delete-orphan")

class Link(Base):
    __tablename__ = "links"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(100), nullable=False)
    url = Column(String(500), nullable=False)
    position = Column(Integer, nullable=False)
    click_count = Column(Integer, default=0)
    
    user = relationship("User", back_populates="links")
