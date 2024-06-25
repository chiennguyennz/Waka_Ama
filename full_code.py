import customtkinter
from tkinter import filedialog, messagebox
import tkinter as tk
import os
import csv
import time
import subprocess

# Set appearance mode and theme for the app
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

# Initialize the main application window
app = customtkinter.CTk()
app.title("Waka Ama")
app.geometry("500x500")

# Create and set up the main frame
frame1 = customtkinter.CTkFrame(master=app, width=350, height=250, bg_color="blue", fg_color="white", corner_radius=10)
frame1.pack(padx=20, pady=20)

# Add the title label to the frame
title_label = customtkinter.CTkLabel(master=frame1, text='Waka Ama Race Result', width=155, height=40, bg_color="black", font=('impact', 20))
title_label.place(relx=0.5, rely=0.75, anchor=tk.CENTER)
title_label.pack()

class WakaAmaApp:
    def __init__(self, master):
        self.master = master
        self.username = 'Waka_Ama'
        self.password = 'wakawaka'
        self.trials = 0

        # Create the login frame
        self.create_login_frame()

    # Function to create the login frame
    def create_login_frame(self):
        frame_login = customtkinter.CTkFrame(master=self.master, width=350, height=250, bg_color="blue", fg_color="white", corner_radius=10)
        frame_login.pack(padx=20, pady=20)

        self.user_entry = customtkinter.CTkEntry(master=frame_login, placeholder_text="Username", width=200, height=35, border_width=2, corner_radius=10)
        self.user_entry.place(relx=0.5, rely=0.2, anchor='n')

        self.password_entry = customtkinter.CTkEntry(master=frame_login, placeholder_text="Password", width=200, height=35, border_width=2, show="*", corner_radius=10)
        self.password_entry.place(relx=0.5, rely=0.4, anchor='n')

        button_login = customtkinter.CTkButton(master=frame_login, text="LOGIN", command=self.login)
        button_login.place(relx=0.5, rely=0.6, anchor='n')

        self.text_var = customtkinter.StringVar()
        login_label = customtkinter.CTkLabel(master=frame_login, textvariable=self.text_var, width=120, height=25, fg_color=("white", "black"), corner_radius=8)
        login_label.place(relx=0.5, rely=0.75, anchor='n')

    # Function to handle login action
    def login(self):
        if self.user_entry.get() == self.username and self.password_entry.get() == self.password:
            self.text_var.set("Success Login")
            self.mainwin()
        else:
            self.text_var.set("Wrong username or password")
            self.trials += 1
            if self.trials >= 3:
                messagebox.showwarning(title="Error", message="Too many failed attempts")
                self.master.quit()

    # Function to create the main window after successful login
    def mainwin(self):
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

        # Function to handle the CSV download and processing
        def dlcsv():
            year = Ykword.get()
            racetype = kkword.get()
            resources = file_entry.get()
            races = []
            filename = []

            # Function to read files with various encodings
            def read_file(file_path):
                encodings = ['utf-8', 'latin-1', 'utf-16']
                placeholder = "'"

                for encoding in encodings:
                    try:
                        with open(file_path, 'r', encoding=encoding, errors='replace') as file:
                            file_content = file.read()
                        return file_content.replace('\ufffd', placeholder)
                    except UnicodeDecodeError:
                        continue
                print(f"Oops! Something went wrong with file: {file_path}")
                return None

            # Function to find folders by year and call find_files to search for race files
            def find_folder(year, race, folder_path):
                abs_path = os.path.abspath(folder_path)

                for root, dirs, files in os.walk(abs_path):
                    for dir in dirs:
                        if year in dir:
                            dir_path = os.path.join(abs_path, dir)
                            find_files(race, dir_path)

            # Function to find files by race type within the specified folder
            def find_files(race, folder_path):
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        if race in file:
                            file_path = os.path.join(folder_path, file)
                            races.append(read_file(file_path))
                            filename.append(file_path)

            find_folder(year, racetype, resources)

            file_count_label = customtkinter.CTkLabel(master=newwin, text="Files Read: 0", font=('Arial', 15, 'bold'))
            file_count_label.place(x=80, y=350)

            # Function to display filenames sequentially and update the number of files read
            def display_filenames(filenames, files_read_label, files_read=0):
                if filenames:
                    filename = filenames[0]
                    filenames = filenames[1:]

                    file_label = customtkinter.CTkLabel(master=newwin, text=os.path.basename(filename), font=('Arial', 15, 'bold'))
                    file_label.place(x=80, y=300)

                    files_read += 1
                    files_read_label.configure(text=f"Files Read: {files_read}")

                    newwin.after(10, file_label.destroy)
                    newwin.after(10, display_filenames, filenames, files_read_label, files_read)

            display_filenames(filename, file_count_label)

            if not races:
                messagebox.showwarning(title="Error", message="Invalid. Make sure you have correct information")
                return

            # Function to assign points based on the finishing place
            def assign_points(place):
                points = [0, 8, 7, 6, 5, 4, 3, 2]
                return points[place] if place < len(points) else 1

            # Class to process and validate race info
            class Info:
                def __init__(self, line):
                    entries = [entry.strip() for entry in line.split(',')]
                    if len(entries) < 10:
                        self.broken = entries
                        self.valid = False
                        return
                    self.place = entries[0] if entries[0] else '0'
                    self.club = entries[4]
                    self.points = assign_points(int(self.place))
                    self.valid = True

            inlist = []

            for race in races:
                lines = race.split('\n')

                for line in lines[1:]:
                    entries = [entry.strip() for entry in line.split(',')]
                    filter_line = ','.join(filter(None, entries))
                    race_info = Info(line)
                    inlist.append(race_info)

            club_points = {}

            for race in races:
                lines = race.split('\n')
                for line in lines[1:]:
                    line = line.split(',')
                    filter_line = ','.join(filter(None, line))
                    race_info = Info(filter_line)

                    if not race_info.valid:
                        continue

                    if race_info.club in club_points:
                        club_points[race_info.club] += race_info.points
                    else:
                        club_points[race_info.club] = race_info.points

                sorted_data = sorted(club_points.items(), key=lambda x: x[1], reverse=True)

                file_name = "waka-ama_results.csv"
                dpath = os.path.join(os.path.expanduser("~"), "Desktop")
                file_path = os.path.join(dpath, file_name)

                # Write the results to a CSV file
                with open(file_path, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Club Name', 'Total Points'])

                    for club, points in sorted_data:
                        writer.writerow([club, points])

            time.sleep(5)

            # Open the CSV file after creation
            if os.name == 'nt':
                os.startfile(file_path)
            elif os.name == 'posix':
                subprocess.call(['open', file_path])

            messagebox.showinfo(title="Successful", message="Success!")

        # Add the submit button to trigger CSV processing
        submit_button = customtkinter.CTkButton(master=newwin, text="Submit", font=('Arial', 15, 'bold'), command=dlcsv)
        submit_button.place(x=215, y=300)

    # Function to run the main application loop
    def run(self):
        self.master.mainloop()

if __name__ == "__main__":
    waka_ama_app = WakaAmaApp(app)
    waka_ama_app.run()
