"""
MCP Server for College Library Management System
Provides tools and resources for querying and managing the college library
"""

import json
import asyncio
from typing import Any
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from mcp.server import Server
from mcp.types import Tool, TextContent, ToolResult
import subprocess

# Import FastAPI app
try:
    from fast_api import db, Book, Student, BorrowRecord
except ImportError:
    print("Warning: Could not import FastAPI app. Make sure fast_api.py is in the same directory.")

# Create MCP server
server = Server("college-library-mcp")

# ==================== MCP Tools ====================

@server.call_tool()
async def handle_tool_call(name: str, arguments: dict) -> ToolResult:
    """Handle tool calls from MCP clients"""
    
    if name == "add_book":
        return await add_book_tool(arguments)
    elif name == "search_books":
        return await search_books_tool(arguments)
    elif name == "register_student":
        return await register_student_tool(arguments)
    elif name == "list_students":
        return await list_students_tool(arguments)
    elif name == "borrow_book":
        return await borrow_book_tool(arguments)
    elif name == "return_book":
        return await return_book_tool(arguments)
    elif name == "get_student_history":
        return await get_student_history_tool(arguments)
    elif name == "library_statistics":
        return await library_statistics_tool(arguments)
    else:
        return ToolResult(content=[TextContent(type="text", text=f"Unknown tool: {name}")])

async def add_book_tool(arguments: dict) -> ToolResult:
    """Add a new book to the library"""
    try:
        book_dict = {
            "book_id": db.data["book_id_counter"],
            "title": arguments.get("title"),
            "author": arguments.get("author"),
            "isbn": arguments.get("isbn"),
            "publication_year": arguments.get("publication_year"),
            "total_copies": arguments.get("total_copies", 1),
            "available_copies": arguments.get("total_copies", 1),
            "category": arguments.get("category"),
            "description": arguments.get("description")
        }
        db.data["books"].append(book_dict)
        db.data["book_id_counter"] += 1
        db.save_database()
        return ToolResult(content=[TextContent(
            type="text",
            text=f"✓ Book '{book_dict['title']}' added successfully with ID {book_dict['book_id']}"
        )])
    except Exception as e:
        return ToolResult(content=[TextContent(type="text", text=f"✗ Error: {str(e)}")])

async def search_books_tool(arguments: dict) -> ToolResult:
    """Search for books by title, author, or category"""
    try:
        search_term = arguments.get("query", "").lower()
        search_field = arguments.get("field", "all")  # all, title, author, category
        
        results = []
        for book in db.data["books"]:
            match = False
            if search_field in ["all", "title"]:
                if search_term in book["title"].lower():
                    match = True
            if search_field in ["all", "author"]:
                if search_term in book["author"].lower():
                    match = True
            if search_field in ["all", "category"]:
                if search_term in book["category"].lower():
                    match = True
            
            if match:
                results.append(book)
        
        if results:
            result_text = "Found books:\n\n"
            for book in results:
                result_text += f"• {book['title']} by {book['author']}\n"
                result_text += f"  ID: {book['book_id']} | Category: {book['category']}\n"
                result_text += f"  Available: {book['available_copies']}/{book['total_copies']}\n\n"
            return ToolResult(content=[TextContent(type="text", text=result_text)])
        else:
            return ToolResult(content=[TextContent(type="text", text="✓ No books found matching your search.")])
    except Exception as e:
        return ToolResult(content=[TextContent(type="text", text=f"✗ Error: {str(e)}")])

async def register_student_tool(arguments: dict) -> ToolResult:
    """Register a new student"""
    try:
        student_id = arguments.get("student_id")
        
        # Check if student exists
        for s in db.data["students"]:
            if s["student_id"] == student_id:
                return ToolResult(content=[TextContent(type="text", text="✗ Student already exists")])
        
        student_dict = {
            "student_id": student_id,
            "name": arguments.get("name"),
            "email": arguments.get("email"),
            "phone": arguments.get("phone"),
            "enrollment_year": arguments.get("enrollment_year"),
            "active": True
        }
        db.data["students"].append(student_dict)
        db.save_database()
        return ToolResult(content=[TextContent(
            type="text",
            text=f"✓ Student '{student_dict['name']}' registered successfully with ID {student_id}"
        )])
    except Exception as e:
        return ToolResult(content=[TextContent(type="text", text=f"✗ Error: {str(e)}")])

