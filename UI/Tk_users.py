from tkinter import *
from PIL import ImageTk, Image
# Database
import sqlite3

form = Tk()
form.title('User registration:')
form.geometry('350x250')
form.resizable(False, False)

# Connect to one
conn = sqlite3.connect('DB\DBAstai.db')

# Create cursor
c = conn.cursor()

c.execute("""
    SELECT * FROM Projects WHERE Project = 'Test_1';
""")
t = list(c.fetchone())

print(t)

conn.commit()

# Close Connection
conn.close()

form.mainloop()
