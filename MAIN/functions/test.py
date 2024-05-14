import os

demo = {
    "RESUME_URL": "https://firebasestorage.googleapis.com/v0/b/talentov-jay.appspot.com/o/Resumes%2F1692164423103.pdf?alt=media&token=ee332edc-171f-4803-b809-d78ab1990b67",
    "Phase0": "2023-08-16",
    "CURRENT_DESIGNATION": "Senior Software Engineer",
    "E_CTC": "0",
    "PhaseMS22": 1693267200000,
    "SelectedPhaseIndex": 345,
    "Phase22": "2023-08-29",
    "Phase2": "2023-08-29",
    "YEAR_OF_EXPERIENCE": True,
    "TIME_SLOT": "",
    "COUNTER_OFFER": "21 L",
    "SKILLS": "Java, Springboot, Microservices, Hibernate",
    "NOTICE_PERIOD": "LWD - 29.09.2023",
    "id": "1692164423103",
    "C_CTC": "18",
    "SelectedPhaseIndex2": 2,
    "Comid": "1691142820573",
    "CONTACT_NO": "7003825008",
    "CV_SUBMISSION_DATE": "2023-07-05",
    "EMAIL_ID": "shubhendupal66@gmail.com",
    "PhaseMS0": 1692192841163,
    "FeildType": "CRISIL",
    "PROFILE_URL": "",
    "HIRING_LOCATION": "Pune",
    "ASSIGNED_TO": "1692156798174",
    "PhaseMS2": 1693267200000,
    "CURRENT_COMPANY": "Accenture",
    "CANDIDATE_NAME": "Shubhendu Pal",
    "REASON_FOR_CHANGE": "Project Growth & Career Growth",
    "CV_SUBMISSION_DATEMS": 1688515200000,
    "CURRENT_LOCATION": "Kolkata",
    "QUALIFICATION": "Btech",
    "Jobid": "1691143205766"
}


def data(body):
    return demo
import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('example.db')

# Create a cursor object to execute SQL commands
cur = conn.cursor()

# Create a table
cur.execute('''CREATE TABLE IF NOT EXISTS books
               (id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER)''')

def create_book(title, author, year):
    cur.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)", (title, author, year))
    conn.commit()
    print("Book created successfully.")

def read_books():
    cur.execute("SELECT * FROM books")
    books = cur.fetchall()
    print("Books:")
    for book in books:
        print(book)

def update_book_title(book_id, new_title):
    cur.execute("UPDATE books SET title = ? WHERE id = ?", (new_title, book_id))
    conn.commit()
    print("Book title updated successfully.")

def delete_book(book_id):
    cur.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    print("Book deleted successfully.")

# Example usage:
create_book("To Kill a Mockingbird", "Harper Lee", 1960)
create_book("1984", "George Orwell", 1949)
read_books()
update_book_title(1, "New Title for To Kill a Mockingbird")
delete_book(2)
read_books()

# Close the connection
conn.close()
