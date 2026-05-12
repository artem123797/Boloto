import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os
from datetime import datetime

# --- Файл для хранения истории ---
HISTORY_FILE = "password_history.json"

# --- Основные функции ---
def generate_password():
    """Генерирует пароль на основе пользовательских настроек."""
    length = length_var.get()
    # Проверка корректности (пункт 4)
    if not (4 <= length <= 32):
        messagebox.showerror("Ошибка", "Длина пароля должна быть от 4 до 32 символов.")
        return

    # Собираем разрешённые символы (пункт 2)
    chars = ""
    if letters_var.get():
        chars += string.ascii_letters
    if digits_var.get():
        chars += string.digits
    if special_var.get():
        chars += string.punctuation

    if not chars:
        messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов.")
        return

    # Генерируем пароль
    password = "".join(random.choice(chars) for _ in range(length))
    
    # Получаем текущую историю
    history = load_history()
    # Добавляем новую запись (в формате "Дата", "Пароль", "Длина")
    history.append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "password": password,
        "length": length
    })
    # Сохраняем историю в файл
    save_history(history)
    
    # Обновляем таблицу в интерфейсе
    update_history_table()
    # Показываем сгенерированный пароль
    messagebox.showinfo("Пароль", f"Сгенерированный пароль:\n{password}")

def save_history(history):
    """Сохраняет историю паролей в JSON-файл."""
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=4)
    except Exception as e:
        messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить историю: {e}")

def load_history():
    """Загружает историю из JSON-файла. Возвращает список."""
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, Exception):
        messagebox.showwarning("Предупреждение", "Файл истории повреждён. Будет создана новая история.")
        return []

def update_history_table():
    """Очищает и заново заполняет таблицу истории."""
    # Удаляем старые записи из таблицы
    for row in history_tree.get_children():
        history_tree.delete(row)
    # Загружаем актуальные данные
    history = load_history()
    # Добавляем в таблицу в обратном порядке (сначала новые)
    for entry in reversed(history):
        history_tree.insert("", 0, values=(entry["date"], entry["password"], entry["length"]))

# --- Настройка GUI ---
root = tk.Tk()
root.title("Random Password Generator")
root.geometry("550x500")  # Немного увеличил для удобства

# --- Фрейм настроек ---
frame_settings = ttk.LabelFrame(root, text="Настройки пароля", padding=10)
frame_settings.pack(pady=10, padx=10, fill="x")

# 1. Ползунок длины пароля
ttk.Label(frame_settings, text="Длина:").grid(row=0, column=0, sticky="w")
length_var = tk.IntVar(value=12)  # Стандартная длина 12
length_slider = ttk.Scale(frame_settings, from_=4, to=32, variable=length_var, orient="horizontal", length=200)
length_slider.grid(row=0, column=1, sticky="ew", padx=5)
length_label = ttk.Label(frame_settings, textvariable=length_var)
length_label.grid(row=0, column=2, sticky="w")

# 2. Чекбоксы для выбора символов
ttk.Label(frame_settings, text="Символы:").grid(row=1, column=0, sticky="w")

digits_var = tk.BooleanVar(value=True)
ttk.Checkbutton(frame_settings, text="Цифры (0-9)", variable=digits_var).grid(row=1, column=1, sticky="w")

letters_var = tk.BooleanVar(value=True)
ttk.Checkbutton(frame_settings, text="Буквы (a-z, A-Z)", variable=letters_var).grid(row=2, column=1, sticky="w")

special_var = tk.BooleanVar(value=False)
ttk.Checkbutton(frame_settings, text="Спецсимволы (!@#$)", variable=special_var).grid(row=3, column=1, sticky="w")

# 3. Кнопка генерации
generate_button = ttk.Button(frame_settings, text="Сгенерировать пароль", command=generate_password)
generate_button.grid(row=4, column=0, columnspan=3, pady=(10, 0))

# --- Таблица истории ---
frame_history = ttk.LabelFrame(root, text="История паролей", padding=10)
frame_history.pack(pady=10, padx=10, fill="both", expand=True)

columns = ("Дата", "Пароль", "Длина")
history_tree = ttk.Treeview(frame_history, columns=columns, show="headings", height=10)

# Настройка заголовков и ширины колонок
history_tree.heading("Дата", text="Дата создания")
history_tree.heading("Пароль", text="Пароль")
history_tree.heading("Длина", text="Длина")
history_tree.column("Дата", width=150)
history_tree.column("Пароль", width=250)
history_tree.column("Длина", width=60)

# Добавляем скроллбар
scrollbar = ttk.Scrollbar(frame_history, orient="vertical", command=history_tree.yview)
history_tree.configure(yscrollcommand=scrollbar.set)

# Размещаем таблицу и скроллбар
history_tree.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# --- Загрузка истории при старте ---
update_history_table()

# --- Запуск главного цикла ---
root.mainloop()
