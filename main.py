from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime, timedelta

# Путь к файлам для хранения данных
DATA_FILE = "user_data.json"
ASSIGNMENTS_FILE = "assignments_data.json"
MATERIALS_FILE = "materials_data.json"

class User:
    def __init__(self, name, surname, status, password):
        self.name = name
        self.surname = surname
        self.status = status
        self.password = password
        self.username = f"{name.lower()}_{surname.lower()}"
        self.students = [] if self.status == "учитель" else None  # Список учеников для учителя

    def save(self):
        users = User.load_all()
        users[self.username] = {
            "name": self.name,
            "surname": self.surname,
            "status": self.status,
            "password": self.password,
            "students": self.students,  # Сохраняем список учеников, если это учитель
            "username": self.username  # Добавляем username в данные
        }
        with open(DATA_FILE, 'w') as f:
            json.dump(users, f, indent=4)

    @staticmethod
    def load_all():
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        return {}

    @staticmethod
    def find(username):
        users = User.load_all()
        return users.get(username, None)


class Assignment:
    def __init__(self, teacher_username, student_username, title, description, deadline):
        self.teacher_username = teacher_username
        self.student_username = student_username
        self.title = title
        self.description = description
        self.deadline = deadline
        self.submission = None  # Initially no submission

    def save(self):
        assignments = Assignment.load_all()
        assignments[self.title] = {
            "teacher": self.teacher_username,
            "student": self.student_username,
            "title": self.title,
            "description": self.description,
            "deadline": self.deadline,
            "submission": self.submission
        }
        with open(ASSIGNMENTS_FILE, 'w') as f:
            json.dump(assignments, f, indent=4)

    @staticmethod
    def load_all():
        if os.path.exists(ASSIGNMENTS_FILE):
            with open(ASSIGNMENTS_FILE, 'r') as f:
                return json.load(f)
        return {}

    @staticmethod
    def get_by_student(student_username):
        assignments = Assignment.load_all()
        return {title: assignment for title, assignment in assignments.items() if assignment["student"] == student_username}

    @staticmethod
    def get_by_teacher(teacher_username):
        assignments = Assignment.load_all()
        return {title: assignment for title, assignment in assignments.items() if assignment["teacher"] == teacher_username}


