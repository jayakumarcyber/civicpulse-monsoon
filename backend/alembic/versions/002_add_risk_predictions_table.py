"""Add risk_predictions table for storing multi-horizon ML predictions

Revision ID: 002_add_risk_predictions_table
Revises: 001_initial_postgis_schema
Create Date: 2026-08-16 23:20:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '002_add_risk_predictions_table'
down_revision: Union[str, None] = '001_initial_postgis_schema'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'risk_predictions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ward_id', sa.Integer(), nullable=False),
        sa.Column('prediction_timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('horizon_hours', sa.Integer(), nullable=False),
        sa.Column('predicted_probability', sa.Float(), nullable=False),
        sa.Column('risk_level', sa.String(length=20), nullable=False),
        sa.Column('model_version', sa.String(length=50), nullable=False, server_default='XGBoost_v1_DEMO'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['ward_id'], ['wards.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_risk_predictions_horizon_hours', 'risk_predictions', ['horizon_hours'], unique=False)
    op.create_index('ix_risk_predictions_id', 'risk_predictions', ['id'], unique=False)
    op.create_index('ix_risk_predictions_prediction_timestamp', 'risk_predictions', ['prediction_timestamp'], unique=False)
    op.create_index('ix_risk_predictions_risk_level', 'risk_predictions', ['risk_level'], unique=False)
    op.create_index('ix_risk_predictions_ward_id', 'risk_predictions', ['ward_id'], unique=False)


def downgrade() -> None:
    op.drop_table('risk_predictions')
