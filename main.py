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
    """Генерирует пароль и добавляет его в историю"""
    pass # Здесь будет логика

def save_history(history):
    """Сохраняет список паролей в JSON-файл"""
    pass

def load_history():
    """Загружает историю из JSON-файла"""
    pass

# --- Настройка GUI ---
root = tk.Tk()
root.title("Random Password Generator")
root.geometry("500x450") # Ширина x Высота

# Здесь позже будут элементы интерфейса

root.mainloop()
