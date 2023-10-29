from tkinter import Tk, Canvas, PhotoImage, Label, Button, Entry, END
from tkinter import messagebox
import pyperclip
import json
import config

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Password Generator Project
import random


def generate_password():
    letters = [
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
        "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P",
        "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
    ]
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    symbols = ["!", "#", "$", "%", "&", "(", ")", "*", "+"]

    letters_list = [random.choice(letters) for _ in range(random.randint(8, 10))]
    symbols_list = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    numbers_list = [random.choice(numbers) for _ in range(random.randint(2, 4))]

    password_list = letters_list + symbols_list + numbers_list
    random.shuffle(password_list)
    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, string=password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_password():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {website: {"email": email, "password": password}}

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(
            title="Oops", message="Please don't leave any fields empty!"
        )
    else:
        try:
            with open("data.json", mode="r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            data = {}

        data.update(new_data)

        with open("data.json", mode="w") as data_file:
            json.dump(data, data_file, indent=4)

            website_entry.delete(0, END)
            password_entry.delete(0, END)


def find_password():
    website = website_entry.get()

    try:
        with open("data.json", mode="r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(
                title=website,
                message=f"Website: {website}\n E-mail: {email}\n Password: {password}",
            )
        else:
            messagebox.showinfo(
                title="Error", message="No details for the website exists"
            )


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
mypass_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=mypass_image)
canvas.grid(column=1, row=0)

# Labels

website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# Entries

website_entry = Entry(width=21)
website_entry.grid(column=1, columnspan=1, row=1)
website_entry.focus()

email_entry = Entry(width=38)
email_entry.grid(column=1, columnspan=2, row=2)
email_entry.insert(0, config.EMAIL_ADDRESS)

password_entry = Entry(width=21)
password_entry.grid(column=1, row=3)

# Buttons

generate_password_button = Button(
    text="Generate Password", width=13, command=generate_password
)
generate_password_button.grid(column=2, row=3)

Add_password_button = Button(text="Add", width=26, command=add_password)
Add_password_button.grid(column=1, columnspan=2, row=4)

search_button = Button(text="Search", width=13, command=find_password)
search_button.grid(column=2, row=1)

window.mainloop()
