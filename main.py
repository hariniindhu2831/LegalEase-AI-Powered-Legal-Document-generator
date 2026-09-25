from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from backend.generator import generate_document_from_gemini

# Indha 'app' variable-a uvicorn find pannanum
app = FastAPI(
    title="LegalEase API Engine",
    description="Backend API powering AI legal document generation",
    version="1.0.0"
)

class PartyDetail(BaseModel):
    party1_name: str = Field(..., min_length=2)
    party1_role: str = Field(...)
    party1_address: str = Field(...)
    party2_name: str = Field(..., min_length=2)
    party2_role: str = Field(...)
    party2_address: str = Field(...)

class DocumentRequest(BaseModel):
    doc_type: str
    effective_date: str
    parties: PartyDetail
    terms: str

class DocumentResponse(BaseModel):
    status: str
    doc_type: str
    generated_content: str

@app.get("/")
def health_check():
    return {"status": "online", "system": "LegalEase API operational"}

@app.post("/api/v1/generate-document", response_model=DocumentResponse)
def generate_legal_document(payload: DocumentRequest):
    try:
        content = generate_document_from_gemini(
            doc_type=payload.doc_type,
            parties=payload.parties.model_dump(),
            terms=payload.terms,
            effective_date=payload.effective_date
        )
        return DocumentResponse(
            status="success",
            doc_type=payload.doc_type,
            generated_content=content
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Document generation failed: {str(e)}"
        )

