from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import User, Link
from ..schemas import ProfileCreate, ProfileUpdate, ProfileResponse

router = APIRouter(prefix="/api/profiles", tags=["profiles"])

@router.post("", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
def create_profile(profile: ProfileCreate, db: Session = Depends(get_db)):
    """Create a new profile with links"""
    # Check if slug already exists
    existing_user = db.query(User).filter(User.slug == profile.slug).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Slug already exists"
        )
    
    # Create user
    new_user = User(
        slug=profile.slug,
        name=profile.name,
        bio=profile.bio,
        avatar_url=profile.avatar_url,
        theme=profile.theme,
        password=profile.password
    )
    db.add(new_user)
    db.flush()  # Get the user id
    
    # Create links
    for link_data in profile.links:
        new_link = Link(
            user_id=new_user.id,
            title=link_data.title,
            url=link_data.url,
            position=link_data.position
        )
        db.add(new_link)
    
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{slug}", response_model=ProfileResponse)
def get_profile(slug: str, db: Session = Depends(get_db)):
    """Get profile by slug"""
    user = db.query(User).filter(User.slug == slug).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    return user

@router.put("/{slug}", response_model=ProfileResponse)
def update_profile(slug: str, profile: ProfileUpdate, db: Session = Depends(get_db)):
    """Update profile and links"""
    user = db.query(User).filter(User.slug == slug).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    # Update user fields
    if profile.name is not None:
        user.name = profile.name
    if profile.bio is not None:
        user.bio = profile.bio
    if profile.avatar_url is not None:
        user.avatar_url = profile.avatar_url
    if profile.theme is not None:
        user.theme = profile.theme
    if profile.password is not None:
        user.password = profile.password
    
    # Update links if provided
    if profile.links is not None:
        # Delete existing links
        db.query(Link).filter(Link.user_id == user.id).delete()
        
        # Create new links
        for link_data in profile.links:
            new_link = Link(
                user_id=user.id,
                title=link_data.title,
                url=link_data.url,
                position=link_data.position
            )
            db.add(new_link)
    
    db.commit()
    db.refresh(user)
    return user
