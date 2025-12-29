from pydantic import BaseModel
from datetime import date
from typing import Optional


class ArchaeologistBase(BaseModel):
    full_name: str
    salary: Optional[int] = None
    specialization: Optional[str] = None
    qualification: Optional[str] = None
    
class ArchaeologistCreate(ArchaeologistBase):
    pass

class ArchaeologistOut(ArchaeologistBase):
    id: int
    
    class Config:
        from_attributes = True
        
        
class ArtifactBase(BaseModel):
    name: str
    value: Optional[int] = None
    era: Optional[str] = None
    previous_owner: Optional[str] = None
    
class ArtifactCreate(ArtifactBase):
    pass

class ArtifactOut(ArtifactBase):
    id: int
    
    class Config:
        from_attributes = True
        
        
class FindingBase(BaseModel):
    location: str
    found_date: date
    condition: Optional[str] = None
    finding_type: Optional[str] = None
    archaeologist_id: int
    artifact_id: int

class FindingCreate(FindingBase):
    pass

class FindingOut(FindingBase):
    id: int
    
    class Config:
        from_attributes = True