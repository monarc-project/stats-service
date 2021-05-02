"""Added new latitude, longitude columns for the clients.

Revision ID: 71bb20af690a
Revises: b5013a08ce19
Create Date: 2021-04-28 10:54:38.474710

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71bb20af690a'
down_revision = 'b5013a08ce19'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('client', sa.Column('latitude', sa.Float(), nullable=True))
    op.add_column('client', sa.Column('longitude', sa.Float(), nullable=True))
    op.create_unique_constraint(None, 'stats', ['uuid'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'stats', type_='unique')
    op.drop_column('client', 'longitude')
    op.drop_column('client', 'latitude')
    # ### end Alembic commands ###
