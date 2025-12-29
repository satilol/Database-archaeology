from sqlalchemy import Column, Integer, String, Index
from database import Base

class Archaeologist(Base):
    __tablename__ = "archaeologists"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    salary = Column(Integer)
    specialization = Column(String)
    qualification = Column(String)
    experience_years = Column(Integer, server_default="0")
    
    __table_args__ = (Index("idx_arch_name", "full_name"),)