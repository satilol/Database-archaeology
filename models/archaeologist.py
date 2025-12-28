from sqlalchemy import Column, Integer, String
from database import Base

class Archaeologist(Base):
    __tablename__ = "archaeologists"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    salary = Column(Integer)
    specialization = Column(String)
    qualification = Column(String)