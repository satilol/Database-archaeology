import requests
import random
from datetime import date, timedelta

BASE_URL = "http://127.0.0.1:8000"


def seed_data():
    arch_ids = []
    specializations = ["Egyptology", "Antiquity", "Paleolithic", "Mesoamerica"]
    qualifications = ["Junior", "Middle", "Senior", "Professor"]
    print("Populating archaeologists...")
    for i in range(10):
        payload = {"full_name": f"Archaeologist {i+1}",
                   "salary": random.randint(50000, 150000),
                   "specialization": random.choice(specializations),
                   "qualification": random.choice(qualifications)
        }
        response = requests.post(f"{BASE_URL}/archaeologists", json=payload)
        if response.status_code == 200:
            arch_ids.append(response.json()["id"])
            
    
    art_ids = []
    eras = ["Bronze Age", "Iron Age", "Middle Ages", "Renaissance"]
    print("Populating artifacts...")
    for i in range(20):
        payload = {
            "name": f"Artifact No.{random.randint(1000, 9999)}",
            "value": random.randint(100, 1000000),
            "era": random.choice(eras),
            "previous_owner": f"Collector {random.randint(1, 50)}"
        }
        response = requests.post(f"{BASE_URL}/artifacts", json=payload)
        if response.status_code == 200:
            art_ids.append(response.json()["id"])
            
            
    locations = ["Valley of the Kings", "Pompeii", "Stonehenge", "Machu Picchu"]
    conditions = ["Excellent", "Damaged", "Fragments"]
    materials = ["Gold", "Silver", "Bronze", "Clay", "Stone"]
    print("Populating findings...")
    for i in range(30):
        random_days = random.randint(1, 365)
        found_date = (date.today() - timedelta(days=random_days)).isoformat()
        
        extra_info = {
            "material": random.choice(materials),
            "depth_meters": random.randint(1, 15),
            "is_rare": random.choice([True, False])
        }
        
        payload = {
            "location": random.choice(locations),
            "found_date": found_date,
            "condition": random.choice(conditions),
            "finding_type": "Excavation",
            "archaeologist_id": random.choice(arch_ids),
            "artifact_id": random.choice(art_ids),
            "extra_data": extra_info
        }
        response = requests.post(f"{BASE_URL}/findings", json=payload)
        if response.status_code != 200:
            print(f"Error creating finding: {response.text}")

    print("Done! Database populated via API.")

if __name__ == "__main__":
    try:
        seed_data()
    except requests.exceptions.ConnectionError:
        print("Error: FastAPI is not running! Please start uvicorn first.")