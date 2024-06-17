# File: main_window.py
import customtkinter
from tkinter import filedialog, messagebox
import os
import csv
import time
import subprocess

class MainWindow:
    def __init__(self, master):
        self.master = master

        newwin = customtkinter.CTkToplevel(self.master)
        newwin.geometry('500x500+{:d}+{:d}'.format(newwin.winfo_screenwidth() // 2 - 250, newwin.winfo_screenheight() // 2 - 250))
        newwin.title("Waka Ama")
        newwin.resizable(0, 0)

        wellabel = customtkinter.CTkLabel(master=newwin, text="Welcome to results", font=('Helvetica', 35, 'bold'))
        wellabel.place(x=85, y=0)

        # Function to select folder for CSV files
        def select_folder():
            fpath = filedialog.askdirectory()
            if fpath:
                file_entry.delete(0, 'end')
                file_entry.insert(0, fpath)

        file_label = customtkinter.CTkLabel(master=newwin, text="Folder Location:", font=('Arial', 15, 'bold'))
        file_label.place(x=7, y=100)
        file_entry = customtkinter.CTkEntry(master=newwin, font=('Arial', 15))
        file_entry.place(x=150, y=101)

        select_button = customtkinter.CTkButton(master=newwin, text="Select Folder", font=('Arial', 15, 'bold'), command=select_folder)
        select_button.place(x=150, y=130)

        kword = customtkinter.CTkLabel(master=newwin, text="Enter Keyword:", font=('Arial', 15, 'bold'))
        kword.place(x=15, y=185)

        kkword = customtkinter.CTkEntry(master=newwin, font=('Arial', 15))
        kkword.place(x=150, y=185)

        Yword = customtkinter.CTkLabel(master=newwin, text="Enter year:", font=('Arial', 15, 'bold'))
        Yword.place(x=48, y=260)

        Ykword = customtkinter.CTkEntry(master=newwin, font=('Arial', 15))
        Ykword.place(x=150, y=262)

        self.newwin = newwin

    def run(self):
        self.master.mainloop()

if __name__ == "__main__":
    app = customtkinter.CTk()
    app.title("Waka Ama")
    app.geometry("500x500")
    main_window = MainWindow(app)
    main_window.run()
