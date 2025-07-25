# 🐱🐶 Meow & Woof Norris Joke API

```
      /\_/\  
     ( o.o ) 
      > ^ <    "I don't always tell jokes, but when I do, they're purrfect."
                                                    - Meow Norris
```

A fun API that fetches Chuck Norris jokes and transforms them into jokes for our office mascots! Originally built for "Meow Norris" (our cat), now expanded to support "Woof Norris" (our dog) and other pet mascots.

```
    🐶 Woof Norris says: "Fetch this API, it's pawsome!"
```

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


## 📋 Example Responses

### Random Meow Norris Joke
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

### Random Woof Norris Joke
```json
{
  "id": "def456", 
  "joke": "Woof Norris doesn't fetch the ball. The ball fetches itself.",
  "mascot": "Woof Norris",
  "categories": ["animal"],
  "created_at": "2020-01-05 13:42:19.576875",
  "updated_at": "2020-01-05 13:42:19.576875"
}
```

### Available Mascots
```json
{
  "mascots": [
    {
      "name": "Meow Norris",
      "type": "cat",
      "description": "Our office cat mascot - the original and most popular! 🐱",
      "ascii": "  /\\_/\\  \n ( o.o ) \n  > ^ <  "
    },
    {
      "name": "Woof Norris", 
      "type": "dog",
      "description": "Our office dog mascot - loyal and funny! 🐶",
      "ascii": "  /|   /|  \n (  ._.) \n  o_(\")(\") "
    }
  ],
  "total": 4
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
