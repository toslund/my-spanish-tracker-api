from typing import Optional
from .prediction_service import Assesment
import random

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
   


app.include_router(api_router, prefix=settings.API_V1_STR)


#TODO migrate these routes to new router in new project structure
# @app.get("/vocab")
# def read_vocab():
#     return corpus.random_vocab()

# @app.get("/vocab/assesment")
# def read_item():
#     print(random.randint(1, 100))
#     assesment = Assesment.from_corpus(corpus)
#     assesment.generate_questions()
#     print(assesment)
#     print(assesment.questions[0].word)
#     return assesment.questions




