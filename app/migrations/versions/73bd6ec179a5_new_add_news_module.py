"""new add news module

Revision ID: 73bd6ec179a5
Revises: bce97fd8c387
Create Date: 2024-02-21 11:52:52.400721

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text


# revision identifiers, used by Alembic.
revision: str = '73bd6ec179a5'
down_revision: Union[str, None] = 'bce97fd8c387'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Проверьте, есть ли в таблице systems записи с id, отличным от   0
    system_exists = op.get_bind().execute(text("SELECT EXISTS(SELECT   1 FROM systems WHERE id !=   0 LIMIT   1)")).scalar()

    if not system_exists:
        # Если нет, добавьте новую запись в таблицу systems
        op.execute(text("INSERT INTO systems (id, description) VALUES (1, 'Default System')"))

    # Установите действительные значения system_id для существующих записей
    op.execute(text("UPDATE tickets SET system_id =   1 WHERE system_id =   0"))
    # Добавьте внешний ключ
    op.create_foreign_key(None, 'tickets', 'systems', ['system_id'], ['id'], ondelete='CASCADE')

def downgrade():
    # Удалите внешний ключ
    op.drop_constraint(None, 'tickets', type_='foreignkey')
    # Верните system_id обратно к   0 для записей, которые были обновлены
    op.execute(text("UPDATE tickets SET system_id =   0 WHERE system_id =   1"))
    # Удалите запись из таблицы systems, если она была добавлена в процессе миграции
    op.execute(text("DELETE FROM systems WHERE id =   1"))