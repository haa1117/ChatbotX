"""
FAQ API Routes
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter()

class FAQItem(BaseModel):
    id: str
    question: str
    answer: str
    category: str

@router.get("/", response_model=List[FAQItem])
async def get_faqs():
    """Get all FAQ items"""
    try:
        return [
            FAQItem(
                id="1",
                question="How do I enroll in a course?",
                answer="You can enroll by visiting our courses page and clicking the enroll button.",
                category="enrollment"
            ),
            FAQItem(
                id="2",
                question="What payment methods do you accept?",
                answer="We accept credit cards, PayPal, and bank transfers.",
                category="payment"
            )
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving FAQs: {str(e)}")

@router.get("/category/{category}")
async def get_faqs_by_category(category: str):
    """Get FAQs by category"""
    try:
        # TODO: Implement category-based FAQ retrieval
        return {"category": category, "faqs": []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving FAQs by category: {str(e)}") 