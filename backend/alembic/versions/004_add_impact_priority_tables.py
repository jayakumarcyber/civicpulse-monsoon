"""Add impact_assessments and priority_assessments tables

Revision ID: 004_add_impact_priority_tables
Revises: 003_add_drainage_graph_tables
Create Date: 2026-08-16 23:55:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '004_add_impact_priority_tables'
down_revision: Union[str, None] = '003_add_drainage_graph_tables'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'impact_assessments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ward_id', sa.Integer(), nullable=False),
        sa.Column('prediction_id', sa.Integer(), nullable=True),
        sa.Column('potential_population_exposure', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('hospital_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('school_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('emergency_facility_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('transport_facility_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('critical_facility_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('exposed_road_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('exposed_drain_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('historical_waterlogging_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('data_quality_status', sa.String(length=50), nullable=False, server_default='VERIFIED_SPATIAL_EXPOSURE'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['prediction_id'], ['risk_predictions.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['ward_id'], ['wards.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_impact_assessments_id', 'impact_assessments', ['id'], unique=False)
    op.create_index('ix_impact_assessments_prediction_id', 'impact_assessments', ['prediction_id'], unique=False)
    op.create_index('ix_impact_assessments_ward_id', 'impact_assessments', ['ward_id'], unique=False)

    op.create_table(
        'priority_assessments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('impact_assessment_id', sa.Integer(), nullable=False),
        sa.Column('ward_id', sa.Integer(), nullable=False),
        sa.Column('priority_score', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('priority_level', sa.String(length=20), nullable=False),
        sa.Column('priority_reasons', sa.JSON(), nullable=False),
        sa.Column('calculation_version', sa.String(length=50), nullable=False, server_default='CivicPriority_v1_DEMO'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['impact_assessment_id'], ['impact_assessments.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['ward_id'], ['wards.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_priority_assessments_id', 'priority_assessments', ['id'], unique=False)
    op.create_index('ix_priority_assessments_impact_assessment_id', 'priority_assessments', ['impact_assessment_id'], unique=False)
    op.create_index('ix_priority_assessments_priority_level', 'priority_assessments', ['priority_level'], unique=False)
    op.create_index('ix_priority_assessments_ward_id', 'priority_assessments', ['ward_id'], unique=False)


def downgrade() -> None:
    op.drop_table('priority_assessments')
    op.drop_table('impact_assessments')