async def list_students_tool(arguments: dict) -> ToolResult:
    """List all registered students"""
    try:
        active_only = arguments.get("active_only", False)
        students = db.data["students"]
        
        if active_only:
            students = [s for s in students if s["active"]]
        
        if students:
            result_text = f"Registered Students ({len(students)}):\n\n"
            for student in students:
                status = "Active" if student["active"] else "Inactive"
                result_text += f"• {student['name']}\n"
                result_text += f"  ID: {student['student_id']} | Status: {status}\n"
                result_text += f"  Email: {student['email']}\n\n"
            return ToolResult(content=[TextContent(type="text", text=result_text)])
        else:
            return ToolResult(content=[TextContent(type="text", text="✓ No students registered yet.")])
    except Exception as e:
        return ToolResult(content=[TextContent(type="text", text=f"✗ Error: {str(e)}")])

async def borrow_book_tool(arguments: dict) -> ToolResult:
    """Record a student borrowing a book"""
    try:
        student_id = arguments.get("student_id")
        book_id = arguments.get("book_id")
        borrow_days = arguments.get("borrow_days", 14)
        
        # Check student exists
        student = None
        for s in db.data["students"]:
            if s["student_id"] == student_id:
                student = s
                break
        
        if not student:
            return ToolResult(content=[TextContent(type="text", text="✗ Student not found")])
        
        # Check book exists and has copies
        book = None
        for b in db.data["books"]:
            if b["book_id"] == book_id:
                book = b
                break
        
        if not book:
            return ToolResult(content=[TextContent(type="text", text="✗ Book not found")])
        
        if book["available_copies"] <= 0:
            return ToolResult(content=[TextContent(type="text", text="✗ Book not available")])
        
        # Create borrow record
        from datetime import datetime, timedelta
        borrow_date = datetime.now()
        due_date = borrow_date + timedelta(days=borrow_days)
        
        record = {
            "record_id": db.data["record_id_counter"],
            "student_id": student_id,
            "book_id": book_id,
            "borrow_date": borrow_date.isoformat(),
            "return_date": None,
            "due_date": due_date.isoformat(),
            "returned": False
        }
        
        db.data["borrow_records"].append(record)
        db.data["record_id_counter"] += 1
        book["available_copies"] -= 1
        db.save_database()
        
        return ToolResult(content=[TextContent(
            type="text",
            text=f"✓ Book '{book['title']}' borrowed by {student['name']}\nDue: {due_date.strftime('%Y-%m-%d')}"
        )])
    except Exception as e:
        return ToolResult(content=[TextContent(type="text", text=f"✗ Error: {str(e)}")])

async def return_book_tool(arguments: dict) -> ToolResult:
    """Record a student returning a book"""
    try:
        record_id = arguments.get("record_id")
        
        for record in db.data["borrow_records"]:
            if record["record_id"] == record_id:
                if record["returned"]:
                    return ToolResult(content=[TextContent(type="text", text="✗ Book already returned")])
                
                from datetime import datetime
                record["returned"] = True
                record["return_date"] = datetime.now().isoformat()
                
                # Update book availability
                for book in db.data["books"]:
                    if book["book_id"] == record["book_id"]:
                        book["available_copies"] += 1
                        break
                
                db.save_database()
                return ToolResult(content=[TextContent(
                    type="text",
                    text=f"✓ Book returned successfully. Record ID: {record_id}"
                )])
        
        return ToolResult(content=[TextContent(type="text", text="✗ Borrow record not found")])
    except Exception as e:
        return ToolResult(content=[TextContent(type="text", text=f"✗ Error: {str(e)}")])

async def get_student_history_tool(arguments: dict) -> ToolResult:
    """Get borrow history for a student"""
    try:
        student_id = arguments.get("student_id")
        
        records = [r for r in db.data["borrow_records"] if r["student_id"] == student_id]
        
        if records:
            result_text = f"Borrow History for {student_id}:\n\n"
            for record in records:
                # Find book title
                book_title = "Unknown"
                for book in db.data["books"]:
                    if book["book_id"] == record["book_id"]:
                        book_title = book["title"]
                        break
                
                status = "Returned" if record["returned"] else "Active"
                result_text += f"• {book_title}\n"
                result_text += f"  Borrowed: {record['borrow_date'][:10]}\n"
                result_text += f"  Due: {record['due_date'][:10]}\n"
                result_text += f"  Status: {status}\n\n"
            
            return ToolResult(content=[TextContent(type="text", text=result_text)])
        else:
            return ToolResult(content=[TextContent(type="text", text="✓ No borrow records found")])
    except Exception as e:
        return ToolResult(content=[TextContent(type="text", text=f"✗ Error: {str(e)}")])

