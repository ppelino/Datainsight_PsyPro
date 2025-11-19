from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), default="admin")
    created_at = Column(DateTime, default=datetime.utcnow)


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(200), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(String(50), default="ativa")
    created_at = Column(DateTime, default=datetime.utcnow)

    responses = relationship("Response", back_populates="campaign")


class Dimension(Base):
    __tablename__ = "dimensions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)

    responses = relationship("Response", back_populates="dimension")


class Response(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    dimension_id = Column(Integer, ForeignKey("dimensions.id"), nullable=False)
    score = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    campaign = relationship("Campaign", back_populates="responses")
    dimension = relationship("Dimension", back_populates="responses")
