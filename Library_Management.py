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
    cur.execute("INSERT INTO library_books values({},'{}','{}','{}',{})".format(i,b,qu,a,s))
    con.commit()
    print("Inserting Successful \n")

def delete(): # DELETING BOOKS
    b=input("Enter book name to be delete : ")
    cur.execute("SELECT * FROM library_books WHERE Book_Name='{}'".format(b))
    d=cur.fetchone()
    print("The details of the book being deleted are-" ,d)
    cur.execute("DELETE FROM library_books WHERE Book_Name='{}'".format(b))
    con.commit()
    print("Deleting Successful \n")

def search(): # SEARCHING BOOKS
    c=int(input("1. Search by Book Name \n"
                "2. Search by Author \n"
                "3. Search by Genre - "))
    if c==1:
        q=input("Enter Book Name - ")
        l="SELECT * FROM library_books WHERE Book_Name='{}'".format(q)
        cur.execute(l)
        d=cur.fetchone()
        if d:
            print("Search Successful \n")
        else:
            print("Not Found \n")
    elif c==2:
        q=input("Enter Author Name - ")
        m=0
        cur.execute("SELECT * FROM library_books WHERE Author='{}'".format(q))
        d=cur.fetchall()
        for i in d:
            m=1
            print(i)
            print("Search Successful \n")
        if m==0:
            print("Author not Found \n")
    elif c==3:
        q=input("Enter Genre - ")
        m=0
        cur.execute("SELECT * FROM library_books WHERE Genre='{}'".format(q))
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
    cur.execute("SELECT * FROM users WHERE UserID={}".format(un))
    d=cur.fetchone()
    if d:
        flag=1
        print("User Found \n")
    if flag==1:
        s=("SELECT * FROM users WHERE activity<3 AND UserID={}".format(un))
        cur.execute(s)
        d=cur.fetchone()
        if d:
            b=input("Enter Book to Borrow: ")
            l="SELECT * FROM library_books WHERE Book_Name='{}' AND STATUS=1".format(b)
            cur.execute(l)
            f=cur.fetchone()
            if f:
                q=("UPDATE library_books SET status=0 WHERE Book_Name='{}'".format(b))
                cur.execute(q)
                w=("UPDATE users SET activity=activity+1 WHERE UserID={}".format(un))
                cur.execute(w)
                cur.execute("INSERT INTO booking values({},'{}')".format(un,b))
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
        cur.execute("INSERT INTO users values({},'{}',{})".format(un,uname,act))
        con.commit()
        print("Registered \n")
        b=input("Enter Book Name to Borrow: ")
        l="SELECT * FROM library_books WHERE Book_Name = '{}' AND STATUS=1".format(b)
        cur.execute(l)
        f=cur.fetchone()
        if f:
            q=("UPDATE library_books SET status=0 WHERE Book_Name='{}'".format(b))
            cur.execute(q)
            w=("UPDATE users SET activity = activity + 1 WHERE UserID = '{}'".format(un))
            cur.execute(w)
            cur.execute("INSERT INTO booking values({},'{}')".format(un,b))
            con.commit()
            print("Borrowing Successful \n")
        

def Return(): # RETURNING BOOKS
    un=int(input("Enter UsernameID: "))
    flag=0
    cur.execute("SELECT * FROM users WHERE UserID={}".format(un))
    d=cur.fetchone()
    if d:
        flag=1
        print("User Found \n")
    if flag==0:
        print("User Not Found \n")
        return
    b=input("Enter book name which you want to Return-")
    l="SELECT * FROM library_books WHERE Book_Name='{}'".format(b)
    cur.execute(l)
    f=cur.fetchone()
    if f:
        q=("UPDATE library_books SET status=1 WHERE Book_Name='{}'".format(b))
        cur.execute(q)
        w=("UPDATE users SET activity=activity-1 WHERE UserID={}".format(un))
        cur.execute(w)
        cur.execute("DELETE FROM booking WHERE UserID={} AND BookName='{}'".format(un,b))
        con.commit()
        print("Return Successful \n")
    else:
        print("Book Does Not Exist \n")
      
def menu(char): # LIBRARY MENU
    if char=='n':
        print("Thank you for Visiting")
        return
    else:
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
            return
        else:
            print("Invalid choice \n")
        ch=input("Do you wish to continue (y/n) ")
        menu(ch)
    
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
ch = 'y'
menu(ch)
