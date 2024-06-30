import customtkinter
from tkinter import filedialog, messagebox
import tkinter as tk
import os
import csv
import time
import subprocess

# set appearance mode for the app
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

class WakaAmaApp:
    def __init__(self, master):
        self.master = master

    def mainwin(self):
        newwin = customtkinter.CTkToplevel(self.master)
        newwin.geometry('500x500+{:d}+{:d}'.format(newwin.winfo_screenwidth() // 2 - 250, newwin.winfo_screenheight() // 2 - 250))
        newwin.title("Waka Ama")
        newwin.resizable(0, 0)

        wellabel = customtkinter.CTkLabel(master=newwin, text="Welcome to results", font=('Helvetica', 35, 'bold'))
        wellabel.place(x=85, y=0)

        file_label = customtkinter.CTkLabel(master=newwin, text="Folder Location:", font=('Arial', 15, 'bold'))
        file_label.place(x=7, y=100)
        self.file_entry = customtkinter.CTkEntry(master=newwin, font=('Arial', 15))
        self.file_entry.place(x=150, y=101)

        select_button = customtkinter.CTkButton(master=newwin, text="Select Folder", font=('Arial', 15, 'bold'), command=self.select_folder)
        select_button.place(x=150, y=130)

        kword = customtkinter.CTkLabel(master=newwin, text="Enter Keyword:", font=('Arial', 15, 'bold'))
        kword.place(x=15, y=185)

        self.kkword = customtkinter.CTkEntry(master=newwin, font=('Arial', 15))
        self.kkword.place(x=150, y=185)

        Yword = customtkinter.CTkLabel(master=newwin, text="Enter year:", font=('Arial', 15, 'bold'))
        Yword.place(x=48, y=260)

        self.Ykword = customtkinter.CTkEntry(master=newwin, font=('Arial', 15))
        self.Ykword.place(x=150, y=262)

        submit_button = customtkinter.CTkButton(master=newwin, text="Submit", font=('Arial', 15, 'bold'), command=self.dlcsv)
        submit_button.place(x=150, y=300)

    def select_folder(self):
        fpath = filedialog.askdirectory()
        if fpath:
            self.file_entry.delete(0, 'end')
            self.file_entry.insert(0, fpath)

    def dlcsv(self):
        year = self.Ykword.get()
        racetype = self.kkword.get()
        resources = self.file_entry.get()
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

        file_count_label = customtkinter.CTkLabel(master=self.master, text="Files Read: 0", font=('Arial', 15, 'bold'))
        file_count_label.place(x=80, y=350)

        # Function to display filenames sequentially and update the number of files read
        def display_filenames(filenames, files_read_label, files_read=0):
            if filenames:
                filename = filenames[0]
                filenames = filenames[1:]

                file_label = customtkinter.CTkLabel(master=self.master, text=os.path.basename(filename), font=('Arial', 15, 'bold'))
                file_label.place(x=80, y=300)

                files_read += 1
                files_read_label.configure(text=f"Files Read: {files_read}")

                self.master.after(10, file_label.destroy)
                self.master.after(10, display_filenames, filenames, files_read_label, files_read)

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

# Initialize the app for standalone testing
app = customtkinter.CTk()
waka_ama_app = WakaAmaApp(app)
waka_ama_app.mainwin()
app.mainloop()
