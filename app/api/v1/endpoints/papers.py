# app/api/v1/endpoints/papers.py
from fastapi import APIRouter, HTTPException
from app.models.sample_paper import SamplePaper
from app.db.mongodb import mongodb
from app.db.redis import redisdb
from bson import ObjectId
import json

router = APIRouter()

@router.post("/papers")
async def create_paper(paper: SamplePaper):
    """
    Create a new paper in the MongoDB database.

    Args:
        paper (SamplePaper): The paper object to be created.

    Returns:
        dict: The ID of the created paper.
    """
    paper_id = await mongodb.db.papers.insert_one(paper.dict())
    return {"paper_id": str(paper_id.inserted_id)}

@router.get("/papers/{paper_id}")
async def get_paper(paper_id: str):
    """
    Retrieve a paper by its ID, first checking in Redis cache. 
    If the paper is not cached, it retrieves it from MongoDB and caches it in Redis.

    Args:
        paper_id (str): The ID of the paper to retrieve.

    Raises:
        HTTPException: If the paper is not found in MongoDB.

    Returns:
        dict: The paper data.
    """
    cached_paper = await redisdb.get(paper_id)
    if cached_paper:
        return {"paper": cached_paper}
    
    paper = await mongodb.db.papers.find_one({"_id": ObjectId(paper_id)})
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    if isinstance(paper.get('_id'), ObjectId):
        paper['_id'] = str(paper['_id'])
    
    paper_data = json.dumps(paper)
    await redisdb.set(paper_id, paper_data)
    
    return paper

@router.put("/papers/{paper_id}")
async def update_paper(paper_id: str, paper: SamplePaper):
    """
    Update an existing paper in MongoDB by its ID.

    Args:
        paper_id (str): The ID of the paper to update.
        paper (SamplePaper): The updated paper data.

    Raises:
        HTTPException: If the paper is not found.

    Returns:
        dict: A success message.
    """
    result = await mongodb.db.papers.update_one(
        {"_id": ObjectId(paper_id)},
        {"$set": paper.dict()}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Paper not found")
    return {"message": "Paper updated successfully"}

@router.delete("/papers/{paper_id}")
async def delete_paper(paper_id: str):
    """
    Delete a paper from MongoDB by its ID.

    Args:
        paper_id (str): The ID of the paper to delete.

    Raises:
        HTTPException: If the paper is not found.

    Returns:
        dict: A success message.
    """
    result = await mongodb.db.papers.delete_one({"_id": ObjectId(paper_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Paper not found")
    return {"message": "Paper deleted successfully"}