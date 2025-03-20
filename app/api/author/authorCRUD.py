#OM VIGHNHARTAYE NAMO NAMAH :

from ...modals.masters import *
from fastapi import APIRouter , Depends , HTTPException
from typing import List
from ...schemas.masterSchema import *
from sqlalchemy.orm import Session
from ...database.session import getdb
router = APIRouter()

from ...modals.masters import *
from fastapi import APIRouter, Depends, HTTPException, Form
from typing import List
from ...schemas.masterSchema import *
from sqlalchemy.orm import Session
from ...database.session import getdb
from pydantic import ValidationError

router = APIRouter()

@router.post("/authors/", response_model=AuthorResponse , tags=['author'])
def create_author(name: str = Form(...), db: Session = Depends(getdb)):
    try:
        author_data = AuthorCreate(name=name)
        db_author = Author(name=author_data.name)
        db.add(db_author)
        db.commit()
        db.refresh(db_author)
        return db_author
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())

@router.get("/authors/", response_model=List[AuthorResponse], tags=['author'])
def get_authors(db: Session = Depends(getdb)):
    authors = db.query(Author).all()
    return authors

@router.get("/authors/{author_id}", response_model=AuthorResponse, tags=['author'])
def get_author(author_id: int, db: Session = Depends(getdb)):
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author