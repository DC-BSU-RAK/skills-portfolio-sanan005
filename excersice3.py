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

class StudentManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("All Student Records")
        self.root.geometry("800x600")
        self.root.configure(bg="blue")  # Background like in image

        self.students = []
        self.load_data()

        # Left frame for buttons
        left_frame = tk.Frame(root, bg="blue", width=200)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        buttons = [
            ("View All Records", self.view_all),
            ("Individual Record", self.view_individual),
            ("Highest Mark", self.show_highest),
            ("Lowest Mark", self.show_lowest),
            ("Sort Records", self.sort_records),
            ("Add Record", self.add_student),
            ("Delete Record", self.delete_student),
            ("Update Record", self.update_student),
            # ("Chart", self.show_chart)  # If needed, but not in assignment
        ]

        for text, command in buttons:
            btn = tk.Button(left_frame, text=text, command=command, bg="pink", fg="black", font=("Arial", 12), width=15)
            btn.pack(pady=5)

        # Main frame for table
        main_frame = tk.Frame(root)
        main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Treeview table
        columns = ("Name", "ID", "Total Coursework", "Exam", "Overall %", "Grade")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=20)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Bottom labels for summary
        self.summary_frame = tk.Frame(main_frame)
        self.summary_frame.pack(fill=tk.X, pady=10)

        self.num_students_label = tk.Label(self.summary_frame, text="No. Students: 0", font=("Arial", 12))
        self.num_students_label.pack(side=tk.LEFT, padx=10)

        self.avg_percentage_label = tk.Label(self.summary_frame, text="Average Percentage: 0%", font=("Arial", 12))
        self.avg_percentage_label.pack(side=tk.LEFT, padx=10)

        # Initial view
        self.view_all()

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

    def clear_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def insert_student(self, s):
        self.tree.insert("", tk.END, values=(
            s.name,
            s.code,
            f"{s.coursework_total()}/60",
            f"{s.exam}/100",
            f"{s.overall_percentage()}%",
            s.grade()
        ))

    def update_summary(self):
        if not self.students:
            self.num_students_label.config(text="No. Students: 0")
            self.avg_percentage_label.config(text="Average Percentage: 0%")
            return

        total_perc = sum(s.overall_percentage() for s in self.students)
        avg = round(total_perc / len(self.students), 2)
        self.num_students_label.config(text=f"No. Students: {len(self.students)}")
        self.avg_percentage_label.config(text=f"Average Percentage: {avg}%")

    # ====================== BUTTON FUNCTIONS ======================

    def view_all(self):
        self.clear_tree()
        for s in self.students:
            self.insert_student(s)
        self.update_summary()

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

        self.clear_tree()
        self.insert_student(student)
        self.update_summary()  # But summary for one?

    def show_highest(self):
        if not self.students:
            messagebox.showinfo("Info", "No students loaded.")
            return
        best = max(self.students, key=lambda s: s.overall_percentage())
        self.clear_tree()
        self.insert_student(best)
        self.update_summary()

    def show_lowest(self):
        if not self.students:
            messagebox.showinfo("Info", "No students loaded.")
            return
        worst = min(self.students, key=lambda s: s.overall_percentage())
        self.clear_tree()
        self.insert_student(worst)
        self.update_summary()

    def sort_records(self):
        if not self.students:
            messagebox.showinfo("Info", "No students loaded.")
            return

        choice = messagebox.askquestion("Sort Order", "Yes = Descending (highest first)\nNo = Ascending (lowest first)")
        reverse = (choice == "yes")

        self.students.sort(key=lambda s: s.overall_percentage(), reverse=reverse)
        self.save_data()
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

    # Optional chart if needed
    # def show_chart(self):
    #     messagebox.showinfo("Chart", "Chart functionality not implemented.")

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagerApp(root)
    root.mainloop()
