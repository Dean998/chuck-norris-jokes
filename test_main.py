import pytest
import httpx
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from main import app, joke_service

client = TestClient(app)

class TestJokeService:
    """Test the JokeService class"""
    
    def test_transform_to_meow_norris_basic(self):
        """Test basic Chuck Norris to Meow Norris transformation"""
        joke = "Chuck Norris can divide by zero."
        result = joke_service.transform_to_meow_norris(joke)
        assert result == "Meow Norris can divide by zero."
    
    def test_transform_to_meow_norris_case_insensitive(self):
        """Test case-insensitive transformation"""
        joke = "chuck norris and CHUCK NORRIS and Chuck Norris are all the same person."
        result = joke_service.transform_to_meow_norris(joke)
        assert result == "meow norris and MEOW NORRIS and Meow Norris are all the same person."
    
    def test_transform_with_custom_mascot(self):
        """Test transformation with custom mascot"""
        joke = "Chuck Norris doesn't sleep. He waits."
        result = joke_service.transform_to_meow_norris(joke, "Woof Norris")
        assert result == "Woof Norris doesn't sleep. He waits."
    
    def test_transform_empty_string(self):
        """Test transformation with empty string"""
        result = joke_service.transform_to_meow_norris("")
        assert result == ""
    
    def test_transform_no_chuck_norris(self):
        """Test transformation when Chuck Norris is not in the text"""
        joke = "This is a regular joke without the main character."
        result = joke_service.transform_to_meow_norris(joke)
        assert result == joke

class TestAPI:
    """Test the FastAPI endpoints"""
    
    def test_root_endpoint(self):
        """Test the root endpoint returns welcome message"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "Meow Norris" in data["message"]
        assert "endpoints" in data
    
    @patch('main.joke_service.fetch_random_joke')
    def test_random_joke_endpoint(self, mock_fetch):
        """Test the random joke endpoint"""
        mock_fetch.return_value = {
            "id": "test-id",
            "value": "Chuck Norris can speak braille.",
            "categories": ["dev"],
            "created_at": "2020-01-05 13:42:19.576875",
            "updated_at": "2020-01-05 13:42:19.576875"
        }
        
        response = client.get("/jokes/random")
        assert response.status_code == 200
        data = response.json()
        assert "Meow Norris can speak braille." == data["joke"]
        assert data["mascot"] == "Meow Norris"
        assert data["id"] == "test-id"
    
    @patch('main.joke_service.fetch_random_joke')
    def test_random_joke_with_custom_mascot(self, mock_fetch):
        """Test random joke with custom mascot parameter"""
        mock_fetch.return_value = {
            "id": "test-id",
            "value": "Chuck Norris invented the internet.",
            "categories": [],
            "created_at": "2020-01-05 13:42:19.576875",
            "updated_at": "2020-01-05 13:42:19.576875"
        }
        
        response = client.get("/jokes/random?mascot=Woof Norris")
        assert response.status_code == 200
        data = response.json()
        assert "Woof Norris invented the internet." == data["joke"]
        assert data["mascot"] == "Woof Norris"
    
    @patch('main.joke_service.fetch_joke_by_category')
    def test_category_joke_endpoint(self, mock_fetch):
        """Test the category-specific joke endpoint"""
        mock_fetch.return_value = {
            "id": "test-id",
            "value": "Chuck Norris is the reason Waldo is hiding.",
            "categories": ["celebrity"],
            "created_at": "2020-01-05 13:42:19.576875",
            "updated_at": "2020-01-05 13:42:19.576875"
        }
        
        response = client.get("/jokes/category/celebrity")
        assert response.status_code == 200
        data = response.json()
        assert "Meow Norris is the reason Waldo is hiding." == data["joke"]
        assert data["category"] == "celebrity"
    
    @patch('main.joke_service.get_categories')
    def test_categories_endpoint(self, mock_get_categories):
        """Test the categories endpoint"""
        mock_categories = ["animal", "career", "celebrity", "dev", "explicit", "fashion"]
        mock_get_categories.return_value = mock_categories
        
        response = client.get("/jokes/categories")
        assert response.status_code == 200
        data = response.json()
        assert data["categories"] == mock_categories
        assert data["total"] == len(mock_categories)
    
    @patch('main.joke_service.fetch_random_joke')
    def test_api_error_handling(self, mock_fetch):
        """Test API error handling when external service fails"""
        from fastapi import HTTPException
        mock_fetch.side_effect = HTTPException(status_code=503, detail="Unable to fetch joke from external service")
        
        response = client.get("/jokes/random")
        assert response.status_code == 503
        assert "Unable to fetch joke" in response.json()["detail"]
    
    @patch('main.joke_service.fetch_random_joke')
    def test_woof_norris_endpoint(self, mock_fetch):
        """Test the dedicated Woof Norris endpoint"""
        mock_fetch.return_value = {
            "id": "test-id",
            "value": "Chuck Norris doesn't do push-ups. He pushes the Earth down.",
            "categories": ["dev"],
            "created_at": "2020-01-05 13:42:19.576875",
            "updated_at": "2020-01-05 13:42:19.576875"
        }
        
        response = client.get("/jokes/woof/random")
        assert response.status_code == 200
        data = response.json()
        assert "Woof Norris doesn't do push-ups. He pushes the Earth down." == data["joke"]
        assert data["mascot"] == "Woof Norris"
    
    def test_mascots_endpoint(self):
        """Test the mascots information endpoint"""
        response = client.get("/mascots")
        assert response.status_code == 200
        data = response.json()
        assert "mascots" in data
        assert data["total"] == 4
        mascot_names = [mascot["name"] for mascot in data["mascots"]]
        assert "Meow Norris" in mascot_names
        assert "Woof Norris" in mascot_names

@pytest.mark.asyncio
class TestJokeServiceAsync:
    """Test async methods of JokeService"""
    
    @patch('httpx.AsyncClient.get')
    async def test_fetch_joke_http_error(self, mock_get):
        """Test joke fetching with HTTP error"""
        mock_get.side_effect = httpx.HTTPError("Connection failed")
        
        with pytest.raises(Exception):  # Should raise HTTPException
            await joke_service.fetch_random_joke()

if __name__ == "__main__":
    pytest.main([__file__])
