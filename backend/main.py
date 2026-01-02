from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uuid
import os
from typing import Dict, Any, Optional
import json
import base64
from ocr_utils import extract_text_from_image, extract_entities_from_text
from form_mapping import map_entities_to_form
from pdf_generator import create_downloadable_pdf

app = FastAPI(title="AI-Powered Form Filling Assistant", 
              description="An AI system for extracting information from government documents and filling forms",
              version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files from frontend
app.mount("/static", StaticFiles(directory="../frontend"), name="static")
app.mount("/temp", StaticFiles(directory="temp"), name="temp")

class DocumentUploadResponse(BaseModel):
    document_id: str
    message: str

class ExtractionRequest(BaseModel):
    document_id: str

class ExtractionResponse(BaseModel):
    document_id: str
    extracted_text: str
    entities: Dict[str, Any]

class FormFillRequest(BaseModel):
    document_id: str
    form_type: str

class FormFillResponse(BaseModel):
    document_id: str
    form_type: str
    filled_form_data: Dict[str, Any]
    confidence_scores: Dict[str, float]

class VoiceInputRequest(BaseModel):
    audio_data: str  # Base64 encoded audio data
    context: str  # Context for the voice input

class VoiceInputResponse(BaseModel):
    text: str
    message: str

# In-memory storage for documents and extracted data
document_storage: Dict[str, Dict[str, Any]] = {}

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main frontend page"""
    with open("../frontend/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload a document (PDF, image) for processing"""
    try:
        # Generate a unique document ID
        document_id = str(uuid.uuid4())
        
        # Read the file content
        file_content = await file.read()
        
        # Save the file temporarily
        file_extension = file.filename.split('.')[-1].lower()
        file_path = f"temp_{document_id}.{file_extension}"
        
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        # Store document info
        document_storage[document_id] = {
            "file_path": file_path,
            "filename": file.filename,
            "file_type": file.content_type,
            "upload_time": str(uuid.uuid4())  # Using this as a simple timestamp
        }
        
        return DocumentUploadResponse(
            document_id=document_id,
            message=f"Document {file.filename} uploaded successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.post("/extract", response_model=ExtractionResponse)
async def extract_information(request: ExtractionRequest):
    """Extract text and entities from the uploaded document"""
    try:
        print(f"Starting extraction for document ID: {request.document_id}")
        if request.document_id not in document_storage:
            print(f"Document not found in storage: {request.document_id}")
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Extract text from the document
        file_path = document_storage[request.document_id]["file_path"]
        print(f"Extracting text from file: {file_path}")
        extracted_text = extract_text_from_image(file_path)
        print(f"Extracted text length: {len(extracted_text)}")
        print(f"Extracted text preview: {extracted_text[:200]}...")
        
        # Extract entities from the text
        entities = extract_entities_from_text(extracted_text)
        print(f"Extracted entities: {entities}")
        
        # Store extracted data
        document_storage[request.document_id]["extracted_text"] = extracted_text
        document_storage[request.document_id]["entities"] = entities
        
        return ExtractionResponse(
            document_id=request.document_id,
            extracted_text=extracted_text,
            entities=entities
        )
    except Exception as e:
        print(f"Extraction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")

@app.post("/fill-form", response_model=FormFillResponse)
async def fill_form(request: FormFillRequest):
    """Map extracted entities to form fields"""
    try:
        if request.document_id not in document_storage:
            raise HTTPException(status_code=404, detail="Document not found")
        
        if "entities" not in document_storage[request.document_id]:
            raise HTTPException(status_code=400, detail="No entities extracted yet")
        
        # Map entities to form fields
        filled_form_data, confidence_scores = map_entities_to_form(
            document_storage[request.document_id]["entities"], 
            request.form_type
        )
        
        return FormFillResponse(
            document_id=request.document_id,
            form_type=request.form_type,
            filled_form_data=filled_form_data,
            confidence_scores=confidence_scores
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Form filling failed: {str(e)}")

@app.post("/voice-input", response_model=VoiceInputResponse)
async def voice_input(request: VoiceInputRequest):
    """Process voice input to update form fields"""
    try:
        # This is a simplified implementation
        # In a real implementation, you would convert speech to text
        # For now, we'll just return the context as the processed text
        return VoiceInputResponse(
            text=f"Voice input processed: {request.context}",
            message="Voice input processed successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Voice input processing failed: {str(e)}")

@app.post("/generate-pdf")
async def generate_pdf(request: FormFillRequest):
    """Generate a filled PDF form"""
    try:
        print(f"PDF generation requested for document ID: {request.document_id}")
        print(f"Document storage keys: {list(document_storage.keys())}")
        
        if request.document_id not in document_storage:
            print(f"Document {request.document_id} not found in storage")
            raise HTTPException(status_code=404, detail="Document not found")
        
        print(f"Document found: {document_storage[request.document_id].keys()}")
        
        if "entities" not in document_storage[request.document_id]:
            print(f"No entities found for document {request.document_id}")
            raise HTTPException(status_code=400, detail="No entities extracted yet")
        
        # Map entities to form fields
        filled_form_data, confidence_scores = map_entities_to_form(
            document_storage[request.document_id]["entities"], 
            request.form_type
        )
        
        # Generate PDF
        pdf_path = create_downloadable_pdf(filled_form_data, request.form_type)
        
        # Return just the filename for the frontend to construct the download URL
        filename = os.path.basename(pdf_path)
        print(f"PDF generated successfully: /temp/{filename}")
        return {"pdf_path": f"/temp/{filename}", "message": "PDF generated successfully"}
    except Exception as e:
        print(f"PDF generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "AI Form Filling Assistant is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)