async def library_statistics_tool(arguments: dict) -> ToolResult:
    """Get library statistics"""
    try:
        total_books = len(db.data["books"])
        total_copies = sum(b["total_copies"] for b in db.data["books"]) if db.data["books"] else 0
        available_copies = sum(b["available_copies"] for b in db.data["books"]) if db.data["books"] else 0
        borrowed_copies = total_copies - available_copies
        active_students = len([s for s in db.data["students"] if s["active"]])
        active_borrows = len([r for r in db.data["borrow_records"] if not r["returned"]])
        
        stats_text = f"""
📚 College Library Statistics

Books:
  • Total unique books: {total_books}
  • Total copies: {total_copies}
  • Available: {available_copies}
  • Borrowed: {borrowed_copies}

Students:
  • Active students: {active_students}
  • Active borrowers: {active_borrows}
"""
        
        return ToolResult(content=[TextContent(type="text", text=stats_text)])
    except Exception as e:
        return ToolResult(content=[TextContent(type="text", text=f"✗ Error: {str(e)}")])

# ==================== Tool Definitions ====================

def setup_tools():
    """Register all available tools with the server"""
    
    server.tool_schemas = [
        Tool(
            name="add_book",
            description="Add a new book to the library catalog",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Book title"},
                    "author": {"type": "string", "description": "Author name"},
                    "isbn": {"type": "string", "description": "ISBN number"},
                    "publication_year": {"type": "integer", "description": "Year of publication"},
                    "total_copies": {"type": "integer", "description": "Number of copies", "default": 1},
                    "category": {"type": "string", "description": "Book category"},
                    "description": {"type": "string", "description": "Book description"}
                },
                "required": ["title", "author", "isbn", "publication_year", "category"]
            }
        ),
        Tool(
            name="search_books",
            description="Search for books by title, author, or category",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "field": {"type": "string", "enum": ["all", "title", "author", "category"], "default": "all"}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="register_student",
            description="Register a new student in the system",
            inputSchema={
                "type": "object",
                "properties": {
                    "student_id": {"type": "string", "description": "Unique student ID"},
                    "name": {"type": "string", "description": "Student name"},
                    "email": {"type": "string", "description": "Email address"},
                    "phone": {"type": "string", "description": "Phone number"},
                    "enrollment_year": {"type": "integer", "description": "Year of enrollment"}
                },
                "required": ["student_id", "name", "email", "phone", "enrollment_year"]
            }
        ),
        Tool(
            name="list_students",
            description="List all registered students",
            inputSchema={
                "type": "object",
                "properties": {
                    "active_only": {"type": "boolean", "description": "Show only active students", "default": False}
                }
            }
        ),
        Tool(
            name="borrow_book",
            description="Record a student borrowing a book",
            inputSchema={
                "type": "object",
                "properties": {
                    "student_id": {"type": "string", "description": "Student ID"},
                    "book_id": {"type": "integer", "description": "Book ID"},
                    "borrow_days": {"type": "integer", "description": "Number of days to borrow", "default": 14}
                },
                "required": ["student_id", "book_id"]
            }
        ),
        Tool(
            name="return_book",
            description="Record a book being returned",
            inputSchema={
                "type": "object",
                "properties": {
                    "record_id": {"type": "integer", "description": "Borrow record ID"}
                },
                "required": ["record_id"]
            }
        ),
        Tool(
            name="get_student_history",
            description="Get borrow history for a student",
            inputSchema={
                "type": "object",
                "properties": {
                    "student_id": {"type": "string", "description": "Student ID"}
                },
                "required": ["student_id"]
            }
        ),
        Tool(
            name="library_statistics",
            description="Get library statistics and current status",
            inputSchema={"type": "object", "properties": {}}
        )
    ]

def main():
    """Start the MCP server"""
    print("Starting College Library MCP Server...")
    print("Server name: college-library-mcp")
    print("Available tools: 8")
    
    setup_tools()
    
    # Run the server
    import mcp.server.stdio
    mcp.server.stdio.stdio_server(server)

if __name__ == "__main__":
    main()
