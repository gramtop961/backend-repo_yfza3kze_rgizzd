import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import create_document, get_documents, db
from schemas import Token

app = FastAPI(title="Token Forge API", description="Blueprints for token creation from a god-perspective UI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Token Forge Backend running"}

@app.get("/api/hello")
def hello():
    return {"message": "Welcome to Token Forge"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
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

# ------------ Token Blueprint Endpoints ------------

class TokenCreate(BaseModel):
    name: str
    symbol: str
    decimals: int = 18
    total_supply: float
    chain: str = "ethereum"
    description: Optional[str] = None
    image_url: Optional[str] = None
    website: Optional[str] = None
    twitter: Optional[str] = None
    telegram: Optional[str] = None
    owner_wallet: Optional[str] = None
    features: Optional[List[str]] = []

@app.post("/api/tokens")
def create_token(token: TokenCreate):
    try:
        token_doc = Token(**token.model_dump())
        _id = create_document("token", token_doc)
        return {"id": _id, "status": "created"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/tokens")
def list_tokens(chain: Optional[str] = None, owner: Optional[str] = None, limit: int = 50):
    try:
        filt = {}
        if chain:
            filt["chain"] = chain
        if owner:
            filt["owner_wallet"] = owner
        docs = get_documents("token", filt, limit)
        # Convert ObjectId and datetimes to strings
        for d in docs:
            if "_id" in d:
                d["id"] = str(d.pop("_id"))
            for k, v in list(d.items()):
                if hasattr(v, "isoformat"):
                    d[k] = v.isoformat()
        return {"items": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
