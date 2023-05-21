"""empty message

Revision ID: ce3915e4f92d
Revises: 5f915d9d6881
Create Date: 2023-05-20 18:21:46.743965

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce3915e4f92d'
down_revision = '5f915d9d6881'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('aluguel', schema=None) as batch_op:
        batch_op.add_column(sa.Column('forma_pagamento', sa.String(length=3), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('aluguel', schema=None) as batch_op:
        batch_op.drop_column('forma_pagamento')

    # ### end Alembic commands ###
