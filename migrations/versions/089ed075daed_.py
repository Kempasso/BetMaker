"""empty message

Revision ID: 089ed075daed
Revises: 
Create Date: 2024-11-04 20:56:31.426163

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '089ed075daed'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bet',
    sa.Column('id', sa.VARCHAR(length=32), nullable=False),
    sa.Column('event_id', sa.VARCHAR(length=32), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('bet_pkey'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bet')
    # ### end Alembic commands ###