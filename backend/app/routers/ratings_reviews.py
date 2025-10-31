from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import User, Agent, Rating, Review
from app.schemas.schemas import RatingCreate, RatingResponse, ReviewCreate, ReviewUpdate, ReviewResponse
from app.routers.auth import get_current_active_user

router = APIRouter()


# Ratings
@router.post("/ratings", response_model=RatingResponse, status_code=status.HTTP_201_CREATED)
async def create_rating(
    rating: RatingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Check if agent exists
    agent = db.query(Agent).filter(Agent.id == rating.agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Check if user already rated this agent
    existing_rating = db.query(Rating).filter(
        Rating.agent_id == rating.agent_id,
        Rating.user_id == current_user.id
    ).first()
    
    if existing_rating:
        # Update existing rating
        existing_rating.rating = rating.rating
        db.commit()
        db.refresh(existing_rating)
        return existing_rating
    
    # Create new rating
    db_rating = Rating(
        agent_id=rating.agent_id,
        user_id=current_user.id,
        rating=rating.rating
    )
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    
    return db_rating


@router.get("/agents/{agent_id}/ratings", response_model=List[RatingResponse])
async def get_agent_ratings(agent_id: int, db: Session = Depends(get_db)):
    ratings = db.query(Rating).filter(Rating.agent_id == agent_id).all()
    return ratings


# Reviews
@router.post("/reviews", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    review: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Check if agent exists
    agent = db.query(Agent).filter(Agent.id == review.agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Create new review
    db_review = Review(
        agent_id=review.agent_id,
        user_id=current_user.id,
        comment=review.comment
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    
    # Add username to response
    response_dict = {
        "id": db_review.id,
        "agent_id": db_review.agent_id,
        "user_id": db_review.user_id,
        "comment": db_review.comment,
        "created_at": db_review.created_at,
        "updated_at": db_review.updated_at,
        "username": current_user.username
    }
    
    return response_dict


@router.get("/agents/{agent_id}/reviews", response_model=List[ReviewResponse])
async def get_agent_reviews(agent_id: int, db: Session = Depends(get_db)):
    reviews = db.query(Review).filter(Review.agent_id == agent_id).all()
    
    # Add usernames to reviews
    reviews_with_usernames = []
    for review in reviews:
        review_dict = {
            "id": review.id,
            "agent_id": review.agent_id,
            "user_id": review.user_id,
            "comment": review.comment,
            "created_at": review.created_at,
            "updated_at": review.updated_at,
            "username": review.user.username if review.user else None
        }
        reviews_with_usernames.append(review_dict)
    
    return reviews_with_usernames


@router.put("/reviews/{review_id}", response_model=ReviewResponse)
async def update_review(
    review_id: int,
    review_update: ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # Check if user is review creator
    if db_review.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db_review.comment = review_update.comment
    db.commit()
    db.refresh(db_review)
    
    response_dict = {
        "id": db_review.id,
        "agent_id": db_review.agent_id,
        "user_id": db_review.user_id,
        "comment": db_review.comment,
        "created_at": db_review.created_at,
        "updated_at": db_review.updated_at,
        "username": current_user.username
    }
    
    return response_dict


@router.delete("/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # Check if user is review creator or admin
    if db_review.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db.delete(db_review)
    db.commit()
    
    return None
