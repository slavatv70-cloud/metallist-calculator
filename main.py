import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedStyle
import math

class MetallistProApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор Металлиста PRO — Сметная группа СГК")
        self.root.geometry("1280x960")
        
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
        footer_text = "Разработчик Тищенко Вячеслав Владимирович, сметная группа г.Назарово ООО \"СГК\" 2026г. версия 2"
        lbl_footer = tk.Label(footer, text=footer_text, fg="#ff8c00", bg="#2c3e50", font=("Segoe UI", 11, "bold"))
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
        
        self.geom_result = tk.Text(right, bg="#ffffff", fg="#333333", font=("Consolas", 11), bd=1, relief="solid")
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
        
        self.sort_output = tk.Text(tab, bg="#ffffff", font=("Consolas", 10), height=8, bd=1, relief="solid")
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
        
        self.det_output = tk.Text(tab, bg="#ffffff", font=("Consolas", 10), bd=1, relief="solid")
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
            
            # Справочные данные для отводов 90°
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
                # Геометрический расчет
                R_bend = 1.5 * D if "17375" in t else 1.0 * D if "30753" in t else 1.375 * D if "51-515" in t else 15000.0
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

    # ==================== ВКЛАДКА 5: СВАРКА ====================
    def init_welding_tab(self):
        """Инициализация вкладки Сварка с детализированными чертежами"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="⚡ Сварка")
        
        # Верхняя часть - исходные данные и чертеж
        top_frame = ttk.Frame(tab)
        top_frame.pack(fill="x", padx=15, pady=5)
        
        # Левая панель - параметры
        input_frame = ttk.LabelFrame(top_frame, text=" Исходные данные ")
        input_frame.pack(side="left", fill="both", expand=True, padx=(0,10))
        
        # Выбор типа соединения
        ttk.Label(input_frame, text="Соединение:").grid(row=0, column=0, padx=5, pady=3, sticky="w")
        self.w_joint_type = ttk.Combobox(input_frame, values=[
            "C2", "C8", "C17", "У5", "У7", "У8",
            "Н1", "Н2", "Т1", "Т3", "У4"
        ], state="readonly", width=10)
        self.w_joint_type.set("C17")
        self.w_joint_type.grid(row=0, column=1, padx=5, pady=3, sticky="w")
        self.w_joint_type.bind("<<ComboboxSelected>>", self.on_weld_joint_change)
        
        # Выбор материала
        ttk.Label(input_frame, text="Материал:").grid(row=1, column=0, padx=5, pady=3, sticky="w")
        self.w_mat_type = ttk.Combobox(input_frame, values=["Сталь", "Нержавеющая сталь", "Алюминий", "Медь"], state="readonly", width=18)
        self.w_mat_type.set("Сталь")
        self.w_mat_type.grid(row=1, column=1, padx=5, pady=3, sticky="w")
        self.w_mat_type.bind("<<ComboboxSelected>>", self.on_weld_material_change)
        
        # Выбор положения шва
        ttk.Label(input_frame, text="Положение шва:").grid(row=2, column=0, padx=5, pady=3, sticky="w")
        self.w_pos_type = ttk.Combobox(input_frame, values=["Нижнее", "Вертикальное", "Потолочное", "Горизонтальное"], state="readonly", width=15)
        self.w_pos_type.set("Нижнее")
        self.w_pos_type.grid(row=2, column=1, padx=5, pady=3, sticky="w")
        self.w_pos_type.bind("<<ComboboxSelected>>", self.update_welding_current)
        
        # Динамические поля параметров
        self.weld_params_frame = ttk.Frame(input_frame)
        self.weld_params_frame.grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")
        self.weld_params = {}
        
        # Кнопка расчета
        ttk.Button(input_frame, text="Считать", command=self.calc_weld).grid(row=4, column=1, padx=5, pady=5, sticky="e")
        
        # Правая панель - чертеж
        self.weld_canvas = tk.Canvas(top_frame, bg="#ffffff", width=520, height=280, bd=1, relief="solid")
        self.weld_canvas.pack(side="right", fill="both", expand=True)
        
        # Средняя часть - выбор электродов
        mid_frame = ttk.Frame(tab)
        mid_frame.pack(fill="x", padx=15, pady=5)
        
        electrod_frame = ttk.LabelFrame(mid_frame, text=" Выбор сварочного материала ")
        electrod_frame.pack(fill="x", pady=2)
        
        self.w_el_cat = ttk.Combobox(electrod_frame, values=[
            "Углеродистая сталь", "Легированная сталь", 
            "Теплоустойчивая сталь", "Нержавеющая сталь",
            "Алюминий", "Медь и сплавы", "Чугун"
        ], state="readonly", width=30)
        self.w_el_cat.set("Углеродистая сталь")
        self.w_el_cat.pack(side="left", padx=10, pady=5)
        self.w_el_cat.bind("<<ComboboxSelected>>", self.update_electrode_marks)
        
        self.w_el_mark = ttk.Combobox(electrod_frame, values=[], state="readonly", width=15)
        self.w_el_mark.pack(side="left", padx=5, pady=5)
        self.w_el_mark.bind("<<ComboboxSelected>>", self.update_welding_current)
        
        ttk.Label(electrod_frame, text="Диаметр, мм:").pack(side="left", padx=10)
        self.w_el_dia = ttk.Combobox(electrod_frame, values=["2.0", "2.5", "3.0", "4.0", "5.0", "6.0"], width=6, state="readonly")
        self.w_el_dia.set("3.0")
        self.w_el_dia.pack(side="left", padx=5, pady=5)
        self.w_el_dia.bind("<<ComboboxSelected>>", self.update_welding_current)
        
        # Нижняя часть - результаты
        result_frame = ttk.LabelFrame(tab, text=" Расчетные показатели ")
        result_frame.pack(fill="x", padx=15, pady=5)
        
        row1 = ttk.Frame(result_frame)
        row1.pack(fill="x", pady=4)
        
        self.out_e = ttk.Entry(row1, width=10, font=("Consolas", 10, "bold"), justify="center")
        self.out_e.pack(side="left", padx=10)
        ttk.Label(row1, text="- ширина шва (e), мм").pack(side="left")
        
        ttk.Label(row1, text="РЕКОМЕНДУЕМЫЙ ТОК:").pack(side="right", padx=5)
        self.out_current = ttk.Entry(row1, width=15, font=("Consolas", 10, "bold"), justify="center")
        self.out_current.pack(side="right", padx=15)
        
        row2 = ttk.Frame(result_frame)
        row2.pack(fill="x", pady=4)
        
        self.out_el_mass = ttk.Entry(row2, width=10, font=("Consolas", 10, "bold"), justify="center")
        self.out_el_mass.pack(side="left", padx=10)
        ttk.Label(row2, text="- расход электродов, кг").pack(side="left")
        
        ttk.Button(row2, text="Выход", command=self.root.quit).pack(side="right", padx=15)
        
        # Инициализация
        self.build_weld_params()
        self.update_electrode_marks()
        self.draw_weld_joint()

    def on_weld_joint_change(self, event=None):
        """Обработка смены типа соединения"""
        self.build_weld_params()
        self.draw_weld_joint()
        self.calc_weld()

    def on_weld_material_change(self, event=None):
        """Обработка смены материала"""
        mat = self.w_mat_type.get()
        mat_map = {
            "Сталь": "Углеродистая сталь",
            "Нержавеющая сталь": "Нержавеющая сталь",
            "Алюминий": "Алюминий",
            "Медь": "Медь и сплавы"
        }
        if mat in mat_map:
            self.w_el_cat.set(mat_map[mat])
            self.update_electrode_marks()

    def build_weld_params(self):
        """Построение полей параметров сварки"""
        for w in self.weld_params_frame.winfo_children():
            w.destroy()
        self.weld_params.clear()
        
        joint = self.w_joint_type.get()
        params = {
            "C2": [("кол-во швов", "1"), ("D, мм", "60"), ("S, мм", "3"), ("b, мм", "1"), ("c, мм", "0.5"), ("g, мм", "2"), ("α°", "50")],
            "C8": [("кол-во швов", "1"), ("D, мм", "60"), ("S, мм", "3"), ("b, мм", "1"), ("c, мм", "0.5"), ("g, мм", "2"), ("α°", "50")],
            "C17": [("кол-во швов", "1"), ("D, мм", "20"), ("S, мм", "3"), ("b, мм", "1"), ("c, мм", "0.5"), ("g, мм", "2"), ("α°", "30")],
            "У5": [("кол-во швов", "1"), ("D, мм", "108"), ("S, мм", "4"), ("S1, мм", "4"), ("b, мм", "0.5"), ("g, мм", "1")],
            "У7": [("кол-во швов", "1"), ("D, мм", "108"), ("S, мм", "4"), ("S1, мм", "4"), ("b, мм", "0.5"), ("g, мм", "1")],
            "У8": [("кол-во швов", "1"), ("D, мм", "108"), ("S, мм", "4"), ("S1, мм", "4"), ("b, мм", "0.5"), ("g, мм", "1")],
        }
        
        # Для листовых соединений
        if joint in ["Н1", "Н2"]:
            params[joint] = [("S, мм", "5"), ("L, мм", "100"), ("l, мм", "30"), ("g, мм", "1")]
        elif joint in ["Т1", "Т3"]:
            params[joint] = [("S, мм", "5"), ("L, мм", "100"), ("g, мм", "1")]
        elif joint == "У4":
            params[joint] = [("S, мм", "5"), ("L, мм", "100"), ("g, мм", "1")]
        
        for row, (lbl, val) in enumerate(params.get(joint, [])):
            ttk.Label(self.weld_params_frame, text=lbl).grid(row=row, column=0, padx=5, pady=2, sticky="w")
            e = ttk.Entry(self.weld_params_frame, width=8, justify="center")
            e.insert(0, val)
            e.grid(row=row, column=1, padx=5, pady=2)
            self.weld_params[lbl] = e

    def draw_weld_joint(self):
        """Отрисовка детализированного чертежа сварного соединения"""
        self.weld_canvas.delete("all")
        joint = self.w_joint_type.get()
        w = self.weld_canvas.winfo_width()
        h = self.weld_canvas.winfo_height()
        if w < 100:
            w = 520
        if h < 100:
            h = 280
        cx, cy = w // 2, h // 2
        
        # Функции для отрисовки
        def draw_part(x1, y1, x2, y2, color="#bdc3c7"):
            self.weld_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#34495e", width=2)
        
        def draw_weld(points, color="#ff8000"):
            self.weld_canvas.create_polygon(points, fill=color, outline="#d35400", width=2, stipple="gray25")
            self.weld_canvas.create_polygon(points, fill="", outline="#d35400", width=2)
        
        def draw_dim(x1, y1, x2, y2, label, offset=20, color="#2980b9"):
            self.weld_canvas.create_line(x1, y1, x2, y2, fill=color, width=1.5, dash=(4, 2))
            self.weld_canvas.create_line(x1, y1, x1-6, y1-5, fill=color, width=1.5)
            self.weld_canvas.create_line(x1, y1, x1-6, y1+5, fill=color, width=1.5)
            self.weld_canvas.create_line(x2, y2, x2+6, y2-5, fill=color, width=1.5)
            self.weld_canvas.create_line(x2, y2, x2+6, y2+5, fill=color, width=1.5)
            self.weld_canvas.create_text((x1+x2)//2, y1-offset, text=label, font=("Segoe UI", 10, "bold"), fill=color)
        
        # Легенда
        self.weld_canvas.create_rectangle(10, 10, 210, 85, fill="#f8f9fa", outline="#dee2e6")
        self.weld_canvas.create_text(110, 25, text="Условные обозначения:", font=("Segoe UI", 8, "bold"))
        self.weld_canvas.create_rectangle(20, 35, 40, 50, fill="#ff8000", outline="#d35400")
        self.weld_canvas.create_text(50, 45, text="- зона шва", font=("Segoe UI", 8), anchor="w")
        self.weld_canvas.create_rectangle(20, 55, 40, 70, fill="#bdc3c7", outline="#34495e")
        self.weld_canvas.create_text(50, 65, text="- основной металл", font=("Segoe UI", 8), anchor="w")
        self.weld_canvas.create_line(20, 75, 40, 75, fill="#2980b9", width=1.5, dash=(4,2))
        self.weld_canvas.create_text(50, 78, text="- размерная линия", font=("Segoe UI", 8), anchor="w")
        
        # Отрисовка в зависимости от типа
        if joint in ["C2", "C8"]:
            self.weld_canvas.create_text(cx, 20, text=f"Тип {joint} - Стыковое V-образное", font=("Segoe UI", 11, "bold"))
            draw_part(30, cy-35, 180, cy+35)
            draw_part(340, cy-35, 490, cy+35)
            self.weld_canvas.create_line(180, cy-35, 210, cy+20, fill="#34495e", width=2)
            self.weld_canvas.create_line(340, cy-35, 310, cy+20, fill="#34495e", width=2)
            draw_weld([180, cy-35, 210, cy+20, 310, cy+20, 340, cy-35])
            if joint == "C8":
                draw_part(200, cy+25, 320, cy+45, "#95a5a6")
            self.weld_canvas.create_arc(180, cy-50, 340, cy+10, start=0, extent=180, style="arc", outline="#e74c3c", width=2)
            draw_dim(210, cy+25, 310, cy+25, "b")
            draw_dim(170, cy-45, 350, cy-45, "e")
            draw_dim(490, cy-35, 490, cy+35, "S")
            draw_dim(260, cy-10, 260, cy-35, "g", 15)
            self.weld_canvas.create_arc(180, cy-35, 210, cy+20, start=0, extent=45, style="arc", outline="#e74c3c", width=1.5)
            self.weld_canvas.create_text(170, cy-5, text="α°", font=("Segoe UI", 9, "bold"), fill="#e74c3c")
            
        elif joint == "C17":
            self.weld_canvas.create_text(cx, 20, text="Тип C17 - Стыковое U-образное", font=("Segoe UI", 11, "bold"))
            draw_part(30, cy-35, 160, cy+35)
            draw_part(380, cy-35, 490, cy+35)
            self.weld_canvas.create_arc(160, cy-35, 210, cy+35, start=90, extent=90, style="arc", outline="#34495e", width=2)
            self.weld_canvas.create_arc(330, cy-35, 380, cy+35, start=0, extent=90, style="arc", outline="#34495e", width=2)
            draw_weld([160, cy-35, 190, cy-20, 350, cy-20, 380, cy-35, 380, cy+35, 350, cy+20, 190, cy+20, 160, cy+35])
            draw_dim(190, cy+40, 350, cy+40, "b")
            draw_dim(145, cy-45, 395, cy-45, "e")
            draw_dim(490, cy-35, 490, cy+35, "S")
            draw_dim(160, cy-35, 160, cy-5, "c", -10)
            draw_dim(380, cy-35, 380, cy-5, "c", -10)
            
        elif joint in ["У5", "У7", "У8"]:
            names = {"У5": "с разделкой", "У7": "без разделки", "У8": "с двумя скосами"}
            self.weld_canvas.create_text(cx, 20, text=f"Тип {joint} - Угловое {names.get(joint, '')}", font=("Segoe UI", 11, "bold"))
            draw_part(80, cy+25, 420, cy+65)
            draw_part(230, cy-60, 270, cy+25)
            if joint in ["У5", "У8"]:
                self.weld_canvas.create_line(230, cy+25, 250, cy-20, fill="#34495e", width=2)
                self.weld_canvas.create_line(270, cy+25, 250, cy-20, fill="#34495e", width=2)
            if joint == "У8":
                self.weld_canvas.create_line(230, cy-20, 250, cy-40, fill="#34495e", width=2)
                self.weld_canvas.create_line(270, cy-20, 250, cy-40, fill="#34495e", width=2)
            draw_weld([230, cy+25, 250, cy-20, 270, cy+25])
            draw_weld([230, cy+25, 250, cy+45, 270, cy+25])
            draw_dim(280, cy-60, 280, cy+25, "S")
            draw_dim(80, cy+65, 420, cy+65, "S1")
            draw_dim(250, cy-20, 250, cy+25, "k", -10)
            draw_dim(250, cy+25, 250, cy+45, "k", -10)
            
        elif joint in ["Н1", "Н2"]:
            name = "одностороннее" if joint == "Н1" else "двустороннее"
            self.weld_canvas.create_text(cx, 20, text=f"Тип {joint} - Нахлёсточное {name}", font=("Segoe UI", 11, "bold"))
            draw_part(60, cy-35, 460, cy-5)
            draw_part(60, cy+5, 460, cy+35)
            if joint == "Н1":
                draw_weld([200, cy-5, 240, cy-5, 240, cy+5, 200, cy+5])
            else:
                draw_weld([180, cy-5, 210, cy-5, 210, cy+5, 180, cy+5])
                draw_weld([310, cy-5, 340, cy-5, 340, cy+5, 310, cy+5])
            draw_dim(240, cy-50, 280, cy-50, "l")
            draw_dim(60, cy-45, 460, cy-45, "L")
            
        elif joint in ["Т1", "Т3"]:
            name = "без скоса" if joint == "Т1" else "со скосом"
            self.weld_canvas.create_text(cx, 20, text=f"Тип {joint} - Тавровое {name}", font=("Segoe UI", 11, "bold"))
            draw_part(60, cy+10, 460, cy+40)
            draw_part(230, cy-35, 270, cy+10)
            if joint == "Т3":
                self.weld_canvas.create_line(230, cy-10, 250, cy-25, fill="#34495e", width=2)
                self.weld_canvas.create_line(270, cy-10, 250, cy-25, fill="#34495e", width=2)
            draw_weld([230, cy-10, 270, cy-10, 270, cy+10, 230, cy+10])
            draw_dim(280, cy-35, 280, cy+10, "S")
            draw_dim(60, cy+40, 460, cy+40, "L")
            
        elif joint == "У4":
            self.weld_canvas.create_text(cx, 20, text="Тип У4 - Угловое", font=("Segoe UI", 11, "bold"))
            draw_part(60, cy+10, 350, cy+40)
            draw_part(280, cy-35, 310, cy+10)
            draw_weld([280, cy-10, 310, cy-10, 310, cy+10, 280, cy+10])
            draw_dim(320, cy-35, 320, cy+10, "S")
            draw_dim(60, cy+40, 350, cy+40, "L")
        
        self.weld_canvas.tag_lower("all")

    def update_electrode_marks(self, event=None):
        """Обновление списка марок электродов"""
        cat = self.w_el_cat.get()
        marks = {
            "Углеродистая сталь": ["УОНИ-13/45", "УОНИ-13/55", "АНО-4", "МР-3", "ОЗС-4", "ОЗС-6"],
            "Легированная сталь": ["УОНИ-13/85", "АНО-ТМ70", "ЦЛ-18", "ЦЛ-19"],
            "Теплоустойчивая сталь": ["ЦЛ-6", "ЦУ-2М", "ТМЛ-1", "ТМЛ-3У", "ЦЛ-39"],
            "Нержавеющая сталь": ["ОЗЛ-6", "ОЗЛ-8", "ЦЛ-11", "ЦТ-15", "КТИ-9А"],
            "Алюминий": ["ОЗА-1", "ОЗА-2"],
            "Медь и сплавы": ["КОМСОМОЛЕЦ-100", "АНЦ/ОЗМ-2", "АНЦ/ОЗМ-3"],
            "Чугун": ["ЦЧ-4", "АНЧ-1", "ОЗЧ-2", "ОЗЧ-6"]
        }
        self.w_el_mark['values'] = marks.get(cat, [])
        if marks.get(cat):
            self.w_el_mark.set(marks[cat][0])
        self.update_welding_current()

    def update_welding_current(self, event=None):
        """Обновление рекомендуемого тока сварки"""
        mark = self.w_el_mark.get()
        dia = self.w_el_dia.get()
        pos = self.w_pos_type.get()
        
        current_data = {
            "УОНИ-13/45": {"2.0": "40-60", "2.5": "50-75", "3.0": "80-100", "4.0": "130-150"},
            "УОНИ-13/55": {"2.0": "40-60", "2.5": "50-75", "3.0": "80-100", "4.0": "130-160"},
            "АНО-4": {"3.0": "100-140", "4.0": "170-210"},
            "МР-3": {"3.0": "140-180", "4.0": "160-200"},
            "ОЗС-4": {"3.0": "90-100", "4.0": "140-170"},
            "ОЗС-6": {"3.0": "80-110", "4.0": "170-220"}
        }
        
        current = "130-150 A"
        if mark in current_data and dia in current_data[mark]:
            current = current_data[mark][dia]
        
        self.out_current.config(state="normal")
        self.out_current.delete(0, "end")
        self.out_current.insert(0, f"{current} A")
        self.out_current.config(state="readonly")

    def calc_weld(self):
        """Расчет параметров сварного шва"""
        joint = self.w_joint_type.get()
        rho = self.get_density()
        
        try:
            if joint in ["C2", "C8"]:
                n = float(self.weld_params["кол-во швов"].get())
                D = float(self.weld_params["D, мм"].get())
                S = float(self.weld_params["S, мм"].get())
                b = float(self.weld_params["b, мм"].get())
                c = float(self.weld_params["c, мм"].get())
                g = float(self.weld_params["g, мм"].get())
                alpha = float(self.weld_params["α°"].get())
                
                e = b + 2 * (S - c) * math.tan(math.radians(alpha)) + 2
                F = ((b + (e - 2)) / 2) * (S - c) + (b * c) + (2 / 3 * e * g)
                L = math.pi * (D - S)
                m = F * L * rho / 1000000 * n
                
            elif joint == "C17":
                n = float(self.weld_params["кол-во швов"].get())
                D = float(self.weld_params["D, мм"].get())
                S = float(self.weld_params["S, мм"].get())
                b = float(self.weld_params["b, мм"].get())
                c = float(self.weld_params["c, мм"].get())
                g = float(self.weld_params["g, мм"].get())
                alpha = float(self.weld_params["α°"].get())
                
                e = b + 2 * (S - c) * math.tan(math.radians(alpha)) + 2
                F = ((b + (e - 2)) / 2) * (S - c) + (b * c) + (2 / 3 * e * g)
                L = math.pi * (D - S)
                m = F * L * rho / 1000000 * n
                
            elif joint in ["У5", "У7", "У8"]:
                n = float(self.weld_params["кол-во швов"].get())
                D = float(self.weld_params["D, мм"].get())
                S = float(self.weld_params["S, мм"].get())
                S1 = float(self.weld_params["S1, мм"].get())
                b = float(self.weld_params["b, мм"].get())
                g = float(self.weld_params["g, мм"].get())
                
                e = S + S1 + b + 1.5
                K = S + 1
                K1 = S1 + 1
                F = (0.5 * K * K1) + (2 / 3 * max(K, K1) * g)
                L = math.pi * D
                m = F * L * rho / 1000000 * n
                
            elif joint in ["Н1", "Н2"]:
                S = float(self.weld_params["S, мм"].get())
                L = float(self.weld_params["L, мм"].get())
                l = float(self.weld_params["l, мм"].get())
                g = float(self.weld_params["g, мм"].get())
                
                e = S + 2
                F = (0.5 * S * S) + (2 / 3 * e * g)
                m = F * l * rho / 1000000
                if joint == "Н2":
                    m *= 2
                    
            elif joint in ["Т1", "Т3"]:
                S = float(self.weld_params["S, мм"].get())
                L = float(self.weld_params["L, мм"].get())
                g = float(self.weld_params["g, мм"].get())
                
                e = S + 2
                F = (0.5 * S * S) + (2 / 3 * e * g)
                m = F * L * rho / 1000000
                
            elif joint == "У4":
                S = float(self.weld_params["S, мм"].get())
                L = float(self.weld_params["L, мм"].get())
                g = float(self.weld_params["g, мм"].get())
                
                e = S + 2
                F = (0.5 * S * S) + (2 / 3 * e * g)
                m = F * L * rho / 1000000
            else:
                messagebox.showerror("Ошибка", "Неизвестный тип соединения")
                return
            
            # Коэффициент расхода электродов
            mark = self.w_el_mark.get()
            coeff = {"УОНИ-13/45": 1.60, "УОНИ-13/55": 1.62, "АНО-4": 1.70, "МР-3": 1.70, "ОЗС-4": 1.60, "ОЗС-6": 1.50}
            k = coeff.get(mark, 1.62)
            
            self.out_e.config(state="normal")
            self.out_e.delete(0, "end")
            self.out_e.insert(0, f"{e:.1f}")
            self.out_e.config(state="readonly")
            
            self.out_el_mass.config(state="normal")
            self.out_el_mass.delete(0, "end")
            self.out_el_mass.insert(0, f"{m * k:.3f}")
            self.out_el_mass.config(state="readonly")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Проверьте введенные данные!\n{str(e)}")

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
        self.el_all_text = tk.Text(all_frame, height=2, font=("Consolas", 10))
        self.el_all_text.pack(fill="x", padx=5, pady=5)
        
        desc_frame = ttk.LabelFrame(right_frame, text=" Описание ")
        desc_frame.pack(fill="both", expand=True, pady=5)
        self.el_desc_text = tk.Text(desc_frame, bg="#f8f9fa", font=("Segoe UI", 10))
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
                 font=("Segoe UI", 11, "bold"), fg="#8e44ad").pack(pady=10, anchor="w", padx=20)
        
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
        
        self.gost_desc = tk.Text(gost_frame, bg="#f8f9fa", font=("Segoe UI", 10), width=45)
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
        
        self.iso_output = tk.Text(tab, bg="#ffffff", font=("Courier", 10), height=12, bd=1, relief="solid")
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
