import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import db, create_document, get_documents
from schemas import Product, Track, User

app = FastAPI(title="Creator Commerce API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Creator Commerce API running"}

@app.get("/test")
def test_database():
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
            response["database_name"] = os.getenv("DATABASE_NAME") or "❌ Not Set"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:100]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:100]}"
    return response

# Public models for simple responses
class ProductResponse(BaseModel):
    id: str
    title: str
    price: float
    image: Optional[str] = None
    category: str

class TrackResponse(BaseModel):
    id: str
    title: str
    artist: str
    cover: Optional[str] = None
    audio_url: Optional[str] = None

# Seed endpoints (optional convenience for demo)
@app.post("/seed/products")
def seed_products():
    samples = [
        Product(title="Signature Tee", description="Heavyweight tee with minimalist logo.", price=35.0, category="clothing", in_stock=True, image="https://images.unsplash.com/photo-1520975922284-9f585964f9b8" , brand="Your Brand", size="M", color="Black"),
        Product(title="Embroidered Hoodie", description="Premium fleece hoodie.", price=75.0, category="clothing", in_stock=True, image="https://images.unsplash.com/photo-1520975693416-35e282bf002d", brand="Your Brand", size="L", color="Stone"),
        Product(title="House Blend Coffee", description="Balanced chocolate + berry notes.", price=18.0, category="coffee", in_stock=True, image="https://images.unsplash.com/photo-1509042239860-f550ce710b93", brand="Your Coffee", weight_grams=340, roast_level="Medium")
    ]
    ids = []
    for p in samples:
        _id = create_document("product", p)
        ids.append(_id)
    return {"inserted": ids}

@app.post("/seed/tracks")
def seed_tracks():
    samples = [
        Track(title="Sunset Drive", artist="You", cover="https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4", audio_url="", genre="Chillwave"),
        Track(title="Midnight Run", artist="You", cover="https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f", audio_url="", genre="Synthwave")
    ]
    ids = []
    for t in samples:
        _id = create_document("track", t)
        ids.append(_id)
    return {"inserted": ids}

# Public listing endpoints
@app.get("/products", response_model=List[ProductResponse])
def list_products(limit: int = 20, category: Optional[str] = None):
    filt = {"category": category} if category else {}
    docs = get_documents("product", filt, limit)
    out: List[ProductResponse] = []
    for d in docs:
        out.append(ProductResponse(
            id=str(d.get("_id")),
            title=d.get("title"),
            price=float(d.get("price", 0)),
            image=d.get("image"),
            category=d.get("category", "")
        ))
    return out

@app.get("/tracks", response_model=List[TrackResponse])
def list_tracks(limit: int = 20):
    docs = get_documents("track", {}, limit)
    out: List[TrackResponse] = []
    for d in docs:
        out.append(TrackResponse(
            id=str(d.get("_id")),
            title=d.get("title"),
            artist=d.get("artist", ""),
            cover=d.get("cover"),
            audio_url=d.get("audio_url")
        ))
    return out

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
