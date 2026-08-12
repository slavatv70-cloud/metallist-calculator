import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from ttkthemes import ThemedStyle
import math

class MetallistProApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор Металлиста PRO — Сметная группа СГК")
        self.root.geometry("1150x880")
        
        # Настройка графической темы оформления Arc
        self.style = ThemedStyle(self.root)
        self.current_theme = "arc"
        self.style.set_theme(self.current_theme)
        self.style.configure('.', font=('Segoe UI', 10))
        self.style.configure('TNotebook.Tab', font=('Segoe UI', 10, 'bold'), padding=5)
        
        # Верхняя панель управления: Материал и Тема
        top_ctrl = ttk.LabelFrame(root, text=" Глобальные настройки сессии ")
        top_ctrl.pack(fill="x", padx=15, pady=5)
        
        ttk.Label(top_ctrl, text="Материал для расчетов:", font=("Segoe UI", 10, "bold")).pack(side="left", padx=10, pady=8)
        self.global_material = ttk.Combobox(top_ctrl, values=["Черный металл (Сталь)", "Нержавеющая сталь", "Медь (Цветной)"], state="readonly", width=22)
        self.global_material.set("Черный металл (Сталь)")
        self.global_material.pack(side="left", padx=5, pady=8)
        
        # Кнопка переключения тем оформления
        self.theme_btn = ttk.Button(top_ctrl, text="🌓 Сменить тему (Тёмная/Светлая)", command=self.toggle_interface_theme)
        self.theme_btn.pack(side="right", padx=15, pady=8)
        
        # Главный контейнер вкладок
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.init_geometry_tab()
        self.init_sortament_tab()
        self.init_detali_tab()
        self.init_metiz_tab()
        self.init_welding_tab()
        self.init_insulation_tab()  # Новая отдельная вкладка
        
        # Фирменный официальный подвал разработчика
        footer = tk.Frame(root, bg="#2c3e50", height=32)
        footer.pack(fill="x", side="bottom", pady=(5, 0))
        footer_text = "Разработчик Тищенко Вячеслав Владимирович, сметная группа г.Назарово ООО \"СГК\" 2026г. версия 1"
        lbl_footer = tk.Label(footer, text=footer_text, fg="#ff8c00", bg="#2c3e50", font=("Segoe UI", 11, "bold"))
        lbl_footer.pack(pady=4)

    def toggle_interface_theme(self):
        self.current_theme = "equilux" if self.current_theme == "arc" else "arc"
        self.style.set_theme(self.current_theme)

    def get_density(self):
        mat = self.global_material.get()
        if "Нержавеющая" in mat: return 7.92
        elif "Медь" in mat: return 8.94
        return 7.85
    def init_geometry_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📐 Геометрия")
        left = ttk.LabelFrame(tab, text=" Параметры ")
        left.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        
        self.geom_type = ttk.Combobox(left, values=["Круг / Сегмент", "Труба (Кольцо)", "Шестигранник"], state="readonly")
        self.geom_type.set("Круг / Сегмент")
        self.geom_type.pack(fill="x", padx=10, pady=8)
        self.geom_type.bind("<<ComboboxSelected>>", self.update_geom_inputs)
        
        self.geom_inputs_frame = ttk.Frame(left)
        self.geom_inputs_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.entries = {}
        
        ttk.Button(left, text="Рассчитать геометрию", command=self.process_geometry).pack(fill="x", padx=10, pady=12)
        self.geom_canvas = tk.Canvas(left, bg="#ffffff", height=160, bd=1, relief="solid")
        self.geom_canvas.pack(fill="x", padx=10, pady=5)
        
        right = ttk.LabelFrame(tab, text=" Результаты ")
        right.pack(side="right", fill="both", expand=True, padx=15, pady=15)
        self.geom_result = tk.Text(right, bg="#ffffff", fg="#333333", font=("Consolas", 11), bd=1, relief="solid")
        self.geom_result.pack(fill="both", expand=True, padx=8, pady=8)
        self.update_geom_inputs()

    def update_geom_inputs(self, event=None):
        for w in self.geom_inputs_frame.winfo_children(): w.destroy()
        self.entries.clear()
        gtype = self.geom_type.get()
        fields = [("Радиус R, мм", "100"), ("Угол альфа, град", "60")] if gtype == "Круг / Сегмент" else [("Внешний диаметр D, мм", "50"), ("Толщина стенки s, мм", "4")] if gtype == "Труба (Кольцо)" else [("Размер под ключ S, мм", "19"), ("Длина L, мм", "1000")]
        for r, (lbl, val) in enumerate(fields):
            ttk.Label(self.geom_inputs_frame, text=lbl).grid(row=r, column=0, pady=6, sticky="w")
            e = ttk.Entry(self.geom_inputs_frame)
            e.insert(0, val)
            e.grid(row=r, column=1, padx=10, pady=6, sticky="ew")
            e.bind("<KeyRelease>", lambda event: self.draw_geometry_sketch())
            self.entries[lbl] = e
        self.draw_geometry_sketch()

    def draw_geometry_sketch(self):
        self.geom_canvas.delete("all")
        gtype = self.geom_type.get()
        cx, cy = 180, 80
        
        if gtype == "Круг / Сегмент":
            r_px = 55
            try:
                angle_deg = float(self.entries["Угол альфа, град"].get())
                if angle_deg <= 0: angle_deg = 60
                if angle_deg > 360: angle_deg = 360
            except Exception:
                angle_deg = 60
                
            if angle_deg >= 360:
                self.geom_canvas.create_oval(cx-r_px, cy-r_px, cx+r_px, cy+r_px, fill="#e9ecef", outline="black")
                self.geom_canvas.create_line(cx, cy, cx+r_px, cy, fill="#e74c3c", width=2)
                self.geom_canvas.create_text(cx+r_px+15, cy, text="360°", font=("Segoe UI", 8, "bold"), fill="#e74c3c")
            else:
                rad_start, rad_end = math.radians(0), math.radians(angle_deg)
                self.geom_canvas.create_arc(cx-r_px, cy-r_px, cx+r_px, cy+r_px, start=0, extent=angle_deg, fill="#e9ecef", outline="black")
                
                x1, y1 = cx + r_px * math.cos(rad_start), cy - r_px * math.sin(rad_start)
                x2, y2 = cx + r_px * math.cos(rad_end), cy - r_px * math.sin(rad_end)
                
                self.geom_canvas.create_line(x1, y1, x2, y2, fill="#e74c3c", width=2)
                self.geom_canvas.create_line(cx, cy, x1, y1, fill="black", dash=(3,2))
                self.geom_canvas.create_line(cx, cy, x2, y2, fill="black", dash=(3,2))
                self.geom_canvas.create_text(cx+r_px+15, cy, text="0°", font=("Segoe UI", 8))
                self.geom_canvas.create_text(x2+10, y2-5, text=f"{int(angle_deg)}°", font=("Segoe UI", 8, "bold"), fill="#e74c3c")
            
        elif gtype == "Труба (Кольцо)":
            self.geom_canvas.create_oval(cx-60, cy-65, cx+60, cy+65, fill="#dee2e6", outline="black")
            self.geom_canvas.create_oval(cx-40, cy-45, cx+40, cy+45, fill="#ffffff", outline="black")
        elif "Шестигранник" in gtype:
            p = []
            for i in range(6): p.extend([cx + 50*math.cos(math.radians(i*60)), cy + 50*math.sin(math.radians(i*60))])
            self.geom_canvas.create_polygon(p, fill="#e9ecef", outline="black")

    def process_geometry(self):
        gtype = self.geom_type.get(); rho = self.get_density()
        res = f"=== Расчет геометрии заготовки ({self.global_material.get()}) ===\n\n"
        try:
            if gtype == "Круг / Сегмент":
                R, a = float(self.entries["Радиус R, мм"].get()), float(self.entries["Угол альфа, град"].get())
                res += f"Площадь круга: {math.pi*(R**2):.2f} мм²\nПлощадь сегмента: {0.5*(R**2)*(math.radians(a)-math.sin(math.radians(a))):.2f} мм²\n"
            elif gtype == "Труба (Кольцо)":
                D, s = float(self.entries["Внешний диаметр D, мм"].get()), float(self.entries["Толщина стенки s, мм"].get())
                sect = (math.pi / 4) * (D**2 - (D - 2*s)**2)
                res += f"Внутр. диаметр d: {D-2*s:.2f} мм\nПлощадь сечения: {sect:.2f} мм²\nВес 1м заготовки: {(sect*rho/1000):.3f} кг\n"
            elif gtype == "Шестигранник":
                S, L = float(self.entries["Размер под ключ S, мм"].get()), float(self.entries["Длина L, мм"].get())
                res += f"Площадь сечения: {(math.sqrt(3)/2)*(S**2):.2f} мм²\nВес заготовки: {((math.sqrt(3)/2)*(S**2)*L*rho)/1000000:.3f} кг\n"
        except Exception as e: res += f"Ошибка: {str(e)}"
        self.draw_geometry_sketch()
        self.geom_result.config(state="normal"); self.geom_result.delete("1.0", tk.END); self.geom_result.insert("1.0", res); self.geom_result.config(state="disabled")
    def init_sortament_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📊 Сортамент")
        top = ttk.LabelFrame(tab, text=" Параметры проката ")
        top.pack(fill="x", padx=15, pady=10)
        
        ttk.Label(top, text="Тип проката:").grid(row=0, column=0, padx=5, pady=8, sticky="w")
        self.sort_profile = ttk.Combobox(top, values=[
            "Двутавр ГОСТ 8239-89", "Швеллер ГОСТ 8240-97", "Уголок ГОСТ 8509-93",
            "Труба Квадратная ГОСТ 8639-82", "Труба Прямоугольная ГОСТ 8645-68",
            "Труба Круглая ГОСТ 10704-91", "Лист ГОСТ 19903-74"
        ], state="readonly", width=28)
        self.sort_profile.set("Двутавр ГОСТ 8239-89"); self.sort_profile.grid(row=0, column=1, padx=5, pady=8, sticky="w")
        self.sort_profile.bind("<<ComboboxSelected>>", self.on_sortament_type_change)
        
        self.sort_dyn_frame = ttk.Frame(top); self.sort_dyn_frame.grid(row=0, column=2, padx=10, pady=8, sticky="w")
        self.sort_entries = {}
        
        self.sort_len_frame = ttk.Frame(top); self.sort_len_frame.grid(row=0, column=3, padx=10, pady=8, sticky="w")
        ttk.Label(self.sort_len_frame, text="Длина, м:").grid(row=0, column=0, padx=2)
        self.sort_length = ttk.Entry(self.sort_len_frame, width=8); self.sort_length.insert(0, "12"); self.sort_length.grid(row=0, column=1)
        
        ttk.Button(top, text="Рассчитать прокат", command=self.calculate_sortament_weight).grid(row=0, column=4, padx=15, pady=8)
        
        self.sort_tree = ttk.Treeview(tab, columns=("num", "h", "b", "t", "weight"), show="headings", height=10)
        for c, t in [("num", "Размер / № Профиля"), ("h", "Высота h, мм"), ("b", "Ширина b, мм"), ("t", "Толщина t/s, мм"), ("weight", "Вес 1м (Сталь), кг")]: 
            self.sort_tree.heading(c, text=t); self.sort_tree.column(c, width=140, anchor="center")
        self.sort_tree.pack(fill="x", padx=15, pady=5)
        
        self.sort_output = tk.Text(tab, bg="#ffffff", font=("Consolas", 10), height=10, bd=1, relief="solid")
        self.sort_output.pack(fill="both", expand=True, padx=15, pady=10)
        self.on_sortament_type_change()

    def on_sortament_type_change(self, event=None):
        for w in self.sort_dyn_frame.winfo_children(): w.destroy()
        self.sort_entries.clear()
        prof = self.sort_profile.get()
        
        if "Лист ГОСТ" in prof:
            self.sort_tree.pack_forget(); self.sort_len_frame.grid_forget()
            ttk.Label(self.sort_dyn_frame, text="Толщина (t):").pack(side="left", padx=2)
            cb_t = ttk.Combobox(self.sort_dyn_frame, values=["0.5", "1.0", "1.5", "2.0", "3.0", "4.0", "5.0", "8.0", "10", "12", "16", "20", "30"], width=6, state="readonly")
            cb_t.set("4.0"); cb_t.pack(side="left", padx=4)
            self.sort_entries["cb_t"] = cb_t
            
            ttk.Label(self.sort_dyn_frame, text="Раскрой:").pack(side="left", padx=2)
            cb_r = ttk.Combobox(self.sort_dyn_frame, values=["1500х6000", "2000х6000", "1250х2500", "Пользовательский"], width=14, state="readonly")
            cb_r.set("1500х6000"); cb_r.pack(side="left", padx=4)
            self.sort_entries["cb_r"] = cb_r
        else:
            self.sort_tree.pack(fill="x", padx=15, pady=5); self.sort_len_frame.grid(row=0, column=3, padx=10, pady=8, sticky="w")
            self.load_sortament_data()

    def load_sortament_data(self):
        for r in self.sort_tree.get_children(): self.sort_tree.delete(r)
        prof = self.sort_profile.get()
        data = []
        if "Двутавр" in prof:
            data = [("10", "100", "55", "4.5", "9.46"), ("14", "140", "73", "4.9", "13.70"), ("20", "200", "100", "5.2", "21.00"), ("30", "300", "135", "6.5", "36.50"), ("60", "600", "190", "12.0", "108.00")]
        elif "Швеллер" in prof:
            data = [("5У", "50", "32", "4.4", "4.84"), ("10У", "100", "46", "4.5", "8.59"), ("20У", "200", "76", "5.2", "18.40"), ("40У", "400", "115", "8.0", "48.30")]
        elif "Уголок" in prof:
            data = [("25х3", "25", "25", "3.0", "1.12"), ("50х5", "50", "50", "5.0", "3.77"), ("100х8", "100", "100", "8.0", "12.20")]
        elif "Квадратная" in prof:
            data = [("40х40х3", "40", "40", "3.0", "3.37"), ("60х60х4", "60", "60", "4.0", "6.71"), ("100х100х5", "100", "100", "5.0", "14.41")]
        elif "Прямоугольная" in prof:
            data = [("60х40х3", "60", "40", "3.0", "4.31"), ("80х40х4", "80", "40", "4.0", "6.71"), ("120х80х6", "120", "80", "6.0", "17.22")]
        elif "Круглая" in prof:
            data = [("57х3.5", "57", "57", "3.5", "4.62"), ("76х4", "76", "76", "4.0", "7.10"), ("89х4", "89", "89", "4.0", "8.38"), ("108х4", "108", "108", "4.0", "10.26"), ("159х4.5", "159", "159", "4.5", "17.15"), ("219х6", "219", "219", "6.0", "31.52"), ("273х7", "273", "273", "7.0", "45.92"), ("325х8", "325", "325", "8.0", "62.54"), ("426x9", "426", "426", "9.0", "92.55"), ("530x10", "530", "530", "10.0", "128.24")]
        for item in data: self.sort_tree.insert("", "end", values=item)

    def calculate_sortament_weight(self):
        prof = self.sort_profile.get(); rho = self.get_density(); mat_name = self.global_material.get()
        report = f"📊 РЕЗУЛЬТАТЫ РАСЧЕТА СОРТАМЕНТА ({mat_name}):\n--------------------------------------------------\n"
        try:
            if "Лист ГОСТ" in prof:
                t = float(self.sort_entries["cb_t"].get())
                r_val = self.sort_entries["cb_r"].get()
                if "1500х6000" in r_val: B, L = 1500, 6000
                elif "2000х6000" in r_val: B, L = 2000, 6000
                elif "1250х2500" in r_val: B, L = 1250, 2500
                else: B, L = 1000, 1000
                total = (t * B * L * rho) / 1000000
                report += f"• Продукт: Лист ГОСТ 19903 | Габариты: {t}х{B}х{L} мм\n▶ ИТОГОВЫЙ ВЕС ЛИСТА: {total:.3f} кг\n"
            else:
                sel = self.sort_tree.focus()
                if not sel: messagebox.showwarning("Внимание", "Выберите профиль в таблице!"); return
                L = float(self.sort_length.get()); val = self.sort_tree.item(sel, "values")
                report += f"• Наименование: {prof} | Размер: {val}\n▶ ИТОГОВЫЙ ВЕС КОНСТРУКЦИИ ({L} м): {float(val) * (rho / 7.85) * L:.3f} кг\n"
        except Exception as e: messagebox.showerror("Ошибка", f"Ошибка ввода: {e}"); return
        self.sort_output.delete("1.0", tk.END); self.sort_output.insert("1.0", report)
    def init_detali_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔧 Детали трубопроводов")
        left = ttk.LabelFrame(tab, text=" Элементы теплосетей (ГОСТ) ")
        left.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        
        ttk.Label(left, text="Тип детали:").pack(anchor="w", padx=10, pady=2)
        self.det_type = ttk.Combobox(left, values=["Отвод 90° ГОСТ 17375-2001", "Переход ГОСТ 17378-2001", "Фланец ГОСТ 33259-2015"], state="readonly")
        self.det_type.set("Отвод 90° ГОСТ 17375-2001"); self.det_type.pack(fill="x", padx=10, pady=4)
        self.det_type.bind("<<ComboboxSelected>>", self.on_det_type_change)
        
        ttk.Label(left, text="Условный диаметр Ду (DN):").pack(anchor="w", padx=10, pady=2)
        self.det_dy = ttk.Combobox(left, values=["Ду50 (∅57)", "Ду80 (∅89)", "Ду100 (∅108)", "Ду125 (∅133)", "Ду150 (∅159)", "Ду200 (∅219)", "Ду250 (∅273)", "Ду300 (∅325)", "Ду400 (∅426)", "Ду500 (∅530)"], state="readonly")
        self.det_dy.set("Ду150 (∅159)"); self.det_dy.pack(fill="x", padx=10, pady=4)
        
        self.det_extra_frame = ttk.Frame(left); self.det_extra_frame.pack(fill="x", padx=10, pady=4)
        ttk.Label(self.det_extra_frame, text="Параметр детали:").grid(row=0, column=0, sticky="w")
        self.det_param = ttk.Combobox(self.det_extra_frame, values=["Исполнение 2"], width=15, state="readonly")
        self.det_param.set("Исполнение 2"); self.det_param.grid(row=0, column=1, padx=5)
        
        ttk.Label(left, text="Количество, шт:").pack(anchor="w", padx=10, pady=2)
        self.det_count = ttk.Entry(left); self.det_count.insert(0, "10"); self.det_count.pack(fill="x", padx=10, pady=4)
        ttk.Button(left, text="Рассчитать вес деталей", command=self.calculate_detali_weight).pack(fill="x", padx=10, pady=12)
        
        right = ttk.LabelFrame(tab, text=" Спецификация фасонных элементов ")
        right.pack(side="right", fill="both", expand=True, padx=15, pady=15)
        self.det_output = tk.Text(right, bg="#ffffff", font=("Consolas", 10), bd=1, relief="solid")
        self.det_output.pack(fill="both", expand=True, padx=8, pady=8)

    def on_det_type_change(self, event=None):
        dtype = self.det_type.get()
        if "Отвод" in dtype: self.det_param['values'] = ["Исполнение 2"]; self.det_param.set("Исполнение 2")
        elif "Переход" in dtype: self.det_param['values'] = ["Концентрический", "Эксцентрический"]; self.det_param.set("Концентрический")
        elif "Фланец" in dtype: self.det_param['values'] = ["Давление Ру10", "Давление Ру16", "Давление Ру25"]; self.det_param.set("Давление Ру16")

    def calculate_detali_weight(self):
        dtype, dy = self.det_type.get(), self.det_dy.get()
        rho = self.get_density()
        try: count = float(self.det_count.get())
        except ValueError: return
        
        base_w = 1.0
        if "Отвод" in dtype:
            weights_map = {
                "Ду50": 0.7, "Ду80": 2.1, "Ду100": 3.3, "Ду125": 4.9,
                "Ду150": 8.1, "Ду200": 17.2, "Ду250": 33.5, "Ду300": 51.4,
                "Ду400": 98.6, "Ду500": 173.0
            }
            # Точный парсинг ключа Ду из строки combobox
            key = dy.split(" ")[0]
            base_w = weights_map.get(key, 8.1)
        else:
            if "Ду150" in dy: base_w = 4.2 if "Переход" in dtype else 6.8
            elif "Ду200" in dy: base_w = 8.5 if "Переход" in dtype else 11.2
            else: base_w = 3.0

        total = base_w * (rho / 7.85) * count
        res = f"📐 СПЕЦИФИКАЦИЯ ТРУБОПРОВОДНЫХ ДЕТАЛЕЙ СГК:\n----------------------------------------\n• Тип элемента:  {dtype}\n• Диаметр / Типоразмер: {dy}\n• Масса 1 единицы (ГОСТ): {base_w:.2f} кг\n• Объем партии:  {int(count)} шт\n----------------------------------------\n▶ ОБЩИЙ ВЕС СБОРОЧНЫХ ЕДИНИЦ: {total:.3f} кг\n"
        self.det_output.delete("1.0", tk.END); self.det_output.insert("1.0", res)
    def init_metiz_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔩 Метизы")
        left = ttk.LabelFrame(tab, text=" Параметры расчета крепежа ")
        left.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        
        ttk.Label(left, text="Тип метизов:").pack(anchor="w", padx=10, pady=2)
        self.metiz_type = ttk.Combobox(left, values=["Болт ГОСТ 7798 / 7805", "Гайка ГОСТ 5915 / 5927", "Шпилька ГОСТ 22032", "Шайба ГОСТ 11371"], state="readonly")
        self.metiz_type.set("Болт ГОСТ 7798 / 7805"); self.metiz_type.pack(fill="x", padx=10, pady=4); self.metiz_type.bind("<<ComboboxSelected>>", self.on_metiz_type_change)
        
        ttk.Label(left, text="Диаметр (d), мм:").pack(anchor="w", padx=10, pady=2)
        self.metiz_d = ttk.Combobox(left, values=["М3", "М4", "М5", "М6", "М8", "М10", "М12", "М16", "М20", "М24", "М30", "М36", "М42", "М48"], state="readonly")
        self.metiz_d.set("М10"); self.metiz_d.pack(fill="x", padx=10, pady=4)
        
        self.len_frame = ttk.Frame(left); self.len_frame.pack(fill="x", padx=10, pady=2)
        ttk.Label(self.len_frame, text="Длина (L), мм:").pack(anchor="w")
        self.metiz_l = ttk.Entry(self.len_frame); self.metiz_l.insert(0, "40"); self.len_frame.pack(fill="x", pady=2)
        
        self.extra_frame = ttk.Frame(left); self.extra_frame.pack(fill="x", padx=10, pady=4)
        ttk.Label(self.extra_frame, text="Класс прочности:").grid(row=0, column=0, sticky="w", pady=2)
        self.metiz_class = ttk.Combobox(self.extra_frame, values=["5.8", "8.8", "10.9"], width=6, state="readonly")
        self.metiz_class.set("8.8"); self.metiz_class.grid(row=0, column=1, padx=5, sticky="w")
        
        self.kit_check_var = tk.BooleanVar(value=False)
        self.kit_check = ttk.Checkbutton(self.extra_frame, text="Укомплектовать болт (1 гайка + 2 шайбы)", variable=self.kit_check_var)
        self.kit_check.grid(row=1, column=0, columnspan=2, sticky="w", pady=5)
        
        ttk.Label(left, text="Количество, шт:").pack(anchor="w", padx=10, pady=2)
        self.metiz_count = ttk.Entry(left); self.metiz_count.insert(0, "1000"); self.metiz_count.pack(fill="x", padx=10, pady=4)
        ttk.Button(left, text="Рассчитать метизы", command=self.calculate_metiz_weight).pack(fill="x", padx=10, pady=10)
        
        right = ttk.LabelFrame(tab, text=" Спецификация и Техконтроль крепежа ")
        right.pack(side="right", fill="both", expand=True, padx=15, pady=15)
        self.metiz_canvas = tk.Canvas(right, bg="#ffffff", height=120, bd=1, relief="solid"); self.metiz_canvas.pack(fill="x", padx=10, pady=5)
        self.metiz_info = tk.Text(right, bg="#ffffff", font=("Consolas", 10), height=18, bd=1, relief="solid"); self.metiz_info.pack(fill="both", expand=True, padx=10, pady=5)
        self.on_metiz_type_change()

    def on_metiz_type_change(self, event=None):
        mtype = self.metiz_type.get()
        if "Шайба" in mtype:
            self.metiz_d['values'] = ["3", "4", "5", "6", "8", "10", "12", "16", "20", "24", "30", "36", "42", "48"]
            self.metiz_d.set("10"); self.len_frame.pack_forget(); self.extra_frame.pack_forget()
        else:
            self.metiz_d['values'] = ["М3", "М4", "М5", "М6", "М8", "М10", "М12", "М16", "М20", "М24", "М30", "М36", "М42", "М48"]
            self.metiz_d.set("М10")
            if "Гайка" in mtype: self.len_frame.pack_forget(); self.extra_frame.pack_forget()
            else: self.len_frame.pack(fill="x", padx=10, pady=2); self.extra_frame.pack(fill="x", padx=10, pady=4)
        self.draw_metiz_sketch()

    def draw_metiz_sketch(self):
        self.metiz_canvas.delete("all")
        mtype, d = self.metiz_type.get(), self.metiz_d.get()
        self.metiz_canvas.create_text(20, 15, text=f"Эскиз: {mtype}", font=("Segoe UI", 10, "bold"), anchor="w")
        if "Болт" in mtype:
            self.metiz_canvas.create_rectangle(50, 40, 80, 90, fill="#f1f3f5"); self.metiz_canvas.create_rectangle(80, 48, 220, 82, fill="#e9ecef")
        elif "Гайка" in mtype:
            self.metiz_canvas.create_rectangle(100, 35, 150, 95, fill="#f1f3f5"); self.metiz_canvas.create_oval(112, 47, 138, 73, fill="white")
        else: self.metiz_canvas.create_rectangle(50, 50, 230, 80, fill="#f8f9fa", outline="gray")

    def calculate_metiz_weight(self):
        mtype, d_str = self.metiz_type.get(), self.metiz_d.get(); rho = self.get_density()
        try: count = float(self.metiz_count.get())
        except ValueError: return
        d = float(d_str.replace("М", "")); w_1000 = 0.0; details = ""
        p_class = float(self.metiz_class.get())
        torque_nm = (p_class * 10 * d * 3.5) * 0.18
        
        if "Болт" in mtype or "Шпилька" in mtype:
            L = float(self.metiz_l.get()); vol = (math.pi * ((d / 2) ** 2) * L) / 1000
            w_1000 = (vol + (math.pi * (d ** 2) * (d * 0.7)) / 1000) * rho if "Болт" in mtype else vol * rho * 1.02
            details = f"• Рекомендуемый момент затяжки: {torque_nm:.1f} Н·м (Класс {p_class})\n"
            if "Болт" in mtype and self.kit_check_var.get():
                w_nut = ((((d * 1.7) ** 2) * math.sqrt(3) / 2) - (math.pi * ((d / 2) ** 2))) * (d * 0.8) / 1000 * rho
                w_was = (math.pi / 4) * ((d * 2.2)**2 - d**2) * (d * 0.15) / 1000 * rho
                w_1000 += (w_nut + 2 * w_was)
                details += "• Комплектация: Включено (1 Гайка + 2 Шайбы на 1 Болт)\n"
        elif "Гайка" in mtype: w_1000 = (((((d * 1.7) ** 2) * math.sqrt(3) / 2) - (math.pi * ((d / 2) ** 2))) * (d * 0.8) / 1000) * rho
        elif "Шайба" in mtype: w_1000 = ((math.pi / 4) * ((d * 2.2)**2 - d**2) * (d * 0.15) / 1000) * rho

        report = f"🔩 СПЕЦИФИКАЦИЯ КРЕПЕЖА:\n----------------------------------------\n• Тип метиза: {mtype} {d_str}\n{details}• Кол-во в заявке: {int(count)} шт\n----------------------------------------\n" \
                 f"▶ ИТОГОВЫЙ ВЕС ПАРТИИ: {(w_1000 / 1000) * count:.4f} кг\n"
        self.metiz_info.config(state="normal"); self.metiz_info.delete("1.0", tk.END); self.metiz_info.insert("1.0", report); self.metiz_info.config(state="disabled")
    def init_welding_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="⚡ Сварка")
        
        inputs = ttk.LabelFrame(tab, text=" Параметры сварочных швов по ГОСТ ")
        inputs.pack(fill="x", padx=15, pady=10)
        
        ttk.Label(inputs, text="Геометрия стыка:").grid(row=0, column=0, padx=5, pady=6, sticky="w")
        self.weld_geom = ttk.Combobox(inputs, values=["Трубный стык ГОСТ 16037", "Плоский шов ГОСТ 5264-80 (1 метр)"], state="readonly", width=26)
        self.weld_geom.set("Трубный стык ГОСТ 16037"); self.weld_geom.grid(row=0, column=1, padx=5, pady=6, sticky="w")
        
        ttk.Label(inputs, text="Толщина стенки стали s, мм:").grid(row=0, column=2, padx=5, pady=6, sticky="w")
        self.weld_pipe_s = ttk.Entry(inputs, width=12); self.weld_pipe_s.insert(0, "6"); self.weld_pipe_s.grid(row=0, column=3, padx=5, pady=6, sticky="w")
        
        ttk.Label(inputs, text="Тип шва (ГОСТ):").grid(row=1, column=0, padx=5, pady=6, sticky="w")
        self.weld_joint_type = ttk.Combobox(inputs, values=["С2 (Стыковое)", "С17 (V-раздел)", "С21 (X-раздел)"], state="readonly", width=20)
        self.weld_joint_type.set("С17 (V-раздел)"); self.weld_joint_type.grid(row=1, column=1, padx=5, pady=6, sticky="w")
        
        ttk.Label(inputs, text="Метод сварки:").grid(row=1, column=2, padx=5, pady=6, sticky="w")
        self.weld_method = ttk.Combobox(inputs, values=["Ручная дуговая (ММА)", "Полуавтомат (MIG/MAG)"], state="readonly", width=18)
        self.weld_method.set("Ручная дуговая (ММА)"); self.weld_method.grid(row=1, column=3, padx=5, pady=6, sticky="w")
        
        ttk.Button(inputs, text="⚡ Рассчитать расход сварочных материалов", command=self.calculate_only_welding, width=45).grid(row=2, column=0, columnspan=2, pady=10, padx=5, sticky="ew")
        
        self.weld_only_output = tk.Text(tab, bg="#ffffff", font=("Courier", 10), height=14, bd=1, relief="solid")
        self.weld_only_output.pack(fill="both", expand=True, padx=15, pady=10)

    def calculate_only_welding(self):
        try:
            s = float(self.weld_pipe_s.get()); joint = self.weld_joint_type.get(); method = self.weld_method.get(); w_geom = self.weld_geom.get()
            line_length_m = 0.50 if "Трубный" in w_geom else 1.0
            area = (s * 1.5 + 3) if "С2" in joint else ((s**2) * 0.6)
            mass_dep = (area * line_length_m * 7.85) / 1000
            
            if "Полуавтомат" in method:
                w_mat = mass_dep * 1.12; gas_liters = line_length_m * 220
                res = f"⚡ ВЕДОМОСТЬ СВАРКИ MIG/MAG:\n----------------------------------------\n• Конструкция: {w_geom} ({joint})\n• Расход сварочной проволоки: {w_mat:.3f} кг\n• Защитный газ CO2: {gas_liters:.1f} л\n"
            else:
                res = f"⚡ ВЕДОМОСТЬ СВАРКИ MMA:\n----------------------------------------\n• Конструкция: {w_geom} ({joint})\n• Расход электродов с огарками: {mass_dep * 1.62:.3f} кг\n"
        except Exception: res = "❌ Ошибка параметров сварки!"
        self.weld_only_output.delete("1.0", tk.END); self.weld_only_output.insert("1.0", res)

    def init_insulation_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="环 Изоляция")
        
        inputs = ttk.LabelFrame(tab, text=" Геометрический расчет объемов теплоизоляции по схеме ")
        inputs.pack(fill="x", padx=15, pady=10)
        
        ttk.Label(inputs, text="Тип прокладки сети:").grid(row=0, column=0, padx=5, pady=6, sticky="w")
        self.iso_calc_type = ttk.Combobox(inputs, values=["Одна труба", "Несколько труб (Группа в оболочке)"], state="readonly", width=30)
        self.iso_calc_type.set("Одна труба"); self.iso_calc_type.grid(row=0, column=1, padx=5, pady=6, sticky="w")
        self.iso_calc_type.bind("<<ComboboxSelected>>", self.on_iso_calc_type_change)
        
        self.iso_inputs_frame = ttk.Frame(inputs)
        self.iso_inputs_frame.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky="ew")
        self.iso_entries = {}
        
        btn_frame = ttk.Frame(inputs); btn_frame.grid(row=2, column=0, columnspan=4, pady=10, sticky="ew")
        ttk.Button(btn_frame, text="⚡ Рассчитать геометрические объемы изоляции", command=self.calculate_only_insulation, width=45).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="💾 Экспорт ведомости в файл", command=self.export_iso_report, width=45).pack(side="right", padx=5)
        
        self.iso_output = tk.Text(tab, bg="#ffffff", font=("Courier", 10), height=14, bd=1, relief="solid")
        self.iso_output.pack(fill="both", expand=True, padx=15, pady=10)
        self.on_iso_calc_type_change()

    def on_iso_calc_type_change(self, event=None):
        for w in self.iso_inputs_frame.winfo_children(): w.destroy()
        self.iso_entries.clear()
        itype = self.iso_calc_type.get()
        if itype == "Одна труба":
            fields = [("Диаметр трубы D, м", "0.125"), ("Толщина изоляции t, м", "0.08"), ("Длина участка L, м", "130")]
        else:
            fields = [("Диаметр крайних D1, м", "0.108"), ("Диаметр средних D2, м", "0.076"), ("Толщина изоляции t, м", "0.1"), ("Зазор труб p, м", "0.1"), ("Длина участка L, м", "65")]
        for idx, (lbl, val) in enumerate(fields):
            ttk.Label(self.iso_inputs_frame, text=lbl).grid(row=0, column=idx*2, padx=4, pady=4, sticky="w")
            e = ttk.Entry(self.iso_inputs_frame, width=10); e.insert(0, val); e.grid(row=0, column=idx*2+1, padx=4, pady=4)
            self.iso_entries[lbl] = e

    def calculate_only_insulation(self):
        try:
            itype = self.iso_calc_type.get()
            if itype == "Одна труба":
                D = float(self.iso_entries["Диаметр трубы D, м"].get())
                t = float(self.iso_entries["Толщина изоляции t, м"].get())
                L = float(self.iso_entries["Длина участка L, м"].get())
                S_r = math.pi * D * L
                S_pi = math.pi * (D + 2 * t) * L
                V_i = (math.pi / 4) * (((D + 2 * t) ** 2) - (D ** 2)) * L
                
                self.iso_report_data = (
                    f"📝 ВЕДОМОСТЬ ОБЪЕМОВ ИЗОЛЯЦИОННЫХ РАБОТ СГК (ОДНОТРУБНЫЙ УЧАСТОК):\n"
                    f"--------------------------------------------------\n"
                    f"▶ Площадь обертывания (окраски) Sr:        {S_r:.6f} м²\n"
                    f"▶ Площадь покровного слоя Spi:             {S_pi:.6f} м²\n"
                    f"▶ ИТОГОВЫЙ ОБЪЕМ ТЕПЛОИЗОЛЯЦИИ Vi:         {V_i:.6f} м³\n"
                )
            else:
                D1 = float(self.iso_entries["Диаметр крайних D1, м"].get())
                D2 = float(self.iso_entries["Диаметр средних D2, м"].get())
                t = float(self.iso_entries["Толщина изоляции t, м"].get())
                p = float(self.iso_entries["Зазор труб p, м"].get())
                L = float(self.iso_entries["Длина участка L, м"].get())
                M = D1 + D2 + (p * 2)
                B = (D1 * 2) + D2 + (p * 2) + (t * 2)
                S_r = ((math.pi * D1) + (M * 2)) * L
                S_pi = ((math.pi * (D1 + 2 * t)) + (M * 2)) * L
                V_i = (((math.pi / 4) * ((D1 + 2 * t) ** 2 - D1 ** 2)) + (M * 2 * t)) * L
                
                self.iso_report_data = (
                    f"📝 ВЕДОМОСТЬ ОБЪЕМОВ ИЗОЛЯЦИОННЫХ РАБОТ СГК (ГРУППОВАЯ ОСЬ):\n"
                    f"--------------------------------------------------\n"
                    f"• Габаритная ширина блока B:               {B:.3f} м\n"
                    f"--------------------------------------------------\n"
                    f"▶ Площадь обертывания (окраски) Sr:        {S_r:.6f} м²\n"
                    f"▶ Площадь покровного слоя Spi:             {S_pi:.6f} м²\n"
                    f"▶ ИТОГОВЫЙ ОБЪЕМ ТЕПЛОИЗОЛЯЦИИ Vi:         {V_i:.6f} м³\n"
                )
        except Exception as e: self.iso_report_data = f"❌ Ошибка: {e}"
        self.iso_output.delete("1.0", tk.END); self.iso_output.insert("1.0", self.iso_report_data)

    def export_iso_report(self):
        if not hasattr(self, 'iso_report_data') or "❌" in self.iso_report_data:
            messagebox.showwarning("Внимание", "Нет данных для экспорта!"); return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Текстовые файлы", "*.txt")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(self.iso_report_data)
                f.write("\n\nСметная группа г.Назарово ООО \"СГК\" 2026г. версия 1\n")
            messagebox.showinfo("Успех", "Отчет изоляции успешно выгружен!")

if __name__ == "__main__":
    root = tk.Tk()
    app = MetallistProApp(root)
    root.mainloop()
