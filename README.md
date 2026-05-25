Markdown# 📚 Library Management System

A Python-based Library Management System that uses MySQL as the backend database. It allows librarians to manage books, users, borrowing, and returns through a simple, robust command-line interface, complete with built-in financial overdue enforcement and BI analytics routing.

## Features

* **Display Library Rules on Startup** — Automatically fetches and lists active operational protocols.
* **View All Available Books** — Clean listing of active inventory titles, authors, and states.
* **Insert New Books** — Easily append new assets to the library collections.
* **Delete Books** — Instantly remove records from active collection tables.
* **Search Engine** — Multi-index search filtering by Name, Author, or Genre.
* **Smart Borrowing Limits** — Hard-capped validation protecting inventory (max 3 active books per user).
* **Automated Overdue & Fine Processing** — Live timedelta tracking upon return evaluation against a 14-day standard window. Includes a 2-day warning grace period and automated daily fine accumulation calculations (₹5/day).
* **Auto-Registration Loop** — Zero-friction guest registration that seamlessly hands off to the active borrow state without forcing identity re-entry.
* **Smart Identity Resolution** — Adaptive login supporting strict database `UserID` integers or string `UserName` strings during transactional handshakes.
* **Collision Resolution** — Interactive split-screen lookup when multiple accounts share an identical name record.
* **Transactional Context** — Displays a summary table of currently held books and dynamically calculated chronological due dates *before* confirming a return sequence.

## Tech Stack

* **Language:** Python 3.x
* **Database Engine:** MySQL Server
* **Drivers:** `mysql-connector-python`
* **Environment Architecture:** `python-dotenv`
* **Analytics Layer:** Power BI Desktop (Direct SQL Connection Mode)

## Prerequisites

Ensure you have Python 3.x and MySQL Server running locally, then install the required dependencies via pip:

```bash
pip install mysql-connector-python python-dotenv
Database Setup⚠️ Important Change: The database structure has been upgraded from DATETIME to strict DATE definitions to optimize date math operations, resolve formatting offsets, and streamline business intelligence integration.Connect to your MySQL server instance and run the following initialization script:SQLCREATE DATABASE project;
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

-- Tracks active borrowings with exact checkout dates
CREATE TABLE booking (
    UserID INT,
    BookName VARCHAR(100),
    borrow_date DATE,       -- Upgraded from DATETIME to strict DATE
    FOREIGN KEY (UserID) REFERENCES users(UserID)
);
Seed DataPopulate your environment with core configuration items and quick-start testing structures:SQLINSERT INTO library_rules (Rule_Description) VALUES 
('Maximum of 3 books can be borrowed per user.'),
('Standard borrowing period is 14 days.'),
('A fine of ₹5 per day will be charged for each day after the grace period.'),
('A grace period of 2 days is allowed after the due date before any fine is applied.');

INSERT INTO library_books (BookID, Book_Name, Genre, Author) VALUES
(101, 'The Hobbit', 'Fantasy', 'J.R.R. Tolkien'),
(102, 'Dune', 'Sci-Fi', 'Frank Herbert'),
(103, 'Neuromancer', 'Sci-Fi', 'William Gibson'),
(106, 'The Silent Patient', 'Thriller', 'Alex Michaelides');

INSERT INTO users (UserName) VALUES ('Alice');
ConfigurationSystem credentials are securely encapsulated inside environment wrappers away from public tracking layers.Initialize Environment Variables Template:Bashcp .env.example .env
Populate .env Keys with Local Target Details:Code snippetDB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_secure_password
DB_NAME=project
Note: Your local .env configuration file is protected by default patterns declared inside your project's local .gitignore setup.How to RunExecute the main controller via terminal:Bashpython Library_Management.py
Menu OptionsOptionActionContext Notes1Display BooksShows current live catalog and real-time availability bits.2Insert BookRegisters new physical titles directly into relational slots.3Delete BookDeletes catalog records completely based on unique text names.4SearchGranular filtering across matching text vectors (Name, Author, Genre).5BorrowResolves user identity, validates current activity quotas, saves current time.6ReturnAnalyzes chronological difference, triggers warning/fine calculations, processes updates.7ExitSafely closes database context loops and shuts down thread execution.Power BI Analytics IntegrationBy migrating the underlying data structure into native DATE representations, the relational scheme cleanly syncs with native Power BI visualization engines.Suggested Visualization LayoutsOverview Dashboard KPI Cards: High-level counts displaying Total Books Count, Active Borrowed Books, and Total Registered Users.Genre Inventory Donut Chart: Breakdown of catalog volume matching unique Genre strings to analyze distribution percentages.Availability Balance Stacked Bar: Horizontal bars slicing each genre into an available-vs-checked-out ratio.User Activity Distribution Column: Frequency mapping displaying what volume of your community currently holds 0, 1, 2, or the maximum limit of 3 items.Overdue Risk Grid ("Wall of Shame"): Live tabular log filtering rows with conditional formatting highlights targeting accounts currently past due.Recent Changes⏱️ Temporal Fine Engine — Integrated dynamic datetime calculations that cleanly assess late fees against a customized system rulebook.🛡️ Grace Period Handling — Introduced split warning tiers (<= 2 days vs strict fee conditions) to flag returns cleanly without penalty cliffs.📅 Schema Simplification — Replaced ambiguous DATETIME definitions with strict DATE formats to stabilize date calculations and optimize Power BI dashboard performance.🔐 Security Enhancements — Extracted database variables to explicit .env structures and mapped parameterized inputs (%s) across all database queries to mitigate SQL Injection risks.🔁 Loop Stability Core — Cleared runtime-heavy function-level recursion from execution sequences, migrating menu handling and onboarding structures over to infinite while True loop conditions.Roadmap[x] Refactor Registration UX (smooth new user $\rightarrow$ borrow flow)[x] Memory Optimization (removed recursion, while True loop)[x] Scope Bug Fix[x] Data Security (.env for DB credentials)[x] Strict Return Validation (verify user actually borrowed the book)[x] Parameterized Queries (prevent SQL injection)[x] Invalid Choice UX Fix (continue on invalid input)[x] Smart ID/Name Lookup (borrow + return)[x] Duplicate Name Handling[x] Auto-increment UserID + SQL DEFAULT values[x] Input Sanitization (.strip())[x] Temporal Data (track 14-day borrow due dates)[x] Automated Return Overdue Calculations & Grace Logic[x] Power BI Integration Data Prep Architecture[ ] Account Status Flag Model (automating user lockouts on active overdue fines)[ ] Power BI Live Dashboard Metrics PublishProject StructurePlaintextlibrary-management/
│
├── Library_Management.py   # Main application orchestration script
├── .env                    # System parameters (Never commit this data)
├── .env.example            # Template deployment environment variables
├── .gitignore              # Engine instructions preventing safety leakage
└── README.md               # Product documentation manual

AuthorAyeshkant Ray — @Calxile
