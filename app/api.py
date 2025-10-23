from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.db import get_db

router = APIRouter()


@router.post("/patients/", response_model=schemas.Patient)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    db_patient = crud.get_patients(db)
    existing_patient = next(
        (p for p in db_patient if p.medical_record == patient.medical_record), None
    )
    if existing_patient:
        raise HTTPException(status_code=400, detail="Medical record already registered")
    return crud.create_patient(db=db, patient=patient)


@router.get("/patients/", response_model=list[schemas.Patient])
def read_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    patients = crud.get_patients(db, skip=skip, limit=limit)
    return patients


@router.get("/patients/{patient_id}", response_model=schemas.Patient)
def read_patient(patient_id: str, db: Session = Depends(get_db)):
    db_patient = crud.get_patient(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient


@router.put("/patients/{patient_id}", response_model=schemas.Patient)
def update_patient(
    patient_id: str, patient: schemas.PatientUpdate, db: Session = Depends(get_db)
):
    db_patient = crud.get_patient(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return crud.update_patient(db=db, patient_id=patient_id, patient=patient)


@router.delete("/patients/{patient_id}", response_model=schemas.Patient)
def delete_patient(patient_id: str, db: Session = Depends(get_db)):
    db_patient = crud.get_patient(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return crud.delete_patient(db=db, patient_id=patient_id)