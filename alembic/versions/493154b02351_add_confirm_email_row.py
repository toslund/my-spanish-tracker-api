"""add confirm_email row

Revision ID: 493154b02351
Revises: 7978cd8837fd
Create Date: 2022-01-07 12:17:30.706973

"""
from alembic import op
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy import Column, String


# revision identifiers, used by Alembic.
revision = '493154b02351'
down_revision = '7978cd8837fd'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user',
        Column('confirm_email', Boolean, default=False)
    )
    op.add_column('user',
        Column('learner_type',  String(50))
    )
    op.add_column('user',
        Column('learner_level',  String(50))
    )


def downgrade():
    op.drop_column('user', 'confirm_email')
    op.drop_column('user', 'learner_type')
    op.drop_column('user', 'learner_level')
