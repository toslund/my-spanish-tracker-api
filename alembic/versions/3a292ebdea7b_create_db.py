"""create db

Revision ID: 3a292ebdea7b
Revises: 
Create Date: 2021-12-04 12:33:45.691952

"""
from sqlalchemy.sql.elements import True_
from alembic import op
import sqlalchemy as sa

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.sql.sqltypes import Boolean


# revision identifiers, used by Alembic.
revision = '3a292ebdea7b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'vocab',
        Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
        ## TODO change to uuid type in production
        Column('uuid', String(36), nullable=False, unique=True),
        Column('word', String(50), nullable=False),
        Column('pos', String(10)),
        Column('note_data', String()),
        Column('note_qaqc', String()),
        Column('note_grammar', String()),
        Column('note', String()),
        Column('date_added', DateTime),
        Column('date_deprecated', DateTime),
        ## relationship
        # Column('lemma_uuid', String(36), ForeignKey('lemma.uuid')),
        
    )

    op.create_table(
        'lemma',
        Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
        ## TODO change to uuid type in production
        Column('uuid', String(36), nullable=False, unique=True),
        Column('lemma', String(50), nullable=False),
        Column('pos', String(10)),
        Column('rank', Integer, unique=True),

        Column('total_count', Integer),
        Column('academic_count', Integer),
        Column('news_count', Integer),
        Column('fiction_count', Integer),
        Column('spoken_count', Integer),

        Column('note_data', String()),
        Column('note_qaqc', String()),
        Column('note_grammar', String()),
        Column('note', String()),
        Column('date_added', DateTime),
        Column('date_deprecated', DateTime),
    
    )

    op.create_table(
        'definition',
        Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
        ## TODO change to uuid type in production
        Column('uuid', String(36), nullable=False),
        Column('definition', String(), nullable=False),
        Column('note', String),
        Column('rank', Integer),
        Column('region', String()),
        Column('date_added', DateTime),
        Column('date_deprecated', DateTime),
        ## relationship 
        # Column('vocab_uuid', String(36), ForeignKey('lemma.uuid')), 

    )

    op.create_table(
        'user',
        Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
        ## TODO change to uuid type in production
        Column('uuid', String(36), nullable=False),
        Column('full_name', String(36)),
        Column('email', String(), unique=True),
        Column('hashed_password', String, nullable=False),
        Column('is_active', Boolean(), default=True),
        Column('is_superuser', Boolean(), default=False),
    )

    op.create_table(
        'item',
        Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
        ## TODO change to uuid type in production
        Column('uuid', String(36), nullable=False),
        Column('title', String, nullable=False),
        Column('description', String),
        ## relationship
        # Column('owner_uuid', String(36), ForeignKey('user.uuid')), 

    )

def downgrade():
    pass
