from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from database import Base
from models.archaeologist import Archaeologist
from models.artifact import Artifact
from models.finding import Finding
from models.archaeologist import Archaeologist
from models.artifact import Artifact
from models.finding import Finding
import schemas


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Archaeology REST API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/archaeologists", response_model=schemas.ArchaeologistOut) 
def create_archaeologist(data: schemas.ArchaeologistCreate, db: Session = Depends(get_db)): 
    obj = Archaeologist(**data.dict()) 
    db.add(obj) 
    db.commit() 
    db.refresh(obj) 
    return obj 

@app.get("/archaeologists", response_model=list[schemas.ArchaeologistOut]) 
def get_archaeologists(limit: int = 10, offset: int = 0, db: Session = Depends(get_db)): 
    return db.query(Archaeologist).offset(offset).limit(limit).all() 

@app.delete("/archaeologists/{arch_id}") 
def delete_archaeologist(arch_id: int, db: Session = Depends(get_db)): 
    obj = db.query(Archaeologist).get(arch_id) 
    if obj: 
        db.delete(obj) 
        db.commit() 
    return {"status": "deleted"}


@app.post("/artifacts", response_model=schemas.ArtifactOut) 
def create_artifact(data: schemas.ArtifactCreate, db: Session = Depends(get_db)): 
    obj = Artifact(**data.dict()) 
    db.add(obj) 
    db.commit() 
    db.refresh(obj) 
    return obj 

@app.get("/artifacts", response_model=list[schemas.ArtifactOut]) 
def get_artifacts(limit: int = 10, offset: int = 0, db: Session = Depends(get_db)): 
    return db.query(Artifact).offset(offset).limit(limit).all() 

@app.delete("/artifacts/{artifact_id}") 
def delete_artifact(artifact_id: int, db: Session = Depends(get_db)): 
    obj = db.query(Artifact).get(artifact_id) 
    if obj: 
        db.delete(obj) 
        db.commit() 
    return {"status": "deleted"}


@app.post("/findings", response_model=schemas.FindingOut) 
def create_finding(data: schemas.FindingCreate, db: Session = Depends(get_db)): 
    obj = Finding(**data.dict()) 
    db.add(obj) 
    db.commit() 
    db.refresh(obj) 
    return obj 

@app.get("/findings", response_model=list[schemas.FindingOut]) 
def get_findings(limit: int = 10, offset: int = 0, db: Session = Depends(get_db)): 
    return db.query(Finding).offset(offset).limit(limit).all() 

@app.delete("/findings/{finding_id}")
def delete_finding(finding_id: int, db: Session = Depends(get_db)): 
    obj = db.query(Finding).get(finding_id) 
    if obj: 
        db.delete(obj) 
        db.commit() 
    return {"status": "deleted"}