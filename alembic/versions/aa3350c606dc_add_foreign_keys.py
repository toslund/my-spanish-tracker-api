"""add foreign keys

Revision ID: aa3350c606dc
Revises: 3a292ebdea7b
Create Date: 2021-12-07 20:15:54.867461

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String


# revision identifiers, used by Alembic.
revision = 'aa3350c606dc'
down_revision = '3a292ebdea7b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('vocab',
        Column('lemma_uuid', UUID(as_uuid=True), ForeignKey('lemma.uuid'), nullable=True, default=None)
    )
    op.add_column('definition',
        Column('vocab_uuid', UUID(as_uuid=True), ForeignKey('vocab.uuid'))
    )
    op.add_column('item',
        Column('owner_uuid', UUID(as_uuid=True), ForeignKey('user.uuid'))
    )

def downgrade():
    op.drop_column('vocab', 'lemma_uuid')
    op.drop_column('definition', 'vocab_uuid')
    op.drop_column('item', 'owner_uuid')
