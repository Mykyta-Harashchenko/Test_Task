import json

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app import models, schemas

with open("app/breeds.json", "r", encoding='utf-8') as f:
    breeds_data = json.load(f)

allowed_breeds = {breed["name"] for breed in breeds_data}

def create_cat(db: Session, cat: schemas.CatCreate):
    if cat.breed not in allowed_breeds:
        raise HTTPException(
            status_code=400,
            detail=f"Breed '{cat.breed}' is not supported. Available breeds: {', '.join(allowed_breeds)}"
        )
    db_cat = models.Cat(**cat.dict())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

def get_cats(db: Session):
    return db.query(models.Cat).all()

def get_cat(db: Session, cat_id: int):
    return db.query(models.Cat).filter(models.Cat.id == cat_id).first()

def update_cat_salary(db: Session, cat_id: int, salary: float):
    cat = get_cat(db, cat_id)
    if cat:
        cat.salary = salary
        db.commit()
        db.refresh(cat)
    return cat

def delete_cat(db: Session, cat_id: int):
    try:
        cat = get_cat(db, cat_id)
        if cat:
            db.delete(cat)
            db.commit()
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cat is on the mission")

def create_mission_with_targets(db: Session, mission: schemas.MissionCreate):
    if len(mission.targets) < 1 or len(mission.targets) > 3:
        raise HTTPException(
            status_code=400,
            detail="A mission must have between 1 and 3 targets."
        )
    db_mission = models.Mission()
    db.add(db_mission)
    db.commit()
    for target_data in mission.targets:
        db_target = models.Target(
            mission_id=db_mission.id,
            name=target_data.name,
            country=target_data.country,
            notes=target_data.notes,
            completed=target_data.completed
        )
        db.add(db_target)

    db.commit()
    db.refresh(db_mission)
    return db_mission


def assign_mission_to_cat(db: Session, cat_id: int, mission_id: int):
    cat = db.query(models.Cat).filter(models.Cat.id == cat_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    existing_mission = db.query(models.Mission).filter(models.Mission.cat_id == cat_id,
                                                       models.Mission.completed == False).first()
    if existing_mission:
        raise HTTPException(status_code=400, detail="This cat already has an active mission")
    mission = db.query(models.Mission).filter(models.Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    mission.cat_id = cat_id
    db.commit()
    db.refresh(mission)
    return mission


def get_missions(db: Session):
    return db.query(models.Mission).all()

def get_mission(db: Session, mission_id: int):
    return db.query(models.Mission).filter(models.Mission.id == mission_id).first()

def update_target_notes(db: Session, target_id: int, notes: str):
    target = db.query(models.Target).filter(models.Target.id == target_id).first()
    if not target or target.completed:
        raise ValueError("Cannot update notes for completed target")
    target.notes = notes
    db.commit()
    db.refresh(target)
    return target


def mark_target_complete(db: Session, target_id: int):
    target = db.query(models.Target).filter(models.Target.id == target_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")
    target.completed = True
    db.commit()
    db.refresh(target)
    mission = db.query(models.Mission).filter(models.Mission.id == target.mission_id).first()
    all_targets_completed = all(t.completed for t in mission.targets)
    if all_targets_completed:
        mission.completed = True
        db.commit()
        db.refresh(mission)
        cat = db.query(models.Cat).filter(models.Cat.id == mission.cat_id).first()
        cat.mission_id = None
        db.commit()
        db.refresh(cat)
    return target

def delete_mission(db: Session, mission_id: int):
    mission = get_mission(db, mission_id)
    if not mission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mission not found")
    if mission.cat_id is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete mission assigned to a cat")
    db.delete(mission)
    db.commit()
    return {"message": "Mission deleted successfully"}
