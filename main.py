from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import schemas
import crud

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Archaeology REST API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Archaeologists ---
@app.post("/archaeologists", response_model=schemas.ArchaeologistOut) 
def create_archaeologist(data: schemas.ArchaeologistCreate, db: Session = Depends(get_db)): 
    return crud.create_archaeologist(db, data)

@app.get("/archaeologists", response_model=list[schemas.ArchaeologistOut]) 
def get_archaeologists(limit: int = 10, offset: int = 0, db: Session = Depends(get_db)): 
    return crud.get_archaeologists(db, limit, offset)

@app.delete("/archaeologists/{arch_id}") 
def delete_archaeologist(arch_id: int, db: Session = Depends(get_db)): 
    if crud.delete_archaeologist(db, arch_id):
        return {"status": "deleted"}
    raise HTTPException(status_code=404, detail="Not found")

@app.put("/archaeologists/salary_bonus")
def apply_salary_bonus(specialization: str, bonus_amount: int, db: Session = Depends(get_db)):
    return crud.update_salary_bonus(db, specialization, bonus_amount)

# --- Artifacts ---
@app.get("/artifacts/most_valuable", response_model=list[schemas.ArtifactOut])
def get_valuable(limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_most_valuable_artifacts(db, limit)

@app.post("/artifacts", response_model=schemas.ArtifactOut) 
def create_artifact(data: schemas.ArtifactCreate, db: Session = Depends(get_db)): 
    return crud.create_artifact(db, data)

# --- Findings ---
@app.post("/findings", response_model=schemas.FindingOut) 
def create_finding(data: schemas.FindingCreate, db: Session = Depends(get_db)): 
    return crud.create_finding(db, data)

@app.get("/filter/findings")
def filter_findings(location: str, year: int, db: Session = Depends(get_db)):
    return crud.filter_findings(db, location, year)

@app.get("/findings/detailed_report")
def get_detailed_report(db: Session = Depends(get_db)):
    results = crud.get_detailed_report(db)
    return [
        {
            "location": f.location,
            "archaeologist": f.archaeologist.full_name,
            "artifact": f.artifact.name,
            "date": f.found_date
        } for f in results
    ]

@app.get("/stats/locations")
def get_location_stats(db: Session = Depends(get_db)):
    return crud.get_location_stats(db)

@app.get("/findings/search_regex")
def search_json(pattern: str, db: Session = Depends(get_db)):
    return crud.search_findings_json_regex(db, pattern)