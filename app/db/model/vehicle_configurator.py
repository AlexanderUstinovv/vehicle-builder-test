from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import BaseModel
from .data_library import Feature
from .data_library import Formation
from .data_library import Function


class Vehicle(BaseModel):

    __tablename__ = "vehicle"

    name = Column(String(255), unique=True, nullable=False)
    vehicle_metadata = Column(JSONB, nullable=False)


class Component(BaseModel):

    __tablename__ = "component"

    name = Column(String(255), unique=True, nullable=False)
    component_metadata = Column(JSONB, nullable=False)


class LinkFact(BaseModel):

    __tablename__ = "link_fact"

    vehicle_id = Column(UUID, ForeignKey("vehicle.id"), nullable=False)
    vehicle = relationship(Vehicle)
    component_id = Column(UUID, ForeignKey("component.id"), nullable=False)
    component = relationship(Component)
    feature_id = Column(UUID, ForeignKey("feature.id"), nullable=False)
    feature = relationship(Feature)
    formation_id = Column(UUID, ForeignKey("formation.id"), nullable=False)
    formation = relationship(Formation)
    function_id = Column(UUID, ForeignKey("base_function.id"), nullable=False)
    function = relationship(Function)
