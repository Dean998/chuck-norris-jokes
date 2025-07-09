# 🐱🐶 Meow & Woof Norris Joke API

A fun API that fetches Chuck Norris jokes and transforms them into jokes for our office mascots! Originally built for "Meow Norris" (our cat), now expanded to support "Woof Norris" (our dog) and other pet mascots. Built as part of the ManyPets engineering take-home assignment.

## 🚀 Features

- Fetch random Meow Norris jokes
- **NEW**: Dedicated Woof Norris endpoints! 🐶
- Get jokes by category (animal, career, celebrity, etc.)
- Support for custom mascots (Chirp Norris, Oink Norris, etc.)
- Mascot information endpoint
- Comprehensive error handling and logging
- Health check endpoint
- Full test coverage
- Interactive API documentation

## 🛠️ Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **httpx**: Async HTTP client for external API calls
- **Uvicorn**: Lightning-fast ASGI server
- **Pytest**: Testing framework with async support

## 📁 Project Structure

```
many-pets-interview/
├── main.py              # Main FastAPI application
├── test_main.py         # Comprehensive test suite
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .gitignore          # Git ignore patterns
```

## 🏃‍♂️ Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the API

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### 3. View Interactive Documentation

Visit `http://localhost:8000/docs` for Swagger UI documentation, or `http://localhost:8000/redoc` for ReDoc.

## 📚 API Endpoints

### GET `/`
Welcome endpoint with API information and available mascots.

### GET `/jokes/random`
Get a random Meow Norris joke.

**Query Parameters:**
- `mascot` (optional): Custom mascot name (default: "Meow Norris")

### GET `/jokes/woof/random` 🆕
Get a random Woof Norris joke (dedicated dog mascot endpoint).

### GET `/jokes/category/{category}`
Get a Meow Norris joke from a specific category.

### GET `/jokes/woof/category/{category}` 🆕  
Get a Woof Norris joke from a specific category.

### GET `/jokes/categories`
Get all available joke categories.

### GET `/mascots` 🆕
Get information about all available mascots.

### GET `/health`
Health check endpoint.

**Examples:**
```bash
# Meow Norris (original)
curl "http://localhost:8000/jokes/random"

# Woof Norris (new dedicated endpoint)
curl "http://localhost:8000/jokes/woof/random"

# Custom mascot
curl "http://localhost:8000/jokes/random?mascot=Chirp%20Norris"

# Category-specific Woof Norris
curl "http://localhost:8000/jokes/woof/category/animal"

# See all available mascots
curl "http://localhost:8000/mascots"
```

## 🧪 Running Tests

```bash
pytest test_main.py -v
```

For test coverage:
```bash
pytest test_main.py --cov=main --cov-report=html
```

## 📋 Example Responses

### Random Joke
```json
{
  "id": "abc123",
  "joke": "Meow Norris doesn't wear a watch. He decides what time it is.",
  "mascot": "Meow Norris",
  "categories": ["dev"],
  "created_at": "2020-01-05 13:42:19.576875",
  "updated_at": "2020-01-05 13:42:19.576875"
}
```

### Categories
```json
{
  "categories": ["animal", "career", "celebrity", "dev", "explicit", "fashion", "food", "history", "money", "movie", "music", "political", "religion", "science", "sport", "travel"],
  "total": 16
}
```

## 🔧 Configuration

The API uses the Chuck Norris API (`https://api.chucknorris.io`) as the data source. No additional configuration is required.

## 🚨 Error Handling

The API includes comprehensive error handling:

- **503 Service Unavailable**: When the external Chuck Norris API is unreachable
- **Proper HTTP status codes**: For different error scenarios
- **Detailed error messages**: To help with debugging
- **Logging**: For monitoring and troubleshooting

## 🎯 Design Decisions

### Why FastAPI?
- Modern async/await support for better performance
- Automatic API documentation generation
- Excellent type hints and validation
- Great developer experience

### Architecture
- **Service Layer**: `JokeService` handles all external API interactions
- **Separation of Concerns**: Clear separation between API routes and business logic
- **Error Boundaries**: Proper exception handling at service and API levels
- **Resource Management**: Proper cleanup of HTTP connections

### Extensibility
The API is designed to easily support additional mascots and features:
- Custom mascot parameter allows for "Woof Norris", "Bark Norris", etc.
- Service layer makes it easy to add caching or database storage
- Modular structure allows for easy feature additions

## 🤝 Development

This project demonstrates:
- ✅ Clean, readable code with proper type hints
- ✅ RESTful API design principles
- ✅ Comprehensive error handling and validation
- ✅ Async/await for better performance
- ✅ Full test coverage with mocking
- ✅ Proper logging and monitoring hooks
- ✅ Interactive API documentation
- ✅ Git version control best practices

---

Built with ❤️ for the ManyPets engineering team interview process.
