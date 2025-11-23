import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os

FILE_NAME = "studentMarks.txt"

class Student:
    def __init__(self, code, name, cw1, cw2, cw3, exam):
        self.code = int(code)
        self.name = name.strip()
        self.cw1 = int(cw1)
        self.cw2 = int(cw2)
        self.cw3 = int(cw3)
        self.exam = int(exam)

    def coursework_total(self):
        return self.cw1 + self.cw2 + self.cw3

    def overall_percentage(self):
        total = self.coursework_total() + self.exam
        return round((total / 160) * 100, 2)

    def grade(self):
        p = self.overall_percentage()
        if p >= 70:
            return "A"
        elif p >= 60:
            return "B"
        elif p >= 50:
            return "C"
        elif p >= 40:
            return "D"
        else:
            return "F"

    def __str__(self):
        return (f"Name: {self.name}\n"
                f"Student Number: {self.code}\n"
                f"Total Coursework Mark: {self.coursework_total()}/60\n"
                f"Exam Mark: {self.exam}/100\n"
                f"Overall Percentage: {self.overall_percentage()}%\n"
                f"Grade: {self.grade()}\n")


class StudentManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager")
        self.root.geometry("500x600")

        self.students = []          # list of Student objects
        self.load_data()

        # Text area for output
        self.text = tk.Text(root, wrap=tk.WORD, state=tk.DISABLED, font=("Courier", 10))
        self.text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Menu
        menubar = tk.Menu(root)
        root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Menu", menu=file_menu)

        file_menu.add_command(label="1. View all student records", command=self.view_all)
        file_menu.add_command(label="2. View individual student record", command=self.view_individual)
        file_menu.add_command(label="3. Show student with highest total score", command=self.show_highest)
        file_menu.add_command(label="4. Show student with lowest total score", command=self.show_lowest)
        file_menu.add_separator()
        file_menu.add_command(label="5. Sort student records", command=self.sort_records)
        file_menu.add_command(label="6. Add a student record", command=self.add_student)
        file_menu.add_command(label="7. Delete a student record", command=self.delete_student)
        file_menu.add_command(label="8. Update a student record", command=self.update_student)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)

    def load_data(self):
        self.students = []
        if not os.path.exists(FILE_NAME):
            messagebox.showerror("Error", f"{FILE_NAME} not found!")
            return

        with open(FILE_NAME, "r") as f:
            lines = f.readlines()

        if not lines:
            return

        num_students = int(lines[0].strip())
        for line in lines[1:1 + num_students]:
            parts = line.strip().split(",")
            if len(parts) == 6:
                code, name, cw1, cw2, cw3, exam = parts
                self.students.append(Student(code, name, cw1, cw2, cw3, exam))

    def save_data(self):
        with open(FILE_NAME, "w") as f:
            f.write(f"{len(self.students)}\n")
            for s in self.students:
                f.write(f"{s.code},{s.name},{s.cw1},{s.cw2},{s.cw3},{s.exam}\n")

    def clear_text(self):
        self.text.configure(state=tk.NORMAL)
        self.text.delete(1.0, tk.END)
        self.text.configure(state=tk.DISABLED)

    def output(self, text):
        self.text.configure(state=tk.NORMAL)
        self.text.insert(tk.END, text + "\n")
        self.text.configure(state=tk.DISABLED)
        self.text.see(tk.END)

    # ====================== MENU FUNCTIONS ======================

    def view_all(self):
        self.clear_text()
        if not self.students:
            self.output("No students loaded.")
            return

        total_perc = 0
        for s in self.students:
            self.output(str(s))
            self.output("-" * 40)
            total_perc += s.overall_percentage()

        avg = round(total_perc / len(self.students), 2)
        self.output(f"Total students: {len(self.students)}")
        self.output(f"Average percentage mark: {avg}%")

    def view_individual(self):
        if not self.students:
            messagebox.showinfo("Info", "No students loaded.")
            return

        code_str = simpledialog.askstring("Student Code", "Enter student code (1000-9999):")
        if not code_str or not code_str.isdigit():
            return
        code = int(code_str)

        student = next((s for s in self.students if s.code == code), None)
        if not student:
            messagebox.showerror("Not found", f"Student with code {code} not found.")
            return

        self.clear_text()
        self.output(str(student))

    def show_highest(self):
        if not self.students:
            messagebox.showinfo("Info", "No students loaded.")
            return
        best = max(self.students, key=lambda s: s.overall_percentage())
        self.clear_text()
        self.output("=== STUDENT WITH HIGHEST OVERALL MARK ===\n")
        self.output(str(best))

    def show_lowest(self):
        if not self.students:
            messagebox.showinfo("Info", "No students loaded.")
            return
        worst = min(self.students, key=lambda s: s.overall_percentage())
        self.clear_text()
        self.output("=== STUDENT WITH LOWEST OVERALL MARK ===\n")
        self.output(str(worst))

    def sort_records(self):
        if not self.students:
            messagebox.showinfo("Info", "No students loaded.")
            return

        choice = messagebox.askquestion("Sort Order", "Yes = Descending (highest first)\nNo = Ascending (lowest first)")
        reverse = (choice == "yes")

        self.students.sort(key=lambda s: s.overall_percentage(), reverse=reverse)
        self.save_data()           # optional: keep file sorted
        self.view_all()

    def add_student(self):
        code = simpledialog.askinteger("Student Code", "Enter student code (1000-9999):", minvalue=1000, maxvalue=9999)
        if code is None:
            return
        if any(s.code == code for s in self.students):
            messagebox.showerror("Error", "Student code already exists!")
            return

        name = simpledialog.askstring("Name", "Enter student full name:")
        if not name:
            return

        cw1 = simpledialog.askinteger("Coursework 1", "Mark out of 20:", minvalue=0, maxvalue=20)
        cw2 = simpledialog.askinteger("Coursework 2", "Mark out of 20:", minvalue=0, maxvalue=20)
        cw3 = simpledialog.askinteger("Coursework 3", "Mark out of 20:", minvalue=0, maxvalue=20)
        exam = simpledialog.askinteger("Exam", "Exam mark out of 100:", minvalue=0, maxvalue=100)

        if None in (cw1, cw2, cw3, exam):
            return

        self.students.append(Student(code, name, cw1, cw2, cw3, exam))
        self.save_data()
        messagebox.showinfo("Success", "Student added successfully!")
        self.view_all()

    def delete_student(self):
        if not self.students:
            messagebox.showinfo("Info", "No students to delete.")
            return

        code_str = simpledialog.askstring("Delete", "Enter student code to delete:")
        if not code_str or not code_str.isdigit():
            return
        code = int(code_str)

        student = next((s for s in self.students if s.code == code), None)
        if not student:
            messagebox.showerror("Error", "Student not found.")
            return

        if messagebox.askyesno("Confirm", f"Delete {student.name} ({student.code})?"):
            self.students = [s for s in self.students if s.code != code]
            self.save_data()
            messagebox.showinfo("Success", "Student deleted.")
            self.view_all()

    def update_student(self):
        if not self.students:
            messagebox.showinfo("Info", "No students to update.")
            return

        code_str = simpledialog.askstring("Update", "Enter student code to update:")
        if not code_str or not code_str.isdigit():
            return
        code = int(code_str)

        student = next((s for s in self.students if s.code == code), None)
        if not student:
            messagebox.showerror("Error", "Student not found.")
            return

        # Sub-menu for what to update
        options = ["Name", "Coursework 1", "Coursework 2", "Coursework 3", "Exam Mark"]
        choice = simpledialog.askstring("Update Field",
                                        f"What do you want to update for {student.name}?\n"
                                        "Type one of:\n" + "\n".join(options))

        if choice == "Name":
            new = simpledialog.askstring("New Name", "Enter new name:", initialvalue=student.name)
            if new:
                student.name = new.strip()

        elif choice == "Coursework 1":
            new = simpledialog.askinteger("Coursework 1", "New mark (0-20):", minvalue=0, maxvalue=20)
            if new is not None:
                student.cw1 = new
        elif choice == "Coursework 2":
            new = simpledialog.askinteger("Coursework 2", "New mark (0-20):", minvalue=0, maxvalue=20)
            if new is not None:
                student.cw2 = new
        elif choice == "Coursework 3":
            new = simpledialog.askinteger("Coursework 3", "New mark (0-20):", minvalue=0, maxvalue=20)
            if new is not None:
                student.cw3 = new
        elif choice == "Exam Mark":
            new = simpledialog.askinteger("Exam Mark", "New mark (0-100):", minvalue=0, maxvalue=100)
            if new is not None:
                student.exam = new
        else:
            messagebox.showinfo("Cancelled", "No valid field selected.")
            return

        self.save_data()
        messagebox.showinfo("Success", "Record updated!")
        self.view_all()


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagerApp(root)
    root.mainloop()
