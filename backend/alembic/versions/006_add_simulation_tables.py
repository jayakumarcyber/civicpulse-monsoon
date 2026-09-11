"""Add simulation_scenarios and simulation_results tables

Revision ID: 006_add_simulation_tables
Revises: 005_add_optimization_tables
Create Date: 2026-08-17 00:15:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '006_add_simulation_tables'
down_revision: Union[str, None] = '005_add_optimization_tables'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'simulation_scenarios',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('scenario_id', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('rainfall_multiplier', sa.Float(), nullable=False, server_default='1.0'),
        sa.Column('rainfall_24h_mm', sa.Float(), nullable=False, server_default='140.0'),
        sa.Column('rainfall_48h_mm', sa.Float(), nullable=False, server_default='180.0'),
        sa.Column('rainfall_72h_mm', sa.Float(), nullable=False, server_default='220.0'),
        sa.Column('available_teams', sa.Integer(), nullable=False, server_default='3'),
        sa.Column('available_hours', sa.Float(), nullable=False, server_default='24.0'),
        sa.Column('available_budget_inr', sa.Float(), nullable=False, server_default='50000.0'),
        sa.Column('is_preset', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('scenario_id')
    )
    op.create_index('ix_simulation_scenarios_id', 'simulation_scenarios', ['id'], unique=False)
    op.create_index('ix_simulation_scenarios_scenario_id', 'simulation_scenarios', ['scenario_id'], unique=True)

    op.create_table(
        'simulation_results',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('scenario_id', sa.String(length=50), nullable=False),
        sa.Column('high_risk_wards_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('critical_priority_wards_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('total_potential_exposure', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('selected_actions_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('used_budget_inr', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('used_teams_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('baseline_vs_scenario_summary', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['scenario_id'], ['simulation_scenarios.scenario_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_simulation_results_id', 'simulation_results', ['id'], unique=False)
    op.create_index('ix_simulation_results_scenario_id', 'simulation_results', ['scenario_id'], unique=False)


def downgrade() -> None:
    op.drop_table('simulation_results')
    op.drop_table('simulation_scenarios')
