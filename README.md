# College Library Management System - FastAPI + MCP Server

A comprehensive college library management system built with FastAPI and MCP (Model Context Protocol) server integration.

## Features

### 📚 Book Management
- Add, update, delete, and search books
- Track total and available copies
- Organize books by categories
- Store ISBN and publication details

### 👥 Student Management
- Register and manage student profiles
- Track active/inactive students
- Maintain student contact information

### 📖 Borrowing System
- Record book borrowing with automatic due dates
- Process book returns
- Track borrowing history per student
- Prevent over-borrowing

### 📊 Statistics & Reporting
- Library statistics (books, copies, active borrowers)
- Student borrow history
- Active borrowing records

### 🤖 MCP Server Integration
- 8 specialized tools for library operations
- Seamless integration with Claude and other AI models
- Tool-based API for programmatic access

## Project Structure

```
├── fast_api.py                 # Main FastAPI application
├── mcp_library_server.py       # MCP server implementation
├── requirements.txt            # Python dependencies
└── library_db.json             # SQLite-like JSON database (auto-created)
```

## Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Verify installation:**
```bash
python -c "import fastapi; import uvicorn; print('✓ Dependencies installed successfully')"
```

## Running the Application

### Option 1: FastAPI REST API

Start the FastAPI server:

```bash
python fast_api.py
```

The API will be available at: `http://localhost:8000`

- **API Documentation:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Option 2: MCP Server

Start the MCP server:

```bash
python mcp_library_server.py
```

This launches the MCP server for use with Claude and other MCP clients.

## API Endpoints

### Books Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| POST | `/books` | Add a new book |
| GET | `/books` | Get all books (with pagination) |
| GET | `/books/{book_id}` | Get specific book |
| PUT | `/books/{book_id}` | Update book details |
| DELETE | `/books/{book_id}` | Delete a book |

### Student Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/students` | Register new student |
| GET | `/students` | Get all students |
| GET | `/students/{student_id}` | Get specific student |
| PUT | `/students/{student_id}` | Update student info |

### Borrowing Operations

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/borrow` | Borrow a book |
| POST | `/return` | Return a book |
| GET | `/borrow-history/{student_id}` | Get student's history |
| GET | `/active-borrows` | Get all active borrows |

### System

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/statistics` | Library statistics |
| GET | `/health` | Health check |

## Usage Examples

### Example 1: Add a Book

```bash
curl -X POST "http://localhost:8000/books" \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": 0,
    "title": "Python Programming",
    "author": "Guido van Rossum",
    "isbn": "978-0134685991",
    "publication_year": 2015,
    "total_copies": 5,
    "available_copies": 5,
    "category": "Programming",
    "description": "Learning Python programming fundamentals"
  }'
```

### Example 2: Register a Student

```bash
curl -X POST "http://localhost:8000/students" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "STU001",
    "name": "John Doe",
    "email": "john@college.edu",
    "phone": "555-1234",
    "enrollment_year": 2023,
    "active": true
  }'
```

### Example 3: Borrow a Book

```bash
curl -X POST "http://localhost:8000/borrow?student_id=STU001&book_id=1&borrow_days=14" \
  -H "Content-Type: application/json"
```

### Example 4: Get Library Statistics

```bash
curl "http://localhost:8000/statistics"
```

Response:
```json
{
  "total_books": 10,
  "total_copies": 25,
  "available_copies": 15,
  "borrowed_copies": 10,
  "active_students": 50,
  "active_borrows": 10
}
```

## MCP Tools Available

### 1. `add_book`
Add a new book to the library catalog.

**Parameters:**
- `title` (required): Book title
- `author` (required): Author name
- `isbn` (required): ISBN number
- `publication_year` (required): Publication year
- `total_copies` (optional): Number of copies (default: 1)
- `category` (required): Book category
- `description` (optional): Book description

### 2. `search_books`
Search for books by title, author, or category.

**Parameters:**
- `query` (required): Search term
- `field` (optional): Search field - "all", "title", "author", or "category" (default: "all")

### 3. `register_student`
Register a new student.

**Parameters:**
- `student_id` (required): Unique student ID
- `name` (required): Full name
- `email` (required): Email address
- `phone` (required): Phone number
- `enrollment_year` (required): Year of enrollment

### 4. `list_students`
List all registered students.

**Parameters:**
- `active_only` (optional): Show only active students (default: false)

### 5. `borrow_book`
Record a book being borrowed.

**Parameters:**
- `student_id` (required): Student ID
- `book_id` (required): Book ID
- `borrow_days` (optional): Days to borrow (default: 14)

### 6. `return_book`
Record a book being returned.

**Parameters:**
- `record_id` (required): Borrow record ID

### 7. `get_student_history`
Get borrow history for a student.

**Parameters:**
- `student_id` (required): Student ID

### 8. `library_statistics`
Get current library statistics.

**Parameters:** None

## Data Models

### Book
```python
{
    "book_id": int,
    "title": str,
    "author": str,
    "isbn": str,
    "publication_year": int,
    "total_copies": int,
    "available_copies": int,
    "category": str,
    "description": str (optional)
}
```

### Student
```python
{
    "student_id": str,
    "name": str,
    "email": str,
    "phone": str,
    "enrollment_year": int,
    "active": bool
}
```

### BorrowRecord
```python
{
    "record_id": int,
    "student_id": str,
    "book_id": int,
    "borrow_date": str (ISO format),
    "return_date": str (ISO format, optional),
    "due_date": str (ISO format),
    "returned": bool
}
```

## Database

The system uses a JSON-based database (`library_db.json`) for persistence. The database is automatically created on first run and stores:

- Books catalog
- Student records
- Borrow history
- ID counters

## Configuration

Default settings can be modified:

### FastAPI Server
- Host: `0.0.0.0`
- Port: `8000`
- Auto-reload: Enabled

### Borrowing Rules
- Default borrow period: 14 days
- Configurable per borrow request

## Development

### Project Dependencies
- **FastAPI** (0.104.1): Web framework
- **Uvicorn** (0.24.0): ASGI server
- **Pydantic** (2.5.0): Data validation
- **MCP** (0.1.0): Model Context Protocol

### Adding New Features

1. Add new endpoint in `fast_api.py`
2. Add corresponding MCP tool in `mcp_library_server.py`
3. Update documentation

## Testing with Swagger UI

1. Start the server: `python fast_api.py`
2. Open: http://localhost:8000/docs
3. Test endpoints directly from the UI

## Troubleshooting

### Port Already in Use
If port 8000 is already in use:
```bash
python fast_api.py  # Will prompt for alternative port
```

### Database Issues
To reset the database:
```bash
rm library_db.json
python fast_api.py  # Recreates fresh database
```

### MCP Server Issues
Ensure MCP package is installed:
```bash
pip install mcp
```

## Future Enhancements

- [ ] Book reviews and ratings
- [ ] Fine calculation for overdue books
- [ ] Email notifications for due books
- [ ] Book reservation system
- [ ] Advanced search filters
- [ ] Database migration to SQLAlchemy + PostgreSQL
- [ ] Authentication and authorization
- [ ] Book image uploads
- [ ] Inventory reports

## License

This project is provided as-is for educational purposes.

## Support

For issues or questions, please refer to the documentation or contact the system administrator.
