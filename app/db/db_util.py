import os, json
from datetime import datetime
from sqlalchemy.orm import Session
from typing import List, Tuple
from app import crud, schemas
from app.core.config import settings
from app.db import base  # noqa: F401

from fastapi.encoders import jsonable_encoder

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.user.create(db, obj_in=user_in)  # noqa: F841

def dump_data(db: Session):
    print('dumping lemmas')
    lemmas = crud.lemma.get_multi(db, limit = None)
    for l in lemmas:
        break
    lemmas = [jsonable_encoder(schemas.LemmaDBDump.from_orm(lemma)) for lemma in lemmas]

    print('dumping vocabs')
    vocabs = crud.vocab.get_multi(db, limit = None)
    for v in vocabs:
        break
    vocabs = [jsonable_encoder(schemas.VocabDBDump.from_orm(vocab)) for vocab in vocabs]

    print('dumping definitions')
    definitions = crud.definition.get_multi(db, limit = None)
    for d in definitions:
        break
    definitions = [jsonable_encoder(schemas.DefinitionDBDump.from_orm(d)) for d in definitions]


    return (lemmas, vocabs, definitions)

def populate_seed_data_objects(db: Session, lemmas, vocabs, definitions) -> None:

    print('adding lemmas')
    lemma_models = []
    for lemma in lemmas:
        lemma_in = schemas.LemmaDBDump(
            uuid=lemma['uuid'],
            lemma=lemma['lemma'],
            pos=lemma['pos'],
            rank=lemma['rank'],
            total_count=lemma['total_count'],
            academic_count=lemma['academic_count'],
            news_count=lemma['news_count'],
            fiction_count=lemma['fiction_count'],
            spoken_count=lemma['spoken_count'],
            note_data=lemma['note_data'],
            note_qaqc=lemma['note_qaqc'],
            note_grammar=lemma['note_grammar'],
            note=lemma['note'],
            date_added=datetime.fromisoformat(lemma['date_added']),
            date_deprecated=None if not lemma['date_deprecated'] else datetime.fromisoformat(lemma['date_deprecated'])
        )
        lemma_models.append(lemma_in)
    print(len(lemma_models))
    crud.lemma.batch_create(db, objs_in=lemma_models)

    print('adding vocabs')
    vocab_models = []
    for vocab in vocabs:
        vocab_in = schemas.VocabDBDump(
            uuid=vocab['uuid'],
            word=vocab['word'],
            pos=vocab['pos'],
            note_data=vocab['note_data'],
            note_qaqc=vocab['note_qaqc'],
            note_grammar=vocab['note_grammar'],
            note=vocab['note'],
            lemma_uuid=vocab['lemma_uuid'],
            date_added=datetime.fromisoformat(lemma['date_added']),
            date_deprecated=None if not vocab['date_deprecated'] else datetime.fromisoformat(lemma['date_deprecated'])
        )
        vocab_models.append(vocab_in)
    crud.vocab.batch_create(db, objs_in=vocab_models)

    print('adding definitions')
    definition_models = []
    for definition in definitions:
        definition_in = schemas.DefinitionDBDump(
            uuid=definition['uuid'],
            definition=definition['definition'],
            region=definition['region'],
            rank=definition['rank'],
            note=definition['note'],
            vocab_uuid=definition['vocab_uuid'],
            date_added=datetime.fromisoformat(definition['date_added']),
            date_deprecated=None if not definition['date_deprecated'] else datetime.fromisoformat(definition['date_deprecated'])
        )
        definition_models.append(definition_in)
    crud.definition.batch_create(db, objs_in=definition_models)


def populate_seed_data(db: Session) -> None:
    dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    
    lemma_json = os.path.join(dir_path, 'json_data', 'lemmas.json')
    json_lemma_data = os.path.abspath(lemma_json)
    with open(json_lemma_data, 'r') as file:
        print('adding lemmas')
        lemma_data = json.load(file)
        for x in lemma_data.values():
            crud.lemma.create_from_dict(db, dict_in = x)

    vocab_json = os.path.join(dir_path, 'json_data', 'vocab.json')
    json_vocab_data = os.path.abspath(vocab_json)
    with open(json_vocab_data, 'r') as file:
        print('adding vocab')
        vocab_data = json.load(file)
        for x in vocab_data.values():
            crud.vocab.create_from_dict(db, dict_in = x)

    definition_json = os.path.join(dir_path, 'json_data', 'definitions.json')
    json_definition_data = os.path.abspath(definition_json)
    with open(json_definition_data, 'r') as file:
        print('adding defs')
        definition_data = json.load(file)
        for x in definition_data.values():
            crud.definition.create_from_dict(db, dict_in = x)