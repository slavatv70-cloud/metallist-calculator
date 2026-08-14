        contractor_row = ttk.Frame(main_frame)
        contractor_row.pack(fill=tk.X, pady=(5, 20))
        
        self.contractor_entry = ttk.Entry(contractor_row, textvariable=self.contractor_file_path, font=("Arial", 9))
        self.contractor_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 7))
        
        contractor_btn = ttk.Button(contractor_row, text="Обзор...", command=self.browse_contractor_file)
        contractor_btn.pack(side=tk.RIGHT)
        
        # 4. КНОПКА ЗАПУСКА АНАЛИЗА
        run_btn = ttk.Button(main_frame, text="Запустить сверку документов", command=self.run_audit)
        run_btn.pack(fill=tk.X, ipady=5)

    def browse_client_file(self):
        # Метод выбора файла Заказчика (поддерживает Excel и PDF)
        file_path = filedialog.askopenfilename(
            title="Выберите смету Заказчика",
            filetypes=[("Файлы документов", "*.xlsx *.xls *.pdf"), ("Excel файлы", "*.xlsx *.xls"), ("PDF файлы", "*.pdf"), ("Все файлы", "*.*")]
        )
        if file_path:
            self.client_file_path.set(file_path)

    def browse_contractor_file(self):
        # Метод выбора файла Подрядчика (только Excel)
        file_path = filedialog.askopenfilename(
            title="Выберите смету Подрядчика",
            filetypes=[("Excel файлы", "*.xlsx *.xls"), ("Все файлы", "*.*")]
        )
        if file_path:
            self.contractor_file_path.set(file_path)

    def run_audit(self):
        # Проверка заполнения путей к файлам перед анализом
        client = self.client_file_path.get()
        contractor = self.contractor_file_path.get()
        
        if not client or not contractor:
            messagebox.showwarning("Внимание", "Необходимо выбрать оба файла для проведения сверки!")
            return
            
        if not os.path.exists(client) or not os.path.exists(contractor):
            messagebox.showerror("Ошибка", "Один или оба указанных файла не найдены на диске!")
            return
            
        # Здесь будет вызываться ваша функция бэкенд-аналитики
        messagebox.showinfo("Успех", f"Файлы успешно приняты в обработку.\n\nЗаказчик: {os.path.basename(client)}\nПодрядчик: {os.path.basename(contractor)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetCheckerGUI(root)
    root.mainloop()
