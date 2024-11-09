import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime, timedelta

# Путь к файлам для хранения данных
DATA_FILE = "user_data.json"
ASSIGNMENTS_FILE = "assignments_data.json"

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
            "submission": self.submission  # Store the student's submission
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
        self.root.title("Взаимодействие Учителя и Ученика")
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
        teacher_window.geometry("600x800")
        teacher_window.configure(bg="#E6E6FA")

        # Создаем холст для прокрутки
        canvas = tk.Canvas(teacher_window, bg="#E6E6FA")
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Добавляем полосу прокрутки
        scrollbar = tk.Scrollbar(teacher_window, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Связываем полосу прокрутки с холстом
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Создаем фрейм внутри холста для размещения виджетов
        teacher_frame = tk.Frame(canvas, bg="#E6E6FA")
        canvas.create_window((0, 0), window=teacher_frame, anchor="nw")

        # Загрузить данные учителя
        users = User.load_all()
        teacher = users[username]

        # Показать прикрепленных учеников
        tk.Label(teacher_frame, text="Прикрепленные ученики:", font=("Arial", 16), bg="#E6E6FA", fg="black").pack(pady=10)
        attached_students_listbox = tk.Listbox(teacher_frame, font=("Arial", 14), height=5, width=50)
        attached_students_listbox.pack(pady=10)

        # Загружаем прикрепленных учеников
        for student_username in teacher["students"]:
            student = users.get(student_username)
            attached_students_listbox.insert(tk.END, f"{student['name']} {student['surname']}")

        # Список всех учеников для прикрепления
        tk.Label(teacher_frame, text="Все ученики:", font=("Arial", 16), bg="#E6E6FA", fg="black").pack(pady=10)
        all_students_listbox = tk.Listbox(teacher_frame, font=("Arial", 14), height=5, width=50)
        all_students_listbox.pack(pady=10)

        # Загружаем всех учеников
        for user in users.values():
            if user["status"] == "ученик" and username not in teacher["students"]:
                all_students_listbox.insert(tk.END, f"{user['name']} {user['surname']}")

        # Функция прикрепления ученика
        def attach_student():
            selected_student = all_students_listbox.curselection()
            if selected_student:
                selected_student_name = all_students_listbox.get(selected_student[0]).split()[0]
                selected_student_surname = all_students_listbox.get(selected_student[0]).split()[1]
                student_username = f"{selected_student_name.lower()}_{selected_student_surname.lower()}"

                if student_username not in teacher["students"]:
                    teacher["students"].append(student_username)

                    # Сохраняем обновленного учителя
                    users[username] = teacher
                    with open(DATA_FILE, 'w') as f:
                        json.dump(users, f, indent=4)

                    # Обновляем список прикрепленных учеников
                    attached_students_listbox.insert(tk.END, f"{selected_student_name} {selected_student_surname}")
                    all_students_listbox.delete(selected_student[0])

                    messagebox.showinfo("Успех",
                                        f"Ученик {selected_student_name} {selected_student_surname} прикреплен!")
                else:
                    messagebox.showwarning("Ошибка", "Этот ученик уже прикреплен.")
            else:
                messagebox.showwarning("Ошибка", "Выберите ученика для прикрепления.")

        tk.Button(teacher_frame, text="Прикрепить ученика", command=attach_student, bg="#8A2BE2", fg="black",
                  font=("Arial", 14), width=22, height=2, relief="raised", bd=5).pack(pady=10)

        # Section for creating assignments
        tk.Label(teacher_frame, text="Создать домашнее задание:", font=("Arial", 16), bg="#E6E6FA", fg="black").pack(pady=10)
        tk.Label(teacher_frame, text="Заголовок задания:", font=("Arial", 14), bg="#E6E6FA", fg="black").pack(pady=5)
        entry_title = tk.Entry(teacher_frame, font=("Arial", 14), width=40)
        entry_title.pack(pady=5)
        tk.Label(teacher_frame, text="Описание задания:", font=("Arial", 14), bg="#E6E6FA", fg="black").pack(pady=5)
        entry_description = tk.Entry(teacher_frame, font=("Arial", 14), width=40)
        entry_description.pack(pady=5)
        tk.Label(teacher_frame, text="Срок выполнения:", font=("Arial", 14), bg="#E6E6FA", fg="black").pack(pady=5)
        entry_deadline = tk.Entry(teacher_frame, font=("Arial", 14), width=40)
        entry_deadline.pack(pady=5)

        def assign_homework():
            title = entry_title.get()
            description = entry_description.get()
            deadline = entry_deadline.get()
            if title and description and deadline:
                selected_student = attached_students_listbox.curselection()
                if selected_student:
                    selected_student_name = attached_students_listbox.get(selected_student[0]).split()[0]
                    selected_student_surname = attached_students_listbox.get(selected_student[0]).split()[1]
                    student_username = f"{selected_student_name.lower()}_{selected_student_surname.lower()}"
                    assignment = Assignment(username, student_username, title, description, deadline)
                    assignment.save()
                    messagebox.showinfo("Успех",
                                        f"Задание для {selected_student_name} {selected_student_surname} успешно создано!")
                    entry_title.delete(0, tk.END)
                    entry_description.delete(0, tk.END)
                    entry_deadline.delete(0, tk.END)
                else:
                    messagebox.showwarning("Ошибка", "Выберите ученика для задания!")
            else:
                messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля!")

        tk.Button(teacher_frame, text="Назначить задание", command=assign_homework, bg="#8A2BE2", fg="black",
                  font=("Arial", 14), width=22, height=2, relief="raised", bd=5).pack(pady=10)

        # Определение списка для сданных заданий
        submitted_assignments_listbox = tk.Listbox(teacher_frame, font=("Arial", 14), height=10, width=50)
        submitted_assignments_listbox.pack(pady=10)

        def load_submitted_assignments():
            assignments = Assignment.get_by_teacher(username)
            submitted_assignments_listbox.delete(0, tk.END)  # Очистить список перед загрузкой
            for assignment in assignments.values():
                submission_status = " (Сдано)" if assignment.get("submission") else " (Не сдано)"
                submitted_assignments_listbox.insert(tk.END, f"{assignment['title']}{submission_status}")

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
                    submission_window.configure(bg="#E6E6FA")

                    tk.Label(submission_window, text=f"Решение для задания '{assignment_title}':", font=("Arial", 16),
                             bg="#E6E6FA", fg="black").pack(pady=10)

                    submission_text = tk.Text(submission_window, font=("Arial", 14), wrap=tk.WORD, width=50, height=15)
                    submission_text.insert(tk.END, assignment_data["submission"])
                    submission_text.config(state=tk.DISABLED)
                    submission_text.pack(pady=10)

                    tk.Button(submission_window, text="Закрыть", command=submission_window.destroy, bg="#FF5733",
                              fg="black", font=("Arial", 14), width=22, height=2).pack(pady=20)
                else:
                    messagebox.showwarning("Ошибка", "Для этого задания нет доступного решения.")

        load_submitted_assignments()

        # Добавляем кнопку для просмотра решения
        tk.Button(teacher_frame, text="Просмотреть решение", command=view_submission, bg="#8A2BE2", fg="black",
                  font=("Arial", 14), width=22, height=2).pack(pady=10)

        def exit_teacher():
            teacher_window.destroy()
            self.root.deiconify()

        tk.Button(teacher_frame, text="Выход", command=exit_teacher, bg="#FF5733", fg="black", font=("Arial", 14),
                  width=22, height=2, relief="raised", bd=5).pack(pady=20)


    def open_student_window(self, username):
        student_window = tk.Toplevel(self.root)
        student_window.title("Ученик")
        student_window.geometry("600x800")
        student_window.configure(bg="#E6E6FA")

        tk.Label(student_window, text="Ваши задания:", font=("Arial", 16), bg="#E6E6FA", fg="black").pack(pady=10)
        assignments_listbox = tk.Listbox(student_window, font=("Arial", 14), height=10, width=50)
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
        tk.Label(student_window, text="Введите ваш ответ/задание:", font=("Arial", 14), bg="#E6E6FA", fg="black").pack(pady=10)
        entry_submission = tk.Entry(student_window, font=("Arial", 14), width=40)
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

                        # Обновляем файл с заданиями
                        assignments[assignment_title] = assignment_data
                        with open(ASSIGNMENTS_FILE, 'w') as f:
                            json.dump(assignments, f, indent=4)

                        messagebox.showinfo("Успех", f"Задание '{assignment_title}' успешно отправлено!")
                        entry_submission.delete(0, tk.END)
                    else:
                        messagebox.showwarning("Ошибка", "Пожалуйста, введите решение задания!")

        tk.Button(student_window, text="Отправить задание", command=submit_homework, bg="#4CAF50", fg="black", font=("Arial", 14), width=22, height=2, relief="raised", bd=5).pack(pady=10)
        tk.Button(student_window, text="Просмотр", command=show_assignment_details, bg="#4CAF50", fg="black", font=("Arial", 14), width=22, height=2, relief="raised", bd=5).pack(pady=20)
        tk.Button(student_window, text="Выход", command=student_window.destroy, bg="#FF5733", fg="black", font=("Arial", 14), width=22, height=2, relief="raised", bd=5).pack(pady=20)

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
