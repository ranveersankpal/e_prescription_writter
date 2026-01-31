from fastapi import FastAPI, UploadFile, File
from utils.doc_loader import extract_text_from_document
from utils.voice_loader import extract_text_from_audio

app = FastAPI(title="E-Prescription Loader Service with LangChain")

@app.post("/doc-to-text")
async def doc_to_text(file: UploadFile = File(...)):
    text = await extract_text_from_document(file)
    return {
        "filename": file.filename,
        "text": text
    }

@app.post("/voice-to-text")
async def voice_to_text(file: UploadFile = File(...)):
    text = await extract_text_from_audio(file)
    return {
        "filename": file.filename,
        "text": text
    }
