from pydantic import BaseModel


class PatientBase(BaseModel):
    name: str
    sex: str
    age: int
    medical_record: str


class PatientCreate(PatientBase):
    pass


class PatientUpdate(PatientBase):
    pass


class Patient(PatientBase):
    id: str

    class Config:
        from_attributes = True