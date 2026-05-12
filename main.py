import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

class QuoteGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Путь к файлу с историей
        self.history_file = "quotes_history.json"
        
        # Предопределенные цитаты
        self.default_quotes = [
            {"text": "Будьте сами собой, все остальные роли уже заняты.", "author": "Оскар Уайльд", "topic": "Жизнь"},
            {"text": "Жизнь — это то, что происходит с вами, пока вы строите другие планы.", "author": "Джон Леннон", "topic": "Жизнь"},
            {"text": "Успех — это способность идти от неудачи к неудаче, не теряя энтузиазма.", "author": "Уинстон Черчилль", "topic": "Успех"},
            {"text": "Единственный способ сделать отличную работу — любить то, что вы делаете.", "author": "Стив Джобс", "topic": "Работа"},
            {"text": "Ваше время ограничено, не тратьте его, живя чужой жизнью.", "author": "Стив Джобс", "topic": "Жизнь"},
            {"text": "Образование — это самое мощное оружие, которое вы можете использовать, чтобы изменить мир.", "author": "Нельсон Мандела", "topic": "Образование"},
            {"text": "Лучшее время посадить дерево было 20 лет назад. Следующее лучшее время — сегодня.", "author": "Китайская пословица", "topic": "Мотивация"},
            {"text": "Инновация отличает лидера от последователя.", "author": "Стив Джобс", "topic": "Инновации"},
            {"text": "Счастье не в деньгах, а в том, как вы их зарабатываете.", "author": "Генри Форд", "topic": "Счастье"},
            {"text": "Сложности — это не конец пути, а начало нового.", "author": "Уинстон Черчилль", "topic": "Мотивация"}
        ]
        
        # Инициализация данных
        self.quotes = self.default_quotes.copy()
        self.history = []
        self.load_history()
        
        # Создание интерфейса
        self.create_widgets()
        
    def create_widgets(self):
        # Заголовок
        title_label = tk.Label(self.root, text="Генератор случайных цитат", 
                              font=("Arial", 16, "bold"), bg='#f0f0f0')
        title_label.pack(pady=10)
        
        # Фрейм для фильтров
        filter_frame = tk.Frame(self.root, bg='#f0f0f0')
        filter_frame.pack(pady=10)
        
        # Фильтр по автору
        tk.Label(filter_frame, text="Фильтр по автору:", bg='#f0f0f0').grid(row=0, column=0, padx=5)
        self.author_var = tk.StringVar()
        self.author_combo = ttk.Combobox(filter_frame, textvariable=self.author_var, width=20)
        self.author_combo['values'] = ['Все'] + list(set([q['author'] for q in self.quotes]))
        self.author_combo.set('Все')
        self.author_combo.grid(row=0, column=1, padx=5)
        self.author_combo.bind('<<ComboboxSelected>>', self.on_filter_change)
        
        # Фильтр по теме
        tk.Label(filter_frame, text="Фильтр по теме:", bg='#f0f0f0').grid(row=0, column=2, padx=5)
        self.topic_var = tk.StringVar()
        self.topic_combo = ttk.Combobox(filter_frame, textvariable=self.topic_var, width=20)
        self.topic_combo['values'] = ['Все'] + list(set([q['topic'] for q in self.quotes]))
        self.topic_combo.set('Все')
        self.topic_combo.grid(row=0, column=3, padx=5)
        self.topic_combo.bind('<<ComboboxSelected>>', self.on_filter_change)
        
        # Отображение текущей цитаты
        self.quote_frame = tk.Frame(self.root, bg='white', relief=tk.RAISED, borderwidth=2)
        self.quote_frame.pack(pady=20, padx=20, fill=tk.X)
        
        self.quote_text = tk.Label(self.quote_frame, text="", wraplength=700, 
                                  font=("Arial", 12, "italic"), bg='white', height=3)
        self.quote_text.pack(pady=10, padx=10)
        
        self.author_text = tk.Label(self.quote_frame, text="", font=("Arial", 10, "bold"), bg='white')
        self.author_text.pack(pady=5)
        
        self.topic_text = tk.Label(self.quote_frame, text="", font=("Arial", 10), bg='white', fg='gray')
        self.topic_text.pack(pady=5)
        
        # Кнопки
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(pady=10)
        
        self.generate_btn = tk.Button(button_frame, text="Сгенерировать цитату", 
                                     command=self.generate_quote, bg='#4CAF50', fg='white',
                                     font=("Arial", 11), padx=20, pady=5)
        self.generate_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_history_btn = tk.Button(button_frame, text="Очистить историю", 
                                          command=self.clear_history, bg='#f44336', fg='white',
                                          font=("Arial", 11), padx=20, pady=5)
        self.clear_history_btn.pack(side=tk.LEFT, padx=5)
        
        # Фрейм для добавления новой цитаты
        add_frame = tk.LabelFrame(self.root, text="Добавить новую цитату", bg='#f0f0f0', padx=10, pady=10)
        add_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(add_frame, text="Цитата:", bg='#f0f0f0').grid(row=0, column=0, sticky='w')
        self.new_quote_entry = tk.Entry(add_frame, width=60)
        self.new_quote_entry.grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(add_frame, text="Автор:", bg='#f0f0f0').grid(row=1, column=0, sticky='w')
        self.new_author_entry = tk.Entry(add_frame, width=60)
        self.new_author_entry.grid(row=1, column=1, padx=5, pady=2)
        
        tk.Label(add_frame, text="Тема:", bg='#f0f0f0').grid(row=2, column=0, sticky='w')
        self.new_topic_entry = tk.Entry(add_frame, width=60)
        self.new_topic_entry.grid(row=2, column=1, padx=5, pady=2)
        
        self.add_btn = tk.Button(add_frame, text="Добавить", command=self.add_quote,
                                bg='#2196F3', fg='white', padx=20)
        self.add_btn.grid(row=3, column=1, pady=10)
        
        # История цитат
        history_frame = tk.LabelFrame(self.root, text="История сгенерированных цитат", bg='#f0f0f0', padx=10, pady=10)
        history_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Создаем Listbox с скроллбаром
        listbox_frame = tk.Frame(history_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set,
                                         font=("Arial", 10), height=8)
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.history_listbox.yview)
        
        # Загрузка истории в listbox
        self.update_history_display()
        
    def get_filtered_quotes(self):
        """Фильтрация цитат по выбранным критериям"""
        filtered = self.quotes.copy()
        
        author_filter = self.author_var.get()
        topic_filter = self.topic_var.get()
        
        if author_filter != 'Все':
            filtered = [q for q in filtered if q['author'] == author_filter]
        
        if topic_filter != 'Все':
            filtered = [q for q in filtered if q['topic'] == topic_filter]
        
        return filtered
    
    def generate_quote(self):
        """Генерация случайной цитаты"""
        filtered_quotes = self.get_filtered_quotes()
        
        if not filtered_quotes:
            messagebox.showwarning("Предупреждение", "Нет цитат для отображения с выбранными фильтрами")
            return
        
        quote = random.choice(filtered_quotes)
        
        # Отображение цитаты
        self.quote_text.config(text=f'"{quote["text"]}"')
        self.author_text.config(text=f"— {quote['author']}")
        self.topic_text.config(text=f"Тема: {quote['topic']}")
        
        # Добавление в историю
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history_entry = {
            "text": quote["text"],
            "author": quote["author"],
            "topic": quote["topic"],
            "timestamp": timestamp
        }
        
        self.history.append(history_entry)
        self.save_history()
        self.update_history_display()
    
    def add_quote(self):
        """Добавление новой цитаты"""
        text = self.new_quote_entry.get().strip()
        author = self.new_author_entry.get().strip()
        topic = self.new_topic_entry.get().strip()
        
        # Проверка на пустые строки
        if not text:
            messagebox.showerror("Ошибка", "Текст цитаты не может быть пустым!")
            return
        
        if not author:
            messagebox.showerror("Ошибка", "Автор не может быть пустым!")
            return
        
        if not topic:
            messagebox.showerror("Ошибка", "Тема не может быть пустой!")
            return
        
        # Добавление цитаты
        new_quote = {
            "text": text,
            "author": author,
            "topic": topic
        }
        
        self.quotes.append(new_quote)
        
        # Обновление комбобоксов
        self.author_combo['values'] = ['Все'] + list(set([q['author'] for q in self.quotes]))
        self.topic_combo['values'] = ['Все'] + list(set([q['topic'] for q in self.quotes]))
        
        # Очистка полей
        self.new_quote_entry.delete(0, tk.END)
        self.new_author_entry.delete(0, tk.END)
        self.new_topic_entry.delete(0, tk.END)
        
        messagebox.showinfo("Успех", "Цитата успешно добавлена!")
    
    def on_filter_change(self, event=None):
        """Обработчик изменения фильтров"""
        # Просто обновляем отображение, если есть активная цитата
        pass
    
    def save_history(self):
        """Сохранение истории в JSON"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить историю: {str(e)}")
    
    def load_history(self):
        """Загрузка истории из JSON"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить историю: {str(e)}")
                self.history = []
        else:
            self.history = []
    
    def clear_history(self):
        """Очистка истории"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю?"):
            self.history = []
            self.save_history()
            self.update_history_display()
    
    def update_history_display(self):
        """Обновление отображения истории"""
        self.history_listbox.delete(0, tk.END)
        
        for entry in reversed(self.history):  # Показываем новые записи сверху
            display_text = f"[{entry['timestamp']}] {entry['author']}: {entry['text'][:50]}..."
            self.history_listbox.insert(0, display_text)

def main():
    root = tk.Tk()
    app = QuoteGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
