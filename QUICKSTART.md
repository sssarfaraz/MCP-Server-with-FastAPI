# Quick Start Guide - College Library Management System

## 5-Minute Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Initialize Sample Data (Optional)
```bash
python init_sample_data.py
```

### Step 3: Start the Server
```bash
python fast_api.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 4: Open API Documentation
Visit: **http://localhost:8000/docs**

You'll see the interactive Swagger UI with all available endpoints.

---

## Common Tasks

### 📚 Add a Book

```bash
curl -X POST "http://localhost:8000/books" \
  -H "Content-Type: application/json" \
  -d {
    "book_id": 0,
    "title": "Learn FastAPI",
    "author": "Sebastián Ramírez",
    "isbn": "123-456-789",
    "publication_year": 2023,
    "total_copies": 3,
    "available_copies": 3,
    "category": "Web Development",
    "description": "Build APIs with FastAPI"
  }'
```

Or use Swagger UI:
1. Click `/books POST` endpoint
2. Click "Try it out"
3. Fill in the fields
4. Click "Execute"

### 👥 Register a Student

```bash
curl -X POST "http://localhost:8000/students" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "STU999",
    "name": "Jane Doe",
    "email": "jane@college.edu",
    "phone": "555-9999",
    "enrollment_year": 2024,
    "active": true
  }'
```

### 📖 Borrow a Book

```bash
curl -X POST "http://localhost:8000/borrow?student_id=STU001&book_id=1&borrow_days=14"
```

Response:
```json
{
  "record_id": 1,
  "student_id": "STU001",
  "book_id": 1,
  "borrow_date": "2024-05-31T10:30:00.000000",
  "due_date": "2024-06-14T10:30:00.000000",
  "returned": false
}
```

### 📥 Return a Book

```bash
curl -X POST "http://localhost:8000/return?record_id=1"
```

### 🔍 Search Books

```bash
curl "http://localhost:8000/books?category=Programming&limit=5"
```

### 👤 Get Student Info

```bash
curl "http://localhost:8000/students/STU001"
```

### 📊 Get Statistics

```bash
curl "http://localhost:8000/statistics"
```

Response:
```json
{
  "total_books": 10,
  "total_copies": 27,
  "available_copies": 18,
  "borrowed_copies": 9,
  "active_students": 5,
  "active_borrows": 3
}
```

---

## Using the MCP Server

### Start MCP Server
```bash
python mcp_library_server.py
```

This server provides 8 tools for programmatic access:
- `add_book` - Add books to catalog
- `search_books` - Find books
- `register_student` - Register students
- `list_students` - View all students
- `borrow_book` - Borrow books
- `return_book` - Return books
- `get_student_history` - View borrow history
- `library_statistics` - Get library stats

---

## Project Files

| File | Purpose |
|------|---------|
| `fast_api.py` | Main FastAPI application |
| `mcp_library_server.py` | MCP server with 8 tools |
| `init_sample_data.py` | Sample data initialization |
| `library_db.json` | Auto-created database file |
| `requirements.txt` | Python dependencies |
| `README.md` | Full documentation |

---

## Troubleshooting

### ❌ ModuleNotFoundError: No module named 'fastapi'
**Solution:** 
```bash
pip install -r requirements.txt
```

### ❌ Port 8000 already in use
**Solution:** Edit `fast_api.py`, change port in last line:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Use 8001 instead
```

### ❌ Database errors
**Solution:** Delete `library_db.json` and restart the server (it will recreate it)

### ❌ CORS errors in browser
Already handled! The system includes CORS middleware for all origins.

---

## Next Steps

1. ✅ Run sample data: `python init_sample_data.py`
2. ✅ Start server: `python fast_api.py`
3. ✅ Open Swagger UI: http://localhost:8000/docs
4. ✅ Test a few endpoints
5. ✅ Read README.md for detailed documentation

---

## Tips

- **Swagger UI** at `/docs` is perfect for testing endpoints
- **ReDoc** at `/redoc` shows beautiful API documentation
- **Database** is automatically saved after each operation
- **Sample data** includes 10 books and 6 students for testing
- **Free 14-day borrow period** by default

---

Enjoy using the College Library Management System! 📚
