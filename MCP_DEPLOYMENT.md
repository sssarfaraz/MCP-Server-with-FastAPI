# MCP Server Deployment Guide

## Overview

The College Library Management System can run as an MCP (Model Context Protocol) server, providing AI models like Claude with the ability to interact with the library system programmatically.

## MCP Server Architecture

```
┌─────────────────────────────────────┐
│     Claude / AI Client              │
└──────────────┬──────────────────────┘
               │ (JSON-RPC over stdio)
               │
┌──────────────▼──────────────────────┐
│  MCP Library Server                 │
│  (mcp_library_server.py)            │
│  - add_book                         │
│  - search_books                     │
│  - register_student                 │
│  - list_students                    │
│  - borrow_book                      │
│  - return_book                      │
│  - get_student_history              │
│  - library_statistics               │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  FastAPI Server (fast_api.py)       │
│  (Optional - for REST API)          │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  JSON Database (library_db.json)    │
└─────────────────────────────────────┘
```

## Installation for MCP

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `fastapi` - API framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation
- `mcp` - Model Context Protocol

### 2. Start MCP Server

```bash
python mcp_library_server.py
```

You should see:
```
Starting College Library MCP Server...
Server name: college-library-mcp
Available tools: 8
```

The server will listen on stdin/stdout for JSON-RPC messages.

## Integration with Claude

### Option 1: Claude Desktop (Mac/Windows/Linux)

1. **Configure Claude Desktop to use the MCP server**

   On **Mac/Linux**, edit `~/.config/Claude/claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "college-library": {
         "command": "python",
         "args": [
           "path/to/mcp_library_server.py"
         ],
         "env": {
           "PYTHONUNBUFFERED": "1"
         }
       }
     }
   }
   ```

   On **Windows**, edit `%APPDATA%\Claude\claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "college-library": {
         "command": "python",
         "args": [
           "C:\\path\\to\\mcp_library_server.py"
         ],
         "env": {
           "PYTHONUNBUFFERED": "1"
         }
       }
     }
   }
   ```

2. **Restart Claude Desktop**

3. **Test with Claude**
   - Open Claude
   - The library tools should now be available
   - Try asking: "What books do we have in our library?"

### Option 2: Claude via Web UI

The web version of Claude doesn't directly support local MCP servers. Instead, you can:

1. Keep the REST API server running: `python fast_api.py`
2. Use Claude to call the REST API endpoints through its tools

### Option 3: Custom Integration

Create a wrapper that translates MCP calls to your system:

```python
import asyncio
from mcp_library_server import handle_tool_call

async def call_mcp_tool(tool_name, arguments):
    """Call MCP tool from external code"""
    result = await handle_tool_call(tool_name, arguments)
    return result

# Usage
result = asyncio.run(call_mcp_tool("library_statistics", {}))
```

## Example Claude Conversations

### Example 1: Searching for Books

**User:** "Find all Python programming books in our library"

**Claude will:**
1. Call `search_books` tool with query="Python" and field="title"
2. Receive list of matching books
3. Format and present results

**Behind the scenes:**
```json
{
  "tool": "search_books",
  "arguments": {
    "query": "Python",
    "field": "title"
  }
}
```

### Example 2: Managing Student Borrowing

**User:** "Register a new student Alice (alice@college.edu) with ID STU999 enrolled in 2024"

**Claude will:**
1. Call `register_student` tool with provided information
2. Create the student record
3. Confirm registration

**Behind the scenes:**
```json
{
  "tool": "register_student",
  "arguments": {
    "student_id": "STU999",
    "name": "Alice",
    "email": "alice@college.edu",
    "phone": "555-0000",
    "enrollment_year": 2024
  }
}
```

### Example 3: Borrow/Return Books

**User:** "Student STU001 wants to borrow book ID 5"

**Claude will:**
1. Call `borrow_book` tool
2. Create borrow record
3. Update book availability
4. Return confirmation with due date

