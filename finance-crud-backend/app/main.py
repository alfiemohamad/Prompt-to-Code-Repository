from fastapi import FastAPI, HTTPException
from app.database import engine
from app.routers import user
from pydantic import BaseModel
from app.bisnislogic import hitung_skor_risiko

app = FastAPI()

# Include the user router
app.include_router(user.router)

# Endpoint untuk menghitung skor risiko nasabah
class RiskRequest(BaseModel):
    penghasilan_bulanan: float
    keterlambatan: int
    usia: int
    status_pekerjaan: str
    total_pinjaman: int

class RiskResponse(BaseModel):
    kategori_risiko: str

@app.post("/risk-score", response_model=RiskResponse)
def calculate_risk_score(req: RiskRequest):
    try:
        kategori = hitung_skor_risiko(
            req.penghasilan_bulanan,
            req.keterlambatan,
            req.usia,
            req.status_pekerjaan,
            req.total_pinjaman
        )
        return {"kategori_risiko": kategori}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Create the database tables
@app.on_event("startup")
async def startup():
    import app.models.user  # Import models to create tables
    async with engine.begin() as conn:
        await conn.run_sync(app.models.user.Base.metadata.create_all)