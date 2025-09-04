"""
Rasa NLU/Core Service Integration
Advanced chatbot conversation handling
"""

import asyncio
import httpx
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import hashlib
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from langdetect import detect, DetectorFactory

from app.core.config import settings
from app.core.database import get_collection
from app.core.redis_client import cache_manager
from app.services.nlp_service import NLPService
from app.services.booking_service import BookingService
from app.services.faq_service import FAQService

# Set seed for consistent language detection
DetectorFactory.seed = 0

logger = logging.getLogger(__name__)

class RasaService:
    """Rasa service for NLP and conversation management"""
    
    def __init__(self):
        self.rasa_url = settings.RASA_SERVER_URL
        self.nlp_service = NLPService()
        self.booking_service = BookingService()
        self.faq_service = FAQService()
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.client = None
        self.is_initialized = False
    
    async def initialize(self):
        """Initialize Rasa service"""
        try:
            logger.info("🤖 Initializing Rasa service...")
            
            # Initialize HTTP client
            self.client = httpx.AsyncClient(timeout=30.0)
            
            # Check Rasa server availability
            await self._check_rasa_health()
            
            # Initialize sub-services
            await self.nlp_service.initialize()
            await self.booking_service.initialize()
            await self.faq_service.initialize()
            
            self.is_initialized = True
            logger.info("✅ Rasa service initialized successfully!")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize Rasa service: {e}")
            # Fallback to rule-based responses
            self.is_initialized = False
    
    async def _check_rasa_health(self):
        """Check if Rasa server is healthy"""
        try:
            response = await self.client.get(f"{self.rasa_url}/status")
            if response.status_code == 200:
                logger.info("✅ Rasa server is healthy")
                return True
        except Exception as e:
            logger.warning(f"⚠️ Rasa server not available: {e}")
            return False
    
    def is_healthy(self) -> bool:
        """Check service health"""
        return self.is_initialized
    
    async def process_message(
        self, 
        message: str, 
        sender_id: str, 
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Process incoming message and generate response"""
        try:
            # Validate input
            if not message or not message.strip():
                return await self._generate_error_response("Empty message received")
            
            # Normalize message
            message = message.strip()
            
            # Detect language
            language = await self._detect_language(message)
            
            # Analyze sentiment
            sentiment = await self._analyze_sentiment(message)
            
            # Get conversation context
            context = await cache_manager.get_conversation_context(sender_id) or {}
            
            # Process through Rasa or fallback
            if self.is_initialized:
                rasa_response = await self._send_to_rasa(message, sender_id, metadata)
            else:
                rasa_response = await self._fallback_processing(message, sender_id, context)
            
            # Enhance response with additional services
            enhanced_response = await self._enhance_response(
                rasa_response, message, sender_id, language, sentiment, context
            )
            
            # Update conversation context
            await self._update_context(sender_id, message, enhanced_response, context)
            
            # Log conversation
            await self._log_conversation(sender_id, message, enhanced_response, metadata)
            
            return enhanced_response
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return await self._generate_error_response(
                "I apologize, but I'm experiencing technical difficulties. Please try again."
            )
    
    async def _send_to_rasa(
        self, 
        message: str, 
        sender_id: str, 
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Send message to Rasa server"""
        try:
            payload = {
                "sender": sender_id,
                "message": message,
                "metadata": metadata or {}
            }
            
            response = await self.client.post(
                f"{self.rasa_url}/webhooks/rest/webhook",
                json=payload
            )
            
            if response.status_code == 200:
                rasa_responses = response.json()
                
                if rasa_responses:
                    # Combine multiple responses if any
                    combined_text = ""
                    buttons = []
                    quick_replies = []
                    custom_data = {}
                    
                    for resp in rasa_responses:
                        if "text" in resp:
                            combined_text += resp["text"] + " "
                        if "buttons" in resp:
                            buttons.extend(resp["buttons"])
                        if "quick_replies" in resp:
                            quick_replies.extend(resp["quick_replies"])
                        if "custom" in resp:
                            custom_data.update(resp["custom"])
                    
                    return {
                        "text": combined_text.strip(),
                        "buttons": buttons,
                        "quick_replies": quick_replies,
                        "custom": custom_data,
                        "source": "rasa",
                        "confidence": 0.8
                    }
                else:
                    return await self._generate_fallback_response()
            else:
                logger.error(f"Rasa server error: {response.status_code}")
                return await self._generate_fallback_response()
                
        except Exception as e:
            logger.error(f"Error communicating with Rasa: {e}")
            return await self._generate_fallback_response()
    
    async def _fallback_processing(
        self, 
        message: str, 
        sender_id: str, 
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Fallback processing when Rasa is not available"""
        try:
            # Check for greetings
            if await self._is_greeting(message):
                return await self._generate_greeting_response(sender_id)
            
            # Check for FAQ queries
            faq_response = await self.faq_service.search_faq(message)
            if faq_response and faq_response.get("results"):
                return await self._format_faq_response(faq_response["results"][0])
            
            # Check for booking intents
            if await self._is_booking_intent(message):
                return await self._handle_booking_intent(message, sender_id, context)
            
            # Check for course information
            if await self._is_course_query(message):
                return await self._handle_course_query(message)
            
            # Default response
            return await self._generate_default_response()
            
        except Exception as e:
            logger.error(f"Error in fallback processing: {e}")
            return await self._generate_error_response("I'm having trouble understanding. Could you please rephrase?")
    
    async def _enhance_response(
        self,
        base_response: Dict[str, Any],
        message: str,
        sender_id: str,
        language: str,
        sentiment: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Enhance response with additional information and personalization"""
        try:
            enhanced = base_response.copy()
            
            # Add metadata
            enhanced["metadata"] = {
                "timestamp": datetime.utcnow().isoformat(),
                "language": language,
                "sentiment": sentiment,
                "user_id": sender_id,
                "response_time": 0.2  # Placeholder
            }
            
            # Add personalization based on context
            if context.get("user_name"):
                enhanced["text"] = f"Hi {context['user_name']}, " + enhanced.get("text", "")
            
            # Add quick replies based on intent
            if not enhanced.get("quick_replies"):
                enhanced["quick_replies"] = await self._generate_quick_replies(base_response, context)
            
            # Add suggestions
            enhanced["suggestions"] = await self._generate_suggestions(message, context)
            
            # Handle negative sentiment
            if sentiment.get("compound", 0) < -0.5:
                enhanced["text"] += "\n\nI understand this might be frustrating. Would you like me to connect you with a human agent?"
                enhanced["escalation_suggested"] = True
            
            return enhanced
            
        except Exception as e:
            logger.error(f"Error enhancing response: {e}")
            return base_response
    
    async def _detect_language(self, text: str) -> str:
        """Detect language of the text"""
        try:
            if settings.ENABLE_LANGUAGE_DETECTION:
                detected = detect(text)
                if detected in settings.SUPPORTED_LANGUAGES:
                    return detected
            return settings.DEFAULT_LANGUAGE
        except Exception:
            return settings.DEFAULT_LANGUAGE
    
    async def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of the text"""
        try:
            if not settings.ENABLE_SENTIMENT_ANALYSIS:
                return {"compound": 0.0, "pos": 0.0, "neu": 1.0, "neg": 0.0}
            
            # VADER sentiment analysis
            scores = self.sentiment_analyzer.polarity_scores(text)
            
            # TextBlob analysis for additional insights
            blob = TextBlob(text)
            textblob_sentiment = blob.sentiment
            
            return {
                "compound": scores["compound"],
                "pos": scores["pos"],
                "neu": scores["neu"],
                "neg": scores["neg"],
                "polarity": textblob_sentiment.polarity,
                "subjectivity": textblob_sentiment.subjectivity
            }
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {e}")
            return {"compound": 0.0, "pos": 0.0, "neu": 1.0, "neg": 0.0}
    
    async def _is_greeting(self, message: str) -> bool:
        """Check if message is a greeting"""
        greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]
        return any(greeting in message.lower() for greeting in greetings)
    
    async def _is_booking_intent(self, message: str) -> bool:
        """Check if message has booking intent"""
        booking_keywords = ["book", "reserve", "enroll", "register", "schedule", "appointment"]
        return any(keyword in message.lower() for keyword in booking_keywords)
    
    async def _is_course_query(self, message: str) -> bool:
        """Check if message is asking about courses"""
        course_keywords = ["course", "class", "program", "training", "learn", "study"]
        return any(keyword in message.lower() for keyword in course_keywords)
    
    async def _generate_greeting_response(self, sender_id: str) -> Dict[str, Any]:
        """Generate personalized greeting response"""
        return {
            "text": "Hello! Welcome to our Education Support Assistant. I'm here to help you with course information, enrollments, and answer any questions you might have. How can I assist you today?",
            "quick_replies": [
                {"title": "Browse Courses", "payload": "/browse_courses"},
                {"title": "Enrollment Help", "payload": "/enrollment_help"},
                {"title": "FAQ", "payload": "/faq"},
                {"title": "Contact Support", "payload": "/contact_support"}
            ],
            "source": "greeting",
            "confidence": 1.0
        }
    
    async def _generate_fallback_response(self) -> Dict[str, Any]:
        """Generate fallback response"""
        return {
            "text": "I'm sorry, I didn't quite understand that. Could you please rephrase your question or choose from the options below?",
            "quick_replies": [
                {"title": "Course Information", "payload": "/courses"},
                {"title": "Enrollment", "payload": "/enrollment"},
                {"title": "FAQ", "payload": "/faq"},
                {"title": "Human Agent", "payload": "/human_agent"}
            ],
            "source": "fallback",
            "confidence": 0.3
        }
    
    async def _generate_default_response(self) -> Dict[str, Any]:
        """Generate default response"""
        return {
            "text": "I'm here to help! You can ask me about courses, enrollment, schedules, fees, or any other questions related to our educational programs.",
            "quick_replies": [
                {"title": "Course Catalog", "payload": "/courses"},
                {"title": "Enrollment Process", "payload": "/enrollment"},
                {"title": "Pricing", "payload": "/pricing"},
                {"title": "Support", "payload": "/support"}
            ],
            "source": "default",
            "confidence": 0.5
        }
    
    async def _generate_error_response(self, message: str) -> Dict[str, Any]:
        """Generate error response"""
        return {
            "text": message,
            "source": "error",
            "confidence": 0.0,
            "error": True
        }
    
    async def _handle_booking_intent(
        self, 
        message: str, 
        sender_id: str, 
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle booking-related queries"""
        try:
            # Use booking service to handle the request
            booking_response = await self.booking_service.handle_booking_query(
                message, sender_id, context
            )
            return booking_response
        except Exception as e:
            logger.error(f"Error handling booking intent: {e}")
            return await self._generate_error_response("I'm having trouble with booking requests right now. Please try again later.")
    
    async def _handle_course_query(self, message: str) -> Dict[str, Any]:
        """Handle course information queries"""
        try:
            # Get course data from database
            courses_collection = get_collection("courses")
            courses = await courses_collection.find({"status": "active"}).limit(5).to_list(5)
            
            if courses:
                course_text = "Here are our available courses:\n\n"
                for course in courses:
                    course_text += f"📚 **{course['title']}** ({course['course_code']})\n"
                    course_text += f"   Duration: {course['duration']}\n"
                    course_text += f"   Price: ${course['price']}\n"
                    course_text += f"   Level: {course['level'].title()}\n\n"
                
                return {
                    "text": course_text,
                    "quick_replies": [
                        {"title": "Enroll Now", "payload": "/enroll"},
                        {"title": "More Details", "payload": "/course_details"},
                        {"title": "Schedule", "payload": "/schedule"}
                    ],
                    "source": "course_query",
                    "confidence": 0.9
                }
            else:
                return {
                    "text": "We have many exciting courses available! Please visit our website or contact us directly for the most up-to-date course information.",
                    "source": "course_query",
                    "confidence": 0.7
                }
        except Exception as e:
            logger.error(f"Error handling course query: {e}")
            return await self._generate_error_response("I'm having trouble accessing course information right now.")
    
    async def _format_faq_response(self, faq_item: Dict[str, Any]) -> Dict[str, Any]:
        """Format FAQ response"""
        return {
            "text": faq_item.get("answer", "I don't have an answer for that question."),
            "source": "faq",
            "confidence": 0.85,
            "faq_id": str(faq_item.get("_id", ""))
        }
    
    async def _generate_quick_replies(
        self, 
        response: Dict[str, Any], 
        context: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """Generate contextual quick replies"""
        # Default quick replies
        quick_replies = [
            {"title": "Help", "payload": "/help"},
            {"title": "More Info", "payload": "/more_info"}
        ]
        
        # Add context-specific replies
        if "course" in response.get("text", "").lower():
            quick_replies.append({"title": "Enroll", "payload": "/enroll"})
        
        if "price" in response.get("text", "").lower() or "cost" in response.get("text", "").lower():
            quick_replies.append({"title": "Payment Options", "payload": "/payment"})
        
        return quick_replies[:4]  # Limit to 4 quick replies
    
    async def _generate_suggestions(
        self, 
        message: str, 
        context: Dict[str, Any]
    ) -> List[str]:
        """Generate response suggestions"""
        suggestions = []
        
        # Based on message content
        if "course" in message.lower():
            suggestions.extend([
                "Browse our complete course catalog",
                "Check course prerequisites", 
                "View course schedules"
            ])
        
        if "price" in message.lower() or "cost" in message.lower():
            suggestions.extend([
                "View payment plans",
                "Check for discounts",
                "Compare course prices"
            ])
        
        return suggestions[:3]  # Limit suggestions
    
    async def _update_context(
        self,
        sender_id: str,
        message: str,
        response: Dict[str, Any],
        current_context: Dict[str, Any]
    ):
        """Update conversation context"""
        try:
            # Update context with new information
            context = current_context.copy()
            context.update({
                "last_message": message,
                "last_response": response.get("text", ""),
                "last_intent": response.get("intent", "unknown"),
                "message_count": context.get("message_count", 0) + 1,
                "last_updated": datetime.utcnow().isoformat()
            })
            
            # Cache updated context
            await cache_manager.cache_conversation_context(sender_id, context)
            
        except Exception as e:
            logger.error(f"Error updating context: {e}")
    
    async def _log_conversation(
        self,
        sender_id: str,
        message: str,
        response: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Log conversation to database"""
        try:
            messages_collection = get_collection("messages")
            
            log_entry = {
                "user_id": sender_id,
                "user_message": message,
                "bot_response": response.get("text", ""),
                "intent": response.get("intent", "unknown"),
                "confidence": response.get("confidence", 0.0),
                "source": response.get("source", "unknown"),
                "timestamp": datetime.utcnow(),
                "metadata": metadata or {},
                "sentiment": response.get("metadata", {}).get("sentiment", {}),
                "language": response.get("metadata", {}).get("language", "en")
            }
            
            await messages_collection.insert_one(log_entry)
            
        except Exception as e:
            logger.error(f"Error logging conversation: {e}")
    
    async def cleanup(self):
        """Cleanup resources"""
        if self.client:
            await self.client.aclose() 