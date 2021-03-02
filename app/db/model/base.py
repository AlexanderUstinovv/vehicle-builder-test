import uuid
from typing import Any

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy import MetaData
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates


Base = declarative_base(
    metadata=MetaData(
        naming_convention={
            "ix": "ix_%(column_0_N_label)s",
            "uq": "uq_%(table_name)s_%(column_0_N_name)s",
            "fk": "fk_%(table_name)s_%(column_0_N_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        },
    )
)


class PrimaryKeyMixin(Base):
    __abstract__ = True

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
    )


class TrackMixin(Base):
    __abstract__ = True

    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, onupdate=func.now())


class DeleteMixin(Base):
    __abstract__ = True

    deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime)

    @validates("deleted")
    def update_deleted(self, key: Any, value: Any) -> Any:
        if value is True:
            self.deleted_at = func.now()
        return value


class BaseModel(PrimaryKeyMixin, TrackMixin, DeleteMixin):
    __abstract__ = True
    __mapper_args__ = {"always_refresh": True}
