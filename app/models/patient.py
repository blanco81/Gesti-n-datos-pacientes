from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Patient(Base):
    __tablename__ = "patients"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    sex = Column(String)
    age = Column(Integer)
    medical_record = Column(String, unique=True, index=True)