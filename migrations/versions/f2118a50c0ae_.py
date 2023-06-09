"""empty message

Revision ID: f2118a50c0ae
Revises: edf3e27b181c
Create Date: 2023-04-22 12:36:08.325367

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2118a50c0ae'
down_revision = 'edf3e27b181c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('carro', schema=None) as batch_op:
        batch_op.add_column(sa.Column('descricao', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('descricao_imagem', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('url_imagem', sa.String(length=255), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('carro', schema=None) as batch_op:
        batch_op.drop_column('url_imagem')
        batch_op.drop_column('descricao_imagem')
        batch_op.drop_column('descricao')

    # ### end Alembic commands ###
