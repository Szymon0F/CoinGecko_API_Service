"""initial migration

Revision ID: initial_migration
Revises: 
Create Date: 2024-02-20 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'initial_migration'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create coin_prices table
    op.create_table(
        'coin_prices',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('coin_id', sa.String(), nullable=False),
        sa.Column('symbol', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('current_price', sa.Float(), nullable=True),
        sa.Column('market_cap', sa.Float(), nullable=True),
        sa.Column('market_cap_rank', sa.Integer(), nullable=True),
        sa.Column('total_volume', sa.Float(), nullable=True),
        sa.Column('price_change_24h', sa.Float(), nullable=True),
        sa.Column('price_change_percentage_24h', sa.Float(), nullable=True),
        sa.Column('market_dominance', sa.Float(), nullable=True),
        sa.Column('volume_to_market_cap_ratio', sa.Float(), nullable=True),
        sa.Column('last_updated', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes
    op.create_index('idx_coin_price_date', 'coin_prices',
                    ['coin_id', 'created_at'])
    op.create_index('idx_market_cap_rank', 'coin_prices', ['market_cap_rank'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('idx_market_cap_rank')
    op.drop_index('idx_coin_price_date')

    # Drop table
    op.drop_table('coin_prices')
