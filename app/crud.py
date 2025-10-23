from sqlalchemy.orm import Session
import uuid
from app.models.patient import Patient as DBPatient
from app.schemas import PatientCreate, PatientUpdate


def get_patient(db: Session, patient_id: str):
    return db.query(DBPatient).filter(DBPatient.id == patient_id).first()


def get_patients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DBPatient).offset(skip).limit(limit).all()


def create_patient(db: Session, patient: PatientCreate):
    db_patient = DBPatient(
        id=str(uuid.uuid4()),
        name=patient.name,
        sex=patient.sex,
        age=patient.age,
        medical_record=patient.medical_record,
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def update_patient(db: Session, patient_id: str, patient: PatientUpdate):
    db_patient = get_patient(db, patient_id)
    if db_patient:
        db_patient.name = patient.name
        db_patient.sex = patient.sex
        db_patient.age = patient.age
        db_patient.medical_record = patient.medical_record
        db.commit()
        db.refresh(db_patient)
    return db_patient


def delete_patient(db: Session, patient_id: str):
    db_patient = get_patient(db, patient_id)
    if db_patient:
        db.delete(db_patient)
        db.commit()
    return db_patient