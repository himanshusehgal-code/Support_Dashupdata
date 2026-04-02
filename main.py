from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pdf_service import generate_dashboard_pdf
from pivot_service import create_pivot_csv

app = FastAPI()

# CORS SETUP: GitHub Pages se connection allow karne ke liye
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Frontend se aane wale data ka structure
class PivotRequest(BaseModel):
    csv_data: str

class PDFRequest(BaseModel):
    url: str

@app.get("/")
def read_root():
    return {"status": "DashupData Backend is running perfectly! 🚀"}

@app.post("/export-dashboard-pdf")
async def export_pdf(request: PDFRequest):
    # JSON Body se URL nikaal kar function ko bhej rahe hain
    return await generate_dashboard_pdf(request.url)

@app.post("/generate-pivot")
async def export_pivot(request: PivotRequest):
    return create_pivot_csv(request.csv_data)
