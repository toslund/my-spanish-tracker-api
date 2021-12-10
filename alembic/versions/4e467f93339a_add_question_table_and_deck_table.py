"""add question table and deck table

Revision ID: 4e467f93339a
Revises: aa3350c606dc
Create Date: 2021-12-09 08:09:17.777016

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision = '4e467f93339a'
down_revision = 'aa3350c606dc'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'question',
        Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
        ## TODO change to uuid type in production
        Column('uuid', UUID(as_uuid=True), nullable=False, unique=True),
        Column('correct', Boolean),
        Column('correctness', Integer),
        Column('date_added', DateTime, nullable=False, server_default=func.now()),

        ## relationship
        # Column('lemma_uuid', UUID(as_uuid=True), ForeignKey('lemma.uuid')),
    )

    op.create_table(
        'deck',
        Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
        ## TODO change to uuid type in production
        Column('uuid', UUID(as_uuid=True), nullable=False, unique=True),
        Column('date_added', DateTime, nullable=False, server_default=func.now()),

        ## relationship
        # Column('lemma_uuid', UUID(as_uuid=True), ForeignKey('lemma.uuid')),
    )

def downgrade():
    op.drop_table('question')
    op.drop_table('deck')