class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Платформа EduPhys")
        self.root.geometry("500x550")
        self.root.configure(bg="#E6E6FA")

        tk.Label(self.root, text="Добро пожаловать в систему!", font=("Arial", 24, "bold"), bg="#E6E6FA", fg="black").pack(pady=20)
        tk.Button(self.root, text="Регистрация", command=self.open_registration_window, bg="#4CAF50", fg="black", font=("Arial", 16), width=25, height=2, relief="raised", bd=5).pack(pady=15)
        tk.Button(self.root, text="Авторизация", command=self.open_login_window, bg="#2196F3", fg="black", font=("Arial", 16), width=25, height=2, relief="raised", bd=5).pack(pady=15)

    def open_registration_window(self):
        registration_window = tk.Toplevel(self.root)
        registration_window.title("Регистрация")
        registration_window.geometry("500x700")  # Увеличиваем размер окна
        registration_window.configure(bg="#E6E6FA")

        tk.Label(registration_window, text="Имя:", bg="#E6E6FA", fg="black", font=("Arial", 16)).pack(pady=10)
        entry_name = tk.Entry(registration_window, font=("Arial", 16), relief="flat", highlightthickness=2, highlightbackground="#8A2BE2", width=30)
        entry_name.pack(pady=10, padx=20, fill="x")

        tk.Label(registration_window, text="Фамилия:", bg="#E6E6FA", fg="black", font=("Arial", 16)).pack(pady=10)
        entry_surname = tk.Entry(registration_window, font=("Arial", 16), relief="flat", highlightthickness=2, highlightbackground="#8A2BE2", width=30)
        entry_surname.pack(pady=10, padx=20, fill="x")

        tk.Label(registration_window, text="Статус:", bg="#E6E6FA", fg="black", font=("Arial", 16)).pack(pady=10)

        status_var = tk.StringVar(value="ученик")

        radio_teacher = tk.Radiobutton(registration_window, text="Учитель", variable=status_var, value="учитель", font=("Arial", 16), bg="#E6E6FA", fg="#333333")
        radio_teacher.pack(pady=5)

        radio_student = tk.Radiobutton(registration_window, text="Ученик", variable=status_var, value="ученик", font=("Arial", 16), bg="#E6E6FA", fg="#333333")
        radio_student.pack(pady=5)

        status_label = tk.Label(registration_window, text=f"Вы выбрали статус: {status_var.get()}", bg="#E6E6FA", fg="#333333", font=("Arial", 14))
        status_label.pack(pady=10)

        def update_status(*args):
            status_label.config(text=f"Вы выбрали статус: {status_var.get()}")

        status_var.trace_add("write", update_status)

        tk.Label(registration_window, text="Пароль:", bg="#E6E6FA", fg="black", font=("Arial", 16)).pack(pady=10)
        entry_password = tk.Entry(registration_window, font=("Arial", 16), show="*", relief="flat", highlightthickness=2, highlightbackground="#8A2BE2", width=30)
        entry_password.pack(pady=10, padx=20, fill="x")

        tk.Label(registration_window, text="Повторите пароль:", bg="#E6E6FA", fg="black", font=("Arial", 16)).pack(pady=10)
        entry_confirm_password = tk.Entry(registration_window, font=("Arial", 16), show="*", relief="flat", highlightthickness=2, highlightbackground="#8A2BE2", width=30)
        entry_confirm_password.pack(pady=10, padx=20, fill="x")

        def register():
            name = entry_name.get()
            surname = entry_surname.get()
            status = status_var.get()
            password = entry_password.get()
            confirm_password = entry_confirm_password.get()

            if name and surname and password and confirm_password:
                if password == confirm_password:
                    user = User(name, surname, status, password)
                    user.save()
                    messagebox.showinfo("Успех", "Регистрация прошла успешно!")
                    registration_window.destroy()
                else:
                    messagebox.showwarning("Ошибка", "Пароли не совпадают!")
            else:
                messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля корректно.")

        tk.Button(registration_window, text="Зарегистрироваться", command=register, bg="#4CAF50", fg="black", font=("Arial", 16), width=22, height=2, relief="raised", bd=5).pack(pady=30)

    def open_login_window(self):
        login_window = tk.Toplevel(self.root)
        login_window.title("Авторизация")
        login_window.geometry("500x500")
        login_window.configure(bg="#E6E6FA")

        tk.Label(login_window, text="Имя:", bg="#E6E6FA", fg="black", font=("Arial", 16)).pack(pady=10)
        entry_name = tk.Entry(login_window, font=("Arial", 16), relief="flat", highlightthickness=2, highlightbackground="#8A2BE2", width=30)
        entry_name.pack(pady=10, padx=20, fill="x")

        tk.Label(login_window, text="Фамилия:", bg="#E6E6FA", fg="black", font=("Arial", 16)).pack(pady=10)
        entry_surname = tk.Entry(login_window, font=("Arial", 16), relief="flat", highlightthickness=2, highlightbackground="#8A2BE2", width=30)
        entry_surname.pack(pady=10, padx=20, fill="x")

        tk.Label(login_window, text="Пароль:", bg="#E6E6FA", fg="black", font=("Arial", 16)).pack(pady=10)
        entry_password = tk.Entry(login_window, font=("Arial", 16), show="*", relief="flat", highlightthickness=2, highlightbackground="#8A2BE2", width=30)
        entry_password.pack(pady=10, padx=20, fill="x")

        def login():
            name = entry_name.get()
            surname = entry_surname.get()
            password = entry_password.get()

            if name and surname and password:
                username = f"{name.lower()}_{surname.lower()}"
                user = User.find(username)
                if user and user["password"] == password:
                    if user["status"] == "учитель":
                        self.open_teacher_window(username)
                    else:
                        self.open_student_window(username)
                    login_window.destroy()
                else:
                    messagebox.showwarning("Ошибка", "Неверные данные для входа.")
            else:
                messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля корректно.")

        tk.Button(login_window, text="Войти", command=login, bg="#2196F3", fg="black", font=("Arial", 16), width=22, height=2, relief="raised", bd=5).pack(pady=30)

    def open_teacher_window(self, username):
        teacher_window = tk.Toplevel(self.root)
        teacher_window.title("Учитель")
        teacher_window.geometry("800x800")
        teacher_window.configure(bg="#E6E6FA")

        # Создаем Canvas для прокрутки
        canvas = tk.Canvas(teacher_window)
        canvas.pack(side="left", fill="both", expand=True)

        # Добавляем Scrollbar для Canvas
        scrollbar = tk.Scrollbar(teacher_window, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.config(yscrollcommand=scrollbar.set)

        # Создаем фрейм, который будет содержать все элементы окна
        scrollable_frame = tk.Frame(canvas, bg="#E6E6FA")
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Функция для обновления области прокрутки
        def on_frame_configure(event):
            canvas.config(scrollregion=canvas.bbox("all"))

        # Связываем функцию обновления прокрутки с размером фрейма
        scrollable_frame.bind("<Configure>", on_frame_configure)

        # Создаем вкладки
        notebook = ttk.Notebook(scrollable_frame)
        notebook.pack(fill="both", expand=True)

        # Вкладка для прикрепления учеников и назначения заданий
        manage_frame = tk.Frame(notebook, bg="#E6E6FA")
        notebook.add(manage_frame, text="Управление учениками")

        # Вкладка для создания теоретического материала
        theory_frame = tk.Frame(notebook, bg="#E6E6FA")
        notebook.add(theory_frame, text="Создать теоретический материал")

        # Загрузка данных учителя
        users = User.load_all()
        teacher = users[username]

        # Список прикрепленных учеников
        tk.Label(manage_frame, text="Прикрепленные ученики:", font=("Arial", 16), bg="#E6E6FA", fg="black").pack(
            pady=10)
        attached_students_listbox = tk.Listbox(manage_frame, font=("Arial", 14), height=5, width=50)
        attached_students_listbox.pack(pady=10, padx=100)
        for student_username in teacher["students"]:
            student = users.get(student_username)
            attached_students_listbox.insert(tk.END, f"{student['name']} {student['surname']}")

        # Список всех учеников для прикрепления
        tk.Label(manage_frame, text="Все ученики:", font=("Arial", 16), bg="#E6E6FA", fg="black").pack(pady=10)
        all_students_listbox = tk.Listbox(manage_frame, font=("Arial", 14), height=5, width=50)
        all_students_listbox.pack(pady=10)
        for user in users.values():
            if user["status"] == "ученик" and user["username"] not in teacher["students"]:
                all_students_listbox.insert(tk.END, f"{user['name']} {user['surname']}")

        # Прикрепление ученика
        def attach_student():
            selected_student = all_students_listbox.curselection()
            if selected_student:
                selected_student_name = all_students_listbox.get(selected_student[0]).split()[0]
                selected_student_surname = all_students_listbox.get(selected_student[0]).split()[1]
                student_username = f"{selected_student_name.lower()}_{selected_student_surname.lower()}"
                if student_username not in teacher["students"]:
                    teacher["students"].append(student_username)
                    users[username] = teacher
                    with open(DATA_FILE, 'w') as f:
                        json.dump(users, f, indent=4)
                    attached_students_listbox.insert(tk.END, f"{selected_student_name} {selected_student_surname}")
                    all_students_listbox.delete(selected_student[0])
                    messagebox.showinfo("Успех",
                                        f"Ученик {selected_student_name} {selected_student_surname} прикреплен!")
                else:
                    messagebox.showwarning("Ошибка", "Этот ученик уже прикреплен.")
            else:
                messagebox.showwarning("Ошибка", "Выберите ученика для прикрепления.")

        tk.Button(manage_frame, text="Прикрепить ученика", command=attach_student, bg="#8A2BE2", fg="black",
                  font=("Arial", 14), width=22, height=2, relief="raised", bd=5).pack(pady=10)

        # Функционал для создания задания
        tk.Label(manage_frame, text="Создать домашнее задание:", font=("Arial", 16), bg="#E6E6FA", fg="black").pack(
            pady=10)
        entry_title = tk.Entry(manage_frame, font=("Arial", 14), width=40)
        entry_description = tk.Entry(manage_frame, font=("Arial", 14), width=40)
        entry_deadline = tk.Entry(manage_frame, font=("Arial", 14), width=40)
        tk.Label(manage_frame, text="Заголовок:", font=("Arial", 14), bg="#E6E6FA", fg="black").pack(pady=5)
        entry_title.pack(pady=5)
        tk.Label(manage_frame, text="Описание:", font=("Arial", 14), bg="#E6E6FA", fg="black").pack(pady=5)
        entry_description.pack(pady=5)
        tk.Label(manage_frame, text="Срок:", font=("Arial", 14), bg="#E6E6FA", fg="black").pack(pady=5)
        entry_deadline.pack(pady=5)

        def assign_homework():
            title, description, deadline = entry_title.get(), entry_description.get(), entry_deadline.get()
            selected_student = attached_students_listbox.curselection()
            if title and description and deadline and selected_student:
                selected_student_name = attached_students_listbox.get(selected_student[0]).split()[0]
                selected_student_surname = attached_students_listbox.get(selected_student[0]).split()[1]
                student_username = f"{selected_student_name.lower()}_{selected_student_surname.lower()}"
                assignment = Assignment(username, student_username, title, description, deadline)
                assignment.save()
                messagebox.showinfo("Успех", f"Задание для {selected_student_name} успешно создано!")
                entry_title.delete(0, tk.END)
                entry_description.delete(0, tk.END)
                entry_deadline.delete(0, tk.END)
            else:
                messagebox.showwarning("Ошибка", "Заполните все поля и выберите ученика!")

        tk.Button(manage_frame, text="Назначить задание", command=assign_homework, bg="#8A2BE2", fg="black",
                  font=("Arial", 14), width=22, height=2, relief="raised", bd=5).pack(pady=10)

        # Раздел для просмотра сданных заданий
        submitted_assignments_listbox = tk.Listbox(manage_frame, font=("Arial", 14), height=10, width=50)
        submitted_assignments_listbox.pack(pady=10)

        def load_submitted_assignments():
            assignments = Assignment.get_by_teacher(username)
            submitted_assignments_listbox.delete(0, tk.END)
            for assignment in assignments.values():
                status = " (Сдано)" if assignment.get("submission") else " (Не сдано)"
                submitted_assignments_listbox.insert(tk.END, f"{assignment['title']}{status}")

        def view_submission():
            selected_assignment = submitted_assignments_listbox.curselection()
            if selected_assignment:
                assignment_title = submitted_assignments_listbox.get(selected_assignment[0]).split(" (")[0]
                assignments = Assignment.get_by_teacher(username)
                assignment_data = assignments.get(assignment_title)
                if assignment_data and assignment_data.get("submission"):
                    submission_window = tk.Toplevel(teacher_window)
                    submission_window.title(f"Решение: {assignment_title}")
                    submission_window.geometry("600x500")
                    tk.Label(submission_window, text=f"Решение для задания '{assignment_title}':",
                             font=("Arial", 16)).pack(pady=10)
                    submission_text = tk.Text(submission_window, font=("Arial", 14), wrap=tk.WORD, width=50, height=15)
                    submission_text.insert(tk.END, assignment_data["submission"])
                    submission_text.config(state=tk.DISABLED)
                    submission_text.pack(pady=10)
                    tk.Button(submission_window, text="Закрыть", command=submission_window.destroy, bg="#FF5733",
                              fg="black", font=("Arial", 14), width=22, height=2).pack(pady=20)
                else:
                    messagebox.showwarning("Ошибка", "Для этого задания нет доступного решения.")

        tk.Button(manage_frame, text="Просмотреть решение", command=view_submission, bg="#8A2BE2", fg="black",
                  font=("Arial", 14), width=22, height=2).pack(pady=10)

        load_submitted_assignments()

        def exit_teacher():
            teacher_window.destroy()
            self.root.deiconify()

        tk.Button(manage_frame, text="Выход", command=exit_teacher, bg="#FF5733", fg="black", font=("Arial", 14),
                  width=22, height=2, relief="raised", bd=5).pack(pady=10)

        # Вкладка для создания теоретического материала
        tk.Label(theory_frame, text="Создать теоретический материал:", font=("Arial", 16), bg="#E6E6FA",
                 fg="black").pack(pady=10)

        # Добавляем выпадающий список для выбора ученика
        tk.Label(theory_frame, text="Выберите ученика для материала:", font=("Arial", 14), bg="#E6E6FA",
                 fg="black").pack(pady=10)
        student_select = ttk.Combobox(theory_frame, font=("Arial", 14), width=40)
        student_select['values'] = [f"{student['name']} {student['surname']}" for student in users.values() if
                                    student["status"] == "ученик" and student["username"] in teacher["students"]]
        student_select.pack(pady=10)

        tk.Label(theory_frame, text="Название материала:", font=("Arial", 14), bg="#E6E6FA",
                 fg="black").pack(pady=10)
        entry_material_title = tk.Entry(theory_frame, font=("Arial", 14), width=40)
        entry_material_title.pack(pady=5)
        tk.Label(theory_frame, text="Содержание материала:", font=("Arial", 14), bg="#E6E6FA",
                 fg="black").pack(pady=10)
        text_material_content = tk.Text(theory_frame, font=("Arial", 14), wrap=tk.WORD, height=10, width=40)
        text_material_content.pack(pady=10)

        def save_material():
            material_title = entry_material_title.get()
            material_content = text_material_content.get("1.0", tk.END).strip()
            selected_student = student_select.get()
            if material_title and material_content and selected_student:
                student_username = f"{selected_student.split()[0].lower()}_{selected_student.split()[1].lower()}"
                new_material = {"title": material_title, "content": material_content, "student": student_username}
                if os.path.exists("materials_data.json"):
                    with open("materials_data.json", 'r', encoding='utf-8') as file:
                        materials_data = json.load(file)
                else:
                    materials_data = []
                materials_data.append(new_material)
                with open("materials_data.json", 'w', encoding='utf-8') as file:
                    json.dump(materials_data, file, indent=4)
                messagebox.showinfo("Успех", "Материал успешно сохранен для ученика!")
                entry_material_title.delete(0, tk.END)
                text_material_content.delete("1.0", tk.END)
            else:
                messagebox.showwarning("Ошибка", "Заполните все поля и выберите ученика!")

        tk.Button(theory_frame, text="Сохранить материал", command=save_material, bg="#8A2BE2", fg="black",
                  font=("Arial", 14), width=22, height=2).pack(pady=10)

    def open_student_window(self, username):
        student_window = tk.Toplevel(self.root)
        student_window.title("Ученик")
        student_window.geometry("600x800")
        student_window.configure(bg="#E6E6FA")

        # Create Notebook for tabs
        notebook = ttk.Notebook(student_window)
        notebook.pack(fill="both", expand=True)

        # Tab for Assignments
        assignments_frame = tk.Frame(notebook, bg="#E6E6FA")
        notebook.add(assignments_frame, text="Ваши задания")

        # Create Listbox for assignments
        tk.Label(assignments_frame, text="Ваши задания:", font=("Arial", 16), bg="#E6E6FA", fg="black").pack(pady=10)
        assignments_listbox = tk.Listbox(assignments_frame, font=("Arial", 14), height=10, width=50)
        assignments_listbox.pack(pady=10)

        assignments = Assignment.get_by_student(username)
        for assignment in assignments.values():
            assignments_listbox.insert(tk.END, f"{assignment['title']} - {assignment['deadline']}")

        def show_assignment_details():
            selected_assignment = assignments_listbox.curselection()
            if selected_assignment:
                assignment_title = assignments_listbox.get(selected_assignment[0]).split(" - ")[0]
                assignment_data = next(
                    (a for a in assignments.values() if a["title"] == assignment_title), None
                )
                if assignment_data:
                    self.show_assignment_description(assignment_data)

        # Add a text field for submission
        tk.Label(assignments_frame, text="Введите ваш ответ/задание:", font=("Arial", 14), bg="#E6E6FA",
                 fg="black").pack(pady=10)
        entry_submission = tk.Entry(assignments_frame, font=("Arial", 14), width=40)
        entry_submission.pack(pady=10)

        def submit_homework():
            selected_assignment = assignments_listbox.curselection()
            if selected_assignment:
                assignment_title = assignments_listbox.get(selected_assignment[0]).split(" - ")[0]
                assignment_data = next(
                    (a for a in assignments.values() if a["title"] == assignment_title), None
                )
                if assignment_data:
                    submission = entry_submission.get()
                    if submission:
                        assignment_data["submission"] = submission  # Сохранение ответа ученика

                        # Update the file with the student's submission
                        assignments[assignment_title] = assignment_data
                        with open(ASSIGNMENTS_FILE, 'w') as f:
                            json.dump(assignments, f, indent=4)

                        messagebox.showinfo("Успех", f"Задание '{assignment_title}' успешно отправлено!")
                        entry_submission.delete(0, tk.END)
                    else:
                        messagebox.showwarning("Ошибка", "Пожалуйста, введите решение задания!")

        tk.Button(assignments_frame, text="Отправить задание", command=submit_homework, bg="#4CAF50", fg="black",
                  font=("Arial", 14), width=22, height=2, relief="raised", bd=5).pack(pady=10)
        tk.Button(assignments_frame, text="Просмотр", command=show_assignment_details, bg="#4CAF50", fg="black",
                  font=("Arial", 14), width=22, height=2, relief="raised", bd=5).pack(pady=20)

        # Tab for Theoretical Materials
        theory_frame = tk.Frame(notebook, bg="#E6E6FA")
        notebook.add(theory_frame, text="Теоретические материалы")

        # Create Listbox for theoretical materials
        tk.Label(theory_frame, text="Теоретические материалы:", font=("Arial", 16), bg="#E6E6FA", fg="black").pack(
            pady=10)
        materials_listbox = tk.Listbox(theory_frame, font=("Arial", 14), height=10, width=50)
        materials_listbox.pack(pady=10)

        # Load and display the materials assigned to this student
        if os.path.exists("materials_data.json"):
            with open("materials_data.json", 'r', encoding='utf-8') as file:
                materials_data = json.load(file)
            for material in materials_data:
                if material['student'] == username:  # Check if this material is for the current student
                    materials_listbox.insert(tk.END, material['title'])

        def view_material_content():
            selected_material = materials_listbox.curselection()
            if selected_material:
                material_title = materials_listbox.get(selected_material[0])
                # Find the material content
                material_data = next((m for m in materials_data if m['title'] == material_title), None)
                if material_data:
                    material_window = tk.Toplevel(student_window)
                    material_window.title(f"Теоретический материал: {material_title}")
                    material_window.geometry("600x500")
                    tk.Label(material_window, text=f"Теоретический материал: {material_title}", font=("Arial", 16),
                             bg="#E6E6FA", fg="black").pack(pady=10)
                    tk.Label(material_window, text=f"Содержание:\n\n{material_data['content']}", font=("Arial", 14),
                             bg="#E6E6FA", fg="black").pack(pady=10)

        tk.Button(theory_frame, text="Просмотр материала", command=view_material_content, bg="#4CAF50", fg="black",
                  font=("Arial", 14), width=22, height=2, relief="raised", bd=5).pack(pady=10)

        # Exit Button
        tk.Button(student_window, text="Выход", command=student_window.destroy, bg="#FF5733", fg="black",
                  font=("Arial", 14), width=22, height=2, relief="raised", bd=5).pack(pady=20)

    def show_assignment_description(self, assignment_data):
        description_window = tk.Toplevel(self.root)
        description_window.title(f"Описание задания: {assignment_data['title']}")
        description_window.geometry("600x500")
        description_window.configure(bg="#E6E6FA")

        tk.Label(description_window, text=f"Задание: {assignment_data['title']}", font=("Arial", 16), bg="#E6E6FA", fg="black").pack(pady=10)
        tk.Label(description_window, text=f"Описание: {assignment_data['description']}", font=("Arial", 14), bg="#E6E6FA", fg="black").pack(pady=10)
        tk.Label(description_window, text=f"Крайний срок: {assignment_data['deadline']}", font=("Arial", 14), bg="#E6E6FA", fg="black").pack(pady=10)
        tk.Button(description_window, text="Закрыть", command=description_window.destroy, bg="#FF5733", fg="black", font=("Arial", 14), width=22, height=2, relief="raised", bd=5).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
