"""
Database connection and management for MongoDB
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.collection import Collection
from typing import Optional, Dict, Any, List
import logging
from datetime import datetime

from app.core.config import settings

logger = logging.getLogger(__name__)

class Database:
    client: Optional[AsyncIOMotorClient] = None
    database: Optional[AsyncIOMotorDatabase] = None

db = Database()

# Collection names
COLLECTIONS = {
    "users": "users",
    "conversations": "conversations", 
    "messages": "messages",
    "faq": "faq",
    "courses": "courses",
    "bookings": "bookings",
    "analytics": "analytics",
    "feedback": "feedback",
    "knowledge_base": "knowledge_base",
    "notifications": "notifications",
    "user_sessions": "user_sessions",
    "intents": "intents",
    "entities": "entities",
    "training_data": "training_data",
    "settings": "settings",
    "logs": "logs"
}

async def init_database():
    """Initialize database connection"""
    try:
        logger.info("🔌 Connecting to MongoDB...")
        db.client = AsyncIOMotorClient(settings.MONGODB_URL)
        db.database = db.client[settings.DATABASE_NAME]
        
        # Test connection
        await db.client.admin.command('ping')
        logger.info("✅ Connected to MongoDB successfully!")
        
        # Create indexes
        await create_indexes()
        
        # Initialize default data
        await init_default_data()
        
    except Exception as e:
        logger.error(f"❌ Failed to connect to MongoDB: {e}")
        raise

async def close_database():
    """Close database connection"""
    if db.client:
        db.client.close()
        logger.info("🔌 MongoDB connection closed")

async def create_indexes():
    """Create database indexes for optimal performance"""
    try:
        logger.info("📊 Creating database indexes...")
        
        # Users collection indexes
        await db.database[COLLECTIONS["users"]].create_index("email", unique=True)
        await db.database[COLLECTIONS["users"]].create_index("user_id", unique=True)
        await db.database[COLLECTIONS["users"]].create_index("created_at")
        
        # Conversations collection indexes
        await db.database[COLLECTIONS["conversations"]].create_index("user_id")
        await db.database[COLLECTIONS["conversations"]].create_index("session_id")
        await db.database[COLLECTIONS["conversations"]].create_index("created_at")
        
        # Messages collection indexes
        await db.database[COLLECTIONS["messages"]].create_index("conversation_id")
        await db.database[COLLECTIONS["messages"]].create_index("timestamp")
        await db.database[COLLECTIONS["messages"]].create_index("intent")
        
        # Bookings collection indexes
        await db.database[COLLECTIONS["bookings"]].create_index("user_id")
        await db.database[COLLECTIONS["bookings"]].create_index("course_id")
        await db.database[COLLECTIONS["bookings"]].create_index("booking_date")
        await db.database[COLLECTIONS["bookings"]].create_index("status")
        
        # FAQ collection indexes
        await db.database[COLLECTIONS["faq"]].create_index([("question", "text"), ("answer", "text")])
        await db.database[COLLECTIONS["faq"]].create_index("category")
        await db.database[COLLECTIONS["faq"]].create_index("language")
        
        # Courses collection indexes
        await db.database[COLLECTIONS["courses"]].create_index("course_code", unique=True)
        await db.database[COLLECTIONS["courses"]].create_index("category")
        await db.database[COLLECTIONS["courses"]].create_index("start_date")
        await db.database[COLLECTIONS["courses"]].create_index("status")
        
        # Analytics collection indexes
        await db.database[COLLECTIONS["analytics"]].create_index("timestamp")
        await db.database[COLLECTIONS["analytics"]].create_index("event_type")
        await db.database[COLLECTIONS["analytics"]].create_index("user_id")
        
        logger.info("✅ Database indexes created successfully!")
        
    except Exception as e:
        logger.error(f"❌ Failed to create indexes: {e}")

async def init_default_data():
    """Initialize default data"""
    try:
        logger.info("📝 Initializing default data...")
        
        # Default FAQ data
        default_faqs = [
            {
                "question": "What courses do you offer?",
                "answer": "We offer a wide range of courses including Computer Science, Data Science, Web Development, Mobile App Development, AI/ML, and Digital Marketing. Visit our course catalog for detailed information.",
                "category": "courses",
                "language": "en",
                "priority": 1,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "question": "How do I enroll in a course?",
                "answer": "You can enroll in a course by visiting our website, selecting your desired course, and completing the registration process. You can also ask me to help you with the enrollment process.",
                "category": "enrollment",
                "language": "en",
                "priority": 1,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "question": "What are the payment options?",
                "answer": "We accept various payment methods including credit cards, debit cards, PayPal, and bank transfers. We also offer installment plans for select courses.",
                "category": "payment",
                "language": "en",
                "priority": 1,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "question": "Do you provide certificates?",
                "answer": "Yes, we provide industry-recognized certificates upon successful completion of courses. Our certificates are accredited and can be verified online.",
                "category": "certification",
                "language": "en",
                "priority": 1,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        ]
        
        # Insert FAQ if collection is empty
        faq_count = await db.database[COLLECTIONS["faq"]].count_documents({})
        if faq_count == 0:
            await db.database[COLLECTIONS["faq"]].insert_many(default_faqs)
            logger.info("✅ Default FAQ data inserted")
        
        # Default course categories
        default_categories = [
            {"name": "Computer Science", "description": "Programming and software development courses"},
            {"name": "Data Science", "description": "Data analysis and machine learning courses"},
            {"name": "Web Development", "description": "Frontend and backend web development"},
            {"name": "Mobile Development", "description": "iOS and Android app development"},
            {"name": "AI/ML", "description": "Artificial Intelligence and Machine Learning"},
            {"name": "Digital Marketing", "description": "Online marketing and SEO courses"},
            {"name": "Business", "description": "Business administration and management"},
            {"name": "Design", "description": "UI/UX and graphic design courses"}
        ]
        
        # Default courses
        default_courses = [
            {
                "course_code": "CS101",
                "title": "Introduction to Programming",
                "description": "Learn the fundamentals of programming with Python",
                "category": "Computer Science",
                "duration": "8 weeks",
                "price": 299.99,
                "currency": "USD",
                "level": "beginner",
                "status": "active",
                "max_students": 30,
                "instructor": "Dr. Jane Smith",
                "start_date": "2024-02-01",
                "end_date": "2024-03-26",
                "schedule": "Mon/Wed/Fri 10:00-12:00",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "course_code": "DS201",
                "title": "Data Science Fundamentals",
                "description": "Introduction to data analysis and visualization",
                "category": "Data Science",
                "duration": "10 weeks",
                "price": 399.99,
                "currency": "USD",
                "level": "intermediate",
                "status": "active",
                "max_students": 25,
                "instructor": "Dr. John Doe",
                "start_date": "2024-02-15",
                "end_date": "2024-04-24",
                "schedule": "Tue/Thu 14:00-16:00",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        ]
        
        # Insert courses if collection is empty
        courses_count = await db.database[COLLECTIONS["courses"]].count_documents({})
        if courses_count == 0:
            await db.database[COLLECTIONS["courses"]].insert_many(default_courses)
            logger.info("✅ Default course data inserted")
        
        logger.info("✅ Default data initialization complete!")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize default data: {e}")

def get_collection(collection_name: str):
    """Get a collection from the database"""
    if collection_name not in COLLECTIONS:
        raise ValueError(f"Unknown collection: {collection_name}")
    return db.database[COLLECTIONS[collection_name]]

async def health_check() -> bool:
    """Check database health"""
    try:
        await db.client.admin.command('ping')
        return True
    except Exception:
        return False 