import tkinter as tk
from tkinter import ttk, messagebox
import os

class StudentRecordApp:
    FILENAME = "students.txt"

    def __init__(self, root):
        self.root = root
        self.root.title("Student Record Manager")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        self.setup_ui()
        self.load_students()

    # UI SETUP
    def setup_ui(self):
        # Title
        tk.Label(self.root, text="📚 Student Record Manager", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=10)

        # Add student frame
        add_frame = tk.LabelFrame(self.root, text="Add Student", bg="#f0f0f0", padx=10, pady=10)
        add_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(add_frame, text="Name:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(add_frame, width=20)
        self.name_entry.grid(row=0, column=1, padx=5)

        tk.Label(add_frame, text="Roll:", bg="#f0f0f0").grid(row=0, column=2, padx=5)
        self.roll_entry = tk.Entry(add_frame, width=10)
        self.roll_entry.grid(row=0, column=3, padx=5)

        tk.Label(add_frame, text="Marks:", bg="#f0f0f0").grid(row=0, column=4, padx=5)
        self.marks_entry = tk.Entry(add_frame, width=10)
        self.marks_entry.grid(row=0, column=5, padx=5)

        tk.Button(add_frame, text="Add", command=self.add_student, bg="#90ee90").grid(row=0, column=6, padx=5)

        # Treeview
        columns = ("Name", "Roll", "Marks")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_column(c, False))
            self.tree.column(col, width=200 if col == "Name" else 100, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Search frame
        search_frame = tk.LabelFrame(self.root, text="Search Student", bg="#f0f0f0", padx=10, pady=10)
        search_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(search_frame, text="Name:", bg="#f0f0f0").grid(row=0, column=0)
        self.search_entry = tk.Entry(search_frame, width=25)
        self.search_entry.grid(row=0, column=1, padx=5)
        tk.Button(search_frame, text="Search", command=self.search_student, bg="#87ceeb").grid(row=0, column=2, padx=5)
        tk.Button(search_frame, text="Show All", command=self.load_students).grid(row=0, column=3, padx=5)

        # Update frame
        update_frame = tk.LabelFrame(self.root, text="Update Marks", bg="#f0f0f0", padx=10, pady=10)
        update_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(update_frame, text="Roll:", bg="#f0f0f0").grid(row=0, column=0)
        self.update_roll_entry = tk.Entry(update_frame, width=10)
        self.update_roll_entry.grid(row=0, column=1, padx=5)

        tk.Label(update_frame, text="New Marks:", bg="#f0f0f0").grid(row=0, column=2)
        self.update_marks_entry = tk.Entry(update_frame, width=10)
        self.update_marks_entry.grid(row=0, column=3, padx=5)

        tk.Button(update_frame, text="Update", command=self.update_marks, bg="#ffd700").grid(row=0, column=4, padx=5)

        # Delete frame
        delete_frame = tk.LabelFrame(self.root, text="Delete Student", bg="#f0f0f0", padx=10, pady=10)
        delete_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(delete_frame, text="Roll:", bg="#f0f0f0").grid(row=0, column=0)
        self.delete_roll_entry = tk.Entry(delete_frame, width=10)
        self.delete_roll_entry.grid(row=0, column=1, padx=5)

        tk.Button(delete_frame, text="Delete", command=self.delete_student, bg="#ff9999").grid(row=0, column=2, padx=5)

        # Export Button
        tk.Button(self.root, text="Export Top Scorers (>75)", command=self.export_top, bg="#32cd32", fg="white").pack(pady=10)

    # CORE FUNCTIONS
    def read_file(self):
        if not os.path.exists(self.FILENAME):
            return []
        with open(self.FILENAME, "r") as f:
            return [line.strip().split(",") for line in f if line.strip()]

    def write_file(self, students):
        with open(self.FILENAME, "w") as f:
            for s in students:
                f.write(",".join(s) + "\n")

    def load_students(self):
        self.tree.delete(*self.tree.get_children())
        for student in self.read_file():
            self.tree.insert("", tk.END, values=student)

    def add_student(self):
        name, roll, marks = self.name_entry.get(), self.roll_entry.get(), self.marks_entry.get()
        if not (name and roll and marks):
            messagebox.showwarning("Input Error", "All fields are required.")
            return
        students = self.read_file()
        students.append([name, roll, marks])
        self.write_file(students)
        self.load_students()
        self.clear_entries()

    def search_student(self):
        query = self.search_entry.get().lower()
        self.tree.delete(*self.tree.get_children())
        found = False
        for student in self.read_file():
            if query in student[0].lower():
                self.tree.insert("", tk.END, values=student)
                found = True
        if not found:
            messagebox.showinfo("Search", "No matching student found.")

    def update_marks(self):
        roll = self.update_roll_entry.get()
        new_marks = self.update_marks_entry.get()
        students = self.read_file()
        updated = False
        for student in students:
            if student[1] == roll:
                student[2] = new_marks
                updated = True
        if updated:
            self.write_file(students)
            self.load_students()
            messagebox.showinfo("Update", "Marks updated successfully.")
        else:
            messagebox.showinfo("Update", "Roll number not found.")

    def delete_student(self):
        roll = self.delete_roll_entry.get()
        students = [s for s in self.read_file() if s[1] != roll]
        self.write_file(students)
        self.load_students()
        messagebox.showinfo("Delete", "Student deleted (if existed).")

    def export_top(self):
        students = [s for s in self.read_file() if int(s[2]) > 75]
        with open("top_students.txt", "w") as f:
            for s in students:
                f.write(",".join(s) + "\n")
        messagebox.showinfo("Export", "Top scorers exported to top_students.txt")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.roll_entry.delete(0, tk.END)
        self.marks_entry.delete(0, tk.END)

    def sort_column(self, col, reverse):
        data = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
        try:
            data.sort(key=lambda t: int(t[0]), reverse=reverse)
        except ValueError:
            data.sort(reverse=reverse)
        for index, (val, k) in enumerate(data):
            self.tree.move(k, "", index)
        self.tree.heading(col, command=lambda: self.sort_column(col, not reverse))


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentRecordApp(root)
    root.mainloop()