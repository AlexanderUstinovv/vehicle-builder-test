from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID

from .base import BaseView


class VehicleEntries(BaseView):
    __table__ = Table(
        "vehicle_entries",
        BaseView.metadata,
        Column("sid", UUID, primary_key=True),
        Column("vehicle_id", UUID),
        Column("vehicle_name", String(255)),
        Column("formation_name", String(255)),
        Column("formation_type", String(255)),
        Column("formation_id", UUID),
        Column("parent_id", UUID, nullable=True),
        Column("features", JSONB),
    )
