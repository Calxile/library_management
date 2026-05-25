# 📚 Library Management System

A Python-based Library Management System that uses MySQL as the backend database. It allows librarians to manage books, users, borrowing, and returns through a simple command-line interface.

---

## Features

- Display library rules on startup
- View all available books
- Insert new books into the library
- Delete books from the collection
- Search books by name, author, or genre
- Borrow books (with a limit of 3 books per user)
- Return borrowed books
- Auto-registration for new users on first borrow — seamlessly continues to borrowing without re-entering ID
- Smart identity lookup — login by User ID or Name during borrow and return
- Duplicate name handling — shows list with IDs if multiple users share the same name
- Borrowed books list displayed before returning

---

## Tech Stack

- **Language:** Python 3
- **Database:** MySQL
- **Connector:** `mysql-connector-python`
- **Environment Management:** `python-dotenv`

---

## Prerequisites

- Python 3.x
- MySQL Server
- `mysql-connector-python` package
- `python-dotenv` package

Install via pip:

```bash
pip install mysql-connector-python python-dotenv
```

---

## Database Setup

> ⚠️ The original database was lost during transfer. Recreate it manually using the schema below.

Connect to your MySQL server and run the following SQL to set up the required schema:

```sql
CREATE DATABASE project;
USE project;

-- Stores library rules displayed on startup
CREATE TABLE library_rules (
    RuleID INT PRIMARY KEY AUTO_INCREMENT,
    Rule_Description VARCHAR(255)
);

-- Stores all books in the library
CREATE TABLE library_books (
    BookID INT PRIMARY KEY,
    Book_Name VARCHAR(100),
    Genre VARCHAR(50),
    Author VARCHAR(100),
    STATUS INT DEFAULT 1  -- 1 = Available, 0 = Borrowed
);

-- Stores registered users
CREATE TABLE users (
    UserID INT PRIMARY KEY AUTO_INCREMENT,
    UserName VARCHAR(100),
    activity INT DEFAULT 0  -- Tracks number of books currently borrowed (max 3)
);

-- Tracks active borrowings
CREATE TABLE booking (
    UserID INT,
    BookName VARCHAR(100),
    FOREIGN KEY (UserID) REFERENCES users(UserID)
);
```

You can also insert some sample data to get started:

```sql
INSERT INTO library_rules VALUES (1, 'Maximum 3 books can be borrowed at a time.');
INSERT INTO library_rules VALUES (2, 'Books must be returned within 14 days.');

INSERT INTO library_books (BookID, Book_Name, Genre, Author) VALUES
(101, 'The Hobbit', 'Fantasy', 'J.R.R. Tolkien'),
(102, 'Dune', 'Sci-Fi', 'Frank Herbert');

INSERT INTO users (UserName) VALUES ('Alice');
```

---

## Configuration

Database credentials are managed via a `.env` file to keep sensitive information out of the source code.

### 1. Copy the example env file
```bash
cp .env.example .env
```

### 2. Fill in your credentials in `.env`
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=project
```

> ⚠️ Never share or commit your `.env` file. It is already listed in `.gitignore`.

---

## How to Run

```bash
python Library_Management.py
```

On launch, the program will:
1. Connect to the MySQL database
2. Display the library rules
3. Show the main menu

---

## Menu Options

| Option | Action |
|--------|--------|
| 1 | Display all books |
| 2 | Insert a new book |
| 3 | Delete a book |
| 4 | Search for a book |
| 5 | Borrow a book |
| 6 | Return a book |
| 7 | Exit |

---

## Notes

- A user can borrow a maximum of **3 books** at a time.
- If a user is not found during borrowing, they are prompted to register and immediately continue to borrow — no need to re-enter their ID.
- Book status is automatically updated on borrow (`0`) and return (`1`).
- Invalid menu choices loop back to the menu directly without asking "Do you wish to continue".
- Both borrow and return accept **User ID or Name** as input.
- If multiple users share the same name, a list is displayed with IDs to pick from.
- Borrowed books are displayed before asking which book to return.
- `STATUS` and `activity` default values are handled at the database level.
- `UserID` is auto-incremented by MySQL — no manual ID entry needed for new users.

---

## Recent Changes

| Area | Change |
|---|---|
| 🔐 **Security** | Removed hardcoded DB credentials — moved to `.env` file using `python-dotenv` |
| 🛡️ **Git Safety** | Added `.gitignore` to prevent `.env` from being pushed to GitHub |
| 🔁 **UX Flow** | New users are registered and immediately proceed to borrow without re-entering their ID |
| 🧠 **Memory** | Replaced all recursive `menu()` and `borrow()` calls with iterative `while True` loops |
| 🐛 **Bug Fix** | Fixed `UnboundLocalError` scope bug in `borrow()` function |
| 🗄️ **DB Cleanup** | Renamed tables `users1` → `users` and `booking1` → `booking` |
| 🔒 **SQL Security** | Replaced all string-formatted queries with parameterized `%s` queries |
| ✅ **Return Validation** | Return now checks `booking` table to verify user actually borrowed the book |
| 🎯 **Invalid Choice UX** | Invalid menu input now loops back directly without prompting "Do you wish to continue" |
| 🔑 **Smart Login** | Borrow and Return now accept User ID or Name as input |
| 👥 **Duplicate Name Handling** | Shows list with IDs if multiple users share the same name |
| 🗂️ **DB Defaults** | `STATUS` and `activity` defaults moved to SQL schema; `UserID` is now AUTO_INCREMENT |
| 📋 **Borrowed Books Display** | Return function now shows currently borrowed books before asking which to return |
| 🧹 **Input Sanitization** | Added `.strip()` to all identity inputs to handle accidental whitespace |

---

## Roadmap

```
[X] Refactor Registration UX (smooth new user → borrow flow)
[X] Memory Optimization (removed recursion, while True loop)
[X] Scope Bug Fix
[X] Data Security (.env for DB credentials)
[X] Strict Return Validation (verify user actually borrowed the book)
[X] Parameterized Queries (prevent SQL injection)
[X] Invalid Choice UX Fix (continue on invalid input)
[X] Smart ID/Name Lookup (borrow + return)
[X] Duplicate Name Handling
[X] Auto-increment UserID + SQL DEFAULT values
[X] Input Sanitization (.strip())
[ ] Temporal Data (track 14-day borrow due dates)
[ ] Power BI Integration (visual dashboards for book & user analytics)
```

---

## Project Structure

```
library-management/
│
├── Library_Management.py   # Main application file
├── .env                    # Your local credentials (never commit this)
├── .env.example            # Template for environment variables
├── .gitignore              # Ensures .env is never pushed to GitHub
└── README.md
```

---

## Author

**Ayeshkant Ray** — [@Calxile](https://github.com/Calxile)
