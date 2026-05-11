import json
import random
import tkinter as tk
from tkinter import messagebox

class QuoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator")
        self.root.geometry("700x550")

        # Загрузка данных
        self.quotes = self.load_quotes()
        self.history = self.load_history()

        # Переменные для фильтров
        self.filter_author_var = tk.StringVar()
        self.filter_topic_var = tk.StringVar()

        self.create_widgets()
        self.refresh_history_display()

    # ------------------- Работа с JSON -------------------
    def load_quotes(self):
        """Загружает цитаты из quotes_data.json, если файла нет – создаёт с предопределёнными."""
        default_quotes = [
            {"text": "Будь изменением, которое хочешь видеть в мире.", "author": "Махатма Ганди", "topic": "мотивация"},
            {"text": "Я мыслю, следовательно существую.", "author": "Рене Декарт", "topic": "философия"},
            {"text": "Жизнь – это то, что с тобой происходит, пока ты строишь планы.", "author": "Джон Леннон", "topic": "жизнь"},
            {"text": "В двух словах я могу резюмировать всё, что я узнал о жизни: она продолжается.", "author": "Роберт Фрост", "topic": "жизнь"},
            {"text": "Не судите о каждом дне по урожаю, который вы собрали, а по семенам, которые вы посадили.", "author": "Роберт Льюис Стивенсон", "topic": "мудрость"}
        ]
        try:
            with open("quotes_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                # Если файл существует, но пуст или не список – вернуть default
                if not isinstance(data, list) or len(data) == 0:
                    self.save_quotes(default_quotes)
                    return default_quotes
                return data
        except FileNotFoundError:
            self.save_quotes(default_quotes)
            return default_quotes

    def save_quotes(self, quotes):
        with open("quotes_data.json", "w", encoding="utf-8") as f:
            json.dump(quotes, f, ensure_ascii=False, indent=4)

    def load_history(self):
        try:
            with open("history.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except FileNotFoundError:
            return []

    def save_history(self):
        with open("history.json", "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)

    # ------------------- GUI -------------------
    def create_widgets(self):
        # Рамка для генерации
        gen_frame = tk.LabelFrame(self.root, text="Генератор", padx=10, pady=10)
        gen_frame.pack(fill="x", padx=10, pady=5)

        self.quote_label = tk.Label(gen_frame, text="Нажмите кнопку", font=("Arial", 12), wraplength=600, justify="left")
        self.quote_label.pack(fill="x", pady=5)

        btn_generate = tk.Button(gen_frame, text="Сгенерировать цитату", command=self.generate_quote, bg="#4CAF50", fg="white")
        btn_generate.pack(pady=5)

        # Рамка добавления новой цитаты
        add_frame = tk.LabelFrame(self.root, text="Добавить свою цитату", padx=10, pady=10)
        add_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(add_frame, text="Текст:").grid(row=0, column=0, sticky="e")
        self.text_entry = tk.Entry(add_frame, width=50)
        self.text_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(add_frame, text="Автор:").grid(row=1, column=0, sticky="e")
        self.author_entry = tk.Entry(add_frame, width=30)
        self.author_entry.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        tk.Label(add_frame, text="Тема:").grid(row=2, column=0, sticky="e")
        self.topic_entry = tk.Entry(add_frame, width=20)
        self.topic_entry.grid(row=2, column=1, padx=5, pady=2, sticky="w")

        btn_add = tk.Button(add_frame, text="Добавить цитату", command=self.add_quote, bg="#2196F3", fg="white")
        btn_add.grid(row=3, column=1, pady=5, sticky="w")

        # Рамка фильтрации
        filter_frame = tk.LabelFrame(self.root, text="Фильтр истории", padx=10, pady=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(filter_frame, text="Автор:").grid(row=0, column=0, sticky="e")
        self.filter_author_entry = tk.Entry(filter_frame, textvariable=self.filter_author_var, width=20)
        self.filter_author_entry.grid(row=0, column=1, padx=5)

        tk.Label(filter_frame, text="Тема:").grid(row=0, column=2, sticky="e")
        self.filter_topic_entry = tk.Entry(filter_frame, textvariable=self.filter_topic_var, width=15)
        self.filter_topic_entry.grid(row=0, column=3, padx=5)

        btn_filter = tk.Button(filter_frame, text="Применить фильтр", command=self.filter_history, bg="#FFC107")
        btn_filter.grid(row=0, column=4, padx=10)
        btn_clear_filter = tk.Button(filter_frame, text="Сбросить", command=self.clear_filter, bg="#9E9E9E", fg="white")
        btn_clear_filter.grid(row=0, column=5)

        # История
        history_frame = tk.LabelFrame(self.root, text="История генераций", padx=10, pady=10)
        history_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.history_listbox = tk.Listbox(history_frame, height=12)
        self.history_listbox.pack(fill="both", expand=True)

        # Кнопка очистки истории
        btn_clear_history = tk.Button(history_frame, text="Очистить историю", command=self.clear_history, bg="#F44336", fg="white")
        btn_clear_history.pack(pady=5)

        # При закрытии окна сохраняем историю
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # ------------------- Логика -------------------
    def generate_quote(self):
        if not self.quotes:
            messagebox.showwarning("Нет цитат", "Сначала добавьте хотя бы одну цитату.")
            return
        quote = random.choice(self.quotes)
        # Сохраняем в историю полную запись
        self.history.append(quote.copy())
        self.save_history()
        self.quote_label.config(text=f"«{quote['text']}»\n\n— {quote['author']} (тема: {quote['topic']})")
        self.refresh_history_display()

    def add_quote(self):
        text = self.text_entry.get().strip()
        author = self.author_entry.get().strip()
        topic = self.topic_entry.get().strip()

        # Валидация
        if not text or not author or not topic:
            messagebox.showerror("Ошибка", "Все поля (текст, автор, тема) должны быть заполнены!")
            return

        new_quote = {"text": text, "author": author, "topic": topic}
        self.quotes.append(new_quote)
        self.save_quotes(self.quotes)

        # Очистить поля ввода
        self.text_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.topic_entry.delete(0, tk.END)

        messagebox.showinfo("Успех", "Цитата добавлена!")

    def refresh_history_display(self, filtered_history=None):
        """Обновляет список отображаемой истории (с учётом фильтра или без)."""
        self.history_listbox.delete(0, tk.END)
        to_show = filtered_history if filtered_history is not None else self.history
        for idx, item in enumerate(to_show, start=1):
            # Ограничим длину текста в списке для читаемости
            short_text = item['text'][:50] + "..." if len(item['text']) > 50 else item['text']
            display = f"{idx}. «{short_text}» — {item['author']} [{item['topic']}]"
            self.history_listbox.insert(tk.END, display)

    def filter_history(self):
        author_filter = self.filter_author_var.get().strip().lower()
        topic_filter = self.filter_topic_var.get().strip().lower()

        if not author_filter and not topic_filter:
            messagebox.showinfo("Фильтр", "Введите хотя бы один критерий для фильтрации.")
            self.refresh_history_display()
            return

        filtered = []
        for q in self.history:
            if author_filter and author_filter not in q['author'].lower():
                continue
            if topic_filter and topic_filter not in q['topic'].lower():
                continue
            filtered.append(q)
        self.refresh_history_display(filtered)
        messagebox.showinfo("Фильтр", f"Найдено {len(filtered)} цитат.")

    def clear_filter(self):
        self.filter_author_var.set("")
        self.filter_topic_var.set("")
        self.refresh_history_display()

    def clear_history(self):
        if messagebox.askyesno("Очистка", "Вы уверены, что хотите очистить всю историю?"):
            self.history = []
            self.save_history()
            self.refresh_history_display()

    def on_close(self):
        self.save_history()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteApp(root)
    root.mainloop()
