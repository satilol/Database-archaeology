from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from database import Base

class Finding(Base):
    __tablename__ = "findings"
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String)
    found_date = Column(Date)
    condition = Column(String)
    finding_type = Column(String)
    archaeologist_id = Column(Integer, ForeignKey("archaeologists.id"))
    artifact_id = Column(Integer, ForeignKey("artifacts.id"))
    extra_data = Column(JSONB)
    
    archaeologist = relationship("Archaeologist")
    artifact = relationship("Artifact")
