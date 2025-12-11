from pydantic import BaseModel, HttpUrl
from typing import Optional, List

class LinkBase(BaseModel):
    title: str
    url: str
    position: int

class LinkCreate(LinkBase):
    pass

class LinkResponse(LinkBase):
    id: int
    click_count: int
    
    class Config:
        from_attributes = True

class ProfileCreate(BaseModel):
    slug: str
    name: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    theme: Optional[str] = "light"
    password: Optional[str] = None
    links: List[LinkCreate] = []

class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    theme: Optional[str] = None
    password: Optional[str] = None
    links: Optional[List[LinkCreate]] = None

class ProfileResponse(BaseModel):
    id: int
    slug: str
    name: str
    bio: Optional[str]
    avatar_url: Optional[str]
    theme: str
    links: List[LinkResponse]
    
    class Config:
        from_attributes = True
