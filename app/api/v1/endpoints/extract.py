# app/api/v1/endpoints/extract.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.gemini_service import GeminiService
from pydantic import BaseModel, Field
from typing import List, Optional
from fastapi import Form, HTTPException, APIRouter

router = APIRouter()

gemini_service = GeminiService()

@router.post("/extract/pdf")
async def extract_pdf(file: Optional[UploadFile] = File(None), file_url: str = Form(None)):
    """
    Endpoint to extract content from a PDF file or a URL pointing to a PDF.

    Args:
        file (Optional[UploadFile]): Optional PDF file to extract content from.
        file_url (str, optional): Optional URL pointing to a PDF file.

    Raises:
        HTTPException: If an error occurs during PDF extraction.

    Returns:
        dict: The structured data extracted from the PDF.
    """
    try:
        if file:
            result = await gemini_service.extract_pdf(file=file)
        else:
            result = await gemini_service.extract_pdf(file_url=file_url)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class TextRequest(BaseModel):
    """
    A request model for extracting information from a text string.

    Attributes:
        text (str): The text from which information should be extracted.
    """
    text: str

@router.post("/extract/text")
async def extract_text(request: TextRequest):
    """
    Endpoint to extract structured data from a given text input using Gemini AI.

    Args:
        request (TextRequest): The request body containing the text to be processed.

    Raises:
        HTTPException: If an error occurs during text extraction.

    Returns:
        dict: The structured data extracted from the provided text.
    """
    try:
        print(request.text)
        result = await gemini_service.extract_text(request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))