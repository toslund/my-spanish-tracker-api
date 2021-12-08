"""add foreign keys

Revision ID: aa3350c606dc
Revises: 3a292ebdea7b
Create Date: 2021-12-07 20:15:54.867461

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String


# revision identifiers, used by Alembic.
revision = 'aa3350c606dc'
down_revision = '3a292ebdea7b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('vocab',
        Column('lemma_uuid', String, ForeignKey('lemma.uuid'))
    )
    op.add_column('definition',
        Column('vocab_uuid', String, ForeignKey('vocab.uuid'))
    )


def downgrade():
    op.drop_column('vocab', 'lemma_uuid')
    op.drop_column('definition', 'vocab_uuid')
