#OM VIGHNHARTAYE NAMO NAMAH 
# :
from fastapi import FastAPI 
from starlette.middleware.cors import CORSMiddleware

from app.api.Books.bookCrud import router as bookRouter
from app.api.author.authorCRUD import router as authorRouter
from app.api.genere.genereCRUD import router as genereCRUD
from app.api.reviews.reviewCRUD import router as reviewsRouter

def include_routers(app):
    app.include_router(reviewsRouter)
    app.include_router(genereCRUD)
    app.include_router(authorRouter)
    app.include_router(bookRouter)
    return



def start_application():
    app = FastAPI(docs_url="/api/docs")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Adjust this to specific origins if needed
        allow_credentials=True,
        allow_methods=["*"],  # Allow all HTTP methods
        allow_headers=["*"],  # Allow all headers
    )


    include_routers(app)

    return app

app = start_application()