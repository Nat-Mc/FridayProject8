import sqlite3
from tkinter import *
from tkinter import messagebox

# Connect to SQLite Database
def create_database():
    conn = sqlite3.connect('feedback.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS feedback (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        feedback TEXT NOT NULL
                      )''')
    conn.commit()
    conn.close()

# Insert Feedback to Database
def submit_feedback():
    name = name_entry.get()
    email = email_entry.get()
    feedback = feedback_entry.get("1.0", END)
    
    if name and email and feedback.strip():
        conn = sqlite3.connect('feedback.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO feedback (name, email, feedback) VALUES (?, ?, ?)", (name, email, feedback))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Feedback submitted successfully!")
        name_entry.delete(0, END)
        email_entry.delete(0, END)
        feedback_entry.delete("1.0", END)
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields.")

# Display All Feedback with Password Protection
def view_feedback():
    password = password_entry.get()
    if password == "admin123":  # Simple password protection
        conn = sqlite3.connect('feedback.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM feedback")
        feedbacks = cursor.fetchall()
        conn.close()
        
        print("\nAll Feedback Entries:")
        for feedback in feedbacks:
            print(f"ID: {feedback[0]}, Name: {feedback[1]}, Email: {feedback[2]}, Feedback: {feedback[3]}\n")
    else:
        messagebox.showerror("Access Denied", "Incorrect password!")

# Set up the GUI
def setup_gui():
    global name_entry, email_entry, feedback_entry, password_entry
    
    window = Tk()
    window.title("Customer Feedback Application")

    Label(window, text="Name").grid(row=0, column=0, padx=10, pady=5)
    name_entry = Entry(window, width=30)
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    Label(window, text="Email").grid(row=1, column=0, padx=10, pady=5)
    email_entry = Entry(window, width=30)
    email_entry.grid(row=1, column=1, padx=10, pady=5)

    Label(window, text="Feedback").grid(row=2, column=0, padx=10, pady=5)
    feedback_entry = Text(window, width=30, height=5)
    feedback_entry.grid(row=2, column=1, padx=10, pady=5)

    submit_button = Button(window, text="Submit Feedback", command=submit_feedback)
    submit_button.grid(row=3, column=1, pady=10)

    Label(window, text="Admin Password").grid(row=4, column=0, padx=10, pady=5)
    password_entry = Entry(window, show="*", width=30)
    password_entry.grid(row=4, column=1, padx=10, pady=5)

    view_button = Button(window, text="View Feedback (Admin Only)", command=view_feedback)
    view_button.grid(row=5, column=1, pady=10)

    window.mainloop()

# Initialize database and GUI
if __name__ == "__main__":
    create_database()
    setup_gui()
