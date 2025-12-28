from sqlalchemy import Column, Integer, String
from database import Base

class Artifact(Base):
    __tablename__ = "artifacts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    value = Column(Integer)
    era = Column(String)
    previous_owner = Column(String)