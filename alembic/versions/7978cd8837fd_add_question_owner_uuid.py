"""add question.owner_uuid

Revision ID: 7978cd8837fd
Revises: 469f4a89ed91
Create Date: 2021-12-10 10:26:33.961238

"""
from alembic import op
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = '7978cd8837fd'
down_revision = '469f4a89ed91'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('question',
        Column('owner_uuid', UUID(as_uuid=True), ForeignKey('user.uuid'))
    )


def downgrade():
    op.drop_column('question', 'owner_uuid')
