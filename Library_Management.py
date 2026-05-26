import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import mysql.connector as mc

load_dotenv()

def display(): # FUNCTION TO DISPLAY RULES 
    qu="SELECT * FROM library_rules"
    cur.execute(qu)
    data=cur.fetchall()
    for x in data:
        print(x)

def disbook(): # DISPLAYING ALL BOOKS
    q="SELECT * FROM library_books"
    cur.execute(q)
    d=cur.fetchall()
    for i in d:
        print(i)
        
def insert(): # INSERTING BOOKS
    qu=input("Enter Book Genre: ")
    i=int(input("Enter BookID: "))
    b=input("Enter Book Name: ")
    a=input("Enter Author's Name: ")
    query="INSERT INTO library_books (BookID, Book_Name, Genre, Author) values(%s,%s,%s,%s)"
    cur.execute(query, (i,b,qu,a))
    con.commit()
    print("Inserting Successful \n")

def delete(): # DELETING BOOKS
    b=input("Enter book name to be delete: ")
    query="SELECT * FROM library_books WHERE Book_Name=%s"
    cur.execute(query, (b,))
    d=cur.fetchone()
    if d:
        print("The details of the book being deleted are: " ,d)
        query="DELETE FROM library_books WHERE Book_Name=%s"
        cur.execute(query, (b,))
        con.commit()
        print("Deleting Successful \n")
    else:
        print("Book does not exist in the library system.\n")

def search(): # SEARCHING BOOKS
    c=int(input("1. Search by Book Name \n"
                "2. Search by Author \n"
                "3. Search by Genre - "))
    if c==1:
        q=input("Enter Book Name: ")
        l="SELECT * FROM library_books WHERE Book_Name=%s"
        cur.execute(l,(q,))
        d=cur.fetchone()
        if d:
            print("Search Successful \n")
        else:
            print("Not Found \n")
    elif c==2:
        q=input("Enter Author Name: ")
        m=0
        query="SELECT * FROM library_books WHERE Author=%s"
        cur.execute(query, (q,))
        d=cur.fetchall()
        for i in d:
            m=1
            print(i)
            print("Search Successful \n")
        if m==0:
            print("Author not Found \n")
    elif c==3:
        q=input("Enter Genre: ")
        m=0
        query="SELECT * FROM library_books WHERE Genre=%s"
        cur.execute(query, (q,))
        d=cur.fetchall()
        for i in d:
            m=1
            print(i)
            print("Search Successful \n")
        if m==0:
            print("Genre Unavailable \n")

def borrow(): # BORROWING BOOKS
    choice = input("Enter User ID or Name (or press Enter if you are a New User): ").strip()
    un = None
 
    # Step 1 - Resolve user
    if choice.isdigit():
        un = int(choice)
        query = "SELECT * FROM users WHERE UserID=%s"
        cur.execute(query, (un,))
        d = cur.fetchone()
        if d:
            print("User Found\n")
        else:
            print("User Does Not Exist\n")
            return
 
    elif choice == "":  # New User Registration
        print("\nNew User Registration")
        uname = input("Enter Your Name: ")
        try:
            query = "INSERT INTO users (UserName) values(%s)"
            cur.execute(query, (uname,))
            con.commit()
            un = cur.lastrowid
            print(f"New User Registered! Your User ID is: {un}\n")
            print("Please remember this ID for future visits.\n")
        except Exception as e:
            print(f"Registration failed: {e}")
            con.rollback()
            return
 
    else:
        query = "SELECT * FROM users WHERE UserName=%s"
        cur.execute(query, (choice,))
        d = cur.fetchall()
        if len(d) == 0:
            print("User Does Not Exist\n")
            return
        elif len(d) == 1:
            print("User Found\n")
            un = d[0][0]
        else:
            for i in d:
                print(f"ID: {i[0]} | Name: {i[1]}")
            un = int(input("Enter your UserID from the above list: "))
 
    if un is None:
        return
 
    # Step 2 - Check activity limit
    s = "SELECT activity FROM users WHERE activity < 3 AND UserID=%s"
    cur.execute(s, (un,))
    f = cur.fetchone()
 
    if f:
        b = input("Enter Book Name to Borrow: ")
        l = "SELECT BookID FROM library_books WHERE Book_Name=%s AND status = 1"
        cur.execute(l, (b,))
        bor = cur.fetchone()
 
        if bor:
            try:
                book_id = bor[0]
                borrow_date = datetime.now().date()
                due_date = borrow_date + timedelta(days=14)
 
                q = "UPDATE library_books SET status = 0 WHERE Book_Name=%s"
                cur.execute(q, (b,))
 
                w = "UPDATE users SET activity = activity + 1 WHERE UserID=%s"
                cur.execute(w, (un,))
 
                query = "INSERT INTO booking (UserID, BookID, borrow_date, due_date) VALUES (%s, %s, %s, %s)"
                cur.execute(query, (un, book_id, borrow_date, due_date))
 
                con.commit()
                print("Borrowing Successful\n")
                print(f"Due Date: {due_date.strftime('%d-%b-%Y')}")
            except Exception as e:
                print(f"Sorry, an unexpected error occurred: {e}")
                con.rollback()
        else:
            print("Book Not Available. Sorry :(\n")
    else:
        print("Sorry but your activity has reached its limit, first return some books if you want to borrow more.\n")
        
