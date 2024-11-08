from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from . import models, schemas, crud
from .database import engine, Base, get_db

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.post("/cats/", response_model=schemas.Cat)
def create_cat(cat: schemas.CatCreate, db: Session = Depends(get_db)):
    return crud.create_cat(db=db, cat=cat)

@app.get("/cats/", response_model=list[schemas.Cat])
def get_cats(db: Session = Depends(get_db)):
    return crud.get_cats(db=db)

@app.get("/cats/{cat_id}", response_model=schemas.Cat)
def get_cat(cat_id: int, db: Session = Depends(get_db)):
    cat = crud.get_cat(db=db, cat_id=cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    return cat

@app.put("/cats/{cat_id}", response_model=schemas.Cat)
def update_cat_salary(cat_id: int, salary: float, db: Session = Depends(get_db)):
    cat = crud.update_cat_salary(db=db, cat_id=cat_id, salary=salary)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    return cat

@app.delete("/cats/{cat_id}")
def delete_cat(cat_id: int, db: Session = Depends(get_db)):
    crud.delete_cat(db=db, cat_id=cat_id)
    return {"ok": True}

@app.post("/missions/", response_model=schemas.Mission)
def create_mission(mission: schemas.MissionCreate, db: Session = Depends(get_db)):
    return crud.create_mission_with_targets(db=db, mission=mission)

@app.post("/missions/{mission_id}/assign_cat/{cat_id}", response_model=schemas.Mission)
def assign_cat_to_mission_endpoint(mission_id: int, cat_id: int, db: Session = Depends(get_db)):
    return crud.assign_mission_to_cat(db=db, mission_id=mission_id, cat_id=cat_id)

@app.get("/missions/", response_model=list[schemas.Mission])
def get_missions(db: Session = Depends(get_db)):
    return crud.get_missions(db=db)

@app.get("/missions/{mission_id}", response_model=schemas.Mission)
def get_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = crud.get_mission(db=db, mission_id=mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission

@app.delete("/missions/{mission_id}")
def delete_mission(mission_id: int, db: Session = Depends(get_db)):
    crud.delete_mission(db=db, mission_id=mission_id)
    return {"ok": True}

@app.put("/missions/{mission_id}/targets/{target_id}")
def update_target_notes(target_id: int, notes: str, db: Session = Depends(get_db)):
    try:
        return crud.update_target_notes(db=db, target_id=target_id, notes=notes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/missions/{mission_id}/targets/{target_id}/complete")
def mark_target_as_complete(target_id: int, db: Session = Depends(get_db)):
    try:
        return crud.mark_target_complete(db=db, target_id=target_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))