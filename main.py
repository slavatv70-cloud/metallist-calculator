import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedStyle
import math

class MetallistProApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор Металлиста PRO — Сметная группа СГК")
        self.root.geometry("1400x1000")
        
        # Настройка графической темы
        self.style = ThemedStyle(self.root)
        self.current_theme = "arc"
        try:
            self.style.set_theme(self.current_theme)
        except:
            self.current_theme = "clam"
            self.style.set_theme(self.current_theme)
        self.style.configure('.', font=('Segoe UI', 10))
        self.style.configure('TNotebook.Tab', font=('Segoe UI', 10, 'bold'), padding=5)
        
        # Панель глобальных настроек
        self.create_header()
        
        # Главный контейнер вкладок
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Создание всех вкладок
        self.init_geometry_tab()
        self.init_sortament_tab()
        self.init_detali_tab()
        self.init_metiz_tab()
        self.init_welding_tab()
        self.init_electrodes_tab()
        self.init_designation_tab()
        self.init_insulation_tab()
        
        # Подвал
        self.create_footer()

    def create_header(self):
        """Создание верхней панели с настройками"""
        top_ctrl = ttk.LabelFrame(self.root, text=" Глобальные настройки сессии ")
        top_ctrl.pack(fill="x", padx=15, pady=5)
        
        ttk.Label(top_ctrl, text="Материал для расчетов:", font=("Segoe UI", 10, "bold")).pack(side="left", padx=10, pady=8)
        self.global_material = ttk.Combobox(top_ctrl, values=[
            "Черный металл (Сталь)", "Нержавеющая сталь", "Алюминий", 
            "Бронза", "Латунь", "Медь", "Никель", "Чугун"
        ], state="readonly", width=22)
        self.global_material.set("Черный металл (Сталь)")
        self.global_material.pack(side="left", padx=5, pady=8)
        
        self.theme_btn = ttk.Button(top_ctrl, text="🌓 Сменить тему (Тёмная/Светлая)", command=self.toggle_interface_theme)
        self.theme_btn.pack(side="right", padx=15, pady=8)

    def create_footer(self):
        """Создание нижнего колонтитула"""
        footer = tk.Frame(self.root, bg="#2c3e50", height=32)
        footer.pack(fill="x", side="bottom", pady=(5, 0))
        footer_text = "Разработчик Тищенко Вячеслав Владимирович, сметная группа г.Назарово ООО \"СГК\" 2026г. версия 3.0"
        lbl_footer = tk.Label(footer, text=footer_text, foreground="#ff8c00", background="#2c3e50", font=("Segoe UI", 11, "bold"))
        lbl_footer.pack(pady=4)

    def toggle_interface_theme(self):
        """Переключение темы интерфейса"""
        try:
            self.current_theme = "equilux" if self.current_theme == "arc" else "arc"
            self.style.set_theme(self.current_theme)
        except:
            messagebox.showwarning("Внимание", "Не удалось сменить тему. Используется текущая.")
            self.current_theme = "clam"
            self.style.set_theme(self.current_theme)

    def get_density(self):
        """Получение плотности материала"""
        mat = self.global_material.get()
        densities = {
            "Нержавеющая": 7.92,
            "Алюминий": 2.70,
            "Бронза": 8.80,
            "Латунь": 8.50,
            "Медь": 8.94,
            "Никель": 8.90,
            "Чугун": 7.20
        }
        for key, value in densities.items():
            if key in mat:
                return value
        return 7.85

    def get_electrode_group(self, mark):
        """Определение группы электродов по марке согласно Сборнику 30"""
        group1 = ["ЛБ-52А", "ВСФ-65У", "ВСФ-75У", "ВСФ-85", "ОЗШ-1", "ВСЦ-4А", "ОЗЛ-25Б"]
        group2 = ["УОНИ-13/45", "АНО-11", "ТМУ-21У", "ОЗС-18", "ОЗС-6", "ОЗС-17Н", "ВСЦ-4", 
                  "ВСЦ-60", "ТМЛ-1У", "ТМЛ-3У", "УТ-28", "ОЗЛ-5", "ОЗЛ-29", "ОЗЛ-25", "ОЗЛ-36", "АНВ-20"]
        group3 = ["ОЗЛ-8", "ОЗЛ-7", "ОЗЛ-14А", "НИИАТ-1", "ОЗЛ-3", "ОЗЛ-21", "ОЗЛ-23", "ВН-48", 
                  "УОНИ-13/55К", "ЦУ-5", "ДСК-50", "ОЗС-25", "СК2-50", "УОНИ-13/55У", "УОНИ-13/65", 
                  "АНП-2", "УОНИ-13/85", "НИАТ-3М", "АНО-5", "ОЗС-23", "АНО-4", "АНО-14", "ОЗС-4", 
                  "ОЗС-22Н", "ОЗС-22Р", "ТМЛ-4В", "ЦЛ-39", "СМВ-96", "СМВ-95", "СМА-96", "ОЗЛ-6", 
                  "КТИ-7А", "ОЗЛ-2", "ОЗЛ-35", "АНЖР-2"]
        group4 = ["ОЗЛ-37-1", "СМ-11", "УОНИ-13/55", "ОЗС-24", "АНО-6", "АНО-18", "ОЗС-12", "МР-3", 
                  "ОЗС-21", "ОМА-2", "ОЗЛ-9А", "ГС-1", "АНЖР-1", "АНЖР-3У", "ОЗЛ-19", "НИИ-48Г", 
                  "УОНИ-13/НК", "ЦЛ-11", "ЦЛ-15", "ЦЛ-9", "ОЗЛ-17У"]
        
        if mark in group1:
            return 1, 1.4
        elif mark in group2:
            return 2, 1.5
        elif mark in group3:
            return 3, 1.6
        elif mark in group4:
            return 4, 1.7
        return 3, 1.6  # По умолчанию группа III

    # ==================== ВКЛАДКА 1: ГЕОМЕТРИЯ ====================
    def init_geometry_tab(self):
        """Инициализация вкладки Геометрия"""
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
        self.geom_entries = {}
        
        ttk.Button(left, text="Рассчитать геометрию", command=self.process_geometry).pack(fill="x", padx=10, pady=12)
        
        self.geom_canvas = tk.Canvas(left, bg="#ffffff", height=160, bd=1, relief="solid")
        self.geom_canvas.pack(fill="x", padx=10, pady=5)
        
        right = ttk.LabelFrame(tab, text=" Результаты ")
        right.pack(side="right", fill="both", expand=True, padx=15, pady=15)
        
        self.geom_result = tk.Text(right, bg="#ffffff", foreground="#333333", font=("Consolas", 11), bd=1, relief="solid")
        self.geom_result.pack(fill="both", expand=True, padx=8, pady=8)
        self.update_geom_inputs()

    def update_geom_inputs(self, event=None):
        """Обновление полей ввода геометрии"""
        for w in self.geom_inputs_frame.winfo_children():
            w.destroy()
        self.geom_entries.clear()
        
        gtype = self.geom_type.get()
        fields = {
            "Круг / Сегмент": [("Радиус R, мм", "100"), ("Угол альфа, град", "60")],
            "Труба (Кольцо)": [("Внешний диаметр D, мм", "50"), ("Толщина стенки s, мм", "4")],
            "Шестигранник": [("Размер под ключ S, мм", "19"), ("Длина L, мм", "1000")]
        }
        
        for r, (lbl, val) in enumerate(fields.get(gtype, [])):
            ttk.Label(self.geom_inputs_frame, text=lbl).grid(row=r, column=0, pady=6, sticky="w")
            e = ttk.Entry(self.geom_inputs_frame)
            e.insert(0, val)
            e.grid(row=r, column=1, padx=10, pady=6, sticky="ew")
            e.bind("<KeyRelease>", lambda event: self.draw_geometry_sketch())
            self.geom_entries[lbl] = e
        self.draw_geometry_sketch()

    def draw_geometry_sketch(self):
        """Отрисовка геометрической фигуры"""
        self.geom_canvas.delete("all")
        gtype = self.geom_type.get()
        cx, cy = 180, 80
        
        if gtype == "Круг / Сегмент":
            r_px = 55
            try:
                angle_deg = float(self.geom_entries.get("Угол альфа, град", tk.Entry()).get() or 60)
                angle_deg = max(0, min(360, angle_deg))
            except:
                angle_deg = 60
            
            if angle_deg >= 360:
                self.geom_canvas.create_oval(cx-r_px, cy-r_px, cx+r_px, cy+r_px, fill="#e9ecef", outline="black")
            else:
                self.geom_canvas.create_arc(cx-r_px, cy-r_px, cx+r_px, cy+r_px, start=0, extent=angle_deg, fill="#e9ecef", outline="black")
        elif gtype == "Труба (Кольцо)":
            self.geom_canvas.create_oval(cx-60, cy-65, cx+60, cy+65, fill="#dee2e6", outline="black")
            self.geom_canvas.create_oval(cx-40, cy-45, cx+40, cy+45, fill="#ffffff", outline="black")
        else:  # Шестигранник
            points = []
            for i in range(6):
                angle = math.radians(i * 60)
                points.extend([cx + 50 * math.cos(angle), cy + 50 * math.sin(angle)])
            self.geom_canvas.create_polygon(points, fill="#e9ecef", outline="black")

    def process_geometry(self):
        """Расчет геометрических параметров"""
        gtype = self.geom_type.get()
        rho = self.get_density()
        res = f"=== Расчет геометрии заготовки ===\nМатериал: {self.global_material.get()}\nПлотность: {rho:.2f} г/см³\n\n"
        
        try:
            if gtype == "Круг / Сегмент":
                R = float(self.geom_entries["Радиус R, мм"].get())
                a = float(self.geom_entries["Угол альфа, град"].get())
                area_circle = math.pi * R**2
                area_segment = 0.5 * R**2 * (math.radians(a) - math.sin(math.radians(a)))
                res += f"Площадь круга: {area_circle:.2f} мм²\n"
                res += f"Площадь сегмента: {area_segment:.2f} мм²\n"
                res += f"Вес сегмента: {area_segment * rho / 1000:.3f} г\n"
            elif gtype == "Труба (Кольцо)":
                D = float(self.geom_entries["Внешний диаметр D, мм"].get())
                s = float(self.geom_entries["Толщина стенки s, мм"].get())
                sect = (math.pi / 4) * (D**2 - (D - 2*s)**2)
                res += f"Площадь сечения: {sect:.2f} мм²\n"
                res += f"Вес 1м заготовки: {(sect * rho / 1000):.3f} кг\n"
            else:  # Шестигранник
                S = float(self.geom_entries["Размер под ключ S, мм"].get())
                L = float(self.geom_entries["Длина L, мм"].get())
                area = (math.sqrt(3) / 2) * S**2
                weight = area * L * rho / 1000000
                res += f"Площадь сечения: {area:.2f} мм²\n"
                res += f"Вес заготовки: {weight:.3f} кг\n"
        except Exception as e:
            res += f"Ошибка: {str(e)}"
        
        self.geom_result.config(state="normal")
        self.geom_result.delete("1.0", tk.END)
        self.geom_result.insert("1.0", res)
        self.geom_result.config(state="disabled")

    # ==================== ВКЛАДКА 2: СОРТАМЕНТ ====================
    def init_sortament_tab(self):
        """Инициализация вкладки Сортамент"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📊 Сортамент")
        
        top = ttk.LabelFrame(tab, text=" Параметры проката и труб ")
        top.pack(fill="x", padx=15, pady=10)
        top.grid_columnconfigure(1, weight=1)
        top.grid_columnconfigure(3, weight=1)
        
        ttk.Label(top, text="Тип проката:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.sort_profile = ttk.Combobox(top, values=["Двутавр ГОСТ 8239-89", "Швеллер ГОСТ 8240-97", "Труба Круглая ГОСТ 10704-91", "Лист ГОСТ 19903-74"], state="readonly", width=25)
        self.sort_profile.set("Труба Круглая ГОСТ 10704-91")
        self.sort_profile.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.sort_profile.bind("<<ComboboxSelected>>", self.on_sortament_profile_change)
        
        self.lbl_main_len = ttk.Label(top, text="Длина участка, м:")
        self.lbl_main_len.grid(row=0, column=2, padx=10, pady=5, sticky="w")
        self.sort_length = ttk.Entry(top, width=10)
        self.sort_length.insert(0, "12")
        self.sort_length.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        
        self.sort_manual_frame = ttk.LabelFrame(top, text=" Ручной ввод параметров геометрии (СГК-САПР) ")
        self.sort_manual_frame.grid(row=1, column=0, columnspan=4, padx=5, pady=8, sticky="ew")
        self.sort_dyn_widgets = {}
        
        ttk.Button(top, text="Рассчитать прокат / трубу", command=self.calculate_sortament_weight).grid(row=2, column=0, columnspan=4, padx=15, pady=8, sticky="ew")
        
        self.sort_tree = ttk.Treeview(tab, columns=("num", "weight"), show="headings", height=6)
        self.sort_tree.heading("num", text="Типоразмер / Профиль по справочнику ГОСТ")
        self.sort_tree.heading("weight", text="Вес 1 погонного метра (или листа), кг")
        self.sort_tree.column("num", width=350, anchor="center")
        self.sort_tree.column("weight", width=200, anchor="center")
        self.sort_tree.pack(fill="x", padx=15, pady=5)
        
        self.sort_output = tk.Text(tab, bg="#ffffff", foreground="#000000", font=("Consolas", 10), height=8, bd=1, relief="solid")
        self.sort_output.pack(fill="both", expand=True, padx=15, pady=10)
        self.on_sortament_profile_change()

    def rebuild_sortament_manual_inputs(self):
        """Перестройка полей ручного ввода сортамента"""
        for w in self.sort_manual_frame.winfo_children():
            w.destroy()
        self.sort_dyn_widgets.clear()
        
        prof = self.sort_profile.get()
        
        if "Лист" in prof:
            self.lbl_main_len.grid_remove()
            self.sort_length.grid_remove()
            
            fields = [("Ширина листа, мм", "1500"), ("Длина листа, мм", "6000"), ("Толщина листа, мм", "4")]
            for col, (lbl, val) in enumerate(fields):
                ttk.Label(self.sort_manual_frame, text=lbl).grid(row=0, column=col*2, padx=5, pady=6, sticky="w")
                e = tk.Entry(self.sort_manual_frame, width=10, bg="#fff2cc", justify="center")
                e.insert(0, val)
                e.grid(row=0, column=col*2+1, padx=5, pady=6, sticky="w")
                self.sort_dyn_widgets[lbl] = e
        else:
            self.lbl_main_len.grid()
            self.sort_length.grid()
            
            fields = [("Внешний диаметр (D), мм", ""), ("Толщина стенки (s), мм", "")]
            for col, (lbl, val) in enumerate(fields):
                ttk.Label(self.sort_manual_frame, text=lbl).grid(row=0, column=col*2, padx=8, pady=6, sticky="w")
                e = tk.Entry(self.sort_manual_frame, width=12, bg="#fff2cc", justify="center")
                e.insert(0, val)
                e.grid(row=0, column=col*2+1, padx=5, pady=6, sticky="w")
                self.sort_dyn_widgets[lbl] = e

    def on_sortament_profile_change(self, event=None):
        """Обновление справочных данных при смене профиля"""
        for r in self.sort_tree.get_children():
            self.sort_tree.delete(r)
        
        prof = self.sort_profile.get()
        data = {
            "Двутавр": [("№ 10", "9.46"), ("№ 14", "13.70"), ("№ 20", "21.00"), ("№ 30", "36.50"), ("№ 45", "66.50"), ("№ 60", "108.00")],
            "Швеллер": [("5У", "4.84"), ("10У", "8.59"), ("20У", "18.40"), ("30У", "31.80"), ("40У", "48.30")],
            "Лист": [("Лист t=2мм (1500х6000)", "141.3"), ("Лист t=4мм (1500х6000)", "282.6"), ("Лист t=10мм (2000х6000)", "942.0"), ("Лист t=20мм (2000х6000)", "1884.0")],
            "Труба": [
                ("∅57х3.5", "4.62"), ("∅89х4", "8.38"), ("∅108х4", "10.26"), ("∅159х5", "18.99"), 
                ("∅219х6", "31.52"), ("∅273х7", "45.92"), ("∅325х8", "62.54"), ("∅426х9", "92.55"), 
                ("∅530х10", "128.24"), ("∅630х10", "152.90"), ("∅720х10", "175.10"), ("∅820х10", "199.76"), 
                ("∅920х10", "224.42"), ("∅1024х10", "250.07"), ("∅1220х12", "357.50"), ("∅1420х14", "499.20")
            ]
        }
        
        for key, values in data.items():
            if key in prof:
                for item in values:
                    self.sort_tree.insert("", "end", values=item)
                break
        
        self.rebuild_sortament_manual_inputs()

    def calculate_sortament_weight(self):
        """Расчет веса сортамента"""
        rho = self.get_density()
        prof = self.sort_profile.get()
        res = ""
        
        try:
            if "Лист" in prof:
                w_mm = float(self.sort_dyn_widgets["Ширина листа, мм"].get())
                l_mm = float(self.sort_dyn_widgets["Длина листа, мм"].get())
                t_mm = float(self.sort_dyn_widgets["Толщина листа, мм"].get())
                total = w_mm * l_mm * t_mm / 1000000.0 * rho
                res = f"📊 РЕЗУЛЬТАТ РАСЧЕТА ЛИСТОВОГО ПРОКАТА:\n"
                res += f"• Спецификация: {prof}\n"
                res += f"• Размеры раскроя: {w_mm} мм х {l_mm} мм, толщина {t_mm} мм\n"
                res += f"• Плотность сплава: {rho:.2f} г/см³\n"
                res += "-" * 60 + "\n"
                res += f"▶ ИТОГОВЫЙ ВЕС ЛИСТА: {total:.3f} кг\n"
            else:
                L = float(self.sort_length.get() or 12)
                man_d = self.sort_dyn_widgets.get("Внешний диаметр (D), мм", tk.Entry()).get().strip()
                man_s = self.sort_dyn_widgets.get("Толщина стенки (s), мм", tk.Entry()).get().strip()
                
                if man_d and man_s and "Труба" in prof:
                    D = float(man_d)
                    s = float(man_s)
                    w_meter = math.pi * (D - s) * s * (rho / 1000.0)
                    desc_str = f"Ручной ввод (∅{D}х{s})"
                else:
                    sel = self.sort_tree.focus()
                    if not sel:
                        messagebox.showwarning("Внимание", "Выберите строку в таблице справочника или заполните желтые поля!")
                        return
                    item_data = self.sort_tree.item(sel)
                    desc_str = str(item_data["values"][0])
                    w_meter = float(item_data["values"][1]) * (rho / 7.85)
                
                total = w_meter * L
                res = f"📊 РЕЗУЛЬТАТ РАСЧЕТА СОРТАМЕНТА:\n"
                res += f"• Профиль: {prof}\n"
                res += f"• Типоразмер: {desc_str}\n"
                res += f"• Вес 1 п.м.: {w_meter:.3f} кг\n"
                res += f"• Длина участка: {L} м\n"
                res += "-" * 60 + "\n"
                res += f"▶ ИТОГОВЫЙ ВЕС ПАРТИИ: {total:.3f} кг\n"
        except Exception as e:
            res = f"❌ Ошибка: {str(e)}"
        
        self.sort_output.delete("1.0", tk.END)
        self.sort_output.insert("1.0", res)

    # ==================== ВКЛАДКА 3: ДЕТАЛИ ТРУБОПРОВОДОВ ====================
    def init_detali_tab(self):
        """Инициализация вкладки Детали трубопроводов"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔧 Детали трубопроводов")
        
        left = ttk.LabelFrame(tab, text=" Параметры арматуры и отводов ")
        left.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        
        ttk.Label(left, text="Тип стандарта / Спецификация:").pack(anchor="w", padx=10, pady=2)
        self.det_type = ttk.Combobox(left, values=[
            "Отвод ГОСТ 17375-2001 (Тип 3D, R≈1.5DN)", 
            "Отвод ГОСТ 30753-2001 (Тип 2D, R≈1.0DN)", 
            "Отвод ТУ 51-515-91 (Промысловый хладостойкий)", 
            "Отвод ГОСТ 24950-81 (Магистральный гнутый R=15-60м)",
            "Фланец ГОСТ 33259-2015 (Плоский/Воротниковый)"
        ], state="readonly", width=42)
        self.det_type.set("Отвод ГОСТ 17375-2001 (Тип 3D, R≈1.5DN)")
        self.det_type.pack(fill="x", padx=10, pady=4)
        self.det_type.bind("<<ComboboxSelected>>", self.toggle_detali_widgets_view)
        
        self.f_det_angle = ttk.Frame(left)
        self.f_det_angle.pack(fill="x", padx=10, pady=4)
        ttk.Label(self.f_det_angle, text="Угол изгиба оси отвода, град:").pack(side="left")
        self.det_angle = ttk.Combobox(self.f_det_angle, values=["30", "45", "90"], state="readonly", width=8)
        self.det_angle.set("90")
        self.det_angle.pack(side="left", padx=10)
        
        self.man_det_frame = ttk.LabelFrame(left, text=" Ручной ввод геометрических параметров заготовки ")
        self.man_det_frame.pack(fill="x", padx=10, pady=6)
        
        ttk.Label(self.man_det_frame, text="Внешний диаметр D, мм:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.det_manual_d = tk.Entry(self.man_det_frame, width=10, bg="#fff2cc", justify="center")
        self.det_manual_d.insert(0, "159")
        self.det_manual_d.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.man_det_frame, text="Толщина стенки s, мм:").grid(row=0, column=2, padx=10, pady=5, sticky="w")
        self.det_manual_s = tk.Entry(self.man_det_frame, width=10, bg="#fff2cc", justify="center")
        self.det_manual_s.insert(0, "5")
        self.det_manual_s.grid(row=0, column=3, padx=5, pady=5)
        
        self.lbl_flange_dy = ttk.Label(left, text="Для фланцев - условный проход Ду (DN):")
        self.det_flange_dy = ttk.Combobox(left, values=["Ду50", "Ду80", "Ду100", "Ду150", "Ду200", "Ду250", "Ду300", "Ду400", "Ду500", "Ду600", "Ду800", "Ду1000"], state="readonly")
        self.det_flange_dy.set("Ду150")
        
        ttk.Label(left, text="Общий объем партии, шт:").pack(anchor="w", padx=10, pady=2)
        self.det_cnt = ttk.Entry(left)
        self.det_cnt.insert(0, "10")
        self.det_cnt.pack(fill="x", padx=10, pady=4)
        
        ttk.Button(left, text="Посчитать точную массу по ГОСТ/ТУ", command=self.proc_detali_calc).pack(fill="x", padx=10, pady=10)
        
        self.det_output = tk.Text(tab, bg="#ffffff", foreground="#000000", font=("Consolas", 10), bd=1, relief="solid")
        self.det_output.pack(side="right", fill="both", expand=True, padx=15, pady=15)
        self.toggle_detali_widgets_view()

    def toggle_detali_widgets_view(self, event=None):
        """Переключение видимости виджетов деталей"""
        t = self.det_type.get()
        if "Фланец" in t:
            self.f_det_angle.pack_forget()
            self.man_det_frame.pack_forget()
            self.lbl_flange_dy.pack(anchor="w", padx=10, pady=2)
            self.det_flange_dy.pack(fill="x", padx=10, pady=4)
        else:
            self.lbl_flange_dy.pack_forget()
            self.det_flange_dy.pack_forget()
            self.f_det_angle.pack(fill="x", padx=10, pady=4)
            self.man_det_frame.pack(fill="x", padx=10, pady=6)

    def proc_detali_calc(self):
        """Расчет веса деталей трубопроводов"""
        t = self.det_type.get()
        rho = self.get_density()
        try:
            c = float(self.det_cnt.get())
        except:
            c = 1.0
        
        if "Фланец" in t:
            f_dy = self.det_flange_dy.get()
            w_flanges = {"Ду50": 2.4, "Ду80": 3.6, "Ду100": 4.7, "Ду150": 6.8, "Ду200": 10.5, "Ду250": 14.8, "Ду300": 19.3, "Ду400": 28.5, "Ду500": 38.2, "Ду600": 54.0, "Ду800": 86.0, "Ду1000": 124.0}
            w_unit = w_flanges.get(f_dy, 6.8) * (rho / 7.85)
            desc_str = f"ГОСТ 33259-2015 ({f_dy})"
        else:
            try:
                D = float(self.det_manual_d.get().strip())
                s = float(self.det_manual_s.get().strip())
                angle_val = float(self.det_angle.get())
            except:
                messagebox.showerror("Ошибка", "Проверьте ввод диаметра и стенки отвода!")
                return
            
            # Справочные данные для отводов 90° по ГОСТ 17375 и ГОСТ 30753
            gost_data = {
                "17375": [(57,3.5,0.7), (89,4,2.1), (108,4,3.3), (159,5,8.1), (219,6,17.2), (273,7,33.5), (325,8,51.4), (426,9,98.6), (530,10,173.0)],
                "30753": [(57,3.5,0.5), (89,4,1.4), (108,4,2.1), (159,5,5.3), (219,6,11.4), (273,7,21.6), (325,8,33.1), (426,9,63.8), (530,10,111.0)]
            }
            
            gost_key = "17375" if "17375" in t else "30753" if "30753" in t else None
            base_w_90 = None
            
            if gost_key in gost_data:
                for d, s_ref, w_ref in gost_data[gost_key]:
                    if d == D and s_ref == s:
                        base_w_90 = w_ref
                        break
            
            if base_w_90 is not None:
                w_unit = (base_w_90 / 90.0) * angle_val * (rho / 7.85)
                desc_str = f"Табличный ГОСТ {gost_key}, угол {int(angle_val)}°, ∅{D}х{s}"
            else:
                # Геометрический расчет по Сборнику 30
                if "17375" in t:
                    R_bend = 1.5 * D
                elif "30753" in t:
                    R_bend = 1.0 * D
                elif "51-515" in t:
                    R_bend = 1.375 * D
                else:
                    R_bend = 15000.0
                
                V_metal = ((angle_val / 360.0) * (2.0 * math.pi**2 * R_bend * ((D - s) / 2.0) * s)) / 1000000.0
                if "51-515" in t:
                    V_metal *= 1.06
                w_unit = V_metal * rho
                st_name = "ГОСТ 24950" if "24950" in t else "ТУ 51-515" if "51-515" in t else "Геометрический"
                desc_str = f"{st_name}, угол {int(angle_val)}°, ∅{D}х{s}"
        
        total = w_unit * c
        self.det_output.delete("1.0", "end")
        self.det_output.insert("1.0", f"🔧 ВЕДОМОСТЬ ФАСОННЫХ ЭЛЕМЕНТОВ:\n")
        self.det_output.insert("end", f"• Тип изделия: {t}\n")
        self.det_output.insert("end", f"• Спецификация: {desc_str}\n")
        self.det_output.insert("end", f"• Плотность: {rho:.2f} г/см³\n")
        self.det_output.insert("end", f"• Масса 1 шт: {w_unit:.3f} кг\n")
        self.det_output.insert("end", f"• Количество: {int(c)} шт\n")
        self.det_output.insert("end", "-" * 60 + "\n")
        self.det_output.insert("end", f"▶ ИТОГОВАЯ МАССА: {total:.2f} кг\n")

    # ==================== ВКЛАДКА 4: МЕТИЗЫ ====================
    def init_metiz_tab(self):
        """Инициализация вкладки Метизы"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔩 Метизы")
        
        # Настройка сетки
        for i in range(2):
            tab.grid_rowconfigure(i, weight=1)
            tab.grid_columnconfigure(i, weight=1)
        
        # Болты
        self.create_bolt_section(tab)
        # Гайки
        self.create_nut_section(tab)
        # Шайбы
        self.create_washer_section(tab)
        # Шпильки
        self.create_stud_section(tab)

    def create_bolt_section(self, parent):
        """Создание секции болтов"""
        f = ttk.LabelFrame(parent, text=" БОЛТЫ ")
        f.grid(row=0, column=0, padx=10, pady=8, sticky="nsew")
        f.grid_columnconfigure(0, weight=1)
        
        self.b_gost = ttk.Combobox(f, values=["ГОСТ 7798-70", "ГОСТ R 52644-2006", "ГОСТ 10602-94"], state="readonly")
        self.b_gost.set("ГОСТ 7798-70")
        self.b_gost.grid(row=0, column=0, padx=8, pady=3, sticky="ew")
        
        self.b_mat = ttk.Combobox(f, values=["Сталь", "Нержавейка", "Латунь"], state="readonly")
        self.b_mat.set("Сталь")
        self.b_mat.grid(row=1, column=0, padx=8, pady=3, sticky="ew")
        
        g = ttk.Frame(f)
        g.grid(row=2, column=0, padx=8, pady=5, sticky="ew")
        
        labels = ["n шт", "диаметр", "Длина", "Масса ед.", "Общая масса"]
        for col, lbl in enumerate(labels):
            ttk.Label(g, text=lbl).grid(row=0, column=col, padx=2)
        
        self.b_pcs = tk.Entry(g, width=6, bg="#fff2cc", justify="center")
        self.b_pcs.insert(0, "8")
        self.b_pcs.grid(row=1, column=0, pady=2, padx=2)
        
        self.b_d = ttk.Combobox(g, values=["М10","М12","М16","М20","М24","М30","М36","М42","М48"], width=6, state="readonly")
        self.b_d.set("М16")
        self.b_d.grid(row=1, column=1, pady=2, padx=2)
        
        self.b_l = ttk.Combobox(g, values=[str(x) for x in range(40,161,10)] + [str(x) for x in range(180,301,20)], width=5, state="readonly")
        self.b_l.set("50")
        self.b_l.grid(row=1, column=2, pady=2, padx=2)
        
        self.b_one = tk.Entry(g, width=8, justify="center")
        self.b_one.grid(row=1, column=3, pady=2, padx=2)
        self.b_tot = tk.Entry(g, width=8, justify="center")
        self.b_tot.grid(row=1, column=4, pady=2, padx=2)
        
        # Обратная задача
        g_rev = ttk.Frame(f)
        g_rev.grid(row=3, column=0, padx=8, pady=5, sticky="ew")
        
        ttk.Label(g_rev, text="кг").grid(row=0, column=0, padx=2)
        ttk.Label(g_rev, text="диаметр").grid(row=0, column=1, padx=2)
        ttk.Label(g_rev, text="Длина").grid(row=0, column=2, padx=2)
        ttk.Label(g_rev, text="Кол-во шт.").grid(row=0, column=3, padx=2)
        
        self.b_kg_rev = tk.Entry(g_rev, width=6, bg="#fff2cc", justify="center")
        self.b_kg_rev.insert(0, "1")
        self.b_kg_rev.grid(row=1, column=0, pady=2, padx=2)
        
        self.b_d_rev = ttk.Combobox(g_rev, values=["М10","М12","М16","М20","М24","М30","М36","М42","М48"], width=6, state="readonly")
        self.b_d_rev.set("М16")
        self.b_d_rev.grid(row=1, column=1, pady=2, padx=2)
        
        self.b_l_rev = ttk.Combobox(g_rev, values=[str(x) for x in range(40,161,10)] + [str(x) for x in range(180,301,20)], width=5, state="readonly")
        self.b_l_rev.set("50")
        self.b_l_rev.grid(row=1, column=2, pady=2, padx=2)
        
        self.b_pcs_rev = tk.Entry(g_rev, width=8, justify="center")
        self.b_pcs_rev.grid(row=1, column=3, pady=2, padx=2)

    def create_nut_section(self, parent):
        """Создание секции гаек"""
        f = ttk.LabelFrame(parent, text=" ГАЙКИ ")
        f.grid(row=0, column=1, padx=10, pady=8, sticky="nsew")
        f.grid_columnconfigure(0, weight=1)
        
        self.n_gost = ttk.Combobox(f, values=["ГОСТ 5915-70", "ГОСТ 9064-75", "ГОСТ R 52645-2006"], state="readonly")
        self.n_gost.set("ГОСТ 5915-70")
        self.n_gost.grid(row=0, column=0, padx=8, pady=3, sticky="ew")
        
        self.n_mat = ttk.Combobox(f, values=["Сталь", "Нержавейка"], state="readonly")
        self.n_mat.set("Сталь")
        self.n_mat.grid(row=1, column=0, padx=8, pady=3, sticky="ew")
        
        g = ttk.Frame(f)
        g.grid(row=2, column=0, padx=8, pady=5, sticky="ew")
        
        labels = ["n шт", "диаметр", "Масса ед.", "Общая масса"]
        for col, lbl in enumerate(labels):
            ttk.Label(g, text=lbl).grid(row=0, column=col, padx=2)
        
        self.n_pcs = tk.Entry(g, width=6, bg="#fff2cc", justify="center")
        self.n_pcs.insert(0, "8")
        self.n_pcs.grid(row=1, column=0, pady=2, padx=2)
        
        self.n_d = ttk.Combobox(g, values=["М10","М12","М16","М20","М24","М30","М36","М42","М48"], width=7, state="readonly")
        self.n_d.set("М16")
        self.n_d.grid(row=1, column=1, pady=2, padx=2)
        
        self.n_one = tk.Entry(g, width=8, justify="center")
        self.n_one.grid(row=1, column=2, pady=2, padx=2)
        self.n_tot = tk.Entry(g, width=8, justify="center")
        self.n_tot.grid(row=1, column=3, pady=2, padx=2)
        
        # Обратная задача
        g_rev = ttk.Frame(f)
        g_rev.grid(row=3, column=0, padx=8, pady=5, sticky="ew")
        
        ttk.Label(g_rev, text="кг").grid(row=0, column=0, padx=2)
        ttk.Label(g_rev, text="диаметр").grid(row=0, column=1, padx=2)
        ttk.Label(g_rev, text="Кол-во шт.").grid(row=0, column=2, padx=2)
        
        self.n_kg_rev = tk.Entry(g_rev, width=6, bg="#fff2cc", justify="center")
        self.n_kg_rev.insert(0, "1")
        self.n_kg_rev.grid(row=1, column=0, pady=2, padx=2)
        
        self.n_d_rev = ttk.Combobox(g_rev, values=["М10","М12","М16","М20","М24","М30","М36","М42","М48"], width=7, state="readonly")
        self.n_d_rev.set("М16")
        self.n_d_rev.grid(row=1, column=1, pady=2, padx=2)
        
        self.n_pcs_rev = tk.Entry(g_rev, width=8, justify="center")
        self.n_pcs_rev.grid(row=1, column=2, pady=2, padx=2)

    def create_washer_section(self, parent):
        """Создание секции шайб"""
        f = ttk.LabelFrame(parent, text=" ШАЙБЫ ")
        f.grid(row=1, column=0, padx=10, pady=8, sticky="nsew")
        f.grid_columnconfigure(0, weight=1)
        
        self.w_gost = ttk.Combobox(f, values=["ГОСТ 11371-78", "ГОСТ 9065-75", "ГОСТ 6402-70"], state="readonly")
        self.w_gost.set("ГОСТ 11371-78")
        self.w_gost.grid(row=0, column=0, padx=8, pady=3, sticky="ew")
        
        self.w_mat = ttk.Combobox(f, values=["Сталь", "Нержавейка"], state="readonly")
        self.w_mat.set("Сталь")
        self.w_mat.grid(row=1, column=0, padx=8, pady=3, sticky="ew")
        
        g = ttk.Frame(f)
        g.grid(row=2, column=0, padx=8, pady=5, sticky="ew")
        
        labels = ["n шт", "размер", "Масса ед.", "Общая масса"]
        for col, lbl in enumerate(labels):
            ttk.Label(g, text=lbl).grid(row=0, column=col, padx=2)
        
        self.w_pcs = tk.Entry(g, width=6, bg="#fff2cc", justify="center")
        self.w_pcs.insert(0, "100")
        self.w_pcs.grid(row=1, column=0, pady=2, padx=2)
        
        self.w_size = ttk.Combobox(g, values=["М10","М12","М16","М20","М24","М30","М36","М42","М48"], width=7, state="readonly")
        self.w_size.set("М16")
        self.w_size.grid(row=1, column=1, pady=2, padx=2)
        
        self.w_one = tk.Entry(g, width=8, justify="center")
        self.w_one.grid(row=1, column=2, pady=2, padx=2)
        self.w_tot = tk.Entry(g, width=8, justify="center")
        self.w_tot.grid(row=1, column=3, pady=2, padx=2)
        
        # Обратная задача
        g_rev = ttk.Frame(f)
        g_rev.grid(row=3, column=0, padx=8, pady=5, sticky="ew")
        
        ttk.Label(g_rev, text="кг").grid(row=0, column=0, padx=2)
        ttk.Label(g_rev, text="размер").grid(row=0, column=1, padx=2)
        ttk.Label(g_rev, text="Кол-во шт.").grid(row=0, column=2, padx=2)
        
        self.w_kg_rev = tk.Entry(g_rev, width=6, bg="#fff2cc", justify="center")
        self.w_kg_rev.insert(0, "1")
        self.w_kg_rev.grid(row=1, column=0, pady=2, padx=2)
        
        self.w_size_rev = ttk.Combobox(g_rev, values=["М10","М12","М16","М20","М24","М30","М36","М42","М48"], width=7, state="readonly")
        self.w_size_rev.set("М16")
        self.w_size_rev.grid(row=1, column=1, pady=2, padx=2)
        
        self.w_pcs_rev = tk.Entry(g_rev, width=8, justify="center")
        self.w_pcs_rev.grid(row=1, column=2, pady=2, padx=2)

    def create_stud_section(self, parent):
        """Создание секции шпилек"""
        f = ttk.LabelFrame(parent, text=" ШПИЛЬКИ ")
        f.grid(row=1, column=1, padx=10, pady=8, sticky="nsew")
        f.grid_columnconfigure(0, weight=1)
        
        self.s_gost = ttk.Combobox(f, values=["ГОСТ 9066-75", "ГОСТ 22032-76", "ГОСТ 10619-80"], state="readonly")
        self.s_gost.set("ГОСТ 9066-75")
        self.s_gost.grid(row=0, column=0, padx=8, pady=3, sticky="ew")
        
        self.s_mat = ttk.Combobox(f, values=["Сталь", "Нержавейка"], state="readonly")
        self.s_mat.set("Сталь")
        self.s_mat.grid(row=1, column=0, padx=8, pady=3, sticky="ew")
        
        g = ttk.Frame(f)
        g.grid(row=2, column=0, padx=8, pady=5, sticky="ew")
        
        labels = ["n шт", "dxL", "Масса ед.", "Общая масса"]
        for col, lbl in enumerate(labels):
            ttk.Label(g, text=lbl).grid(row=0, column=col, padx=2)
        
        self.s_pcs = tk.Entry(g, width=6, bg="#fff2cc", justify="center")
        self.s_pcs.insert(0, "100")
        self.s_pcs.grid(row=1, column=0, pady=2, padx=2)
        
        self.s_size = ttk.Combobox(g, values=["М12х60","М16х90","М20x110","М24x130","М30x150","М36x180","М42x220","М48x260"], width=9, state="readonly")
        self.s_size.set("М16х90")
        self.s_size.grid(row=1, column=1, pady=2, padx=2)
        
        self.s_one = tk.Entry(g, width=8, justify="center")
        self.s_one.grid(row=1, column=2, pady=2, padx=2)
        self.s_tot = tk.Entry(g, width=8, justify="center")
        self.s_tot.grid(row=1, column=3, pady=2, padx=2)
        
        # Обратная задача
        g_rev = ttk.Frame(f)
        g_rev.grid(row=3, column=0, padx=8, pady=5, sticky="ew")
        
        ttk.Label(g_rev, text="кг").grid(row=0, column=0, padx=2)
        ttk.Label(g_rev, text="dxL").grid(row=0, column=1, padx=2)
        ttk.Label(g_rev, text="Кол-во шт.").grid(row=0, column=2, padx=2)
        
        self.s_kg_rev = tk.Entry(g_rev, width=6, bg="#fff2cc", justify="center")
        self.s_kg_rev.insert(0, "1")
        self.s_kg_rev.grid(row=1, column=0, pady=2, padx=2)
        
        self.s_size_rev = ttk.Combobox(g_rev, values=["М12х60","М16х90","М20x110","М24x130","М30x150","М36x180","М42x220","М48x260"], width=9, state="readonly")
        self.s_size_rev.set("М16х90")
        self.s_size_rev.grid(row=1, column=1, pady=2, padx=2)
        
        self.s_pcs_rev = tk.Entry(g_rev, width=8, justify="center")
        self.s_pcs_rev.grid(row=1, column=2, pady=2, padx=2)
        
        # Привязка событий для автоматического расчета
        self.bind_metiz_events()

    def bind_metiz_events(self):
        """Привязка событий для автоматического расчета метизов"""
        widgets = [
            self.b_pcs, self.b_kg_rev, self.n_pcs, self.n_kg_rev,
            self.w_pcs, self.w_kg_rev, self.s_pcs, self.s_kg_rev
        ]
        for w in widgets:
            w.bind("<KeyRelease>", lambda e: self.calc_all_metiz())
        
        combos = [
            self.b_d, self.b_l, self.b_d_rev, self.b_l_rev, self.b_gost, self.b_mat,
            self.n_d, self.n_d_rev, self.n_gost, self.n_mat,
            self.w_size, self.w_size_rev, self.w_gost, self.w_mat,
            self.s_size, self.s_size_rev, self.s_gost, self.s_mat
        ]
        for c in combos:
            c.bind("<<ComboboxSelected>>", lambda e: self.calc_all_metiz())
        
        self.calc_all_metiz()

    def calc_all_metiz(self):
        """Расчет всех метизов"""
        rho_coeff = self.get_density() / 7.85
        
        # Данные для расчетов
        bolt_data = {"М10":0.068,"М12":0.102,"М16":0.198,"М20":0.342,"М24":0.564,"М30":0.985,"М36":1.540,"М42":2.280,"М48":3.120}
        nut_data = {"М10":0.011,"М12":0.015,"М16":0.033,"М20":0.064,"М24":0.110,"М30":0.230,"М36":0.390,"М42":0.620,"М48":0.960}
        washer_data = {"М10":0.004,"М12":0.006,"М16":0.011,"М20":0.017,"М24":0.032,"М30":0.054,"М36":0.092,"М42":0.182,"М48":0.274}
        stud_data = {"М12":0.080,"М16":0.142,"М20":0.246,"М24":0.395,"М30":0.670,"М36":1.020,"М42":1.480,"М48":2.050}
        
        # 1. Болты
        try:
            bd = self.b_d.get()
            bl = float(self.b_l.get())
            w_base = bolt_data.get(bd, 0.198) * (bl / 90.0)
            if "52644" in self.b_gost.get():
                w_base *= 1.15
            w_one = w_base * rho_coeff
            self.update_entry(self.b_one, f"{w_one:.3f}")
            
            bp = float(self.b_pcs.get())
            self.update_entry(self.b_tot, f"{bp * w_one:.2f}")
            
            kg = float(self.b_kg_rev.get())
            bd_r = self.b_d_rev.get()
            bl_r = float(self.b_l_rev.get())
            w_base_r = bolt_data.get(bd_r, 0.198) * (bl_r / 90.0)
            if "52644" in self.b_gost.get():
                w_base_r *= 1.15
            pcs = int(kg / (w_base_r * rho_coeff)) if w_base_r * rho_coeff > 0 else 0
            self.update_entry(self.b_pcs_rev, str(pcs))
        except:
            pass
        
        # 2. Гайки
        try:
            nd = self.n_d.get()
            w_base = nut_data.get(nd, 0.033)
            if "9064" in self.n_gost.get():
                w_base *= 1.25
            w_one = w_base * rho_coeff
            self.update_entry(self.n_one, f"{w_one:.4f}")
            
            np = float(self.n_pcs.get())
            self.update_entry(self.n_tot, f"{np * w_one:.2f}")
            
            kg = float(self.n_kg_rev.get())
            nd_r = self.n_d_rev.get()
            w_base_r = nut_data.get(nd_r, 0.033)
            if "9064" in self.n_gost.get():
                w_base_r *= 1.25
            pcs = int(kg / (w_base_r * rho_coeff)) if w_base_r * rho_coeff > 0 else 0
            self.update_entry(self.n_pcs_rev, str(pcs))
        except:
            pass
        
        # 3. Шайбы
        try:
            ws = self.w_size.get()
            w_base = washer_data.get(ws, 0.011)
            if "9065" in self.w_gost.get():
                w_base *= 1.4
            elif "6402" in self.w_gost.get():
                w_base *= 0.7
            w_one = w_base * rho_coeff
            self.update_entry(self.w_one, f"{w_one:.5f}")
            
            wp = float(self.w_pcs.get())
            self.update_entry(self.w_tot, f"{wp * w_one:.2f}")
            
            kg = float(self.w_kg_rev.get())
            ws_r = self.w_size_rev.get()
            w_base_r = washer_data.get(ws_r, 0.011)
            if "9065" in self.w_gost.get():
                w_base_r *= 1.4
            elif "6402" in self.w_gost.get():
                w_base_r *= 0.7
            pcs = int(kg / (w_base_r * rho_coeff)) if w_base_r * rho_coeff > 0 else 0
            self.update_entry(self.w_pcs_rev, str(pcs))
        except:
            pass
        
        # 4. Шпильки
        try:
            ss = self.s_size.get()
            if "М" in ss:
                parts = ss.replace("М", "").split("х")
                sd = "М" + parts[0]
                sl = float(parts[1]) if len(parts) > 1 else 90.0
                w_base = stud_data.get(sd, 0.142) * (sl / 90.0)
            else:
                w_base = 0.00049
            w_one = w_base * rho_coeff
            self.update_entry(self.s_one, f"{w_one:.5f}")
            
            sp = float(self.s_pcs.get())
            self.update_entry(self.s_tot, f"{sp * w_one:.2f}")
            
            kg = float(self.s_kg_rev.get())
            ss_r = self.s_size_rev.get()
            if "М" in ss_r:
                parts_r = ss_r.replace("М", "").split("х")
                sdr = "М" + parts_r[0]
                srl = float(parts_r[1]) if len(parts_r) > 1 else 90.0
                w_base_r = stud_data.get(sdr, 0.142) * (srl / 90.0)
            else:
                w_base_r = 0.00049
            pcs = int(kg / (w_base_r * rho_coeff)) if w_base_r * rho_coeff > 0 else 0
            self.update_entry(self.s_pcs_rev, str(pcs))
        except:
            pass

    def update_entry(self, entry, value):
        """Обновление значения в поле ввода"""
        entry.config(state="normal")
        entry.delete(0, "end")
        entry.insert(0, value)
        entry.config(state="readonly")

    # ==================== ВКЛАДКА 5: СВАРКА (ПЕРЕРАБОТАНА ПО СБОРНИКУ 30) ====================
    def init_welding_tab(self):
        """Инициализация вкладки Сварка по Сборнику 30"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="⚡ Сварка")
        
        # Основной контейнер
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Верхняя панель - выбор типа соединения
        top_frame = ttk.LabelFrame(main_frame, text=" Параметры сварного соединения ")
        top_frame.pack(fill="x", pady=5)
        
        # Строка 1: Раздел и тип соединения
        row1 = ttk.Frame(top_frame)
        row1.pack(fill="x", pady=3)
        
        ttk.Label(row1, text="Раздел:").pack(side="left", padx=5)
        self.weld_section = ttk.Combobox(row1, values=[
            "Раздел I. Сварка листовых и решетчатых конструкций",
            "Раздел II. Сварка трубопроводов",
            "Раздел III. Сварка арматуры и закладных деталей",
            "Раздел IV. Газовая резка"
        ], state="readonly", width=40)
        self.weld_section.set("Раздел I. Сварка листовых и решетчатых конструкций")
        self.weld_section.pack(side="left", padx=5)
        self.weld_section.bind("<<ComboboxSelected>>", self.on_weld_section_change)
        
        ttk.Label(row1, text="Тип соединения:").pack(side="left", padx=5)
        self.weld_joint_type = ttk.Combobox(row1, values=[], state="readonly", width=15)
        self.weld_joint_type.pack(side="left", padx=5)
        self.weld_joint_type.bind("<<ComboboxSelected>>", self.on_weld_joint_change)
        
        # Строка 2: Материал и положение шва
        row2 = ttk.Frame(top_frame)
        row2.pack(fill="x", pady=3)
        
        ttk.Label(row2, text="Материал:").pack(side="left", padx=5)
        self.weld_material = ttk.Combobox(row2, values=["Сталь", "Нержавеющая сталь", "Алюминий", "Медь"], state="readonly", width=18)
        self.weld_material.set("Сталь")
        self.weld_material.pack(side="left", padx=5)
        
        ttk.Label(row2, text="Положение шва:").pack(side="left", padx=5)
        self.weld_position = ttk.Combobox(row2, values=["Нижнее", "Вертикальное", "Горизонтальное", "Потолочное"], state="readonly", width=15)
        self.weld_position.set("Нижнее")
        self.weld_position.pack(side="left", padx=5)
        
        ttk.Label(row2, text="Метод сварки:").pack(side="left", padx=5)
        self.weld_method = ttk.Combobox(row2, values=[
            "Ручная дуговая (электроды)",
            "Механизированная в CO2",
            "Автоматическая под флюсом",
            "Газовая",
            "Аргонодуговая",
            "Комбинированная"
        ], state="readonly", width=25)
        self.weld_method.set("Ручная дуговая (электроды)")
        self.weld_method.pack(side="left", padx=5)
        self.weld_method.bind("<<ComboboxSelected>>", self.on_weld_method_change)
        
        # Строка 3: Марка электрода и диаметр
        row3 = ttk.Frame(top_frame)
        row3.pack(fill="x", pady=3)
        
        ttk.Label(row3, text="Марка электрода:").pack(side="left", padx=5)
        self.weld_electrode = ttk.Combobox(row3, values=[], state="readonly", width=18)
        self.weld_electrode.pack(side="left", padx=5)
        self.weld_electrode.bind("<<ComboboxSelected>>", self.update_electrode_info)
        
        ttk.Label(row3, text="Диаметр электрода, мм:").pack(side="left", padx=5)
        self.weld_diameter = ttk.Combobox(row3, values=["2.0", "2.5", "3.0", "4.0", "5.0", "6.0"], width=6, state="readonly")
        self.weld_diameter.set("3.0")
        self.weld_diameter.pack(side="left", padx=5)
        
        # Информация о группе электрода
        self.electrode_group_label = ttk.Label(row3, text="Группа: I, K=1.4", foreground="#2980b9")
        self.electrode_group_label.pack(side="left", padx=15)
        
        # Строка 4: Параметры соединения (динамические)
        self.params_frame = ttk.LabelFrame(top_frame, text=" Параметры соединения ")
        self.params_frame.pack(fill="x", pady=5, padx=5)
        self.weld_params = {}
        
        # Кнопка расчета
        btn_frame = ttk.Frame(top_frame)
        btn_frame.pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="Рассчитать по нормам Сборника 30", command=self.calc_weld_by_sbornik).pack(side="right", padx=5)
        
        # Панель результатов
        result_frame = ttk.LabelFrame(main_frame, text=" Результаты расчета по Сборнику 30 ")
        result_frame.pack(fill="both", expand=True, pady=5)
        
        # Таблица результатов
        self.result_tree = ttk.Treeview(result_frame, columns=("param", "value", "unit"), show="headings", height=8)
        self.result_tree.heading("param", text="Параметр")
        self.result_tree.heading("value", text="Значение")
        self.result_tree.heading("unit", text="Ед. изм.")
        self.result_tree.column("param", width=250)
        self.result_tree.column("value", width=150)
        self.result_tree.column("unit", width=100)
        self.result_tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Подробный вывод
        self.result_text = tk.Text(result_frame, bg="#f8f9fa", font=("Consolas", 10), height=6, bd=1, relief="solid")
        self.result_text.pack(fill="x", padx=5, pady=5)
        
        # Инициализация
        self.update_weld_joint_types()
        self.update_electrode_list()
        self.build_weld_params()

    def on_weld_section_change(self, event=None):
        """Обработка смены раздела сварки"""
        self.update_weld_joint_types()
        self.build_weld_params()

    def update_weld_joint_types(self):
        """Обновление списка типов соединений в зависимости от раздела"""
        section = self.weld_section.get()
        joints = {
            "Раздел I. Сварка листовых и решетчатых конструкций": [
                "C1 (Стыковое с отбортовкой)", "C2 (Стыковое без скоса)", 
                "C7 (Стыковое без скоса двустороннее)", "C8 (Стыковое со скосом одной кромки)",
                "C15 (Стыковое с двумя скосами)", "C17 (Стыковое со скосом двух кромок)",
                "C25 (Стыковое с двумя скосами двустороннее)",
                "У1 (Угловое с отбортовкой)", "У4 (Угловое без скоса)", 
                "У6 (Угловое со скосом)", "У8 (Угловое с двумя скосами)",
                "У9 (Угловое со скосом двух кромок)",
                "Т1 (Тавровое без скоса)", "Т3 (Тавровое без скоса двустороннее)",
                "Т6 (Тавровое со скосом)", "Т8 (Тавровое с двумя скосами)",
                "Н1 (Нахлёсточное)", "Н2 (Нахлёсточное двустороннее)"
            ],
            "Раздел II. Сварка трубопроводов": [
                "С2 (Стыковое без скоса)",
                "С8 (Стыковое со скосом одной кромки)",
                "С17 (Стыковое со скосом двух кромок)",
                "С18 (Стыковое на съемной подкладке)",
                "С5 (Стыковое на остающейся подкладке)",
                "С10 (Стыковое горизонтальное на подкладке)",
                "С19 (Стыковое на остающейся подкладке)",
                "С52 (Стыковое криволинейное)",
                "С53 (Стыковое криволинейное)",
                "У18 (Вварка патрубков без скоса)",
                "У19 (Вварка патрубков со скосом)",
                "У5 (Приварка фланцев У5)",
                "У7 (Приварка фланцев У7)",
                "У8 (Приварка фланцев У8)"
            ],
            "Раздел III. Сварка арматуры и закладных деталей": [
                "Тип 2 (Крестообразное точечное)",
                "Тип 3 (Крестообразное с формированием)",
                "Тип 5 (Стыковое в формах)",
                "Тип 6 (Стыковое со скосом)",
                "Тип 7 (Стыковое вертикальное)",
                "Тип 9 (На скобе-подкладке)",
                "Тип 10 (На скобе-накладке)",
                "Тип 11 (Вертикальное с разделкой)",
                "Тип 12 (Нахлёсточное)",
                "Тип 13 (Нахлёсточное)",
                "Тип 14 (Нахлёсточное)",
                "Тип 18 (Тавровое)",
                "Тип 20 (Тавровое)",
                "Тип 21 (Тавровое)"
            ],
            "Раздел IV. Газовая резка": [
                "Резка листовой стали",
                "Резка угловой стали",
                "Резка двутавров",
                "Резка швеллеров",
                "Резка квадрата",
                "Резка круга",
                "Резка рельсов",
                "Резка труб",
                "Вырезка отверстий"
            ]
        }
        self.weld_joint_type['values'] = joints.get(section, [])
        if joints.get(section):
            self.weld_joint_type.set(joints[section][0])

    def update_electrode_list(self):
        """Обновление списка электродов в зависимости от раздела"""
        method = self.weld_method.get()
        section = self.weld_section.get()
        
        if "Ручная дуговая" in method:
            electrodes = ["УОНИ-13/45", "УОНИ-13/55", "АНО-4", "МР-3", "ОЗС-4", "ОЗС-6", 
                         "ТМУ-21У", "ОЗС-12", "УОНИ-13/85", "ЦЛ-6", "ЦУ-2М", "ОЗЛ-6", "ОЗЛ-8"]
        elif "CO2" in method or "Механизированная" in method:
            electrodes = ["Св-08Г2С", "Св-08ГС", "Св-10Г2", "ПП-АН8", "ПП-АН9"]
        elif "под флюсом" in method:
            electrodes = ["Св-08А", "Св-10ГА", "Св-10Г2", "Св-08ГА"]
        elif "Газовая" in method:
            electrodes = ["Св-08", "Св-08А", "Св-10Г2"]
        elif "Аргонодуговая" in method:
            electrodes = ["Св-04Х19Н9", "Св-08Х19Н10Б", "Св-10Х17Н13М2Т", "Св-10Х25Н13"]
        elif "Комбинированная" in method:
            electrodes = ["УОНИ-13/45 + Св-08Г2С", "УОНИ-13/55 + Св-08Г2С"]
        else:
            electrodes = []
        
        self.weld_electrode['values'] = electrodes
        if electrodes:
            self.weld_electrode.set(electrodes[0])
            self.update_electrode_info()

    def update_electrode_info(self, event=None):
        """Обновление информации о группе электрода"""
        mark = self.weld_electrode.get()
        if mark:
            group, coeff = self.get_electrode_group(mark)
            group_names = {1: "I", 2: "II", 3: "III", 4: "IV"}
            self.electrode_group_label.config(text=f"Группа: {group_names.get(group, 'III')}, K={coeff}")

    def on_weld_method_change(self, event=None):
        """Обработка смены метода сварки"""
        self.update_electrode_list()
        self.build_weld_params()

    def on_weld_joint_change(self, event=None):
        """Обработка смены типа соединения"""
        self.build_weld_params()

    def build_weld_params(self):
        """Построение полей параметров для текущего соединения"""
        for w in self.params_frame.winfo_children():
            w.destroy()
        self.weld_params.clear()
        
        joint = self.weld_joint_type.get()
        section = self.weld_section.get()
        method = self.weld_method.get()
        
        params = []
        
        if "Раздел I" in section:
            if "C" in joint or "С" in joint:
                params = [
                    ("Толщина деталей S, мм", "4"),
                    ("Длина шва L, м", "1.0"),
                    ("Количество швов n", "1")
                ]
                if "C8" in joint or "C15" in joint or "C17" in joint or "C25" in joint:
                    params.append(("Угол скоса α°, град", "50"))
            elif "У" in joint:
                params = [
                    ("Катет шва K, мм", "4"),
                    ("Длина шва L, м", "1.0"),
                    ("Количество швов n", "1")
                ]
            elif "Т" in joint:
                params = [
                    ("Катет шва K, мм", "4"),
                    ("Длина шва L, м", "1.0"),
                    ("Количество швов n", "1")
                ]
            elif "Н" in joint:
                params = [
                    ("Катет шва K, мм", "4"),
                    ("Длина шва L, м", "1.0"),
                    ("Количество швов n", "1")
                ]
        elif "Раздел II" in section:
            if "С2" in joint or "С8" in joint:
                params = [
                    ("Толщина стенки S, мм", "4"),
                    ("Диаметр трубы D, мм", "57"),
                    ("Количество стыков", "1")
                ]
            else:
                params = [
                    ("Толщина стенки S, мм", "4"),
                    ("Диаметр трубы D, мм", "57"),
                    ("Количество стыков", "1")
                ]
            if "фланец" in joint.lower():
                params.append(("Толщина фланца S1, мм", "4"))
        elif "Раздел III" in section:
            params = [
                ("Диаметр стержня d, мм", "20"),
                ("Количество соединений", "1")
            ]
            if "крестообразное" in joint.lower():
                params.append(("Расстояние между стержнями", "100"))
        elif "Раздел IV" in section:
            params = [
                ("Толщина металла S, мм", "10"),
                ("Длина реза L, м", "1.0")
            ]
            if "труб" in joint.lower() or "отверстий" in joint.lower():
                params.append(("Диаметр трубы D, мм", "57"))
        
        # Добавление параметров в интерфейс
        for row, (lbl, val) in enumerate(params):
            ttk.Label(self.params_frame, text=lbl).grid(row=row, column=0, padx=5, pady=3, sticky="w")
            e = ttk.Entry(self.params_frame, width=10, justify="center")
            e.insert(0, val)
            e.grid(row=row, column=1, padx=5, pady=3)
            self.weld_params[lbl] = e

    def calc_weld_by_sbornik(self):
        """Расчет по нормам Сборника 30"""
        try:
            section = self.weld_section.get()
            joint = self.weld_joint_type.get()
            method = self.weld_method.get()
            rho = self.get_density()
            
            # Получение группы электрода
            mark = self.weld_electrode.get()
            group, k_el = self.get_electrode_group(mark)
            
            # Поправочные коэффициенты для положения шва (из Сборника 30)
            pos = self.weld_position.get()
            pos_coeff = {"Нижнее": 1.0, "Вертикальное": 1.12, "Горизонтальное": 1.13, "Потолочное": 1.26}
            k_pos = pos_coeff.get(pos, 1.0)
            
            # Справочные данные по нормам расхода электродов (Сборник 30, Таблицы 002-016)
            # Нормы на 1 м шва для ручной дуговой сварки (группы электродов I-IV)
            norms = {
                "C2": {  # Таблица 002
                    1: {"I": 0.052, "II": 0.056, "III": 0.059, "IV": 0.063},
                    2: {"I": 0.108, "II": 0.115, "III": 0.123, "IV": 0.131},
                    3: {"I": 0.119, "II": 0.127, "III": 0.136, "IV": 0.144},
                    4: {"I": 0.229, "II": 0.246, "III": 0.262, "IV": 0.278}
                },
                "C17": {  # Таблица 006
                    3: {"I": 0.155, "II": 0.166, "III": 0.177, "IV": 0.188},
                    4: {"I": 0.196, "II": 0.210, "III": 0.224, "IV": 0.238},
                    5: {"I": 0.246, "II": 0.264, "III": 0.282, "IV": 0.299},
                    6: {"I": 0.340, "II": 0.364, "III": 0.389, "IV": 0.413},
                    8: {"I": 0.494, "II": 0.529, "III": 0.565, "IV": 0.600},
                    10: {"I": 0.721, "II": 0.772, "III": 0.824, "IV": 0.875},
                    12: {"I": 0.981, "II": 1.051, "III": 1.121, "IV": 1.191}
                },
                "У4": {  # Таблица 009
                    4: {"I": 0.259, "II": 0.278, "III": 0.296, "IV": 0.315},
                    5: {"I": 0.361, "II": 0.387, "III": 0.413, "IV": 0.439},
                    6: {"I": 0.532, "II": 0.570, "III": 0.608, "IV": 0.646},
                    8: {"I": 0.828, "II": 0.886, "III": 0.946, "IV": 1.005},
                    10: {"I": 1.186, "II": 1.271, "III": 1.356, "IV": 1.441}
                },
                "Т1": {  # Таблица 013
                    3: {"I": 0.084, "II": 0.090, "III": 0.096, "IV": 0.102},
                    4: {"I": 0.133, "II": 0.143, "III": 0.152, "IV": 0.161},
                    6: {"I": 0.266, "II": 0.285, "III": 0.304, "IV": 0.328},
                    8: {"I": 0.441, "II": 0.472, "III": 0.504, "IV": 0.536},
                    10: {"I": 0.661, "II": 0.707, "III": 0.755, "IV": 0.802}
                }
            }
            
            # Определение параметров
            if "C2" in joint or "С2" in joint:
                S = float(self.weld_params.get("Толщина деталей S, мм", ttk.Entry()).get())
                L = float(self.weld_params.get("Длина шва L, м", ttk.Entry()).get() or 1.0)
                n = float(self.weld_params.get("Количество швов n", ttk.Entry()).get() or 1)
                
                # Поиск нормы для заданной толщины
                norm_data = norms.get("C2", {})
                s_key = min(norm_data.keys(), key=lambda x: abs(x - S))
                if s_key in norm_data:
                    norm = norm_data[s_key].get(["I","II","III","IV"][group-1], 0.1)
                else:
                    norm = 0.1
                
                # Расчет
                norm *= k_pos * k_el / 1.6  # Корректировка на группу электрода
                total = norm * L * n
                
                self.display_results(joint, {
                    "Норма расхода на 1 м шва": f"{norm:.4f}",
                    "Длина шва": f"{L}",
                    "Количество швов": f"{int(n)}",
                    "Общий расход электродов": f"{total:.4f}",
                    "Группа электродов": f"{['I','II','III','IV'][group-1]} (K={k_el})",
                    "Коэффициент положения": f"{k_pos}"
                }, "кг")
                
                self.result_text.delete("1.0", tk.END)
                self.result_text.insert("1.0", 
                    f"Расчет по Сборнику 30 (Таблица 002)\n"
                    f"Соединение: {joint}\n"
                    f"Толщина: {S} мм, Длина шва: {L} м\n"
                    f"Электрод: {mark}, Группа {['I','II','III','IV'][group-1]}\n"
                    f"ИТОГО: {total:.4f} кг электродов\n"
                )
                
            elif "C17" in joint or "С17" in joint:
                S = float(self.weld_params.get("Толщина деталей S, мм", ttk.Entry()).get())
                L = float(self.weld_params.get("Длина шва L, м", ttk.Entry()).get() or 1.0)
                n = float(self.weld_params.get("Количество швов n", ttk.Entry()).get() or 1)
                
                norm_data = norms.get("C17", {})
                s_key = min(norm_data.keys(), key=lambda x: abs(x - S))
                if s_key in norm_data:
                    norm = norm_data[s_key].get(["I","II","III","IV"][group-1], 0.2)
                else:
                    # Экстраполяция
                    base_norm = 0.2 * (S / 6) ** 0.8
                    norm = base_norm
                
                norm *= k_pos * k_el / 1.6
                total = norm * L * n
                
                self.display_results(joint, {
                    "Норма расхода на 1 м шва": f"{norm:.4f}",
                    "Длина шва": f"{L}",
                    "Количество швов": f"{int(n)}",
                    "Общий расход электродов": f"{total:.4f}",
                    "Группа электродов": f"{['I','II','III','IV'][group-1]} (K={k_el})",
                    "Коэффициент положения": f"{k_pos}"
                }, "кг")
                
                self.result_text.delete("1.0", tk.END)
                self.result_text.insert("1.0", 
                    f"Расчет по Сборнику 30 (Таблица 006)\n"
                    f"Соединение: {joint}\n"
                    f"Толщина: {S} мм, Длина шва: {L} м\n"
                    f"Электрод: {mark}, Группа {['I','II','III','IV'][group-1]}\n"
                    f"ИТОГО: {total:.4f} кг электродов\n"
                )
                
            elif "У4" in joint:
                K = float(self.weld_params.get("Катет шва K, мм", ttk.Entry()).get())
                L = float(self.weld_params.get("Длина шва L, м", ttk.Entry()).get() or 1.0)
                n = float(self.weld_params.get("Количество швов n", ttk.Entry()).get() or 1)
                
                norm_data = norms.get("У4", {})
                k_key = min(norm_data.keys(), key=lambda x: abs(x - K))
                if k_key in norm_data:
                    norm = norm_data[k_key].get(["I","II","III","IV"][group-1], 0.3)
                else:
                    norm = 0.3 * (K / 6) ** 1.2
                
                norm *= k_pos * k_el / 1.6
                total = norm * L * n
                
                self.display_results(joint, {
                    "Норма расхода на 1 м шва": f"{norm:.4f}",
                    "Длина шва": f"{L}",
                    "Количество швов": f"{int(n)}",
                    "Общий расход электродов": f"{total:.4f}",
                    "Группа электродов": f"{['I','II','III','IV'][group-1]} (K={k_el})",
                    "Коэффициент положения": f"{k_pos}"
                }, "кг")
                
            elif "Т1" in joint:
                K = float(self.weld_params.get("Катет шва K, мм", ttk.Entry()).get())
                L = float(self.weld_params.get("Длина шва L, м", ttk.Entry()).get() or 1.0)
                n = float(self.weld_params.get("Количество швов n", ttk.Entry()).get() or 1)
                
                norm_data = norms.get("Т1", {})
                k_key = min(norm_data.keys(), key=lambda x: abs(x - K))
                if k_key in norm_data:
                    norm = norm_data[k_key].get(["I","II","III","IV"][group-1], 0.2)
                else:
                    norm = 0.2 * (K / 6) ** 1.3
                
                norm *= k_pos * k_el / 1.6
                total = norm * L * n
                
                self.display_results(joint, {
                    "Норма расхода на 1 м шва": f"{norm:.4f}",
                    "Длина шва": f"{L}",
                    "Количество швов": f"{int(n)}",
                    "Общий расход электродов": f"{total:.4f}",
                    "Группа электродов": f"{['I','II','III','IV'][group-1]} (K={k_el})",
                    "Коэффициент положения": f"{k_pos}"
                }, "кг")
                
            elif "Раздел II" in section:
                # Сварка трубопроводов
                S = float(self.weld_params.get("Толщина стенки S, мм", ttk.Entry()).get())
                D = float(self.weld_params.get("Диаметр трубы D, мм", ttk.Entry()).get())
                n = float(self.weld_params.get("Количество стыков", ttk.Entry()).get() or 1)
                
                # Расчет длины шва для трубы
                L_shv = math.pi * (D - S) / 1000  # в метрах
                
                # Базовая норма для труб (ориентировочно по Сборнику 30)
                base_norm = 0.15 * (S / 4) ** 0.7
                norm = base_norm * k_pos * k_el / 1.6
                total = norm * L_shv * n
                
                self.display_results(joint, {
                    "Норма на 1 м шва": f"{norm:.4f}",
                    "Длина шва на стык": f"{L_shv:.3f}",
                    "Количество стыков": f"{int(n)}",
                    "Общий расход": f"{total:.4f}",
                    "Группа электродов": f"{['I','II','III','IV'][group-1]} (K={k_el})",
                    "Коэффициент положения": f"{k_pos}"
                }, "кг")
                
                self.result_text.delete("1.0", tk.END)
                self.result_text.insert("1.0", 
                    f"Расчет по Сборнику 30 (Раздел II)\n"
                    f"Соединение: {joint}\n"
                    f"Труба ∅{D}х{S} мм, Длина шва: {L_shv:.3f} м\n"
                    f"Электрод: {mark}, Группа {['I','II','III','IV'][group-1]}\n"
                    f"ИТОГО: {total:.4f} кг электродов\n"
                )
                
            elif "Раздел III" in section:
                # Сварка арматуры
                d = float(self.weld_params.get("Диаметр стержня d, мм", ttk.Entry()).get())
                n = float(self.weld_params.get("Количество соединений", ttk.Entry()).get() or 1)
                
                # Ориентировочные нормы для арматуры
                if d <= 10:
                    norm_one = 0.005
                elif d <= 16:
                    norm_one = 0.01
                elif d <= 22:
                    norm_one = 0.02
                elif d <= 28:
                    norm_one = 0.035
                elif d <= 36:
                    norm_one = 0.06
                else:
                    norm_one = 0.1
                
                norm_one *= k_el / 1.6
                total = norm_one * n
                
                self.display_results(joint, {
                    "Норма на 1 соединение": f"{norm_one:.4f}",
                    "Количество соединений": f"{int(n)}",
                    "Общий расход": f"{total:.4f}",
                    "Группа электродов": f"{['I','II','III','IV'][group-1]} (K={k_el})"
                }, "кг")
                
                self.result_text.delete("1.0", tk.END)
                self.result_text.insert("1.0", 
                    f"Расчет по Сборнику 30 (Раздел III)\n"
                    f"Соединение: {joint}\n"
                    f"Диаметр стержня: {d} мм\n"
                    f"ИТОГО: {total:.4f} кг электродов\n"
                )
                
            elif "Раздел IV" in section:
                # Газовая резка
                S = float(self.weld_params.get("Толщина металла S, мм", ttk.Entry()).get())
                L = float(self.weld_params.get("Длина реза L, м", ttk.Entry()).get() or 1.0)
                
                # Ориентировочные нормы расхода газов (Сборник 30, Таблица 094)
                if S <= 5:
                    oxygen = 59.4 * L
                    acetylene = 12.5 * L
                elif S <= 10:
                    oxygen = 90.0 * L
                    acetylene = 18.3 * L
                elif S <= 20:
                    oxygen = 180.0 * L
                    acetylene = 33.6 * L
                else:
                    oxygen = 300.0 * L
                    acetylene = 50.0 * L
                
                self.display_results(joint, {
                    "Расход кислорода": f"{oxygen:.2f}",
                    "Расход ацетилена": f"{acetylene:.2f}",
                    "Длина реза": f"{L}",
                    "Толщина металла": f"{S}"
                }, "л")
                
                self.result_text.delete("1.0", tk.END)
                self.result_text.insert("1.0", 
                    f"Расчет по Сборнику 30 (Раздел IV)\n"
                    f"Резка: {joint}\n"
                    f"Толщина: {S} мм, Длина: {L} м\n"
                    f"Кислород: {oxygen:.2f} л, Ацетилен: {acetylene:.2f} л\n"
                )
            else:
                messagebox.showinfo("Информация", "Для данного типа соединения расчет выполняется по общим формулам")
                self.result_text.delete("1.0", tk.END)
                self.result_text.insert("1.0", "Для данного соединения используйте ручной расчет по Сборнику 30")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при расчете: {str(e)}")
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert("1.0", f"Ошибка: {str(e)}")

    def display_results(self, joint, params, unit):
        """Отображение результатов в таблице"""
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        
        for param, value in params.items():
            self.result_tree.insert("", "end", values=(param, value, unit))

    # ==================== ВКЛАДКА 6: СПРАВОЧНИК ЭЛЕКТРОДОВ ====================
    def init_electrodes_tab(self):
        """Инициализация вкладки Справочник электродов"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📖 Справочник электродов")
        
        ttk.Label(tab, text="Выбор марки электрода в зависимости от свариваемого материала", font=("Segoe UI", 11, "bold")).pack(pady=8, anchor="w", padx=15)
        
        top_frame = ttk.LabelFrame(tab, text=" Категория сталей/сплавов ")
        top_frame.pack(fill="x", padx=15, pady=5)
        
        self.el_cat_list = tk.Listbox(top_frame, height=5, font=("Segoe UI", 10))
        self.el_cat_list.pack(fill="x", padx=10, pady=5)
        categories = [
            "Углеродистые и низколегированные стали",
            "Легированные конструкционные стали",
            "Теплоустойчивые стали",
            "Нержавеющие и жаропрочные стали",
            "Чугун, цветные металлы"
        ]
        for cat in categories:
            self.el_cat_list.insert("end", cat)
        
        bottom_frame = ttk.Frame(tab)
        bottom_frame.pack(fill="both", expand=True, padx=15, pady=5)
        
        left_frame = ttk.LabelFrame(bottom_frame, text=" Марки электродов ")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0,5), pady=5)
        
        self.el_mark_list = tk.Listbox(left_frame, font=("Consolas", 10, "bold"))
        self.el_mark_list.pack(fill="both", expand=True, padx=5, pady=5)
        
        right_frame = ttk.Frame(bottom_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5,0), pady=5)
        
        all_frame = ttk.LabelFrame(right_frame, text=" Все марки в группе ")
        all_frame.pack(fill="x", pady=5)
        self.el_all_text = tk.Text(all_frame, bg="#ffffff", foreground="#000000", height=2, font=("Consolas", 10))
        self.el_all_text.pack(fill="x", padx=5, pady=5)
        
        desc_frame = ttk.LabelFrame(right_frame, text=" Описание ")
        desc_frame.pack(fill="both", expand=True, pady=5)
        self.el_desc_text = tk.Text(desc_frame, bg="#f8f9fa", foreground="#000000", font=("Segoe UI", 10))
        self.el_desc_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.el_cat_list.bind("<<ListboxSelect>>", self.on_electrode_category_change)
        self.el_cat_list.select_set(0)
        self.on_electrode_category_change(None)

    def on_electrode_category_change(self, event=None):
        """Обновление списка электродов при смене категории"""
        sel = self.el_cat_list.curselection()
        if not sel:
            return
        
        idx = sel[0]
        self.el_mark_list.delete(0, "end")
        
        data = [
            (["ТМУ-21У", "ОЗС-4", "ОЗС-6", "ОЗС-12", "АНО-4", "УОНИ-13/45", "УОНИ-13/55", "МР-3"],
             "ТМУ-21У, ОЗС-4, ОЗС-6, ОЗС-12, АНО-4, УОНИ-13/45, УОНИ-13/55, МР-3",
             "ГОСТ 9467: Типы Э42, Э46, Э50. Для сварки ответственных конструкций."),
            (["АНО-ТМ70", "АНП-1", "УОНИ-13/85", "ЦЛ-18", "ЦЛ-19"],
             "АНО-ТМ70, АНП-1, УОНИ-13/85, ЦЛ-18, ЦЛ-19",
             "Для сварки легированных сталей повышенной прочности."),
            (["ЦЛ-6", "ЦУ-2М", "ТМЛ-1", "ТМЛ-3У", "ЦЛ-39", "ЦЛ-17", "ЦЛ-21", "ЦЛ-57"],
             "ЦЛ-6, ЦУ-2М, ТМЛ-1, ТМЛ-3У, ЦЛ-39, ЦЛ-17, ЦЛ-21, ЦЛ-57",
             "ГОСТ 9467: Для теплоустойчивых сталей котельного оборудования."),
            (["ОЗЛ-6", "ОЗЛ-8", "ЦЛ-11", "ЦТ-15", "КТИ-5", "АНЖ-2", "НЖ-13", "ЭА-400/13"],
             "ОЗЛ-6, ОЗЛ-8, ЦЛ-11, ЦТ-15, КТИ-5, АНЖ-2, НЖ-13, ЭА-400/13",
             "Для нержавеющих сталей аустенитного класса. Защита от МКК."),
            (["ЦЧ-4", "АНЧ-1", "ОЗА-1", "ОЗА-2", "КОМСОМОЛЕЦ-100", "АНЦ/ОЗМ-2", "ОЗБ-2М", "Т-590", "Т-620"],
             "ЦЧ-4, АНЧ-1 (Чугун); ОЗА-1, ОЗА-2 (Алюминий); КОМСОМОЛЕЦ-100, АНЦ/ОЗМ-2 (Медь); ОЗБ-2М (Бронза); Т-590, Т-620 (Наплавка)",
             "Специализированные марки для сварки чугуна, цветных металлов и наплавки.")
        ]
        
        marks, all_text, desc = data[idx]
        for m in marks:
            self.el_mark_list.insert("end", m)
        
        self.el_all_text.delete("1.0", "end")
        self.el_all_text.insert("1.0", all_text)
        
        self.el_desc_text.delete("1.0", "end")
        self.el_desc_text.insert("1.0", desc)

    # ==================== ВКЛАДКА 7: ОБОЗНАЧЕНИЕ ШВОВ ====================
    def init_designation_tab(self):
        """Инициализация вкладки Обозначение швов"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📝 Обозначение швов (ГОСТ)")
        
        ttk.Label(tab, text="Структура условного обозначения сварного шва по ГОСТ 2.312-72", 
                 font=("Segoe UI", 11, "bold"), foreground="#8e44ad").pack(pady=10, anchor="w", padx=20)
        
        # Схема расположения знаков
        arrow_frame = ttk.LabelFrame(tab, text=" Схема расположения знаков ")
        arrow_frame.pack(fill="x", padx=20, pady=5)
        
        fields_frame = ttk.Frame(arrow_frame)
        fields_frame.pack(pady=10)
        
        fields = ["1. Стандарт", "2. Тип", "3. Способ", "4. Катет", "5. Длина", "6. Вспом. знаки"]
        for i, lbl in enumerate(fields):
            ttk.Label(fields_frame, text=f" {lbl} ", font=("Segoe UI", 9, "bold")).pack(side="left", padx=5)
            e = ttk.Entry(fields_frame, width=10, justify="center")
            e.insert(0, f"[{i+1}]")
            e.pack(side="left", padx=2)
        
        # Вспомогательные знаки
        znaki_frame = ttk.LabelFrame(tab, text=" Вспомогательные технологические знаки ")
        znaki_frame.pack(fill="x", padx=20, pady=5)
        
        self.znak_var = tk.StringVar(value="По замкнутому контуру")
        znaks = [
            ("По замкнутому контуру", "Шов по замкнутой линии"),
            ("Монтажный шов", "Сварка при монтаже"),
            ("Усиление снять", "Снять выпуклость механически"),
            ("Плавный переход", "Плавное сопряжение")
        ]
        
        znak_row = ttk.Frame(znaki_frame)
        znak_row.pack(pady=5)
        for text, _ in znaks:
            ttk.Radiobutton(znak_row, text=text, variable=self.znak_var, value=text, 
                          command=self.update_gost_info).pack(side="left", padx=10)
        
        # Стандарты
        gost_frame = ttk.LabelFrame(tab, text=" Стандарты на типы соединений ")
        gost_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        self.gost_list = tk.Listbox(gost_frame, font=("Segoe UI", 10), height=4)
        self.gost_list.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        gost_data = [
            "ГОСТ 16037-80 — Стальные трубопроводы",
            "ГОСТ 5264-80 — Ручная дуговая сварка",
            "ГОСТ 14771-76 — Сварка в защитном газе",
            "ГОСТ 8713-79 — Сварка под флюсом"
        ]
        for g in gost_data:
            self.gost_list.insert("end", g)
        
        self.gost_desc = tk.Text(gost_frame, bg="#f8f9fa", foreground="#000000", font=("Segoe UI", 10), width=45)
        self.gost_desc.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        
        self.gost_list.bind("<<ListboxSelect>>", self.update_gost_info)
        self.gost_list.select_set(0)
        self.update_gost_info()

    def update_gost_info(self, event=None):
        """Обновление информации о ГОСТ"""
        self.gost_desc.delete("1.0", "end")
        sel = self.gost_list.curselection()
        
        info = {
            0: "ГОСТ 16037-80:\nПрименяется для стальных технологических трубопроводов.\nТипы швов: С2, С8, С17, У5, У7, У8.\n",
            1: "ГОСТ 5264-80:\nОсновной стандарт на ручную дуговую сварку.\nЛистовые металлоконструкции, балки, резервуары.\n",
            2: "ГОСТ 14771-76:\nДуговая сварка в защитных газах (аргон, CO2).\nДля нержавеющих и легированных конструкций.\n",
            3: "ГОСТ 8713-79:\nАвтоматическая сварка под флюсом.\nВысокая производительность для толстого металла.\n"
        }
        
        if sel:
            self.gost_desc.insert("1.0", info.get(sel[0], ""))
        self.gost_desc.insert("end", f"\nВыбранный знак:\n{self.znak_var.get()}")

    # ==================== ВКЛАДКА 8: ИЗОЛЯЦИЯ ====================
    def init_insulation_tab(self):
        """Инициализация вкладки Изоляция"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="环 Изоляция")
        
        input_frame = ttk.LabelFrame(tab, text=" Параметры изоляции ")
        input_frame.pack(fill="x", padx=15, pady=10)
        
        ttk.Label(input_frame, text="Тип прокладки:").grid(row=0, column=0, padx=5, pady=6, sticky="w")
        self.iso_type = ttk.Combobox(input_frame, values=["Одна труба", "Группа труб"], state="readonly", width=30)
        self.iso_type.set("Одна труба")
        self.iso_type.grid(row=0, column=1, padx=5, pady=6, sticky="w")
        self.iso_type.bind("<<ComboboxSelected>>", self.update_iso_inputs)
        
        self.iso_params_frame = ttk.Frame(input_frame)
        self.iso_params_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        self.iso_params = {}
        
        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(btn_frame, text="Рассчитать объем изоляции", command=self.calc_insulation, width=40).pack()
        
        self.iso_output = tk.Text(tab, bg="#ffffff", foreground="#000000", font=("Courier", 10), height=12, bd=1, relief="solid")
        self.iso_output.pack(fill="both", expand=True, padx=15, pady=10)
        self.update_iso_inputs()

    def update_iso_inputs(self, event=None):
        """Обновление полей ввода изоляции"""
        for w in self.iso_params_frame.winfo_children():
            w.destroy()
        self.iso_params.clear()
        
        if self.iso_type.get() == "Одна труба":
            fields = [("Диаметр D, м", "1.024"), ("Толщина изоляции t, м", "0.1"), ("Длина L, м", "100")]
        else:
            fields = [("Диаметр крайних D1, м", "1.024"), ("Диаметр средних D2, м", "0.720"), 
                     ("Толщина изоляции t, м", "0.1"), ("Зазор p, м", "0.15"), ("Длина L, м", "50")]
        
        for i, (lbl, val) in enumerate(fields):
            ttk.Label(self.iso_params_frame, text=lbl).grid(row=0, column=i*2, padx=4, pady=4, sticky="w")
            e = ttk.Entry(self.iso_params_frame, width=10)
            e.insert(0, val)
            e.grid(row=0, column=i*2+1, padx=4, pady=4)
            self.iso_params[lbl] = e

    def calc_insulation(self):
        """Расчет объема изоляции"""
        try:
            if self.iso_type.get() == "Одна труба":
                D = float(self.iso_params["Диаметр D, м"].get())
                t = float(self.iso_params["Толщина изоляции t, м"].get())
                L = float(self.iso_params["Длина L, м"].get())
                
                S_r = math.pi * D * L
                S_pi = math.pi * (D + 2 * t) * L
                V_i = math.pi / 4 * ((D + 2 * t)**2 - D**2) * L
                
                res = f"📝 ВЕДОМОСТЬ ИЗОЛЯЦИИ (ОДНА ТРУБА):\n"
                res += "-" * 50 + "\n"
                res += f"▶ Площадь обертывания Sr: {S_r:.4f} м²\n"
                res += f"▶ Площадь покровного слоя Spi: {S_pi:.4f} м²\n"
                res += f"▶ ОБЪЕМ ИЗОЛЯЦИИ Vi: {V_i:.4f} м³\n"
            else:
                D1 = float(self.iso_params["Диаметр крайних D1, м"].get())
                D2 = float(self.iso_params["Диаметр средних D2, м"].get())
                t = float(self.iso_params["Толщина изоляции t, м"].get())
                p = float(self.iso_params["Зазор p, м"].get())
                L = float(self.iso_params["Длина L, м"].get())
                
                M = D1 + D2 + p * 2
                B = D1 * 2 + D2 + p * 2 + t * 2
                S_r = (math.pi * D1 + M * 2) * L
                S_pi = (math.pi * (D1 + 2 * t) + M * 2) * L
                V_i = (math.pi / 4 * ((D1 + 2 * t)**2 - D1**2) + M * 2 * t) * L
                
                res = f"📝 ВЕДОМОСТЬ ИЗОЛЯЦИИ (ГРУППА ТРУБ):\n"
                res += "-" * 50 + "\n"
                res += f"▶ Габаритная ширина B: {B:.3f} м\n"
                res += f"▶ Площадь обертывания Sr: {S_r:.4f} м²\n"
                res += f"▶ Площадь покровного слоя Spi: {S_pi:.4f} м²\n"
                res += f"▶ ОБЪЕМ ИЗОЛЯЦИИ Vi: {V_i:.4f} м³\n"
        except Exception as e:
            res = f"❌ Ошибка: {str(e)}"
        
        self.iso_output.delete("1.0", tk.END)
        self.iso_output.insert("1.0", res)


if __name__ == "__main__":
    root = tk.Tk()
    app = MetallistProApp(root)
    root.mainloop()
