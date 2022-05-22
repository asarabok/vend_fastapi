from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declared_attr


class IdTitleMixin:
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), nullable=False)


class UserCreatedUpdatedMixin:
    @declared_attr
    def created_by(cls):
        return Column(Integer, ForeignKey("user.id"), nullable=False)

    @declared_attr
    def updated_by(cls):
        return Column(Integer, ForeignKey("user.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow, nullable=True)
