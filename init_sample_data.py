"""
Sample Data Initialization Script
Populates the library database with sample data for testing
"""

import json
import os
from datetime import datetime, timedelta

DB_FILE = "library_db.json"

def create_sample_database():
    """Create a sample database with test data"""
    
    sample_data = {
        "books": [
            {
                "book_id": 1,
                "title": "Python Programming",
                "author": "Guido van Rossum",
                "isbn": "978-0134685991",
                "publication_year": 2015,
                "total_copies": 5,
                "available_copies": 3,
                "category": "Programming",
                "description": "Learn Python programming from basics to advanced concepts"
            },
            {
                "book_id": 2,
                "title": "Clean Code",
                "author": "Robert C. Martin",
                "isbn": "978-0132350884",
                "publication_year": 2008,
                "total_copies": 3,
                "available_copies": 1,
                "category": "Software Engineering",
                "description": "A Handbook of Agile Software Craftsmanship"
            },
            {
                "book_id": 3,
                "title": "Data Structures and Algorithms",
                "author": "Mark Allen Weiss",
                "isbn": "978-0134494082",
                "publication_year": 2013,
                "total_copies": 4,
                "available_copies": 2,
                "category": "Computer Science",
                "description": "Learn fundamental data structures and algorithms"
            },
            {
                "book_id": 4,
                "title": "Introduction to Algorithms",
                "author": "Thomas H. Cormen",
                "isbn": "978-0262033848",
                "publication_year": 2009,
                "total_copies": 3,
                "available_copies": 3,
                "category": "Computer Science",
                "description": "A comprehensive introduction to algorithms"
            },
            {
                "book_id": 5,
                "title": "The Pragmatic Programmer",
                "author": "Andrew Hunt",
                "isbn": "978-0201616224",
                "publication_year": 1999,
                "total_copies": 2,
                "available_copies": 2,
                "category": "Programming",
                "description": "Your Journey to Mastery in Software Development"
            },
            {
                "book_id": 6,
                "title": "Design Patterns",
                "author": "Gang of Four",
                "isbn": "978-0201633610",
                "publication_year": 1994,
                "total_copies": 2,
                "available_copies": 0,
                "category": "Software Engineering",
                "description": "Elements of Reusable Object-Oriented Software"
            },
            {
                "book_id": 7,
                "title": "Database Design",
                "author": "C.J. Date",
                "isbn": "978-0596100124",
                "publication_year": 2005,
                "total_copies": 3,
                "available_copies": 2,
                "category": "Database",
                "description": "Learn relational database design principles"
            },
            {
                "book_id": 8,
                "title": "Web Development with Django",
                "author": "Adrian Holovaty",
                "isbn": "978-1491915523",
                "publication_year": 2017,
                "total_copies": 2,
                "available_copies": 1,
                "category": "Web Development",
                "description": "Build dynamic web applications with Django"
            },
            {
                "book_id": 9,
                "title": "Machine Learning Basics",
                "author": "Aurélien Géron",
                "isbn": "978-1491962282",
                "publication_year": 2017,
                "total_copies": 4,
                "available_copies": 3,
                "category": "Machine Learning",
                "description": "Hands-on machine learning with scikit-learn and tensorflow"
            },
            {
                "book_id": 10,
                "title": "Advanced Python",
                "author": "Luciano Ramalho",
                "isbn": "978-1491946008",
                "publication_year": 2015,
                "total_copies": 2,
                "available_copies": 1,
                "category": "Programming",
                "description": "Fluent Python - Clear, Concise, and Effective Programming"
            }
        ],
        "students": [
            {
                "student_id": "STU001",
                "name": "Alice Johnson",
                "email": "alice.johnson@college.edu",
                "phone": "555-0101",
                "enrollment_year": 2022,
                "active": True
            },
            {
                "student_id": "STU002",
                "name": "Bob Smith",
                "email": "bob.smith@college.edu",
                "phone": "555-0102",
                "enrollment_year": 2021,
                "active": True
            },
            {
                "student_id": "STU003",
                "name": "Carol Williams",
                "email": "carol.williams@college.edu",
                "phone": "555-0103",
                "enrollment_year": 2023,
                "active": True
            },
            {
                "student_id": "STU004",
                "name": "David Brown",
                "email": "david.brown@college.edu",
                "phone": "555-0104",
                "enrollment_year": 2022,
                "active": True
            },
            {
                "student_id": "STU005",
                "name": "Emma Davis",
                "email": "emma.davis@college.edu",
                "phone": "555-0105",
                "enrollment_year": 2023,
                "active": True
            },
            {
                "student_id": "STU006",
                "name": "Frank Miller",
                "email": "frank.miller@college.edu",
                "phone": "555-0106",
                "enrollment_year": 2021,
                "active": False
            }
        ],
        "borrow_records": [
            {
                "record_id": 1,
                "student_id": "STU001",
                "book_id": 1,
                "borrow_date": (datetime.now() - timedelta(days=5)).isoformat(),
                "return_date": None,
                "due_date": (datetime.now() + timedelta(days=9)).isoformat(),
                "returned": False
            },
            {
                "record_id": 2,
                "student_id": "STU002",
                "book_id": 2,
                "borrow_date": (datetime.now() - timedelta(days=10)).isoformat(),
                "return_date": None,
                "due_date": (datetime.now() + timedelta(days=4)).isoformat(),
                "returned": False
            },
            {
                "record_id": 3,
                "student_id": "STU003",
                "book_id": 6,
                "borrow_date": (datetime.now() - timedelta(days=7)).isoformat(),
                "return_date": None,
                "due_date": (datetime.now() + timedelta(days=7)).isoformat(),
                "returned": False
            },
            {
                "record_id": 4,
                "student_id": "STU001",
                "book_id": 3,
                "borrow_date": (datetime.now() - timedelta(days=15)).isoformat(),
                "return_date": (datetime.now() - timedelta(days=1)).isoformat(),
                "due_date": (datetime.now() - timedelta(days=1)).isoformat(),
                "returned": True
            },
            {
                "record_id": 5,
                "student_id": "STU002",
                "book_id": 8,
                "borrow_date": (datetime.now() - timedelta(days=12)).isoformat(),
                "return_date": (datetime.now() - timedelta(days=2)).isoformat(),
                "due_date": (datetime.now() - timedelta(days=2)).isoformat(),
                "returned": True
            }
        ],
        "book_id_counter": 11,
        "record_id_counter": 6
    }
    
    # Save to file
    with open(DB_FILE, 'w') as f:
        json.dump(sample_data, f, indent=2)
    
    print("✓ Sample database created successfully!")
    print(f"\nDatabase file: {DB_FILE}")
    print(f"\nSample Data Summary:")
    print(f"  - {len(sample_data['books'])} books added")
    print(f"  - {len(sample_data['students'])} students registered")
    print(f"  - {len(sample_data['borrow_records'])} borrow records created")
    print(f"\nTo start using the library system:")
    print(f"  1. Run: python fast_api.py")
    print(f"  2. Open: http://localhost:8000/docs")
    print(f"  3. Test the API with sample data")

if __name__ == "__main__":
    if os.path.exists(DB_FILE):
        response = input(f"⚠ {DB_FILE} already exists. Overwrite? (y/n): ").lower()
        if response != 'y':
            print("Cancelled. Database not modified.")
            exit()
    
    create_sample_database()
