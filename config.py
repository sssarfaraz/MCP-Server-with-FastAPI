"""
Configuration file for College Library Management System
Centralize all settings and constants here
"""

import os
from pathlib import Path

# ==================== Server Configuration ====================
SERVER_HOST = os.getenv("LIBRARY_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("LIBRARY_PORT", "8000"))
DEBUG_MODE = os.getenv("LIBRARY_DEBUG", "False").lower() == "true"

# ==================== Database Configuration ====================
DATABASE_DIR = Path(os.getenv("LIBRARY_DB_DIR", "."))
DATABASE_FILE = DATABASE_DIR / "library_db.json"

# Ensure database directory exists
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

# ==================== Application Configuration ====================
APP_NAME = "College Library Management System"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "A comprehensive library management API for college"

# ==================== Borrowing Rules ====================
DEFAULT_BORROW_DAYS = int(os.getenv("LIBRARY_BORROW_DAYS", "14"))
MAX_BOOKS_PER_STUDENT = int(os.getenv("LIBRARY_MAX_BOOKS", "5"))
FINE_PER_DAY = float(os.getenv("LIBRARY_FINE_PER_DAY", "0.50"))

# ==================== API Configuration ====================
API_PREFIX = "/api/v1"
PAGINATION_DEFAULT_LIMIT = 10
PAGINATION_MAX_LIMIT = 100

# ==================== CORS Configuration ====================
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8080",
    "http://127.0.0.1:3000",
]

CORS_ALLOW_ALL = os.getenv("LIBRARY_CORS_ALL", "True").lower() == "true"

# ==================== MCP Configuration ====================
MCP_SERVER_NAME = "college-library-mcp"
MCP_SERVER_VERSION = "1.0.0"
MCP_TOOLS_COUNT = 8

# ==================== Logging Configuration ====================
LOG_LEVEL = os.getenv("LIBRARY_LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# ==================== Feature Flags ====================
ENABLE_STATISTICS = True
ENABLE_HEALTH_CHECK = True
ENABLE_FINE_CALCULATION = False  # Future feature
ENABLE_EMAIL_NOTIFICATIONS = False  # Future feature
ENABLE_AUTHENTICATION = False  # Future feature

# ==================== Category List ====================
BOOK_CATEGORIES = [
    "Programming",
    "Web Development",
    "Database",
    "Software Engineering",
    "Computer Science",
    "Machine Learning",
    "Data Science",
    "DevOps",
    "Mobile Development",
    "UI/UX Design",
    "Reference",
    "Other"
]

# ==================== Helper Functions ====================

def get_database_path():
    """Get the full path to the database file"""
    return str(DATABASE_FILE)

def get_api_url(path: str = ""):
    """Get full API URL"""
    url = f"http://{SERVER_HOST}:{SERVER_PORT}"
    if path:
        url += f"{API_PREFIX}{path}"
    return url

def get_config_summary():
    """Get a summary of current configuration"""
    return {
        "app_name": APP_NAME,
        "app_version": APP_VERSION,
        "server": f"{SERVER_HOST}:{SERVER_PORT}",
        "database": str(DATABASE_FILE),
        "debug": DEBUG_MODE,
        "borrow_days": DEFAULT_BORROW_DAYS,
        "max_books": MAX_BOOKS_PER_STUDENT,
        "cors_all": CORS_ALL,
        "mcp_enabled": True
    }

if __name__ == "__main__":
    # Print configuration when run directly
    import json
    print("\n" + "="*60)
    print("College Library Management System - Configuration")
    print("="*60 + "\n")
    print(json.dumps(get_config_summary(), indent=2))
    print("\n" + "="*60)
