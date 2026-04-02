from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Aapki custom files se functions import kar rahe hain
from pdf_service import generate_dashboard_pdf
from pivot_service import create_pivot_csv

app = FastAPI()

# 🔥 CORS SETUP: GitHub Pages ko block hone se roke ga
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PivotRequest(BaseModel):
    csv_data: str

# Server check karne ka route
@app.get("/")
def read_root():
    return {"status": "DashupData Backend is running perfectly! 🚀"}

# PDF wala Route
@app.post("/export-dashboard-pdf")
async def export_pdf(url: str):
    # Doosri file ka function call kiya
    return await generate_dashboard_pdf(url)

# Pivot wala Route
@app.post("/generate-pivot")
async def export_pivot(request: PivotRequest):
    # Doosri file ka function call kiya
    return create_pivot_csv(request.csv_data)
