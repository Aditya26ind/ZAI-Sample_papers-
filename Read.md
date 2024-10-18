# FastAPI Sample Paper Extraction API

## Overview

This FastAPI application allows users to extract structured data from plain text or PDF files. The application integrates with the Google Gemini API to generate content, extracting structured data such as exam sample papers or other formatted information from the provided text or documents.

You can add user sample paper data and update and delete also here usign different apis.

### Key Features:
- Extract structured data from plain text.
- Extract structured data from PDF files.
- Use of Google Gemini API for AI-powered data extraction.
- Efficient and asynchronous handling of PDF and text data.

---

## Prerequisites

Before setting up and running this application, ensure you have the following installed:
- **Python 3.9+**
- **FastAPI** and **Uvicorn** for running the API.
- **Google Generative AI Python SDK** for the Gemini API.
- **PyMuPDF (`fitz`)** for PDF processing.

---

## Setup and Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/sample-paper-extraction.git
cd sample-paper-extraction

#how to run using docker

    required : Docker in Your system

    # Obtain your API key by visiting: https://aistudio.google.com/app/apikey
    GEMINI_API_KEY=your_gemini_api_key_here

    # To set up your MongoDB cluster, follow these steps:
    1. Visit: https://cloud.mongodb.com/
    2. Create a new cluster
    3. Add the cluster URL to your .env file under the following variable:

    # .env file looks like this :
    MONGODB_URI=MONGODB_URI
    GEMINI_API_KEY=GEMINI_API_KEY

steps: 
    docker-compose build --no-cache 
    docker-compose up



# how to run manually

python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows

pip install -r requirements.txt
GEMINI_API_KEY=your_gemini_api_key_here
uvicorn app.main:app --reload
