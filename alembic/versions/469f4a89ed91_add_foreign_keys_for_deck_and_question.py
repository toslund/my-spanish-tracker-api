"""add foreign keys for deck and question

Revision ID: 469f4a89ed91
Revises: 4e467f93339a
Create Date: 2021-12-09 12:22:49.687659

"""
from alembic import op
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, ForeignKey


# revision identifiers, used by Alembic.
revision = '469f4a89ed91'
down_revision = '4e467f93339a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('question',
        Column('vocab_uuid', UUID(as_uuid=True), ForeignKey('vocab.uuid'))
    )
    op.add_column('question',
        Column('deck_uuid', UUID(as_uuid=True), ForeignKey('deck.uuid'))
    )
    op.add_column('deck',
        Column('owner_uuid', UUID(as_uuid=True), ForeignKey('user.uuid'))
    )


def downgrade():
    op.drop_column('question', 'vocab_uuid')
    op.drop_column('question', 'deck_uuid')
    op.drop_column('deck', 'owner_uuid')
