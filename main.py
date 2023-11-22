from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json

DEFAULT_EMAIL = "name@email.com"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z']
    capital_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                       'T',
                       'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_capital_letters = [choice(capital_letters) for _ in range(randint(3, 5))]
    password_symbols = [choice(symbols) for _ in range(randint(3, 5))]
    password_numbers = [choice(numbers) for _ in range(randint(3, 5))]

    password_list = password_letters + password_capital_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    input_password.insert(0, password)
    input_password_check.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def clear_form():
    input_website.delete(0, END)
    input_password.delete(0, END)
    input_password_check.delete(0, END)


def button_show_or_hide_password():
    password = input_password.get()
    password_check = input_password_check.get()

    if len(password) >= 1 or len(password_check) >= 1:
        if button_show_hide["text"] == "Show":
            button_show_hide.config(text="Hide")
            input_password.config(show="")
            input_password_check.config(show="")
        else:
            button_show_hide.config(text="Show")
            input_password.config(show="*")
            input_password_check.config(show="*")


def save_password():
    website = input_website.get().upper()
    username = input_email_username.get()
    password = input_password.get()
    password_check = input_password_check.get()

    new_data = {website: {"username": username, "password": password}}

    if len(website) == 0 or len(password) == 0 or len(password_check) == 0 or len(username) == 0:
        messagebox.showinfo(title="Empty Fields", message="One or more fields are empty")

    # elif password == password_check:
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)

            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            clear_form()

    # else:
    #     if len(password) <= 12:
    #         short_pass = messagebox.askretrycancel(title="Password Error", message="Password is less than 12 chars")
    #         if not short_pass:
    #             clear_form()
    #     else:
    #         no_match = messagebox.askretrycancel(title="Password Error", message="The passwords didn't match")
    #         if not no_match:
    #             clear_form()


def search_pass():
    website = input_website.get().upper()

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message=f"You have no saved passwords")
    else:
        if website in data:
            username = data[website]["username"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Username: {username}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"There is not match for: '{website}' ")
    

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=0, row=0, columnspan=4)

# Labels
label_website = Label(text="Website:")
label_website.grid(column=0, row=1)

label_email_username = Label(text="Email/UserName:")
label_email_username.grid(column=0, row=2)

label_password = Label(text="Password:")
label_password.grid(column=0, row=3)

label_password = Label(text="Confirm Password:")
label_password.grid(column=0, row=4)

# Entries
input_website = Entry(width=40)
input_website.grid(column=1, row=1, columnspan=2, pady=2)
input_website.focus()

input_email_username = Entry(width=60)
input_email_username.grid(column=1, row=2, columnspan=3, pady=2)
input_email_username.insert(END, string=DEFAULT_EMAIL)

input_password = Entry(width=31, show="*")
input_password.grid(column=1, row=3, pady=2)

input_password_check = Entry(width=31, show="*")
input_password_check.grid(column=1, row=4, pady=2)

# Buttons
button_generate_password = Button(text="Search", width=15, command=search_pass)
button_generate_password.grid(column=3, row=1)

button_show_hide = Button(text="Show", width=5, command=button_show_or_hide_password)
button_show_hide.grid(column=2, row=3, rowspan=2)

button_generate_password = Button(text="Generate Password", width=15, command=generate_password)
button_generate_password.grid(column=3, row=3, rowspan=2)

button_add = Button(text="Add", width=51, command=save_password)
button_add.grid(column=1, row=5, columnspan=3, pady=2)

window.mainloop()
