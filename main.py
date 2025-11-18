import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from database import db, create_document, get_documents
from schemas import Lead, Module

app = FastAPI(title="IA Training Box API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "IA Training Box Backend Ready"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

@app.get("/test")
def test_database():
    """Test endpoint to check database connectivity"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
                response["connection_status"] = "Connected"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"

    return response

# --------- Leads ---------
@app.post("/api/leads", status_code=201)
async def create_lead(lead: Lead):
    try:
        lead_id = create_document("lead", lead)
        return {"id": lead_id, "message": "Lead enregistré"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --------- Modules ---------

# Seed structure for initial modules via code if collection is empty
DEFAULT_MODULES: List[Module] = [
    Module(
        title="Fondamentaux de l'IA pour Sales & Marketing",
        slug="fondamentaux-ia",
        audience="Sales & Marketing",
        level="Débutant",
        duration_min=45,
        tags=["IA", "use cases", "limites"],
        summary="Comprendre ce que l'IA peut réellement apporter à vos process commerciaux et marketing."
    ),
    Module(
        title="Prompting orienté business",
        slug="prompting-business",
        audience="Sales & Marketing",
        level="Intermédiaire",
        duration_min=50,
        tags=["prompt", "cadres", "guardrails"],
        summary="Maîtrisez des cadres de prompting (READY/CRISP) pour produire des livrables fiables."
    ),
    Module(
        title="Prospection augmentée",
        slug="prospection-augmentee",
        audience="Sales",
        level="Intermédiaire",
        duration_min=60,
        tags=["ICP", "séquences", "outbound"],
        summary="Construire ICP, messages et séquences multicanales avec l'aide de l'IA."
    ),
]

@app.get("/api/modules")
async def list_modules():
    try:
        # If DB available, try fetching; if empty, return defaults
        if db is not None:
            docs = get_documents("module")
            if docs:
                # Map to plain dicts with essential fields
                mapped = []
                for d in docs:
                    mapped.append({
                        "title": d.get("title"),
                        "slug": d.get("slug"),
                        "audience": d.get("audience"),
                        "level": d.get("level"),
                        "duration_min": d.get("duration_min"),
                        "tags": d.get("tags", []),
                        "summary": d.get("summary"),
                        "cover": d.get("cover"),
                    })
                return {"items": mapped}
        # Fallback to defaults
        return {"items": [m.model_dump() for m in DEFAULT_MODULES]}
    except Exception:
        # On any error, still return defaults so frontend works
        return {"items": [m.model_dump() for m in DEFAULT_MODULES]}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
