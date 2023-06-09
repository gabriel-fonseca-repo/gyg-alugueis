"""empty message

Revision ID: 098195468854
Revises: a82a15c27d87
Create Date: 2023-05-21 16:05:28.628600

"""
from alembic import op
import flask_security
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '098195468854'
down_revision = 'a82a15c27d87'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('carro',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('placa', sa.String(length=8), nullable=False),
    sa.Column('modelo', sa.String(length=100), nullable=False),
    sa.Column('marca', sa.String(length=100), nullable=False),
    sa.Column('descricao', sa.String(length=255), nullable=False),
    sa.Column('descricao_imagem', sa.Text(), nullable=False),
    sa.Column('url_imagem', sa.String(length=255), nullable=False),
    sa.Column('custo_diario', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('capacidade_pessoas', sa.Integer(), nullable=False),
    sa.Column('quantidade_alugueis', sa.Integer(), nullable=True),
    sa.Column('data_de_insercao', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('placa')
    )
    op.create_table('role',
    sa.Column('page_url', sa.String(length=80), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('permissions', flask_security.datastore.AsaList(), nullable=True),
    sa.Column('update_datetime', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('cpf', sa.String(length=14), nullable=True),
    sa.Column('celular', sa.String(length=15), nullable=True),
    sa.Column('data_cadastro', sa.DateTime(), nullable=True),
    sa.Column('fs_webauthn_user_handle', sa.String(length=64), nullable=True),
    sa.Column('mf_recovery_codes', flask_security.datastore.AsaList(), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('us_phone_number', sa.String(length=128), nullable=True),
    sa.Column('username', sa.String(length=255), nullable=True),
    sa.Column('us_totp_secrets', sa.Text(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('fs_uniquifier', sa.String(length=64), nullable=False),
    sa.Column('confirmed_at', sa.DateTime(), nullable=True),
    sa.Column('last_login_at', sa.DateTime(), nullable=True),
    sa.Column('current_login_at', sa.DateTime(), nullable=True),
    sa.Column('last_login_ip', sa.String(length=64), nullable=True),
    sa.Column('current_login_ip', sa.String(length=64), nullable=True),
    sa.Column('login_count', sa.Integer(), nullable=True),
    sa.Column('tf_primary_method', sa.String(length=64), nullable=True),
    sa.Column('tf_totp_secret', sa.String(length=255), nullable=True),
    sa.Column('tf_phone_number', sa.String(length=128), nullable=True),
    sa.Column('create_datetime', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('update_datetime', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('celular'),
    sa.UniqueConstraint('cpf'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('fs_uniquifier'),
    sa.UniqueConstraint('fs_webauthn_user_handle'),
    sa.UniqueConstraint('us_phone_number'),
    sa.UniqueConstraint('username')
    )
    op.create_table('aluguel',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('inicio_aluguel', sa.DateTime(), nullable=False),
    sa.Column('final_aluguel', sa.DateTime(), nullable=False),
    sa.Column('total_pagar', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('forma_pagamento', sa.String(length=3), nullable=True),
    sa.Column('carro_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['carro_id'], ['carro.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles_users',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('roles_users')
    op.drop_table('aluguel')
    op.drop_table('user')
    op.drop_table('role')
    op.drop_table('carro')
    # ### end Alembic commands ###
