from sqlalchemy.orm import Session
from sqlalchemy import func, cast, String
from models.archaeologist import Archaeologist
from models.artifact import Artifact
from models.finding import Finding
import schemas

# --- Archaeologists ---
def get_archaeologists(db: Session, limit: int = 10, offset: int = 0):
    return db.query(Archaeologist).offset(offset).limit(limit).all()

def create_archaeologist(db: Session, data: schemas.ArchaeologistCreate):
    obj = Archaeologist(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def delete_archaeologist(db: Session, arch_id: int):
    obj = db.query(Archaeologist).get(arch_id)
    if obj:
        db.delete(obj)
        db.commit()
        return True
    return False

# UPDATE
def update_salary_bonus(db: Session, specialization: str, bonus_amount: int):
    db.query(Archaeologist).filter(
        Archaeologist.specialization == specialization
    ).update(
        {"salary": Archaeologist.salary + bonus_amount}
    )
    db.commit()
    return {"message": f"Salary updated for {specialization}"}


# --- Artifacts ---
def get_artifacts(db: Session, limit: int = 10, offset: int = 0):
    return db.query(Artifact).offset(offset).limit(limit).all()

def create_artifact(db: Session, data: schemas.ArtifactCreate):
    obj = Artifact(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

# SORT
def get_most_valuable_artifacts(db: Session, limit: int = 10):
    return db.query(Artifact).order_by(Artifact.value.desc()).limit(limit).all()


# --- Findings ---
def get_findings(db: Session, limit: int = 10, offset: int = 0):
    return db.query(Finding).offset(offset).limit(limit).all()

def create_finding(db: Session, data: schemas.FindingCreate):
    obj = Finding(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

# SELECT WHERE
def filter_findings(db: Session, location: str, year: int):
    return db.query(Finding).filter(
        Finding.location == location,
        func.extract('year', Finding.found_date) == year
    ).all()

# JOIN
def get_detailed_report(db: Session):
    return db.query(Finding).join(Archaeologist).join(Artifact).all()

# GROUP BY
def get_location_stats(db: Session):
    stats = db.query(
        Finding.location, 
        func.count(Finding.id).label("total")
    ).group_by(Finding.location).all()
    return {loc: count for loc, count in stats}

# JSONB search
def search_findings_json_regex(db: Session, pattern: str):
    return db.query(Finding).filter(
        cast(Finding.extra_data, String).op("~")(pattern)
    ).all()