# app/services/gemini_service.py
import base64
import io
from typing import Any, Dict
import httpx
import google.generativeai as genai
import os
import fitz 
from fastapi import UploadFile
from dotenv import load_dotenv
import json
import PyPDF2
from fastapi import UploadFile, File, HTTPException, APIRouter, Body
import shutil
import os


load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

class GeminiService:
    """
    A service class that interacts with Gemini AI to extract data from PDFs and summarize content.

    Attributes:
        model (str): The name of the Gemini AI model used for content generation.
    """
    def __init__(self, model: str = "gemini-1.5-flash"):
        """
        Initializes the GeminiService with the specified model.

        Args:
            model (str): The AI model to use for content generation. Default is "gemini-1.5-flash".
        """
        self.model = genai.GenerativeModel(model)
        
    async def extract_pdf(self, file: str = None, file_url: str = None):
        """
        Extracts text from a provided PDF file or URL, and generates a structured summary using Gemini AI.

        Args:
            file (str, optional): A file object for the PDF.
            file_url (str, optional): A URL pointing to the PDF file.

        Raises:
            ValueError: If neither file nor file_url is provided, or if the file is not a valid PDF.
            Exception: If structured data extraction fails.

        Returns:
            dict: A structured summary of the PDF content in JSON format.
        """
        print("File", file)
        print("File Url", file_url)
        
        if file:
            if not file.filename.endswith(".pdf"):
                raise ValueError("Invalid file format. Only PDF files are supported.")
            
            pdf_content = await self._extract_text_from_pdf(file)
        elif file_url:
            pdf_content = await self._download_and_extract_pdf(file_url)
        else:
            raise ValueError("No file or URL provided.")
        
        try:
            prompt = (
                f"Summarize the key points from the following document text: {pdf_content}. "
                "VERY IMPORTANT: Format the extracted data strictly in valid JSON format with the following structure. "
                "Ensure that the 'marks' and 'marks_per_question' fields contain valid integers. If data is missing for these fields, use 0 as a fallback value instead of null. "
                "Ensure that the 'reference_id' fields contain valid strings. If no reference IDs are available, use an empty string ('') instead of null. "
                "Make sure the 'params' section includes the required fields 'board', 'grade', and 'subject'. If the information is not available, use a placeholder value.\n"
                """example output: {
                    "title": "Sample Paper Title",
                    "type": "previous_year",
                    "time": 180,
                    "marks": 100,  # Ensure this is a valid integer, fallback to 0 if missing
                    "params": {
                        "board": "CBSE",  # Required field
                        "grade": 10,  # Required field
                        "subject": "Maths"  # Required field
                    },
                    "tags": ["algebra", "geometry"],
                    "chapters": ["Quadratic Equations", "Triangles"],
                    "sections": [
                        {
                            "marks_per_question": 5,  # Ensure this is a valid integer, fallback to 0 if missing
                            "type": "default",
                            "questions": [
                                {
                                    "question": "Solve the quadratic equation: x^2 + 5x + 6 = 0",
                                    "answer": "The solutions are x = -2 and x = -3",
                                    "type": "short",
                                    "question_slug": "solve-quadratic-equation",
                                    "reference_id": "QE001",  # Ensure this is a valid string, fallback to "" if missing
                                    "hint": "Use the quadratic formula",
                                    "params": {}
                                },
                                {
                                    "question": "In a right-angled triangle, if one angle is 30°, what is the other acute angle?",
                                    "answer": "60°",
                                    "type": "short",
                                    "question_slug": "right-angle-triangle-angles",
                                    "reference_id": "GT001",  # Ensure this is a valid string, fallback to "" if missing
                                    "params": {}
                                }
                            ]
                        }
                    ]
                }
                """
            )
            response = self.model.generate_content(prompt)
            cleaned_text = response.text.strip('```json\n').strip('```')
            cleaned_text = cleaned_text.strip().strip('```').strip()
            response = json.loads(cleaned_text)
            return response

        except Exception as e:
            print(f"Error during PDF extraction: {e}")
            raise Exception("Failed to extract structured data from the PDF.") from e

    async def _extract_text_from_pdf(self, file):
        """
        Extracts plain text from a PDF file using PyPDF2.

        Args:
            file (UploadFile): The PDF file to extract text from.

        Returns:
            str: The extracted text from the PDF.
        """
        pdf_content = await file.read()

        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
        extracted_text = ""
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text
        return extracted_text
    
    async def _download_and_extract_pdf(self, url: str):
        """
        Downloads a PDF from a given URL and extracts its text content.

        Args:
            url (str): The URL pointing to the PDF.

        Raises:
            Exception: If there is an error during downloading or text extraction.

        Returns:
            str: The extracted text from the downloaded PDF.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                
                with open("temp.pdf", "wb") as f:
                    f.write(response.content)
                
                with open("temp.pdf", "rb") as pdf_file:
                    pdf_reader = PyPDF2.PdfReader(pdf_file)
                    num_pages = len(pdf_reader.pages)
                    extracted_text = ""
                    for page_num in range(num_pages):
                        page = pdf_reader.pages[page_num]
                        extracted_text += page.extract_text()
                os.remove("temp.pdf")
                return extracted_text
        except Exception as e:
            print(f"Error downloading or extracting PDF from URL: {e}")
            raise