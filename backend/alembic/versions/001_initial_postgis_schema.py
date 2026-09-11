"""Initial PostGIS schema for CivicPulse Monsoon

Revision ID: 001_initial_postgis_schema
Revises: 
Create Date: 2026-08-16 22:35:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry

# revision identifiers, used by Alembic.
revision: str = '001_initial_postgis_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Enable PostGIS extension
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis;")

    # 2. Wards Table
    op.create_table(
        'wards',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('city', sa.String(length=50), nullable=False, server_default='Mumbai'),
        sa.Column('state', sa.String(length=50), nullable=False, server_default='Maharashtra'),
        sa.Column('ward_code', sa.String(length=20), nullable=False),
        sa.Column('population', sa.Integer(), nullable=True),
        sa.Column('area_sq_km', sa.Float(), nullable=True),
        sa.Column('geometry', Geometry(geometry_type='MULTIPOLYGON', srid=4326), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_wards_id', 'wards', ['id'], unique=False)
    op.create_index('ix_wards_ward_code', 'wards', ['ward_code'], unique=True)
    op.create_index('idx_wards_geometry', 'wards', ['geometry'], postgresql_using='gist')

    # 3. Civic Incidents Table
    op.create_table(
        'civic_incidents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('incident_type', sa.String(length=50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('location', Geometry(geometry_type='POINT', srid=4326), nullable=False),
        sa.Column('reported_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('severity', sa.String(length=20), nullable=False, server_default='medium'),
        sa.Column('source', sa.String(length=50), nullable=False, server_default='citizen'),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='reported'),
        sa.Column('ward_id', sa.Integer(), nullable=False),
        sa.Column('evidence_quality', sa.Float(), nullable=True, server_default='1.0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['ward_id'], ['wards.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_civic_incidents_id', 'civic_incidents', ['id'], unique=False)
    op.create_index('ix_civic_incidents_incident_type', 'civic_incidents', ['incident_type'], unique=False)
    op.create_index('ix_civic_incidents_reported_at', 'civic_incidents', ['reported_at'], unique=False)
    op.create_index('ix_civic_incidents_status', 'civic_incidents', ['status'], unique=False)
    op.create_index('ix_civic_incidents_ward_id', 'civic_incidents', ['ward_id'], unique=False)
    op.create_index('idx_civic_incidents_location', 'civic_incidents', ['location'], postgresql_using='gist')

    # 4. Rainfall Records Table
    op.create_table(
        'rainfall_records',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('location', Geometry(geometry_type='POINT', srid=4326), nullable=True),
        sa.Column('recorded_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('rainfall_mm', sa.Float(), nullable=False),
        sa.Column('forecast_hours', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('source', sa.String(length=50), nullable=False, server_default='sensor'),
        sa.Column('is_forecast', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('ward_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['ward_id'], ['wards.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_rainfall_records_id', 'rainfall_records', ['id'], unique=False)
    op.create_index('ix_rainfall_records_recorded_at', 'rainfall_records', ['recorded_at'], unique=False)
    op.create_index('ix_rainfall_records_ward_id', 'rainfall_records', ['ward_id'], unique=False)

    # 5. Roads Table
    op.create_table(
        'roads',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('road_type', sa.String(length=50), nullable=False, server_default='local'),
        sa.Column('importance', sa.String(length=20), nullable=False, server_default='medium'),
        sa.Column('geometry', Geometry(geometry_type='LINESTRING', srid=4326), nullable=False),
        sa.Column('ward_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['ward_id'], ['wards.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_roads_id', 'roads', ['id'], unique=False)
    op.create_index('ix_roads_ward_id', 'roads', ['ward_id'], unique=False)
    op.create_index('idx_roads_geometry', 'roads', ['geometry'], postgresql_using='gist')

    # 6. Drains Table
    op.create_table(
        'drains',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('drain_type', sa.String(length=50), nullable=False, server_default='secondary_drain'),
        sa.Column('capacity', sa.Float(), nullable=True),
        sa.Column('status', sa.String(length=30), nullable=False, server_default='operational'),
        sa.Column('geometry', Geometry(geometry_type='LINESTRING', srid=4326), nullable=False),
        sa.Column('ward_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['ward_id'], ['wards.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_drains_id', 'drains', ['id'], unique=False)
    op.create_index('ix_drains_ward_id', 'drains', ['ward_id'], unique=False)
    op.create_index('idx_drains_geometry', 'drains', ['geometry'], postgresql_using='gist')

    # 7. Waterbodies Table
    op.create_table(
        'waterbodies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('type', sa.String(length=50), nullable=False, server_default='lake'),
        sa.Column('geometry', Geometry(geometry_type='POLYGON', srid=4326), nullable=False),
        sa.Column('ward_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['ward_id'], ['wards.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_waterbodies_id', 'waterbodies', ['id'], unique=False)
    op.create_index('ix_waterbodies_ward_id', 'waterbodies', ['ward_id'], unique=False)
    op.create_index('idx_waterbodies_geometry', 'waterbodies', ['geometry'], postgresql_using='gist')

    # 8. Population Zones Table
    op.create_table(
        'population_zones',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('zone_name', sa.String(length=100), nullable=False),
        sa.Column('population', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('density', sa.Float(), nullable=True),
        sa.Column('geometry', Geometry(geometry_type='POLYGON', srid=4326), nullable=False),
        sa.Column('ward_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['ward_id'], ['wards.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_population_zones_id', 'population_zones', ['id'], unique=False)
    op.create_index('ix_population_zones_ward_id', 'population_zones', ['ward_id'], unique=False)
    op.create_index('idx_population_zones_geometry', 'population_zones', ['geometry'], postgresql_using='gist')

    # 9. Critical Facilities Table
    op.create_table(
        'critical_facilities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('facility_type', sa.String(length=50), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('location', Geometry(geometry_type='POINT', srid=4326), nullable=False),
        sa.Column('capacity', sa.Integer(), nullable=True),
        sa.Column('ward_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['ward_id'], ['wards.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_critical_facilities_facility_type', 'critical_facilities', ['facility_type'], unique=False)
    op.create_index('ix_critical_facilities_id', 'critical_facilities', ['id'], unique=False)
    op.create_index('ix_critical_facilities_ward_id', 'critical_facilities', ['ward_id'], unique=False)
    op.create_index('idx_critical_facilities_location', 'critical_facilities', ['location'], postgresql_using='gist')

    # 10. Infrastructure Assets Table
    op.create_table(
        'infrastructure_assets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('asset_type', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('age_years', sa.Integer(), nullable=True),
        sa.Column('condition', sa.String(length=30), nullable=False, server_default='good'),
        sa.Column('owner_department', sa.String(length=100), nullable=False, server_default='Storm Water Drains Dept'),
        sa.Column('geometry', Geometry(geometry_type='POINT', srid=4326), nullable=False),
        sa.Column('ward_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['ward_id'], ['wards.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_infrastructure_assets_asset_type', 'infrastructure_assets', ['asset_type'], unique=False)
    op.create_index('ix_infrastructure_assets_id', 'infrastructure_assets', ['id'], unique=False)
    op.create_index('ix_infrastructure_assets_owner_department', 'infrastructure_assets', ['owner_department'], unique=False)
    op.create_index('ix_infrastructure_assets_ward_id', 'infrastructure_assets', ['ward_id'], unique=False)
    op.create_index('idx_infrastructure_assets_geometry', 'infrastructure_assets', ['geometry'], postgresql_using='gist')

    # 11. Inspections Table
    op.create_table(
        'inspections',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('asset_id', sa.Integer(), nullable=False),
        sa.Column('inspection_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('inspection_type', sa.String(length=50), nullable=False, server_default='routine'),
        sa.Column('findings', sa.Text(), nullable=True),
        sa.Column('condition_score', sa.Float(), nullable=False, server_default='5.0'),
        sa.Column('inspector', sa.String(length=100), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['asset_id'], ['infrastructure_assets.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_inspections_asset_id', 'inspections', ['asset_id'], unique=False)
    op.create_index('ix_inspections_id', 'inspections', ['id'], unique=False)

    # 12. Repair Records Table
    op.create_table(
        'repair_records',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('asset_id', sa.Integer(), nullable=False),
        sa.Column('repair_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('repair_type', sa.String(length=50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('cost', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('status', sa.String(length=30), nullable=False, server_default='scheduled'),
        sa.Column('completed_by', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['asset_id'], ['infrastructure_assets.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_repair_records_asset_id', 'repair_records', ['asset_id'], unique=False)
    op.create_index('ix_repair_records_id', 'repair_records', ['id'], unique=False)


def downgrade() -> None:
    op.drop_table('repair_records')
    op.drop_table('inspections')
    op.drop_table('infrastructure_assets')
    op.drop_table('critical_facilities')
    op.drop_table('population_zones')
    op.drop_table('waterbodies')
    op.drop_table('drains')
    op.drop_table('roads')
    op.drop_table('rainfall_records')
    op.drop_table('civic_incidents')
    op.drop_table('wards')
