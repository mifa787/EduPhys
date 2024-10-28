import tkinter as tk
from tkinter import ttk, messagebox

class EducationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Образовательная платформа")
        self.root.geometry("800x600")

        # Создаем notebook
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True, fill='both')

        # Создаем вкладки
        self.auth_tab = ttk.Frame(self.notebook)
        self.test_tab = ttk.Frame(self.notebook)
        self.lesson_tab = ttk.Frame(self.notebook)
        self.homework_tab = ttk.Frame(self.notebook)

        # Добавляем вкладки в notebook
        self.notebook.add(self.auth_tab, text="Авторизация")
        self.notebook.add(self.test_tab, text="Тестирование")
        self.notebook.add(self.lesson_tab, text="Урок")
        self.notebook.add(self.homework_tab, text="Домашнее задание")

        # Создаем содержимое вкладок
        self.create_auth_tab()
        self.create_test_tab()
        self.create_lesson_tab()
        self.create_homework_tab()

        # Изначально блокируем все вкладки кроме авторизации
        self.disable_tabs()

    def disable_tabs(self):
        """Блокировка всех вкладок кроме авторизации"""
        self.notebook.tab(1, state='disabled')
        self.notebook.tab(2, state='disabled')
        self.notebook.tab(3, state='disabled')

    def enable_tabs(self):
        """Разблокировка всех вкладок"""
        self.notebook.tab(1, state='normal')
        self.notebook.tab(2, state='normal')
        self.notebook.tab(3, state='normal')

    def create_auth_tab(self):
        """Создание вкладки авторизации"""
        # Создаем фрейм для центрирования элементов
        auth_frame = ttk.Frame(self.auth_tab)
        auth_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Заголовок
        title_label = ttk.Label(auth_frame, text="Авторизация", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Логин
        login_label = ttk.Label(auth_frame, text="Логин:")
        login_label.grid(row=1, column=0, padx=5, pady=5)
        self.login_entry = ttk.Entry(auth_frame)
        self.login_entry.grid(row=1, column=1, padx=5, pady=5)

        # Пароль
        password_label = ttk.Label(auth_frame, text="Пароль:")
        password_label.grid(row=2, column=0, padx=5, pady=5)
        self.password_entry = ttk.Entry(auth_frame, show="*")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)

        # Кнопка входа
        login_button = ttk.Button(auth_frame, text="Войти", command=self.login)
        login_button.grid(row=3, column=0, columnspan=2, pady=20)

    def create_test_tab(self):
        """Создание вкладки тестирования"""
        # Заголовок
        title_label = ttk.Label(self.test_tab, text="Тестирование", font=("Arial", 16, "bold"))
        title_label.pack(pady=20)

        # Пример теста
        test_frame = ttk.Frame(self.test_tab)
        test_frame.pack(pady=10)

        # Вопрос
        question_label = ttk.Label(test_frame, text="Вопрос 1: Выберите правильный ответ")
        question_label.pack(pady=10)

        # Варианты ответов
        self.test_var = tk.StringVar()
        answers = [("Ответ A", "A"), ("Ответ B", "B"), ("Ответ C", "C")]

        for text, value in answers:
            radio = ttk.Radiobutton(test_frame, text=text, value=value, variable=self.test_var)
            radio.pack()

        # Кнопка отправки
        submit_button = ttk.Button(test_frame, text="Отправить ответ")
        submit_button.pack(pady=20)

    def create_lesson_tab(self):
        """Создание вкладки урока"""
        # Заголовок
        title_label = ttk.Label(self.lesson_tab, text="Урок", font=("Arial", 16, "bold"))
        title_label.pack(pady=20)

        # Содержание урока
        lesson_text = tk.Text(self.lesson_tab, height=15, width=60)
        lesson_text.pack(pady=10)
        lesson_text.insert(tk.END, "Содержание урока...\n\n")
        lesson_text.config(state='disabled')

        # Кнопки навигации
        nav_frame = ttk.Frame(self.lesson_tab)
        nav_frame.pack(pady=10)

        prev_button = ttk.Button(nav_frame, text="Предыдущий урок")
        prev_button.pack(side=tk.LEFT, padx=5)

        next_button = ttk.Button(nav_frame, text="Следующий урок")
        next_button.pack(side=tk.LEFT, padx=5)

    def create_homework_tab(self):
        """Создание вкладки домашнего задания"""
        # Заголовок
        title_label = ttk.Label(self.homework_tab, text="Домашнее задание", font=("Arial", 16, "bold"))
        title_label.pack(pady=20)

        # Задание
        task_label = ttk.Label(self.homework_tab, text="Задание:", font=("Arial", 12))
        task_label.pack(pady=5)

        task_text = tk.Text(self.homework_tab, height=5, width=60)
        task_text.pack(pady=10)
        task_text.insert(tk.END, "Текст задания...\n")
        task_text.config(state='disabled')

        # Поле для ответа
        answer_label = ttk.Label(self.homework_tab, text="Ваш ответ:", font=("Arial", 12))
        answer_label.pack(pady=5)

        self.answer_text = tk.Text(self.homework_tab, height=10, width=60)
        self.answer_text.pack(pady=10)

        # Кнопка отправки
        submit_button = ttk.Button(self.homework_tab, text="Отправить ответ")
        submit_button.pack(pady=10)

    def login(self):
        """Обработка входа в систему"""
        login = self.login_entry.get()
        password = self.password_entry.get()

        if login and password:
            messagebox.showinfo("Успех", "Вход выполнен успешно!")
        self.enable_tabs()

def main():
    root = tk.Tk()
    app = EducationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()