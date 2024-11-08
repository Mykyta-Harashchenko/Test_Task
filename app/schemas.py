from typing import Optional, List

from pydantic import BaseModel, Field

class CatBase(BaseModel):
    name: str
    experience_years: int
    breed: str
    salary: float

class CatCreate(CatBase):
    pass

class Cat(CatBase):
    id: int

    class Config:
        orm_mode = True

class TargetBase(BaseModel):
    name: str
    country: str
    notes: str = ""
    completed: bool = False

class TargetCreate(TargetBase):
    pass

class Target(TargetBase):
    id: int

    class Config:
        orm_mode = True

class MissionBase(BaseModel):
    completed: bool = False

class MissionCreate(MissionBase):
    targets: List[TargetCreate]

class Mission(MissionBase):
    id: int
    targets: list[Target]
    class Config:
        orm_mode = True

