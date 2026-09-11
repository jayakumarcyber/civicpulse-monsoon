"""Add municipal_teams, intervention_types, intervention_candidates, optimization_runs, and optimization_assignments tables

Revision ID: 005_add_optimization_tables
Revises: 004_add_impact_priority_tables
Create Date: 2026-08-17 00:05:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '005_add_optimization_tables'
down_revision: Union[str, None] = '004_add_impact_priority_tables'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'municipal_teams',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('team_id', sa.String(length=30), nullable=False),
        sa.Column('team_name', sa.String(length=100), nullable=False),
        sa.Column('skill_type', sa.String(length=50), nullable=False),
        sa.Column('daily_capacity_interventions', sa.Integer(), nullable=False, server_default='3'),
        sa.Column('working_hours', sa.Float(), nullable=False, server_default='8.0'),
        sa.Column('department', sa.String(length=100), nullable=False, server_default='Storm Water Drains Dept'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('team_id')
    )
    op.create_index('ix_municipal_teams_id', 'municipal_teams', ['id'], unique=False)
    op.create_index('ix_municipal_teams_skill_type', 'municipal_teams', ['skill_type'], unique=False)
    op.create_index('ix_municipal_teams_team_id', 'municipal_teams', ['team_id'], unique=True)

    op.create_table(
        'intervention_types',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('action_type', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('required_skill', sa.String(length=50), nullable=False),
        sa.Column('estimated_cost_inr', sa.Float(), nullable=False, server_default='5000.0'),
        sa.Column('estimated_duration_hours', sa.Float(), nullable=False, server_default='3.0'),
        sa.Column('eligibility_rule_description', sa.String(length=250), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('action_type')
    )
    op.create_index('ix_intervention_types_action_type', 'intervention_types', ['action_type'], unique=True)
    op.create_index('ix_intervention_types_id', 'intervention_types', ['id'], unique=False)

    op.create_table(
        'intervention_candidates',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('action_id', sa.String(length=50), nullable=False),
        sa.Column('ward_id', sa.Integer(), nullable=False),
        sa.Column('action_type', sa.String(length=50), nullable=False),
        sa.Column('estimated_cost', sa.Float(), nullable=False, server_default='5000.0'),
        sa.Column('estimated_duration', sa.Float(), nullable=False, server_default='3.0'),
        sa.Column('required_skill', sa.String(length=50), nullable=False),
        sa.Column('expected_benefit', sa.Float(), nullable=False, server_default='50.0'),
        sa.Column('evidence_summary', sa.String(length=250), nullable=False),
        sa.Column('data_quality', sa.String(length=50), nullable=False, server_default='DEMO_ELIGIBILITY_EVIDENCE'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['action_type'], ['intervention_types.action_type']),
        sa.ForeignKeyConstraint(['ward_id'], ['wards.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('action_id')
    )
    op.create_index('ix_intervention_candidates_action_id', 'intervention_candidates', ['action_id'], unique=True)
    op.create_index('ix_intervention_candidates_action_type', 'intervention_candidates', ['action_type'], unique=False)
    op.create_index('ix_intervention_candidates_id', 'intervention_candidates', ['id'], unique=False)
    op.create_index('ix_intervention_candidates_ward_id', 'intervention_candidates', ['ward_id'], unique=False)

    op.create_table(
        'optimization_runs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('run_id', sa.String(length=50), nullable=False),
        sa.Column('available_budget_inr', sa.Float(), nullable=False, server_default='50000.0'),
        sa.Column('available_hours', sa.Float(), nullable=False, server_default='24.0'),
        sa.Column('total_teams_count', sa.Integer(), nullable=False, server_default='3'),
        sa.Column('used_budget_inr', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('used_teams_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('selected_actions_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('optimization_status', sa.String(length=30), nullable=False, server_default='OPTIMAL'),
        sa.Column('infeasibility_reason', sa.String(length=250), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('run_id')
    )
    op.create_index('ix_optimization_runs_id', 'optimization_runs', ['id'], unique=False)
    op.create_index('ix_optimization_runs_run_id', 'optimization_runs', ['run_id'], unique=True)

    op.create_table(
        'optimization_assignments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('run_id', sa.String(length=50), nullable=False),
        sa.Column('action_id', sa.String(length=50), nullable=False),
        sa.Column('team_id', sa.String(length=30), nullable=False),
        sa.Column('ward_id', sa.Integer(), nullable=False),
        sa.Column('assigned_cost', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('assigned_duration', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('expected_benefit', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('selection_status', sa.String(length=20), nullable=False, server_default='SELECTED'),
        sa.Column('recommendation_reason', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['action_id'], ['intervention_candidates.action_id']),
        sa.ForeignKeyConstraint(['run_id'], ['optimization_runs.run_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['team_id'], ['municipal_teams.team_id']),
        sa.ForeignKeyConstraint(['ward_id'], ['wards.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_optimization_assignments_action_id', 'optimization_assignments', ['action_id'], unique=False)
    op.create_index('ix_optimization_assignments_id', 'optimization_assignments', ['id'], unique=False)
    op.create_index('ix_optimization_assignments_run_id', 'optimization_assignments', ['run_id'], unique=False)
    op.create_index('ix_optimization_assignments_team_id', 'optimization_assignments', ['team_id'], unique=False)


def downgrade() -> None:
    op.drop_table('optimization_assignments')
    op.drop_table('optimization_runs')
    op.drop_table('intervention_candidates')
    op.drop_table('intervention_types')
    op.drop_table('municipal_teams')
