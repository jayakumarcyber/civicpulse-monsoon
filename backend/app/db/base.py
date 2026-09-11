# Import all the models so that Base has them before being imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.ward import Ward  # noqa
from app.models.incident import CivicIncident  # noqa
from app.models.rainfall import RainfallRecord  # noqa
from app.models.road import Road  # noqa
from app.models.drain import Drain  # noqa
from app.models.waterbody import Waterbody  # noqa
from app.models.population_zone import PopulationZone  # noqa
from app.models.facility import CriticalFacility  # noqa
from app.models.infrastructure import InfrastructureAsset  # noqa
from app.models.inspection import Inspection  # noqa
from app.models.repair import RepairRecord  # noqa
from app.models.prediction import RiskPrediction  # noqa
from app.models.graph import DrainageNode, DrainageEdge  # noqa
from app.models.impact import ImpactAssessment, PriorityAssessment  # noqa
from app.models.optimization import (  # noqa
    MunicipalTeam,
    InterventionType,
    InterventionCandidate,
    OptimizationRun,
    OptimizationAssignment,
)
from app.models.simulation import SimulationScenario, SimulationResult  # noqa
