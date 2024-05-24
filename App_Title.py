# import statement
import customtkinter, tkinter
from tkinter import *


# set appearance mode for the app
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()

app.title("Waka Ama")
app.geometry("500x500")

# Create frame
frame = customtkinter.CTkFrame(master=app,
                                 width=350,
                                 height=250,
                                 bg_color="blue",
                                 fg_color="white",
                                 corner_radius=10)
frame.pack(padx=20,pady=20)

#app title
title_label = customtkinter.CTkLabel(master=frame,
                                     text='Waka Ama Race Result',
                                     width=155,
                                     height=40,
                                     bg_color="black",
                                     font=('impact', 20)
                                     )
title_label.place(relx=0.5, rely=0.75, anchor = tkinter.CENTER )
title_label.pack()

app.mainloop()