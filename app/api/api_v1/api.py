from fastapi import APIRouter

from app.api.api_v1.endpoints import items, login, users, vocabs, definitions, lemmas, decks, questions #, utils

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(vocabs.router, prefix="/vocabs", tags=["vocabs"])
api_router.include_router(definitions.router, prefix="/definitions", tags=["definitions"])
api_router.include_router(lemmas.router, prefix="/lemmas", tags=["lemmas"])
api_router.include_router(decks.router, prefix="/decks", tags=["decks"])
api_router.include_router(questions.router, prefix="/questions", tags=["questions"])

