# College Library Management System - Project Index

## 📦 Project Overview

A complete college library management system built with **FastAPI** and **MCP (Model Context Protocol) server**. This system provides both REST API and AI-friendly MCP tools for managing books, students, and borrowing operations.

---

## 📁 Project Files

### Core Application Files

| File | Purpose | Size |
|------|---------|------|
| **fast_api.py** | Main FastAPI application with REST API endpoints | Core |
| **mcp_library_server.py** | MCP server with 8 AI-friendly tools | Integration |
| **config.py** | Configuration and settings management | Configuration |

### Documentation Files

| File | Purpose |
|------|---------|
| **README.md** | Complete documentation with API reference |
| **QUICKSTART.md** | 5-minute setup and basic usage guide |
| **MCP_DEPLOYMENT.md** | MCP server deployment and Claude integration |
| **INDEX.md** | This file - project overview |

### Utility Files

| File | Purpose |
|------|---------|
| **init_sample_data.py** | Initialize database with sample data |
| **Print.py** | Demo script to test API |
| **requirements.txt** | Python dependencies |

### Auto-Generated Files

| File | Purpose |
|------|---------|
| **library_db.json** | SQLite-like JSON database (created on first run) |

---

## 🚀 Quick Start

### 1. Install
```bash
pip install -r requirements.txt
```

### 2. Initialize Sample Data (Optional)
```bash
python init_sample_data.py
```

### 3. Run REST API
```bash
python fast_api.py
```
Visit: http://localhost:8000/docs

### 4. Run MCP Server (Optional)
```bash
python mcp_library_server.py
```

### 5. Test with Demo Script
```bash
python Print.py
```

---

## 📚 API Overview

### REST API Endpoints (40+)

**Books:**
- `GET /books` - List books
- `POST /books` - Add book
- `GET /books/{id}` - Get book details
- `PUT /books/{id}` - Update book
- `DELETE /books/{id}` - Delete book

**Students:**
- `GET /students` - List students
- `POST /students` - Register student
- `GET /students/{id}` - Get student details
- `PUT /students/{id}` - Update student

**Borrowing:**
- `POST /borrow` - Borrow book
- `POST /return` - Return book
- `GET /borrow-history/{id}` - Student history
- `GET /active-borrows` - Active borrows

**System:**
- `GET /statistics` - Library stats
- `GET /health` - Server health
- `GET /` - Welcome

### MCP Tools (8)

1. **add_book** - Add books to catalog
2. **search_books** - Find books
3. **register_student** - Register students
4. **list_students** - View all students
5. **borrow_book** - Borrow books
6. **return_book** - Return books
7. **get_student_history** - View borrow history
8. **library_statistics** - Get statistics

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────┐
│   REST API Clients                  │
│   (Curl, Postman, Web Apps)         │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   FastAPI Application               │
│   (fast_api.py)                     │
└──────────────┬──────────────────────┘
               │
        ┌──────┴──────┐
        │             │
┌───────▼────┐  ┌─────▼──────────┐
│ JSON DB    │  │  MCP Server    │
│            │  │  (AI Tools)    │
└────────────┘  └────────────────┘
```

---

## 📊 Data Models

### Book
- book_id, title, author, isbn
- publication_year, category
- total_copies, available_copies
- description (optional)

### Student
- student_id, name, email, phone
- enrollment_year, active status

### BorrowRecord
- record_id, student_id, book_id
- borrow_date, due_date, return_date
- returned (boolean)

---

## 🔧 Configuration

Edit `config.py` to customize:
- Server host/port
- Database location
- Borrowing period (default: 14 days)
- Max books per student
- Fine amounts
- CORS settings

---

## 📖 Documentation Guide

**Start here:**
1. **QUICKSTART.md** - Get running in 5 minutes
2. **README.md** - Full feature documentation
3. **MCP_DEPLOYMENT.md** - AI integration guide

**For developers:**
- Look at `fast_api.py` for REST API implementation
- Look at `mcp_library_server.py` for MCP tool definitions
- See `config.py` for configuration options

**For deployment:**
- Follow **MCP_DEPLOYMENT.md** for production setup
- Read environment variables section in config

---

## ✨ Key Features

✅ **Complete REST API** - Full CRUD operations for all resources
✅ **MCP Integration** - 8 AI-friendly tools for Claude
✅ **JSON Database** - Simple, file-based persistence
✅ **Automatic Documentation** - Swagger UI at /docs
✅ **Sample Data** - Initialization script with test data
✅ **Error Handling** - Proper HTTP status codes and messages
✅ **CORS Enabled** - Cross-origin request support
✅ **Type Validation** - Pydantic models for data validation

---

## 🛠️ Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run REST API
python fast_api.py

# Run MCP Server
python mcp_library_server.py

# Initialize sample data
python init_sample_data.py

# Test with demo script
python Print.py

# Check configuration
python config.py
```

---

## 📈 Use Cases

1. **College IT Department** - Manage physical library
2. **Library Automation** - Automate borrowing/returning
3. **Student Portals** - Integration with student systems
4. **AI Assistants** - Claude integration for library queries
5. **Mobile Apps** - REST API for mobile applications
6. **Inventory Management** - Track books and copies

---

## 🔐 Future Enhancements

- [ ] PostgreSQL database integration
- [ ] User authentication & authorization
- [ ] Email notifications for overdue books
- [ ] Book reservation system
- [ ] Fine calculation for overdue books
- [ ] Book reviews and ratings
- [ ] Advanced search with filters
- [ ] Analytics dashboard
- [ ] Multi-branch library support
- [ ] Mobile app

---

## 📞 Support

**Documentation:**
- README.md - Feature overview
- QUICKSTART.md - Getting started
- MCP_DEPLOYMENT.md - AI integration
- config.py - Configuration options

**Troubleshooting:**
See README.md "Troubleshooting" section

---

## 📝 File Structure

```
Python_Practice/
├── fast_api.py                 # Main FastAPI app (280+ lines)
├── mcp_library_server.py       # MCP server (350+ lines)
├── Print.py                    # Demo script (200+ lines)
├── config.py                   # Configuration
├── init_sample_data.py         # Sample data generator
├── library_db.json             # Auto-created database
├── requirements.txt            # Dependencies
├── README.md                   # Full documentation
├── QUICKSTART.md               # Quick start guide
├── MCP_DEPLOYMENT.md           # MCP deployment guide
└── INDEX.md                    # This file
```

---

## 🎯 Getting Started Checklist

- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Initialize sample data: `python init_sample_data.py`
- [ ] Start FastAPI: `python fast_api.py`
- [ ] Open documentation: http://localhost:8000/docs
- [ ] Test endpoints in Swagger UI
- [ ] Read README.md for detailed information
- [ ] Test MCP server: `python mcp_library_server.py`
- [ ] Configure Claude with MCP server (see MCP_DEPLOYMENT.md)

---

## 📌 Version Information

- **System Version:** 1.0.0
- **FastAPI:** 0.104.1
- **Python:** 3.8+
- **Database:** JSON file-based
- **API Type:** REST + MCP

---

## ✅ Status

**✓ Core Features Complete**
- FastAPI REST API
- MCP Server with 8 tools
- Sample data initialization
- Configuration management
- Complete documentation

**Ready for:**
- Testing
- Development
- Production deployment (with enhancements)
- AI integration with Claude

---

Created: May 31, 2026
Last Updated: May 31, 2026

For the latest version and updates, see the README.md file.
