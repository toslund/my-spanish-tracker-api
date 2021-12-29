"""create db

Revision ID: 3a292ebdea7b
Revises: 
Create Date: 2021-12-04 12:33:45.691952

"""
from sqlalchemy.sql.elements import True_
from alembic import op
import sqlalchemy as sa

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy.sql import func


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
        Column('uuid', UUID(as_uuid=True), nullable=False, unique=True),
        Column('word', String(50), nullable=False),
        Column('pos', String(50)),
        Column('note_data', String()),
        Column('note_qaqc', String()),
        Column('note_grammar', String()),
        Column('note', String()),
        Column('date_added', DateTime, nullable=False, server_default=func.now()),
        Column('date_deprecated', DateTime),
        ## relationship
        # Column('lemma_uuid', UUID(as_uuid=True), ForeignKey('lemma.uuid')),
        
    )

    op.create_table(
        'lemma',
        Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
        ## TODO change to uuid type in production
        Column('uuid', UUID(as_uuid=True), nullable=False, unique=True),
        Column('word', String(50), nullable=False),
        Column('pos', String(50)),

        Column('total_count', Integer),
        Column('academic_count', Integer),
        Column('news_count', Integer),
        Column('fiction_count', Integer),
        Column('spoken_count', Integer),

        Column('note_data', String()),
        Column('note_qaqc', String()),
        Column('note_grammar', String()),
        Column('note', String()),
        Column('date_added', DateTime, nullable=False, server_default=func.now()),
        Column('date_deprecated', DateTime),
    
    )

    op.create_table(
        'definition',
        Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
        ## TODO change to uuid type in production
        Column('uuid', UUID(as_uuid=True), nullable=False, unique=True),
        Column('content', String(), nullable=False),
        Column('note', String),
        Column('rank', Integer),
        Column('region', String()),
        Column('date_added', DateTime, nullable=False, server_default=func.now()),
        Column('date_deprecated', DateTime),
        ## relationship 
        # Column('vocab_uuid', UUID(as_uuid=True), ForeignKey('lemma.uuid')), 

    )

    op.create_table(
        'user',
        Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
        ## TODO change to uuid type in production
        Column('uuid', UUID(as_uuid=True), nullable=False, unique=True),
        Column('full_name', String),
        Column('email', String, unique=True),
        Column('hashed_password', String, nullable=False),
        Column('is_active', Boolean(), default=True),
        Column('is_superuser', Boolean(), default=False),
        Column('date_added', DateTime, nullable=False, server_default=func.now()),
    )

    op.create_table(
        'item',
        Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
        ## TODO change to uuid type in production
        Column('uuid', UUID(as_uuid=True), nullable=False, unique=True),
        Column('title', String, nullable=False),
        Column('description', String),
        Column('date_added', DateTime, nullable=False, server_default=func.now()),
        ## relationship
        # Column('owner_uuid', UUID(as_uuid=True), ForeignKey('user.uuid')), 

    )

def downgrade():
    pass
