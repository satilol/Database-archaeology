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
from sqlalchemy import func


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

# SELECT WHERE
@app.get("/filter/findings")
def filter_findings(location: str, year: int, db: Session = Depends(get_db)):
    return db.query(Finding).filter(
        Finding.location == location,
        func.extract('year', Finding.found_date) == year
    ).all()
    
# JOIN
@app.get("/findings/detailed_report")
def get_detailed_report(db: Session = Depends(get_db)):
    results = db.query(Finding).join(Archaeologist).join(Artifact).all()
    return [
        {
            "location": f.location,
            "archaeologist": f.archaeologist.full_name,
            "artifact": f.artifact.name,
            "date": f.found_date
        } for f in results
    ]
    
# UPDATE
@app.put("/archaeologists/salary_bonus")
def apply_salary_bonus(specialization: str, bonus_amount: int, db: Session = Depends(get_db)):
    db.query(Archaeologist).filter(
        Archaeologist.specialization == specialization
    ).update(
        {"salary": Archaeologist.salary + bonus_amount}
    )
    db.commit()
    return {"message": f"Salary updated for {specialization}"}

# GROUP BY
@app.get("/stats/locations")
def get_location_stats(db: Session = Depends(get_db)):
    stats = db.query(
        Finding.location, 
        func.count(Finding.id).label("total")
    ).group_by(Finding.location).all()
    return {loc: count for loc, count in stats}

# SORT
@app.get("/artifacts/most_valuable")
def get_valuable(limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Artifact).order_by(Artifact.value.desc()).limit(limit).all()


# JSONB search
@app.get("/findings/search_regex")
def search_findings_json_regex(pattern: str, db: Session = Depends(get_db)):
    from sqlalchemy import cast, String
    
    results = db.query(Finding).filter(
        cast(Finding.extra_data, String).op("~")(pattern)
    ).all()
    
    return results