#OM VIGHNHARTAYE NAMO NAMAH :

from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import List
from ...schemas.masterSchema import *
from ...modals.masters import Genre, Book, BookGenre, Review
from ...database.session import getdb

router = APIRouter()

@router.get("/books/{book_id}/average-rating", tags=['analytics'])
def get_average_rating(book_id: int, db: Session = Depends(getdb)):
    try:
        avg_rating = db.query(func.avg(Review.rating)).filter(Review.book_id == book_id).scalar()
        if avg_rating is None:
            raise HTTPException(status_code=404, detail="No ratings found for this book")
        return {"book_id": book_id, "average_rating": float(avg_rating)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics/most-reviewed-books", tags=['analytics'])
def get_most_reviewed_books(db: Session = Depends(getdb)):
    try:
        books = (
            db.query(Book, func.count(Review.id).label("review_count"))
            .join(Review, Book.id == Review.book_id)
            .group_by(Book.id)
            .order_by(func.count(Review.id).desc())
            .limit(10)
            .all()
        )
        return [{"book_id": book.id, "title": book.title, "review_count": count} for book, count in books]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics/user-review-count/{user_id}", tags=['analytics'])
def get_user_review_count(user_id: int, db: Session = Depends(getdb)):
    try:
        review_count = db.query(func.count(Review.id)).filter(Review.user_id == user_id).scalar()
        return {"user_id": user_id, "review_count": review_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))