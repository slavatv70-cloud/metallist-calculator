import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class BudgetCheckerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Сметный Аудит: Сверка документов")
        self.root.geometry("620x350")
        self.root.resizable(False, False)
        
        # Переменные для хранения путей к файлам
        self.client_file_path = tk.StringVar()
        self.contractor_file_path = tk.StringVar()
        
        # Инициализация графических элементов
        self.init_interface()

    def init_interface(self):
        # Настройка современного стиля отображения элементов Windows
        style = ttk.Style()
        style.theme_use('vista')
        
        # Главный отступ от краев окна
        main_frame = ttk.Frame(self.root, padding="25")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 1. ЗАГОЛОВОК
        title_label = ttk.Label(
            main_frame, 
            text="Модуль сверки смет Заказчика и Подрядчика", 
            font=("Arial", 12, "bold"), 
            foreground="#1F497D"
        )
        title_label.pack(pady=(0, 20), anchor="w")
        
        # 2. ПЕРВОЕ ОКНО: Выбор сметы Заказчика
        client_label = ttk.Label(main_frame, text="1. Файл оригинальной сметы Заказчика (Excel / PDF):", font=("Arial", 9, "bold"))
        client_label.pack(anchor="w")
        
        client_row = ttk.Frame(main_frame)
        client_row.pack(fill=tk.X, pady=(5, 15))
        
        self.client_entry = ttk.Entry(client_row, textvariable=self.client_file_path, font=("Arial", 9))
        self.client_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 7))
        
        client_btn = ttk.Button(client_row, text="Обзор...", command=self.browse_client_file)
        client_btn.pack(side=tk.RIGHT)
        
        # 3. ВТОРОЕ ОКНО: Выбор сметы Подрядчика
        contractor_label = ttk.Label(main_frame, text="2. Файл проверяемой сметы Подрядчика (Excel):", font=("Arial", 9, "bold"))
        contractor_label.pack(anchor="w")
        
        contractor_row = ttk.Frame(main_frame)
        contractor_row.pack(fill=tk.X, pady=(5, 20))
        
        self.contractor_entry = ttk.Entry(contractor_row, textvariable=self.contractor_file_path, font=("Arial", 9))
        self.contractor_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 7))
        
        contractor_btn = ttk.Button(contractor_row, text="Обзор...", command=self.browse_contractor_file)
        contractor_btn.pack(side=tk.RIGHT)
        
        # 4. ИНДИКАТОР ВЫПОЛНЕНИЯ (Progress Bar)
        self.progress_bar = ttk.Progressbar(main_frame, orient="horizontal", mode="indeterminate")
        self.progress_bar.pack(fill=tk.X, pady=(0, 15))
        
        # 5. КНОПКА ЗАПУСКА ПРОВЕРКИ
        self.start_btn = ttk.Button(
            main_frame, 
            text="ЗАПУСТИТЬ ПРОВЕРКУ", 
            width=35,
            command=self.execute_verification
        )
        self.start_btn.pack(pady=5)

    def browse_client_file(self):
        """Логика кнопки Обзор для Заказчика"""
        file_selected = filedialog.askopenfilename(
            title="Выберите смету Заказчика",
            filetypes=[("Сметные документы (*.xlsx, *.pdf)", "*.xlsx *.pdf"), ("Все файлы", "*.*")]
        )
        if file_selected:
            self.client_file_path.set(file_selected)

    def browse_contractor_file(self):
        """Логика кнопки Обзор для Подрядчика"""
        file_selected = filedialog.askopenfilename(
            title="Выберите смету Подрядчика",
            filetypes=[("Таблицы Excel (*.xlsx)", "*.xlsx"), ("Все файлы", "*.*")]
        )
        if file_selected:
            self.contractor_file_path.set(file_selected)

    def execute_verification(self):
        """Логика кнопки Запустить проверку"""
        client_file = self.client_file_path.get()
        contractor_file = self.contractor_file_path.get()
        
        # Проверка заполнения полей
        if not client_file or not contractor_file:
            messagebox.showwarning(
                "Внимание", 
                "Для проведения анализа необходимо выбрать оба файла!\n\n"
                "1. Укажите смету Заказчика.\n2. Укажите смету Подрядчика."
            )
            return
            
        # Включение анимации загрузки
        self.progress_bar.start(15)
        self.root.update_idletasks()
        
        try:
            # Создаем папку для результатов, если ее нет
            output_folder = "Результаты_Сверки_Смет"
            os.makedirs(output_folder, exist_ok=True)
            
            # --- В этом месте вызывается математический движок сравнения из прошлых шагов ---
            # Для демонстрации работы интерфейса просто симулируем создание выходных файлов
            self.save_dummy_reports(output_folder)
            
            # Останавливаем анимацию
            self.progress_bar.stop()
            
            # Выводим отчет об успешном завершении
            messagebox.showinfo(
                "Проверка завершена", 
                f"Анализ выполнен успешно!\n\n"
                f"Сформировано 3 выходных Excel-документа.\n"
                f"Файлы сохранены в папку:\n{os.path.abspath(output_folder)}"
            )
            
        except Exception as error:
            self.progress_bar.stop()
            messagebox.showerror(
                "Ошибка системы", 
                f"Не удалось выполнить сверку данных.\nТехнический текст ошибки:\n{str(error)}"
            )

    def save_dummy_reports(self, folder):
        """Техническая функция генерации пустых файлов для демонстрации успеха работы GUI"""
        with open(os.path.join(folder, "1_Детальный_анализ.xlsx"), "w") as f: f.write("")
        with open(os.path.join(folder, "2_Заключение_по_смете.xlsx"), "w") as f: f.write("")
        with open(os.path.join(folder, "3_Сводный_анализ.xlsx"), "w") as f: f.write("")

if __name__ == "__main__":
    window = tk.Tk()
    app = BudgetCheckerGUI(window)
    window.mainloop()