**Behind the scenes:**
```json
{
  "tool": "borrow_book",
  "arguments": {
    "student_id": "STU001",
    "book_id": 5,
    "borrow_days": 14
  }
}
```

## MCP Tools Reference

### 1. add_book
Add a new book to the catalog
```
Input: title, author, isbn, publication_year, category, [total_copies], [description]
Output: Confirmation with book ID
```

### 2. search_books
Search books by title, author, or category
```
Input: query, [field: "all"|"title"|"author"|"category"]
Output: List of matching books
```

### 3. register_student
Register a new student
```
Input: student_id, name, email, phone, enrollment_year
Output: Confirmation with student details
```

### 4. list_students
List all registered students
```
Input: [active_only: boolean]
Output: List of students with their info
```

### 5. borrow_book
Record a book borrow
```
Input: student_id, book_id, [borrow_days]
Output: Borrow record with due date
```

### 6. return_book
Record a book return
```
Input: record_id
Output: Confirmation of return
```

### 7. get_student_history
Get borrow history for a student
```
Input: student_id
Output: List of all borrow records for student
```

### 8. library_statistics
Get library statistics
```
Input: (none)
Output: Statistics on books, students, borrowing activity
```

## Environment Variables

Configure behavior with environment variables:

```bash
# Server configuration
export LIBRARY_HOST=0.0.0.0
export LIBRARY_PORT=8000
export LIBRARY_DEBUG=False

# Database location
export LIBRARY_DB_DIR=/path/to/db

# Borrowing rules
export LIBRARY_BORROW_DAYS=14
export LIBRARY_MAX_BOOKS=5
export LIBRARY_FINE_PER_DAY=0.50

# CORS configuration
export LIBRARY_CORS_ALL=True

# Logging
export LIBRARY_LOG_LEVEL=INFO
```

## Running Both Servers

You can run FastAPI and MCP servers simultaneously:

**Terminal 1 - FastAPI REST API:**
```bash
python fast_api.py
# Runs on http://localhost:8000
```

**Terminal 2 - MCP Server:**
```bash
python mcp_library_server.py
# Listens on stdin/stdout for JSON-RPC
```

## Debugging

### Enable Debug Logging

Edit `mcp_library_server.py` and add:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
```

### Test MCP Tools Directly

Create a test script:
```python
import asyncio
from mcp_library_server import handle_tool_call

async def test():
    result = await handle_tool_call("library_statistics", {})
    print(result)

asyncio.run(test())
```

### Verify Database

Check `library_db.json`:
```bash
python -m json.tool library_db.json
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'mcp'"

**Solution:**
```bash
pip install mcp
```

### MCP Server exits immediately

**Check:**
1. Python version (3.8+)
2. All dependencies installed
3. Database file permissions

**Debug:**
```bash
python mcp_library_server.py 2>&1
```

### Claude doesn't see tools

**Check:**
1. MCP server started successfully
2. Claude Desktop configuration syntax is correct
3. File paths are absolute, not relative
4. Restart Claude Desktop after config changes

### Tool calls fail

**Check:**
1. Database file exists and is readable
2. Input parameters match tool schema
3. Database has required data (books, students, etc.)

## Production Deployment

For production use:

1. **Use process manager** (systemd, supervisor)
2. **Add authentication** to REST API if needed
3. **Use proper database** (PostgreSQL instead of JSON)
4. **Enable logging** for audit trail
5. **Set up backups** for database
6. **Monitor resource usage**
7. **Use HTTPS** for REST API

Example systemd service:
```ini
[Unit]
Description=College Library MCP Server
After=network.target

[Service]
Type=simple
User=library
WorkingDirectory=/opt/library
ExecStart=/usr/bin/python3 /opt/library/mcp_library_server.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

## Additional Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [Claude API Documentation](https://docs.anthropic.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## Support

For issues or questions:
1. Check the README.md for general information
2. Check QUICKSTART.md for getting started
3. Review error logs in terminal
4. Verify all dependencies are installed
