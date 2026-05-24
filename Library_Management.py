import os
from dotenv import load_dotenv

load_dotenv()

def display(): # FUNCTION TO DISPLAY RULES 
    qu="SELECT * FROM library_rules"
    cur.execute(qu)
    data=cur.fetchall()
    for x in data:
        print(x)

def disbook(): # DISPLAYING ALL BOOKS
    q="SELECT * FROM LIBRARY_BOOKS"
    cur.execute(q)
    d=cur.fetchall()
    for i in d:
        print(i)
        
def insert(): # INSERTING BOOKS
    qu=input("Enter Book Genre: ")
    i=int(input("Enter BookID: "))
    b=input("Enter Book Name: ")
    a=input("Enter Author's Name: ")
    s=1
    query="INSERT INTO library_books values(%s,%s,%s,%s,%s)"
    cur.execute(query, (i,b,qu,a,s))
    con.commit()
    print("Inserting Successful \n")

def delete(): # DELETING BOOKS
    b=input("Enter book name to be delete: ")
    query="SELECT * FROM library_books WHERE Book_Name=%s"
    cur.execute(query, (b,))
    d=cur.fetchone()
    print("The details of the book being deleted are: " ,d)
    query="DELETE FROM library_books WHERE Book_Name=%s"
    cur.execute(query, (b,))
    con.commit()
    print("Deleting Successful \n")

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
    un=int(input("Enter User ID: ")) # CHECKING WHETHER USER EXIST IN DATABASE IF NOT ENTER NEW USER
    flag=0
    query="SELECT * FROM users WHERE UserID=%s"
    cur.execute(query, (un,))
    d=cur.fetchone()
    if d:
        flag=1
        print("User Found \n")
    if flag==1:
        s="SELECT * FROM users WHERE activity<3 AND UserID=%s"
        cur.execute(s, (un,))
        d=cur.fetchone()
        if d:
            b=input("Enter Book to Borrow: ")
            l="SELECT * FROM library_books WHERE Book_Name=%s AND STATUS=1"
            cur.execute(l, (b,))
            f=cur.fetchone()
            if f:
                q="UPDATE library_books SET status=0 WHERE Book_Name=%s"
                cur.execute(q, (b,))
                w="UPDATE users SET activity=activity+1 WHERE UserID=%s"
                cur.execute(w, (un,))
                query="INSERT INTO booking values(%s,%s)"
                cur.execute(query, (un,b))
                con.commit()
                print("Borrowing Successful \n")
            else:
                print("Book Unavailable \n")
        else:
            print("Activity Limit Reached \n")
    else:
        print("\nNew User Registration")
        uname=input("Enter Your Name: ")
        act=0
        query="INSERT INTO users values(%s,%s,%s)"
        cur.execute(query, (un,uname,act))
        con.commit()
        print("Registered \n")
        b=input("Enter Book Name to Borrow: ")
        l="SELECT * FROM library_books WHERE Book_Name = %s AND STATUS=1"
        cur.execute(l, (b,))
        f=cur.fetchone()
        if f:
            q="UPDATE library_books SET status=0 WHERE Book_Name=%s"
            cur.execute(q, (b,))
            w="UPDATE users SET activity = activity + 1 WHERE UserID = %s"
            cur.execute(w, (un,))
            query="INSERT INTO booking values(%s,%s)"
            cur.execute(query, (un,b))
            con.commit()
            print("Borrowing Successful \n")
        

def Return(): # RETURNING BOOKS
    un=int(input("Enter UsernameID: "))
    flag=0
    query="SELECT * FROM users WHERE UserID=%s"
    cur.execute(query, (un,))
    d=cur.fetchone()
    if d:
        flag=1
        print("User Found \n")
    if flag==0:
        print("User Not Found \n")
        return
    b=input("Enter book name which you want to return: ")
    l="SELECT * FROM booking WHERE UserID=%s AND BookName=%s"
    cur.execute(l, (un,b))
    f=cur.fetchone()
    if f:
        q="UPDATE library_books SET status=1 WHERE Book_Name=%s"
        cur.execute(q, (b,))
        w="UPDATE users SET activity=activity-1 WHERE UserID=%s"
        cur.execute(w, (un,))
        query="DELETE FROM booking WHERE UserID=%s AND BookName=%s"
        cur.execute(query, (un,b))
        con.commit()
        print("Return Successful \n")
    else:
        print("The Book is not issued by the User \n")
      
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
                break
            else:
                print("Invalid choice \n")
                continue
                
            ch=input("Do you wish to continue (y/n) ")
            if ch == 'n':
                print("Thank you for visiting the Library")
                break
    
#MAIN PROGRAM
 
import mysql.connector as mc # CONNECTION FOR MYSQL
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
