import httpx
from fastapi import FastAPI, HTTPException
from typing import Optional
import logging
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown
    await joke_service.close()

app = FastAPI(
    title="Meow Norris Joke API",
    description="A fun API that fetches Chuck Norris jokes and transforms them into Meow Norris jokes for our office cat mascot!",
    version="1.0.0",
    lifespan=lifespan
)

CHUCK_NORRIS_API_BASE = "https://api.chucknorris.io/jokes"

class Mascot(str, Enum):
    """Available mascots for joke transformation"""
    MEOW_NORRIS = "Meow Norris"
    WOOF_NORRIS = "Woof Norris"
    CHIRP_NORRIS = "Chirp Norris"  # For our bird mascot!
    OINK_NORRIS = "Oink Norris"   # For our pig mascot!

class JokeService:
    """Service for fetching and transforming jokes"""
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=10.0)
    
    async def fetch_random_joke(self) -> dict:
        """Fetch a random Chuck Norris joke from the external API"""
        try:
            response = await self.client.get(f"{CHUCK_NORRIS_API_BASE}/random")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Error fetching joke: {e}")
            raise HTTPException(status_code=503, detail="Unable to fetch joke from external service")
    
    async def fetch_joke_by_category(self, category: str) -> dict:
        """Fetch a Chuck Norris joke from a specific category"""
        try:
            response = await self.client.get(f"{CHUCK_NORRIS_API_BASE}/random?category={category}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Error fetching joke by category {category}: {e}")
            raise HTTPException(status_code=503, detail=f"Unable to fetch joke from category '{category}'")
    
    async def get_categories(self) -> list:
        """Get available joke categories"""
        try:
            response = await self.client.get(f"{CHUCK_NORRIS_API_BASE}/categories")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Error fetching categories: {e}")
            raise HTTPException(status_code=503, detail="Unable to fetch categories")
    
    def transform_to_meow_norris(self, joke_text: str, mascot: str = "Meow Norris") -> str:
        """Transform Chuck Norris jokes to use our pet mascot"""
        if not joke_text:
            return joke_text
        
        # Replace all variations of Chuck Norris
        replacements = [
            ("Chuck Norris", mascot),
            ("chuck norris", mascot.lower()),
            ("CHUCK NORRIS", mascot.upper()),
        ]
        
        transformed = joke_text
        for old, new in replacements:
            transformed = transformed.replace(old, new)
        
        return transformed
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

# Initialize the joke service
joke_service = JokeService()

@app.get("/")
async def root():
    """Welcome endpoint with API information"""
    return {
        "message": "Welcome to the Meow Norris Joke API! 🐱🐶",
        "description": "Get Chuck Norris jokes transformed for our office mascots",
        "endpoints": {
            "random_meow_joke": "/jokes/random",
            "random_woof_joke": "/jokes/woof/random", 
            "joke_by_category": "/jokes/category/{category}",
            "woof_joke_by_category": "/jokes/woof/category/{category}",
            "categories": "/jokes/categories",
            "mascots": "/mascots",
            "custom_mascot": "/jokes/random?mascot=YourMascot"
        },
        "popular_mascots": ["Meow Norris", "Woof Norris", "Chirp Norris", "Oink Norris"]
    }

@app.get("/jokes/random")
async def get_random_meow_joke(mascot: Optional[str] = "Meow Norris"):
    """
    Get a random Meow Norris joke
    
    - **mascot**: Optional custom mascot name (default: "Meow Norris")
    """
    joke_data = await joke_service.fetch_random_joke()
    
    original_joke = joke_data.get("value", "")
    transformed_joke = joke_service.transform_to_meow_norris(original_joke, mascot)
    
    return {
        "id": joke_data.get("id"),
        "joke": transformed_joke,
        "mascot": mascot,
        "categories": joke_data.get("categories", []),
        "created_at": joke_data.get("created_at"),
        "updated_at": joke_data.get("updated_at")
    }

@app.get("/jokes/category/{category}")
async def get_joke_by_category(category: str, mascot: Optional[str] = "Meow Norris"):
    """
    Get a Meow Norris joke from a specific category
    
    - **category**: The joke category (e.g., "animal", "career", "celebrity")
    - **mascot**: Optional custom mascot name (default: "Meow Norris")
    """
    joke_data = await joke_service.fetch_joke_by_category(category)
    
    original_joke = joke_data.get("value", "")
    transformed_joke = joke_service.transform_to_meow_norris(original_joke, mascot)
    
    return {
        "id": joke_data.get("id"),
        "joke": transformed_joke,
        "category": category,
        "mascot": mascot,
        "created_at": joke_data.get("created_at"),
        "updated_at": joke_data.get("updated_at")
    }

@app.get("/jokes/categories")
async def get_joke_categories():
    """
    Get all available joke categories
    """
    categories = await joke_service.get_categories()
    return {
        "categories": categories,
        "total": len(categories)
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test external API connectivity
        response = await joke_service.client.get(f"{CHUCK_NORRIS_API_BASE}/categories")
        if response.status_code == 200:
            return {"status": "healthy", "external_api": "connected"}
        else:
            return {"status": "degraded", "external_api": "issues"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {"status": "unhealthy", "external_api": "disconnected"}

@app.get("/jokes/woof/random")
async def get_random_woof_joke():
    """
    Get a random Woof Norris joke (our dog mascot!)
    """
    joke_data = await joke_service.fetch_random_joke()
    
    original_joke = joke_data.get("value", "")
    transformed_joke = joke_service.transform_to_meow_norris(original_joke, "Woof Norris")
    
    return {
        "id": joke_data.get("id"),
        "joke": transformed_joke,
        "mascot": "Woof Norris",
        "categories": joke_data.get("categories", []),
        "created_at": joke_data.get("created_at"),
        "updated_at": joke_data.get("updated_at")
    }

@app.get("/jokes/woof/category/{category}")
async def get_woof_joke_by_category(category: str):
    """
    Get a Woof Norris joke from a specific category
    
    - **category**: The joke category (e.g., "animal", "career", "celebrity")
    """
    joke_data = await joke_service.fetch_joke_by_category(category)
    
    original_joke = joke_data.get("value", "")
    transformed_joke = joke_service.transform_to_meow_norris(original_joke, "Woof Norris")
    
    return {
        "id": joke_data.get("id"),
        "joke": transformed_joke,
        "category": category,
        "mascot": "Woof Norris",
        "created_at": joke_data.get("created_at"),
        "updated_at": joke_data.get("updated_at")
    }

@app.get("/mascots")
async def get_available_mascots():
    """
    Get all available mascots and their descriptions
    """
    return {
        "mascots": [
            {
                "name": "Meow Norris",
                "type": "cat",
                "description": "Our office cat mascot - the original and most popular!",
                "example_endpoint": "/jokes/random?mascot=Meow%20Norris"
            },
            {
                "name": "Woof Norris",
                "type": "dog", 
                "description": "Our office dog mascot - loyal and funny!",
                "example_endpoint": "/jokes/woof/random"
            },
            {
                "name": "Chirp Norris",
                "type": "bird",
                "description": "Our office bird mascot - small but mighty!",
                "example_endpoint": "/jokes/random?mascot=Chirp%20Norris"
            },
            {
                "name": "Oink Norris", 
                "type": "pig",
                "description": "Our office pig mascot - smart and strong!",
                "example_endpoint": "/jokes/random?mascot=Oink%20Norris"
            }
        ],
        "total": 4,
        "note": "You can use any custom mascot name with the 'mascot' parameter!"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
