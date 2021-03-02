import enum

from sqlalchemy import Column
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base
from .base import BaseModel

function_feature_association = Table(
    "function_feature_association",
    Base.metadata,
    Column("base_function_id", UUID, ForeignKey("base_function.id")),
    Column("feature_id", UUID, ForeignKey("feature.id")),
)


class Function(BaseModel):
    """Basic entity to link components to vehicle"""

    __tablename__ = "base_function"

    name = Column(String(255), unique=True, nullable=False)
    features = relationship(
        "Feature", secondary=function_feature_association, back_populates="functions"
    )


feature_formation_association = Table(
    "feature_formation_association",
    Base.metadata,
    Column("feature_id", UUID, ForeignKey("feature.id")),
    Column("formation_id", UUID, ForeignKey("formation.id")),
)


class Feature(BaseModel):
    """Union of features for presenting to users"""

    __tablename__ = "feature"

    name = Column(String(255), unique=True, nullable=False)
    functions = relationship(
        "Function", secondary=function_feature_association, back_populates="features"
    )
    formations = relationship(
        "Formation", secondary=feature_formation_association, back_populates="features"
    )


class FormationType(enum.Enum):
    group = "group"
    subgroup = "subgroup"
    set = "set"


class Formation(BaseModel):
    """Features grouped by specific context"""

    __tablename__ = "formation"

    name = Column(String(255), unique=True, nullable=False)
    type = Column(Enum(FormationType), nullable=False)
    parent_id = Column(UUID, ForeignKey("formation.id"), nullable=True)
    parent = relationship("Formation", remote_side=[id])
    features = relationship(
        "Feature", secondary=feature_formation_association, back_populates="formations"
    )
