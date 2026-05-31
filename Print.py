"""
College Library Management System - Demo Script
Shows how to interact with the library system programmatically
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_section(title):
    """Print a formatted section title"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def demo_add_book():
    """Demo: Add a book to the library"""
    print_section("Demo 1: Adding a Book")
    
    book_data = {
        "book_id": 0,
        "title": "FastAPI Mastery",
        "author": "Sebastián Ramírez",
        "isbn": "978-1234567890",
        "publication_year": 2023,
        "total_copies": 3,
        "available_copies": 3,
        "category": "Web Development",
        "description": "Learn FastAPI from basics to advanced concepts"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/books", json=book_data)
        if response.status_code == 200:
            result = response.json()
            print("✓ Book added successfully!")
            print(f"  Title: {result['title']}")
            print(f"  Author: {result['author']}")
            print(f"  Book ID: {result['book_id']}")
            print(f"  Copies: {result['available_copies']}")
        else:
            print(f"✗ Error: {response.status_code}")
    except Exception as e:
        print(f"✗ Connection error: {e}")
        print(f"  Make sure the server is running: python fast_api.py")

def demo_register_student():
    """Demo: Register a student"""
    print_section("Demo 2: Registering a Student")
    
    student_data = {
        "student_id": "STU_DEMO_001",
        "name": "Demo Student",
        "email": "demo@college.edu",
        "phone": "555-0000",
        "enrollment_year": 2024,
        "active": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}/students", json=student_data)
        if response.status_code == 200:
            result = response.json()
            print("✓ Student registered successfully!")
            print(f"  Name: {result['name']}")
            print(f"  Student ID: {result['student_id']}")
            print(f"  Email: {result['email']}")
            print(f"  Year: {result['enrollment_year']}")
        else:
            print(f"✗ Error: {response.status_code}")
    except Exception as e:
        print(f"✗ Connection error: {e}")

def demo_view_books():
    """Demo: View available books"""
    print_section("Demo 3: Viewing All Books")
    
    try:
        response = requests.get(f"{BASE_URL}/books", params={"limit": 5})
        if response.status_code == 200:
            books = response.json()
            if books:
                print(f"Found {len(books)} books:\n")
                for book in books:
                    print(f"  📖 {book['title']}")
                    print(f"     Author: {book['author']}")
                    print(f"     Available: {book['available_copies']}/{book['total_copies']}")
                    print(f"     Category: {book['category']}\n")
            else:
                print("✓ No books in the library yet.")
        else:
            print(f"✗ Error: {response.status_code}")
    except Exception as e:
        print(f"✗ Connection error: {e}")

def demo_view_students():
    """Demo: View registered students"""
    print_section("Demo 4: Viewing All Students")
    
    try:
        response = requests.get(f"{BASE_URL}/students")
        if response.status_code == 200:
            students = response.json()
            if students:
                print(f"Found {len(students)} students:\n")
                for student in students:
                    status = "✓ Active" if student['active'] else "✗ Inactive"
                    print(f"  👤 {student['name']} ({status})")
                    print(f"     ID: {student['student_id']}")
                    print(f"     Email: {student['email']}\n")
            else:
                print("✓ No students registered yet.")
        else:
            print(f"✗ Error: {response.status_code}")
    except Exception as e:
        print(f"✗ Connection error: {e}")

def demo_statistics():
    """Demo: View library statistics"""
    print_section("Demo 5: Library Statistics")
    
    try:
        response = requests.get(f"{BASE_URL}/statistics")
        if response.status_code == 200:
            stats = response.json()
            print("📊 Current Library Statistics:\n")
            print(f"  Books Management:")
            print(f"    • Total unique books: {stats['total_books']}")
            print(f"    • Total copies: {stats['total_copies']}")
            print(f"    • Available: {stats['available_copies']}")
            print(f"    • Borrowed: {stats['borrowed_copies']}\n")
            print(f"  Student Activity:")
            print(f"    • Active students: {stats['active_students']}")
            print(f"    • Current borrowers: {stats['active_borrows']}")
        else:
            print(f"✗ Error: {response.status_code}")
    except Exception as e:
        print(f"✗ Connection error: {e}")

def demo_health_check():
    """Demo: Health check"""
    print_section("Demo 6: Server Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Server is {result['status'].upper()}")
            print(f"  Timestamp: {result['timestamp']}")
        else:
            print(f"✗ Error: {response.status_code}")
    except Exception as e:
        print(f"✗ Connection error: {e}")
        print(f"\n⚠ IMPORTANT: Make sure to start the FastAPI server first!")
        print(f"  Run: python fast_api.py")

def main():
    """Run all demos"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║  College Library Management System - Demo Script        ║")
    print("╚" + "="*58 + "╝")
    
    # Check if server is running
    print("\nChecking if server is running...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        print("✓ Server is running!\n")
    except:
        print("\n⚠ Server is not running!")
        print("Please start the server first:")
        print("  python fast_api.py\n")
        print("After starting the server, run this script again.")
        return
    
    # Run demos
    demo_view_books()
    demo_view_students()
    demo_statistics()
    demo_add_book()
    demo_register_student()
    demo_health_check()
    
    # Print helpful information
    print_section("Next Steps")
    print("1. Start the FastAPI server:")
    print("   python fast_api.py\n")
    print("2. Open the interactive API documentation:")
    print("   http://localhost:8000/docs\n")
    print("3. Initialize sample data:")
    print("   python init_sample_data.py\n")
    print("4. Read the documentation:")
    print("   - README.md (Full documentation)")
    print("   - QUICKSTART.md (Quick start guide)\n")
    print("5. Use the MCP server for AI integration:")
    print("   python mcp_library_server.py\n")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()