def Return(): # RETURNING BOOKS
    choice = input("Enter User ID or Name: ").strip()
    un = None
 
    # Step 1 - Resolve user
    if choice.isdigit():
        un = int(choice)
        query = "SELECT * FROM users WHERE UserID=%s"
        cur.execute(query, (un,))
        d = cur.fetchone()
        if d:
            print("User Found\n")
        else:
            print("User Not Found\n")
            return
    else:
        query = "SELECT * FROM users WHERE UserName=%s"
        cur.execute(query, (choice,))
        d = cur.fetchall()
        if len(d) == 0:
            print("User Not Found!\n")
            return
        elif len(d) == 1:
            print("User Found\n")
            un = d[0][0]
        else:
            for i in d:
                print(f"ID: {i[0]} | Name: {i[1]}")
            un = int(input("Enter your user ID from the list above: "))
 
    if un is None:
        return
 
    # Step 2 - Show books currently borrowed by user
    issued = """SELECT lb.Book_Name, b.borrow_date, b.due_date 
                FROM booking b 
                JOIN library_books lb ON b.BookID = lb.BookID 
                WHERE b.UserID=%s AND b.return_date IS NULL"""
    cur.execute(issued, (un,))
    books = cur.fetchall()
 
    if books:
        print("Books currently borrowed by you:\n")
        for book in books:
            print(f" - {book[0]} (Due: {book[2].strftime('%d-%b-%Y')})")
    else:
        print("You have no books to return.\n")
        return
 
    # Step 3 - Ask which book to return
    b = input("\nEnter the Book Name which you want to return: ")
 
    # Look up BookID from library_books
    cur.execute("SELECT BookID FROM library_books WHERE Book_Name=%s", (b,))
    book_row = cur.fetchone()
    if not book_row:
        print("Book not found in the library system.\n")
        return
    book_id = book_row[0]
 
    # Fetch the booking record
    l = "SELECT due_date FROM booking WHERE UserID=%s AND BookID=%s AND return_date IS NULL"
    cur.execute(l, (un, book_id))
    f = cur.fetchone()  # f columns: (BookingID, UserID, BookID, borrow_date, due_date)
 
    if f:
        # Step 4 - Overdue logic using stored due_date
        due_date = f[0]
        today = datetime.now().date()
        days_overdue = (today - due_date).days
 
        if days_overdue <= 0:
            print("Returned on time! Thank you.\n")
        elif days_overdue <= 2:
            print(f"⚠️  {days_overdue} day(s) overdue — within grace period. Please return books on time next time!\n")
        else:
            fine = (days_overdue - 2) * 5
            print(f"❌ {days_overdue} days overdue. Fine: ₹{fine}. Please pay at the counter.\n")
 
        # Step 5 - Process the return
        try:
            q = "UPDATE library_books SET status = 1 WHERE Book_Name=%s"
            cur.execute(q, (b,))
 
            w = "UPDATE users SET activity = activity - 1 WHERE UserID=%s"
            cur.execute(w, (un,))
            
            return_date = datetime.now().date()
            query = "UPDATE booking SET return_date=%s WHERE UserID=%s AND BookID=%s AND return_date IS NULL"
            cur.execute(query, (return_date, un, book_id))
 
            con.commit()
            print("Book returned successfully.\n")
        except Exception as e:
            print(f"Sorry, an unexpected error occurred: {e}")
            con.rollback()
    else:
        print("This book is not issued to this user.\n")
      
def menu(): # LIBRARY MENU
    while True:
            print("\n1. Display books \n"
                  "2. Insert book \n"
                  "3. Delete book \n"
                  "4. Search \n"
                  "5. Borrow \n"
                  "6. Return \n"
                  "7. Exit ")
            
            choice=int(input("Enter your choice: "))
            
            if choice==1:
                disbook()
            elif choice==2:
                insert()
            elif choice==3:
                delete()
            elif choice==4:
                search()
            elif choice==5:
                borrow()
            elif choice==6:
                Return()
            elif choice==7:
                print("THANK YOU FOR VISITING LIBRARY")
                cur.close()
                con.close()
                break
            else:
                print("Invalid choice \n")
                continue
                
            ch=input("Do you wish to continue (y/n) ")
            if ch.lower() == 'n':
                print("Thank you for visiting the Library")
                cur.close()
                con.close()
                break
    
#MAIN PROGRAM
  
# Securely reading database credentials from the .env file
db_host = os.environ.get('DB_HOST')
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_name = os.environ.get('DB_NAME')

# Initializing connection using environment variables
con = mc.connect(
    host = db_host,
    user=db_user,
    password=db_password,
    database=db_name
)
cur = con.cursor()

if con.is_connected():
    print("Connection Successful")

print("Welcome to Library") # LIBRARY CODE START
display()
menu()
