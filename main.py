from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pdf_service import generate_dashboard_pdf
from pivot_service import create_pivot_csv

app = FastAPI()

# CORS SETUP
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Models
class PivotRequest(BaseModel):
    csv_data: str

class PDFRequest(BaseModel):
    url: str

@app.get("/")
def read_root():
    return {"status": "DashupData Backend is running perfectly! 🚀"}

@app.post("/export-dashboard-pdf")
async def export_pdf(request: PDFRequest):
    # Pass the URL from the JSON body
    return await generate_dashboard_pdf(request.url)

@app.post("/generate-pivot")
async def export_pivot(request: PivotRequest):
    return create_pivot_csv(request.csv_data)
