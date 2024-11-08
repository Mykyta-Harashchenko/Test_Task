from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Cat(Base):
    __tablename__ = "cats"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    experience_years = Column(Integer)
    breed = Column(String)
    salary = Column(Float)

class Mission(Base):
    __tablename__ = "missions"
    id = Column(Integer, primary_key=True, index=True)
    cat_id = Column(Integer, ForeignKey("cats.id"))
    completed = Column(Boolean, default=False)
    cat = relationship("Cat")
    targets = relationship("Target", cascade="all, delete-orphan")

class Target(Base):
    __tablename__ = "targets"
    id = Column(Integer, primary_key=True, index=True)
    mission_id = Column(Integer, ForeignKey("missions.id"))
    name = Column(String)
    country = Column(String)
    notes = Column(String)
    completed = Column(Boolean, default=False)
    mission = relationship("Mission", back_populates="targets")
