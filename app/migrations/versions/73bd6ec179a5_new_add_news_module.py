"""new add news module

Revision ID: 73bd6ec179a5
Revises: bce97fd8c387
Create Date: 2024-02-21 11:52:52.400721

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '73bd6ec179a5'
down_revision: Union[str, None] = 'bce97fd8c387'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'tickets', 'systems', ['system_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tickets', type_='foreignkey')
    # ### end Alembic commands ###
