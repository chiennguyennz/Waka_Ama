# import statement
import customtkinter, tkinter
from tkinter import *

# set appearance mode for the app
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()

# app title and dimension
app.title("Waka Ama")
app.geometry("500x500")

# Create frame
frame1 = customtkinter.CTkFrame(master=app,
                                 width=350,
                                 height=250,
                                 bg_color="blue",
                                 fg_color="white",
                                 corner_radius=10)
frame1.pack(padx=20,pady=20)

#app title
title_label = customtkinter.CTkLabel(master=frame1,
                                     text='Waka Ama Race Result',
                                     width=155,
                                     height=40,
                                     bg_color="black",
                                     font=('impact', 20)
                                     )
title_label.place(relx=0.5, rely=0.75, anchor = tkinter.CENTER )
title_label.pack()

# login function
frame = customtkinter.CTkFrame(master=app,
                                 width=350,
                                 height=250,
                                 bg_color="blue",
                                 fg_color="white",
                                 corner_radius=10)
frame.pack(padx=20,pady=20)

user_entry = customtkinter.CTkEntry (master=frame,
                                     placeholder_text="Username",
                                     width=200,
                                     height=35,
                                     border_width=2,
                                     corner_radius=10)
user_entry.place(relx=0.5, rely=0.2, anchor = tkinter.CENTER )

password_entry = customtkinter.CTkEntry (master=frame,
                                     placeholder_text="Password",
                                     width=200,
                                     height=35,
                                     border_width=2,
                                     show="*",
                                     corner_radius=10)
password_entry.place(relx=0.5, rely=0.4, anchor = tkinter.CENTER )

user = "Waka_Ama"
password = "wakawaka"

def button_event():
    if (user_entry.get() == user) and (password_entry.get() == password):
        text_var.set("Success Login")
    else:
        text_var.set("Wrong username or password")

button = customtkinter.CTkButton(master=frame, text="LOGIN", command=button_event)
button.place(relx=0.5, rely = 0.6, anchor=tkinter.CENTER)

text_var = StringVar()

login_label = customtkinter.CTkLabel(master=frame,
                                     textvariable = text_var,
                                     width=120,
                                     height=25,
                                     fg_color=("white","black"),
                                     corner_radius=8)
login_label.place(relx=0.5, rely=0.75, anchor = tkinter.CENTER )

app.mainloop()