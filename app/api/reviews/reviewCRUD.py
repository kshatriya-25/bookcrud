#OM VIGHNHARTAYE NAMO NAMAH :

from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List
from ...schemas.masterSchema import GenreCreate, GenreResponse, BookResponse, ReviewCreate, ReviewResponse
from ...modals.masters import Genre, Book, BookGenre, Review
from ...database.session import getdb

router = APIRouter()



@router.post("/reviews/", response_model=ReviewResponse, tags=['review'])
def add_review(user_id: int = Form(...), book_id: int = Form(...), rating: float = Form(...), review_text: str = Form(None), db: Session = Depends(getdb)):
    try:
        review = Review(user_id=user_id, book_id=book_id, rating=rating, review_text=review_text)
        db.add(review)
        db.commit()
        db.refresh(review)
        return review
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/books/{book_id}/reviews", response_model=List[ReviewResponse], tags=['review'])
def get_reviews(book_id: int, db: Session = Depends(getdb)):
    try:
        reviews = db.query(Review).filter(Review.book_id == book_id).all()
        return reviews
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/reviews/{review_id}", response_model=ReviewResponse, tags=['review'])
def update_review(review_id: int, rating: float = Form(...), review_text: str = Form(None), db: Session = Depends(getdb)):
    try:
        review = db.query(Review).filter(Review.id == review_id).first()
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        
        review.rating = rating
        review.review_text = review_text
        db.commit()
        db.refresh(review)
        return review
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/reviews/{review_id}", tags=['review'])
def delete_review(review_id: int, db: Session = Depends(getdb)):
    try:
        review = db.query(Review).filter(Review.id == review_id).first()
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        
        db.delete(review)
        db.commit()
        return {"message": "Review deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
