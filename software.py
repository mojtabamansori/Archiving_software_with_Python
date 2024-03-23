import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3
import os
import subprocess
import sys
import PyInstaller.__main__

# Create or connect to the SQLite database
conn = sqlite3.connect('registration.db')
c = conn.cursor()

# Create a table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS registrations
             (first_name TEXT, last_name TEXT, registration_date TEXT, file_path TEXT)''')
conn.commit()

# Function to register a new entry
def register():
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    registration_date = registration_date_entry.get()

    file_path = filedialog.askopenfilename()

    c.execute("INSERT INTO registrations VALUES (?, ?, ?, ?)",
              (first_name, last_name, registration_date, file_path))
    conn.commit()

    first_name_entry.delete(0, tk.END)
    last_name_entry.delete(0, tk.END)
    registration_date_entry.delete(0, tk.END)

# Function to search for entries
def search():
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    registration_date = registration_date_entry.get()

    c.execute("SELECT * FROM registrations WHERE first_name=? OR last_name=? OR registration_date=?",
              (first_name, last_name, registration_date))
    result = c.fetchall()

    if result:
        display_search_result(result)
    else:
        messagebox.showinfo("No Records Found", "No matching record found.")

# Function to display search results in a separate window
def display_search_result(result):
    result_window = tk.Toplevel(window)
    result_window.title("Search Result")

    result_listbox = tk.Listbox(result_window)
    result_listbox.pack(fill=tk.BOTH, expand=True)

    for row in result:
        result_listbox.insert(tk.END, row)

    result_listbox.bind("<<ListboxSelect>>", on_select)

# Function to handle selection from search results
def on_select(event):
    # Get the widget that triggered the event
    widget = event.widget

    # Get index of selected item
    selected_index = widget.curselection()

    # Get the item from listbox based on index
    selected_item = widget.get(selected_index)

    # Open the file associated with the selected item
    open_file(selected_item[3])  # The file path is at index 3 of the selected item tuple

# Function to open a file
def open_file(file_path):
    # Open the selected file
    if file_path:
        os.system("start " + file_path)
    else:
        messagebox.showinfo("Error", "File path is empty.")

# Function to handle file dialog for registration date entry
def open_file_dialog(event):
    file_path = filedialog.askopenfilename()
    registration_date_entry.delete(0, tk.END)
    registration_date_entry.insert(0, file_path)

# Function to create the executable file
def create_executable():
    main_script = sys.argv[0]
    try:
        subprocess.check_call([sys.executable, "-m", "PyInstaller", "--onefile", main_script])
        messagebox.showinfo("Success", "Executable file created successfully!")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "An error occurred during the creation of the executable file.")

# Create the main window
window = tk.Tk()
window.title("Registration Program")

# Create input form fields
first_name_label = tk.Label(window, text="proj Name:")
first_name_label.grid(row=0, column=0)
first_name_entry = tk.Entry(window)
first_name_entry.grid(row=0, column=1)

last_name_label = tk.Label(window, text="owner Name:")
last_name_label.grid(row=1, column=0)
last_name_entry = tk.Entry(window)
last_name_entry.grid(row=1, column=1)

registration_date_label = tk.Label(window, text="Registration Date:")
registration_date_label.grid(row=2, column=0)
registration_date_entry = tk.Entry(window)
registration_date_entry.grid(row=2, column=1)
registration_date_entry.bind("<<EntryFocusIn>>", open_file_dialog)

register_button = tk.Button(window, text="Register", command=register)
register_button.grid(row=3, column=0)

search_button = tk.Button(window, text="Search", command=search)
search_button.grid(row=3, column=1)

# Check if the script is being run as the main program
if __name__ == "__main__":
    window.mainloop()
    # Close the connection to the database when the main window is closed
    conn.close()
    # Create the executable file after the main loop ends
    PyInstaller.__main__.run(["--onefile", sys.argv[0]])
