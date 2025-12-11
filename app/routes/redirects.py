from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Link

router = APIRouter(prefix="/r", tags=["redirects"])

@router.get("/{slug}/{index}")
def redirect_link(slug: str, index: int, db: Session = Depends(get_db)):
    """Redirect to link URL and increment click count"""
    # Get user
    user = db.query(User).filter(User.slug == slug).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    # Get link by position (index)
    link = db.query(Link).filter(
        Link.user_id == user.id,
        Link.position == index
    ).first()
    
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link not found"
        )
    
    # Increment click count
    link.click_count += 1
    db.commit()
    
    # Redirect to the URL
    return RedirectResponse(url=link.url, status_code=status.HTTP_302_FOUND)
