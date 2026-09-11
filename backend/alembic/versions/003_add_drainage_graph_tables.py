"""Add drainage_nodes and drainage_edges tables

Revision ID: 003_add_drainage_graph_tables
Revises: 002_add_risk_predictions_table
Create Date: 2026-08-16 23:45:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '003_add_drainage_graph_tables'
down_revision: Union[str, None] = '002_add_risk_predictions_table'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'drainage_nodes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('node_id', sa.String(length=50), nullable=False),
        sa.Column('node_type', sa.String(length=30), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('ward_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=30), nullable=True, server_default='unknown'),
        sa.Column('data_source', sa.String(length=50), nullable=False, server_default='SYNTHETIC_DEMO_DATA'),
        sa.Column('confidence', sa.String(length=50), nullable=False, server_default='INFERRED_SPATIAL_RELATIONSHIP'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['ward_id'], ['wards.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('node_id')
    )
    op.create_index('ix_drainage_nodes_id', 'drainage_nodes', ['id'], unique=False)
    op.create_index('ix_drainage_nodes_node_id', 'drainage_nodes', ['node_id'], unique=True)
    op.create_index('ix_drainage_nodes_node_type', 'drainage_nodes', ['node_type'], unique=False)
    op.create_index('ix_drainage_nodes_ward_id', 'drainage_nodes', ['ward_id'], unique=False)

    op.create_table(
        'drainage_edges',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('edge_id', sa.String(length=50), nullable=False),
        sa.Column('source_node_id', sa.String(length=50), nullable=False),
        sa.Column('target_node_id', sa.String(length=50), nullable=False),
        sa.Column('edge_type', sa.String(length=30), nullable=False),
        sa.Column('distance_m', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('relationship_strength', sa.Float(), nullable=False, server_default='1.0'),
        sa.Column('relationship_label', sa.String(length=50), nullable=False, server_default='INFERRED_SPATIAL_RELATIONSHIP'),
        sa.Column('data_source', sa.String(length=50), nullable=False, server_default='SYNTHETIC_DEMO_DATA'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['source_node_id'], ['drainage_nodes.node_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['target_node_id'], ['drainage_nodes.node_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('edge_id')
    )
    op.create_index('ix_drainage_edges_edge_id', 'drainage_edges', ['edge_id'], unique=True)
    op.create_index('ix_drainage_edges_edge_type', 'drainage_edges', ['edge_type'], unique=False)
    op.create_index('ix_drainage_edges_id', 'drainage_edges', ['id'], unique=False)
    op.create_index('ix_drainage_edges_source_node_id', 'drainage_edges', ['source_node_id'], unique=False)
    op.create_index('ix_drainage_edges_target_node_id', 'drainage_edges', ['target_node_id'], unique=False)


def downgrade() -> None:
    op.drop_table('drainage_edges')
    op.drop_table('drainage_nodes')
