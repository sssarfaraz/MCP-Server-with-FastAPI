from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import List, Optional
import json
import os
from pathlib import Path

# FastAPI app initialization
app = FastAPI(
    title="College Library Management System",
    description="A comprehensive library management API for college",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database file path
DB_FILE = "library_db.json"

# ==================== Pydantic Models ====================

class Book(BaseModel):
    book_id: int
    title: str
    author: str
    isbn: str
    publication_year: int
    total_copies: int
    available_copies: int
    category: str
    description: Optional[str] = None

class Student(BaseModel):
    student_id: str
    name: str
    email: str
    phone: str
    enrollment_year: int
    active: bool = True

class BorrowRecord(BaseModel):
    record_id: int
    student_id: str
    book_id: int
    borrow_date: str
    return_date: Optional[str] = None
    due_date: str
    returned: bool = False

class LibraryDatabase:
    def __init__(self, db_file: str = DB_FILE):
        self.db_file = db_file
        self.data = {
            "books": [],
            "students": [],
            "borrow_records": [],
            "book_id_counter": 1,
            "record_id_counter": 1
        }
        self.load_database()

    def load_database(self):
        """Load data from JSON file"""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r') as f:
                    self.data = json.load(f)
            except:
                self.save_database()
        else:
            self.save_database()

    def save_database(self):
        """Save data to JSON file"""
        with open(self.db_file, 'w') as f:
            json.dump(self.data, f, indent=2)

# Initialize database
db = LibraryDatabase()

# ==================== Books Endpoints ====================

@app.post("/books", response_model=Book, tags=["Books"])
def add_book(book: Book):
    """Add a new book to the library"""
    book_dict = book.dict()
    book_dict["book_id"] = db.data["book_id_counter"]
    db.data["books"].append(book_dict)
    db.data["book_id_counter"] += 1
    db.save_database()
    return book_dict

@app.get("/books", response_model=List[Book], tags=["Books"])
def get_all_books(
    category: Optional[str] = Query(None),
    skip: int = Query(0),
    limit: int = Query(10)
):
    """Get all books with optional filtering by category"""
    books = db.data["books"]
    
    if category:
        books = [b for b in books if b["category"].lower() == category.lower()]
    
    return books[skip:skip + limit]

@app.get("/books/{book_id}", response_model=Book, tags=["Books"])
def get_book(book_id: int):
    """Get a specific book by ID"""
    for book in db.data["books"]:
        if book["book_id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.put("/books/{book_id}", response_model=Book, tags=["Books"])
def update_book(book_id: int, updated_book: Book):
    """Update book details"""
    for i, book in enumerate(db.data["books"]):
        if book["book_id"] == book_id:
            book_dict = updated_book.dict()
            book_dict["book_id"] = book_id
            db.data["books"][i] = book_dict
            db.save_database()
            return book_dict
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}", tags=["Books"])
def delete_book(book_id: int):
    """Delete a book from the library"""
    for i, book in enumerate(db.data["books"]):
        if book["book_id"] == book_id:
            db.data["books"].pop(i)
            db.save_database()
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")

# ==================== Students Endpoints ====================

@app.post("/students", response_model=Student, tags=["Students"])
def add_student(student: Student):
    """Register a new student"""
    for s in db.data["students"]:
        if s["student_id"] == student.student_id:
            raise HTTPException(status_code=400, detail="Student already exists")
    
    student_dict = student.dict()
    db.data["students"].append(student_dict)
    db.save_database()
    return student_dict

@app.get("/students", response_model=List[Student], tags=["Students"])
def get_all_students(active: Optional[bool] = Query(None)):
    """Get all students"""
    students = db.data["students"]
    
    if active is not None:
        students = [s for s in students if s["active"] == active]
    
    return students

@app.get("/students/{student_id}", response_model=Student, tags=["Students"])
def get_student(student_id: str):
    """Get a specific student by ID"""
    for student in db.data["students"]:
        if student["student_id"] == student_id:
            return student
    raise HTTPException(status_code=404, detail="Student not found")

@app.put("/students/{student_id}", response_model=Student, tags=["Students"])
def update_student(student_id: str, updated_student: Student):
    """Update student details"""
    for i, student in enumerate(db.data["students"]):
        if student["student_id"] == student_id:
            student_dict = updated_student.dict()
            db.data["students"][i] = student_dict
            db.save_database()
            return student_dict
    raise HTTPException(status_code=404, detail="Student not found")

# ==================== Borrow/Return Endpoints ====================

@app.post("/borrow", response_model=BorrowRecord, tags=["Borrowing"])
def borrow_book(student_id: str, book_id: int, borrow_days: int = 14):
    """Student borrows a book"""
    # Check student exists
    student = None
    for s in db.data["students"]:
        if s["student_id"] == student_id:
            student = s
            break
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check book exists and has available copies
    book = None
    for b in db.data["books"]:
        if b["book_id"] == book_id:
            book = b
            break
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    if book["available_copies"] <= 0:
        raise HTTPException(status_code=400, detail="Book not available")
    
    # Create borrow record
    borrow_date = datetime.now().isoformat()
    due_date = (datetime.now() + timedelta(days=borrow_days)).isoformat()
    
    record = {
        "record_id": db.data["record_id_counter"],
        "student_id": student_id,
        "book_id": book_id,
        "borrow_date": borrow_date,
        "return_date": None,
        "due_date": due_date,
        "returned": False
    }
    
    db.data["borrow_records"].append(record)
    db.data["record_id_counter"] += 1
    
    # Update book availability
    book["available_copies"] -= 1
    
    db.save_database()
    return record

@app.post("/return", response_model=BorrowRecord, tags=["Borrowing"])
def return_book(record_id: int):
    """Student returns a book"""
    for i, record in enumerate(db.data["borrow_records"]):
        if record["record_id"] == record_id:
            if record["returned"]:
                raise HTTPException(status_code=400, detail="Book already returned")
            
            record["returned"] = True
            record["return_date"] = datetime.now().isoformat()
            
            # Update book availability
            for book in db.data["books"]:
                if book["book_id"] == record["book_id"]:
                    book["available_copies"] += 1
                    break
            
            db.save_database()
            return record
    
    raise HTTPException(status_code=404, detail="Borrow record not found")

@app.get("/borrow-history/{student_id}", response_model=List[BorrowRecord], tags=["Borrowing"])
def get_borrow_history(student_id: str):
    """Get borrow history of a student"""
    records = [r for r in db.data["borrow_records"] if r["student_id"] == student_id]
    return records

@app.get("/active-borrows", response_model=List[BorrowRecord], tags=["Borrowing"])
def get_active_borrows():
    """Get all active borrow records"""
    records = [r for r in db.data["borrow_records"] if not r["returned"]]
    return records

# ==================== Statistics Endpoints ====================

@app.get("/statistics", tags=["Statistics"])
def get_statistics():
    """Get library statistics"""
    total_books = len(db.data["books"])
    total_copies = sum(b["total_copies"] for b in db.data["books"])
    available_copies = sum(b["available_copies"] for b in db.data["books"])
    borrowed_copies = total_copies - available_copies
    active_students = len([s for s in db.data["students"] if s["active"]])
    active_borrows = len([r for r in db.data["borrow_records"] if not r["returned"]])
    
    return {
        "total_books": total_books,
        "total_copies": total_copies,
        "available_copies": available_copies,
        "borrowed_copies": borrowed_copies,
        "active_students": active_students,
        "active_borrows": active_borrows
    }

# ==================== Health Check ====================

@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# ==================== Root Endpoint ====================

@app.get("/", tags=["Root"])
def root():
    """Welcome endpoint"""
    return {
        "message": "College Library Management System API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

