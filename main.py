import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from ttkthemes import ThemedStyle
import math

class MetallistProApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор Металлиста PRO — Сметная группа СГК")
        self.root.geometry("1180x920")
        
        # Настройка графической темы оформления Arc
        self.style = ThemedStyle(self.root)
        self.current_theme = "arc"
        self.style.set_theme(self.current_theme)
        self.style.configure('.', font=('Segoe UI', 10))
        self.style.configure('TNotebook.Tab', font=('Segoe UI', 10, 'bold'), padding=5)
        
        # Панель управления глобальными настройками сессии
        top_ctrl = ttk.LabelFrame(root, text=" Глобальные настройки сессии ")
        top_ctrl.pack(fill="x", padx=15, pady=5)
        
        ttk.Label(top_ctrl, text="Материал для расчетов:", font=("Segoe UI", 10, "bold")).pack(side="left", padx=10, pady=8)
        self.global_material = ttk.Combobox(top_ctrl, values=["Черный metal (Сталь)", "Нержавеющая сталь", "Медь (Цветной)"], state="readonly", width=22)
        self.global_material.set("Черный metal (Сталь)")
        self.global_material.pack(side="left", padx=5, pady=8)
        
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
        self.init_insulation_tab()
        
        # Официальный подвал разработчика СГК
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
            except Exception: angle_deg = 60
            if angle_deg >= 360:
                self.geom_canvas.create_oval(cx-r_px, cy-r_px, cx+r_px, cy+r_px, fill="#e9ecef", outline="black")
            else:
                self.geom_canvas.create_arc(cx-r_px, cy-r_px, cx+r_px, cy+r_px, start=0, extent=angle_deg, fill="#e9ecef", outline="black")
        elif gtype == "Труба (Кольцо)":
            self.geom_canvas.create_oval(cx-60, cy-65, cx+60, cy+65, fill="#dee2e6", outline="black")
            self.geom_canvas.create_oval(cx-40, cy-45, cx+40, cy+45, fill="#ffffff", outline="black")
        elif "Шестигранник" in gtype:
            p = []
            for i in range(6): p.extend([cx + 50*math.cos(math.radians(i*60)), cy + 50*math.sin(math.radians(i*60))])
            self.geom_canvas.create_polygon(p, fill="#e9ecef", outline="black")

    def process_geometry(self):
        gtype = self.geom_type.get(); rho = self.get_density()
        res = f"=== Расчет геометрии заготовки ===\n\n"
        try:
            if gtype == "Круг / Сегмент":
                R, a = float(self.entries["Радиус R, мм"].get()), float(self.entries["Угол альфа, град"].get())
                res += f"Площадь круга: {math.pi*(R**2):.2f} мм²\nПлощадь сегмента: {0.5*(R**2)*(math.radians(a)-math.sin(math.radians(a))):.2f} мм²\n"
            elif gtype == "Труба (Кольцо)":
                D, s = float(self.entries["Внешний диаметр D, мм"].get()), float(self.entries["Толщина стенки s, мм"].get())
                sect = (math.pi / 4) * (D**2 - (D - 2*s)**2)
                res += f"Площадь сечения: {sect:.2f} мм²\nВес 1м заготовки: {(sect*rho/1000):.3f} кг\n"
            elif gtype == "Шестигранник":
                S, L = float(self.entries["Размер под ключ S, мм"].get()), float(self.entries["Длина L, мм"].get())
                res += f"Площадь сечения: {(math.sqrt(3)/2)*(S**2):.2f} мм²\n"
        except Exception as e: res += f"Ошибка: {str(e)}"
        self.geom_result.config(state="normal"); self.geom_result.delete("1.0", tk.END); self.geom_result.insert("1.0", res); self.geom_result.config(state="disabled")

    def init_sortament_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📊 Сортамент")
        top = ttk.LabelFrame(tab, text=" Параметры проката ")
        top.pack(fill="x", padx=15, pady=10)
        ttk.Label(top, text="Тип проката:").grid(row=0, column=0, padx=5, pady=8, sticky="w")
        self.sort_profile = ttk.Combobox(top, values=["Двутавр ГОСТ 8239-89", "Швеллер ГОСТ 8240-97", "Труба Круглая ГОСТ 10704-91", "Лист ГОСТ 19903-74"], state="readonly", width=25)
        self.sort_profile.set("Двутавр ГОСТ 8239-89"); self.sort_profile.grid(row=0, column=1, padx=5, pady=8, sticky="w")
        self.sort_tree = ttk.Treeview(tab, columns=("num", "weight"), show="headings", height=8)
        self.sort_tree.heading("num", text="Профиль"); self.sort_tree.heading("weight", text="Вес 1м, кг")
        self.sort_tree.pack(fill="x", padx=15, pady=5)
    def init_detali_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔧 Детали трубопроводов")
        left = ttk.LabelFrame(tab, text=" Параметры арматуры ")
        left.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        ttk.Label(left, text="Элемент сети:").pack(anchor="w", padx=10, pady=2)
        self.det_type = ttk.Combobox(left, values=["Отвод 90° ГОСТ 17375-2001", "Фланец ГОСТ 33259-2015"], state="readonly", width=30)
        self.det_type.set("Отвод 90° ГОСТ 17375-2001"); self.det_type.pack(fill="x", padx=10, pady=4)
        ttk.Label(left, text="Диаметр Ду:").pack(anchor="w", padx=10, pady=2)
        self.det_dy = ttk.Combobox(left, values=["Ду50 (∅57)", "Ду100 (∅108)", "Ду150 (∅159)", "Ду219", "Ду325"], state="readonly")
        self.det_dy.set("Ду150 (∅159)"); self.det_dy.pack(fill="x", padx=10, pady=4)
        self.det_output = tk.Text(tab, bg="#ffffff", font=("Consolas", 10), bd=1, relief="solid")
        self.det_output.pack(side="right", fill="both", expand=True, padx=15, pady=15)

    def init_metiz_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔩 Метизы")
        left = ttk.LabelFrame(tab, text=" Параметры крепежа ")
        left.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        ttk.Label(left, text="Тип крепежа:").pack(anchor="w", padx=10, pady=2)
        self.metiz_type = ttk.Combobox(left, values=["Болт ГОСТ 7798", "Гайка ГОСТ 5915"], state="readonly")
        self.metiz_type.set("Болт ГОСТ 7798"); self.metiz_type.pack(fill="x", padx=10, pady=4)
        ttk.Label(left, text="Размер:").pack(anchor="w", padx=10, pady=2)
        self.metiz_d = ttk.Combobox(left, values=["М10", "М12", "М16", "М20"], state="readonly")
        self.metiz_d.set("М16"); self.metiz_d.pack(fill="x", padx=10, pady=4)
        
        self.kit_check_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(left, text="Укомплектовать болт (1 гайка + 2 шайбы)", variable=self.kit_check_var).pack(anchor="w", padx=10, pady=5)
        
        self.metiz_info = tk.Text(tab, bg="#ffffff", font=("Consolas", 10), bd=1, relief="solid")
        self.metiz_info.pack(side="right", fill="both", expand=True, padx=15, pady=15)

    def on_sortament_type_change(self, event=None): pass
    def init_welding_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="⚡ Сварка")
        
        # Левая панель ввода исходных данных (Скриншот 1 и 5)
        left_p = ttk.LabelFrame(tab, text=" Исходные данные шва ")
        left_p.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        ttk.Label(left_p, text="Соединение по ГОСТ:").grid(row=0, column=0, padx=5, pady=4, sticky="w")
        self.weld_joint = ttk.Combobox(left_p, values=["С17 (Стыковое ГОСТ 16037)", "У5 (Угловое/Фланец ГОСТ 16037)", "Листы Н1 (Нахлест)", "Листы Т1 (Тавр)"], state="readonly", width=22)
        self.weld_joint.set("С17 (Стыковое ГОСТ 16037)"); self.weld_joint.grid(row=0, column=1, padx=5, pady=4, sticky="w")
        self.weld_joint.bind("<<ComboboxSelected>>", self.toggle_weld_fields)
        
        ttk.Label(left_p, text="Положение шва:").grid(row=1, column=0, padx=5, pady=4, sticky="w")
        self.weld_pos = ttk.Combobox(left_p, values=["Горизонтальное", "Вертикальное", "Нижнее", "Потолочное"], state="readonly", width=22)
        self.weld_pos.set("Горизонтальное"); self.weld_pos.grid(row=1, column=1, padx=5, pady=4, sticky="w")
        
        # Динамический контейнер параметров разделки (меняется С17 / У5 / Листы)
        self.weld_fields_frame = ttk.Frame(left_p)
        self.weld_fields_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        self.w_entries = {}
        
        # Панель справочников (Кнопки вызова окон Скриншотов 2 и 3)
        spr_frame = ttk.LabelFrame(left_p, text=" Инженерные ГОСТ-справочники ")
        spr_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=8, sticky="ew")
        
        ttk.Button(spr_frame, text="📖 Справочник марок электродов (ГОСТ 9467)", command=self.open_electrodes_window).pack(fill="x", padx=10, pady=4)
        ttk.Button(spr_frame, text="📐 Структура обозначений швов (ГОСТ 2.312)", command=self.open_gost_designation_window).pack(fill="x", padx=10, pady=4)
        
        # Кнопки расчета и выхода
        btn_f = ttk.Frame(left_p)
        btn_f.grid(row=4, column=0, columnspan=2, padx=5, pady=10, sticky="ew")
        ttk.Button(btn_f, text="Считать расход", command=self.calculate_welding_efficiency, width=18).pack(side="left", padx=5)
        
        # Правая панель с Чертежом и Результатами (Скриншот 1 и 5)
        right_p = ttk.LabelFrame(tab, text=" Эскиз и Технологический результат ")
        right_p.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        self.weld_canvas = tk.Canvas(right_p, bg="#ffffff", height=150, bd=1, relief="solid")
        self.weld_canvas.pack(fill="x", padx=10, pady=5)
        
        self.w_res_text = tk.Text(right_p, bg="#f8f9fa", font=("Consolas", 10), height=14, bd=1, relief="solid")
        self.w_res_text.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.toggle_weld_fields()

    def toggle_weld_fields(self, event=None):
        for w in self.weld_fields_frame.winfo_children(): w.destroy()
        self.w_entries.clear()
        joint = self.weld_joint.get()
        
        if "С17" in joint:
            fields = [("кол-во св. швов", "1"), ("диаметр трубы (D), мм", "159"), ("толщина стенки (S), мм", "6"), ("зазор прихватки (b), мм", "1"), ("притупление кромки (c), мм", "0.5"), ("выпуклость шва (g), мм", "2"), ("угол фаски (A°)", "30")]
        elif "У5" in joint:
            fields = [("кол-во св. швов", "1"), ("диаметр трубы (D), мм", "108"), ("толщина стенки (S), мм", "4"), ("толщина фланца (S1), мм", "4"), ("зазор прихватки (b), мм", "0.5"), ("выпуклость шва (g), мм", "1")]
        else: # Листы Н1/Т1
            fields = [("Катет шва, мм", "5"), ("Длина шва, мм", "1000"), ("Доп.% на огарки", "10")]
            
        for r, (lbl, val) in enumerate(fields):
            ttk.Label(self.weld_fields_frame, text=f"- {lbl}:").grid(row=r, column=0, pady=3, sticky="w")
            e = ttk.Entry(self.weld_fields_frame, width=12); e.insert(0, val); e.grid(row=r, column=1, padx=10, pady=3, sticky="w")
            self.w_entries[lbl] = e
        self.draw_welding_diagram()
    def draw_welding_diagram(self):
        self.weld_canvas.delete("all"); joint = self.weld_joint.get(); cx, cy = 180, 75
        if "С17" in joint:
            self.weld_canvas.create_line(40, 50, 140, 50, width=2); self.weld_canvas.create_line(140, 50, 160, 90, width=2)
            self.weld_canvas.create_line(220, 50, 320, 50, width=2); self.weld_canvas.create_line(220, 50, 200, 90, width=2)
            self.weld_canvas.create_oval(150, 35, 210, 65, fill="#ff8c00")
            self.weld_canvas.create_text(cx, cy+40, text="Разделка кромок С17", font=("Segoe UI", 9, "bold"))
        elif "У5" in joint:
            self.weld_canvas.create_rectangle(140, 20, 220, 110, fill="#dee2e6")
            self.weld_canvas.create_rectangle(60, 65, 140, 95, fill="#b2bec3")
            self.weld_canvas.create_polygon(140,65, 120,45, 140,45, fill="#ff8c00")
            self.weld_canvas.create_text(cx, cy+45, text="Угловое тавровое У5", font=("Segoe UI", 9, "bold"))

    def calculate_welding_efficiency(self):
        joint = self.weld_joint.get(); rho = self.get_density(); res = ""
        try:
            if "С17" in joint:
                n = float(self.w_entries["кол-во св. швов"].get())
                D = float(self.w_entries["диаметр трубы (D), мм"].get())
                S = float(self.w_entries["толщина стенки (S), мм"].get())
                b = float(self.w_entries["зазор прихватки (b), мм"].get())
                c = float(self.w_entries["притупление кромки (c), мм"].get())
                g = float(self.w_entries["выпуклость шва (g), мм"].get())
                A = float(self.w_entries["угол фаски (A°)"].get())
                
                # Точные формулы тригонометрии разделки кромок со Скриншота 1
                e = b + 2 * (S - c) * math.tan(math.radians(A)) + 2
                F_weld = ((b + (e - 2)) / 2) * (S - c) + (b * c) + (2 / 3 * e * g)
                L_weld = math.pi * (D - S)
                m_dep = (F_weld * L_weld * rho / 1000000) * n
                
                res = f"=== РЕЗУЛЬТАТ РАСЧЕТА ШВА С17 (ГОСТ 16037) ===\n" \
                      f"• Расчетная ширина сварного шва (e): {e:.2f} мм\n" \
                      f"• Площадь наплавленного сечения:   {F_weld:.2f} мм²\n" \
                      f"• Длина одного кольцевого стыка:    {L_weld:.1f} мм\n" \
                      f"--------------------------------------------------\n" \
                      f"▶ ПОТРЕБНОСТЬ ЭЛЕКТРОДОВ (ММА):     {m_dep * 1.62:.3f} кг\n" \
                      f"▶ ПОТРЕБНОСТЬ ПРОВОЛОКИ (MIG/MAG):  {m_dep * 1.12:.3f} кг\n"
                      
            elif "У5" in joint:
                n = float(self.w_entries["кол-во св. швов"].get())
                D = float(self.w_entries["диаметр трубы (D), мм"].get())
                S = float(self.w_entries["толщина стенки (S), мм"].get())
                S1 = float(self.w_entries["толщина фланца (S1), мм"].get())
                b = float(self.w_entries["зазор прихватки (b), мм"].get())
                g = float(self.w_entries["выпуклость шва (g), мм"].get())
                
                K = S + 1; K1 = S1 + 1 # Конструктивные катеты шва У5
                F_weld = (0.5 * K * K1) + (2 / 3 * max(K, K1) * g)
                L_weld = math.pi * D
                m_dep = (F_weld * L_weld * rho / 1000000) * n
                
                res = f"=== РЕЗУЛЬТАТ РАСЧЕТА ШВА У5 (ГОСТ 16037) ===\n" \
                      f"• Расчетный внешний катет шва (K):   {K:.1f} мм\n" \
                      f"• Расчетный внутренний катет (K1):  {K1:.1f} мм\n" \
                      f"--------------------------------------------------\n" \
                      f"▶ ПОТРЕБНОСТЬ ЭЛЕКТРОДОВ (ММА):     {m_dep * 1.65:.3f} кг\n" \
                      f"▶ ПОТРЕБНОСТЬ ПРОВОЛОКИ (MIG/MAG):  {m_dep * 1.15:.3f} кг\n"
            else:
                k = float(self.w_entries["Катет шва, мм"].get())
                L = float(self.w_entries["Длина шва, мм"].get())
                loss = float(self.w_entries["Доп.% на огарки"].get())
                F_weld = 0.5 * (k ** 2)
                m_dep = (F_weld * L * rho / 1000000) * (1 + loss/100)
                res = f"=== РЕЗУЛЬТАТ РАСЧЕТА ЛИСТОВЫХ КОНСТРУКЦИЙ ===\n• Площадь шва: {F_weld:.2f} мм²\n▶ РАСХОД МАРКИ АНО-4/ОЗС с учетом огарков: {m_dep * 1.62:.3f} кг\n"
        except Exception as e: res = f"Ошибка ввода параметров шва: {e}"
        self.w_res_text.delete("1.0", tk.END); self.w_res_text.insert("1.0", res)
    def open_electrodes_window(self):
        # Полноценная реализация Окна со Скриншота №2
        win = tk.Toplevel(self.root); win.title("Выбор электрода по типу сталей"); win.geometry("760x520")
        ttk.Label(win, text="Выбор электрода в зависимости от свариваемого материала", font=("Segoe UI", 11, "bold")).pack(pady=6)
        
        cats = [
            "Сварка углеродистых, низколегированных конструкционных сталей",
            "Сварка легированных конструкционных сталей с повышенной прочностью",
            "Сварка теплоустойчивых сталей по ГОСТ 9467",
            "Сварка жаропрочных, жаростойких спецсталей",
            "Сварка коррозионно-стойких сплавов (Нержавеющая сталь)",
            "Сварка чугуна и его наплавки"
        ]
        lb_cat = tk.Listbox(win, height=6, font=("Segoe UI", 9)); lb_cat.pack(fill="x", padx=10, pady=4)
        for c in cats: lb_cat.insert("end", c)
        
        f_bot = ttk.Frame(win); f_bot.pack(fill="both", expand=True, padx=10, pady=5)
        lb_m = tk.Listbox(f_bot, width=22); lb_m.pack(side="left", fill="y", pady=5)
        
        t_all = tk.Text(f_bot, bg="#ffffff", height=4, font=("Consolas", 10)); t_all.pack(fill="x", pady=5)
        t_desc = tk.Text(f_bot, bg="#f8f9fa", font=("Segoe UI", 10)); t_desc.pack(fill="both", expand=True, pady=5)
        
        def on_cat_select(e):
            sel = lb_cat.curselection()
            if not sel: return
            idx = sel[0]
            lb_m.delete(0, "end")
            if idx == 0:
                mar = ["АНО-3", "АНО-4", "АНО-6", "УОНИ-13/45", "УОНИ-13/55", "МР-3"]; txt = "АНО-4, АНО-6, УОНИ-13/45, УОНИ-13/55, МР-3, ОЗС-12, ОЗС-4"; desc = "Предназначены для ручной дуговой сварки конструкций из углеродистых сталей с содержанием углерода до 0.25%."
            elif idx == 2:
                mar = ["ТМЛ-1", "ТМЛ-3У", "ЦУ-2М", "ЦЛ-39"]; txt = "ТМЛ-1, ТМЛ-3У, ЦУ-2М, ЦЛ-39, ЦЛ-6"; desc = "Для сварки элементов котлов, сосудов и паропроводов, работающих при высоких температурах (до 565°С)."
            else:
                mar = ["ОЗЛ-8", "ЦЛ-11", "ЦЧ-4"]; txt = "ОЗЛ-8, ЦЛ-11, ЦЧ-4, ОЗА-1"; desc = "Специализированные электроды для высоколегированных сталей, нержавейки и ремонтной наплавки чугуна."
            for m in mar: lb_m.insert("end", m)
            t_all.delete("1.0", "end"); t_all.insert("1.0", txt)
            t_desc.delete("1.0", "end"); t_desc.insert("1.0", desc)
            
        lb_cat.bind("<<ListboxSelect>>", on_cat_select)
        lb_cat.select_set(0); on_cat_select(None)

    def open_gost_designation_window(self):
        # Полноценная реализация Окна со Скриншота №3 (ГОСТ 2.312-72)
        win = tk.Toplevel(self.root); win.title("Условное обозначение швов ГОСТ 2.312-72"); win.geometry("780x560")
        ttk.Label(win, text="Условное обозначение сварных швов на чертежах (ГОСТ 2.312-72)", font=("Segoe UI", 10, "bold"), fg="purple").pack(pady=5)
        
        f_top = ttk.Frame(win); f_top.pack(fill="x", padx=10, pady=5)
        for i in range(1, 7):
            ttk.Label(f_top, text=f" {i} ").pack(side="left", padx=15)
            ttk.Entry(f_top, width=6).pack(side="left", padx=2)
            
        lbl_box = ttk.LabelFrame(win, text=" Место для значка "); lbl_box.pack(fill="x", padx=15, pady=5)
        ttk.Label(lbl_box, text="О - Сварка по замкнутому контуру\n] - Монтажный шов шва конструкции", font=("Consolas", 10)).pack(padx=10, pady=5)
        
        ttk.Label(win, text="1 - Стандарт на тип и конструктивные элементы швов:", font=("Segoe UI", 10, "bold"), fg="green").pack(anchor="w", padx=15)
        lb = tk.Listbox(win, height=4); lb.pack(fill="x", padx=15, pady=2)
        for g in ["ГОСТ 5264-80 (Ручная дуговая сталей)", "ГОСТ 16037-80 (Стальные трубопроводы)", "ГОСТ 14771-76 (Дуковая в защитных газах)"]: lb.insert("end", g)
        
        ttk.Label(win, text="2 - Буквенно-цифровое обозначение шва по стандарту:", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=15, pady=3)
        ttk.Label(win, text="С1-С21, С23-С28 (Стыковые);  У1-У10 (Угловые);  Т1-Т9 (Тавровые);  Н1-Н2 (Нахлест)", font=("Consolas", 10), relief="solid", bd=1, bg="#ffffff").pack(fill="x", padx=15, pady=2)
        
        ttk.Label(win, text="6 - Вспомогательные знаки для обозначения:", font=("Segoe UI", 9, "bold"), fg="purple").pack(anchor="w", padx=15, pady=3)
        f_rad = ttk.Frame(win); f_rad.pack(fill="x", padx=15, pady=2)
        for z in ["𝓞 (Замкнутый)", "⌿ (Монтажный)", "⎓ (Усиление снять)", "Smooth"]: ttk.Radiobutton(f_rad, text=z).pack(side="left", padx=12)
    def init_insulation_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="环 Изоляция")
        inputs = ttk.LabelFrame(tab, text=" Геометрический расчет объемов теплоизоляции по схеме ")
        inputs.pack(fill="x", padx=15, pady=10)
        
        ttk.Label(inputs, text="Тип прокладки сети:").grid(row=0, column=0, padx=5, pady=6, sticky="w")
        self.iso_calc_type = ttk.Combobox(inputs, values=["Одна труба", "Несколько труб (Группа в оболочке)"], state="readonly", width=30)
        self.iso_calc_type.set("Одна труба"); self.iso_calc_type.grid(row=0, column=1, padx=5, pady=6, sticky="w")
        self.iso_calc_type.bind("<<ComboboxSelected>>", self.on_iso_calc_type_change)
        
        self.iso_inputs_frame = ttk.Frame(inputs); self.iso_inputs_frame.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky="ew")
        self.iso_entries = {}
        
        btn_frame = ttk.Frame(inputs); btn_frame.grid(row=2, column=0, columnspan=4, pady=10, sticky="ew")
        ttk.Button(btn_frame, text="⚡ Рассчитать геометрические объемы изоляции", command=self.calculate_only_insulation, width=45).pack(side="left", padx=5)
        
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
                S_r = math.pi * D * L; S_pi = math.pi * (D + 2 * t) * L
                V_i = (math.pi / 4) * (((D + 2 * t) ** 2) - (D ** 2)) * L
                res = f"📝 ВЕДОМОСТЬ ОБЪЕМОВ ИЗОЛЯЦИОННЫХ РАБОТ СГК (ОДНОТРУБНЫЙ УЧАСТОК):\n--------------------------------------------------\n▶ Площадь обертывания (окраски) Sr:        {S_r:.6f} м²\n▶ Площадь покровного слоя Spi:             {S_pi:.6f} м²\n▶ ИТОГОВЫЙ ОБЪЕМ ТЕПЛОИЗОЛЯЦИИ Vi:         {V_i:.6f} м³\n"
            else:
                D1 = float(self.iso_entries["Диаметр крайних D1, м"].get()); D2 = float(self.iso_entries["Диаметр средних D2, м"].get())
                t = float(self.iso_entries["Толщина изоляции t, м"].get()); p = float(self.iso_entries["Зазор труб p, м"].get()); L = float(self.iso_entries["Длина участка L, м"].get())
                M = D1 + D2 + (p * 2); B = (D1 * 2) + D2 + (p * 2) + (t * 2)
                S_r = ((math.pi * D1) + (M * 2)) * L; S_pi = ((math.pi * (D1 + 2 * t)) + (M * 2)) * L
                V_i = (((math.pi / 4) * ((D1 + 2 * t) ** 2 - D1 ** 2)) + (M * 2 * t)) * L
                res = f"📝 ВЕДОМОСТЬ ОБЪЕМОВ ИЗОЛЯЦИОННЫХ РАБОТ СГК (ГРУППОВАЯ ОСЬ):\n--------------------------------------------------\n• Габаритная ширина блока B:               {B:.3f} м\n--------------------------------------------------\n▶ Площадь обертывания (окраски) Sr:        {S_r:.6f} м²\n▶ Площадь покровного слоя Spi:             {S_pi:.6f} м²\n▶ ИТОГОВЫЙ ОБЪЕМ ТЕПЛОИЗОЛЯЦИИ Vi:         {V_i:.6f} м³\n"
        except Exception as e: res = f"❌ Ошибка: {e}"
        self.iso_output.delete("1.0", tk.END); self.iso_output.insert("1.0", res)

if __name__ == "__main__":
    root = tk.Tk()
    app = MetallistProApp(root)
    root.mainloop()
