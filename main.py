import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from ttkthemes import ThemedStyle
import math

class MetallistProApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор Металлиста PRO — Сметная группа СГК")
        self.root.geometry("1220x960")
        
        # Настройка графической темы оформления Arc
        self.style = ThemedStyle(self.root)
        self.current_theme = "arc"
        self.style.set_theme(self.current_theme)
        self.style.configure('.', font=('Segoe UI', 10))
        self.style.configure('TNotebook.Tab', font=('Segoe UI', 10, 'bold'), padding=5)
        
        # Глобальная панель настроек материала сессии
        top_ctrl = ttk.LabelFrame(root, text=" Глобальные настройки сессии ")
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
        
        # Главный контейнер вкладок
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Последовательный вызов всех 8 вкладок комплекса
        self.init_geometry_tab()
        self.init_sortament_tab()
        self.init_detali_tab()
        self.init_metiz_tab()          
        self.init_welding_tab()        
        self.init_electrodes_tab()     
        self.init_designation_tab()    
        self.init_insulation_tab()
        
        # Крупный фирменный оранжевый подвал СГК 
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
        elif "Алюминий" in mat: return 2.70
        elif "Бронза" in mat: return 8.80
        elif "Латунь" in mat: return 8.50
        elif "Медь" in mat: return 8.94
        elif "Никель" in mat: return 8.90
        elif "Чугун" in mat: return 7.20
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
            if angle_deg >= 360: self.geom_canvas.create_oval(cx-r_px, cy-r_px, cx+r_px, cy+r_px, fill="#e9ecef", outline="black")
            else: self.geom_canvas.create_arc(cx-r_px, cy-r_px, cx+r_px, cy+r_px, start=0, extent=angle_deg, fill="#e9ecef", outline="black")
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
                res += f"Площадь сечения: {(math.sqrt(3)/2)*(S**2):.2f} мм²\nВес заготовки: {((math.sqrt(3)/2)*(S**2)*L*rho)/1000000:.3f} кг\n"
        except Exception as e: res += f"Ошибка: {str(e)}"
        self.geom_result.config(state="normal"); self.geom_result.delete("1.0", tk.END); self.geom_result.insert("1.0", res); self.geom_result.config(state="disabled")
    def init_sortament_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📊 Сортамент")
        top = ttk.LabelFrame(tab, text=" Параметры проката ")
        top.pack(fill="x", padx=15, pady=10)
        
        ttk.Label(top, text="Тип проката:").grid(row=0, column=0, padx=5, pady=8, sticky="w")
        self.sort_profile = ttk.Combobox(top, values=["Двутавр ГОСТ 8239-89", "Швеллер ГОСТ 8240-97", "Труба Круглая ГОСТ 10704-91", "Лист ГОСТ 19903-74"], state="readonly", width=25)
        self.sort_profile.set("Труба Круглая ГОСТ 10704-91"); self.sort_profile.grid(row=0, column=1, padx=5, pady=8, sticky="w")
        self.sort_profile.bind("<<ComboboxSelected>>", self.on_sortament_profile_change)
        
        self.sort_len_frame = ttk.Frame(top)
        self.sort_len_frame.grid(row=0, column=2, padx=10, pady=8, sticky="w")
        ttk.Label(self.sort_len_frame, text="Длина, м:").pack(side="left")
        self.sort_length = ttk.Entry(self.sort_len_frame, width=8); self.sort_length.insert(0, "12"); self.sort_length.pack(side="left", padx=5)
        
        ttk.Button(top, text="Рассчитать прокат", command=self.calculate_sortament_weight).grid(row=0, column=3, padx=15, pady=8)
        
        self.sort_tree = ttk.Treeview(tab, columns=("num", "weight"), show="headings", height=8)
        self.sort_tree.heading("num", text="Типоразмер / Профиль по ГОСТ"); self.sort_tree.heading("weight", text="Вес 1 погонного метра, кг")
        self.sort_tree.column("num", width=350, anchor="center"); self.sort_tree.column("weight", width=250, anchor="center")
        self.sort_tree.pack(fill="x", padx=15, pady=5)
        
        self.sort_output = tk.Text(tab, bg="#ffffff", font=("Consolas", 10), height=10, bd=1, relief="solid")
        self.sort_output.pack(fill="both", expand=True, padx=15, pady=10)
        self.on_sortament_profile_change()

    def on_sortament_profile_change(self, event=None):
        for r in self.sort_tree.get_children(): self.sort_tree.delete(r)
        prof = self.sort_profile.get()
        if "Двутавр" in prof:
            data = [("№ 10", "9.46"), ("№ 14", "13.70"), ("№ 20", "21.00"), ("№ 30", "36.50"), ("№ 45", "66.50"), ("№ 60", "108.00")]
        elif "Швеллер" in prof:
            data = [("5У", "4.84"), ("10У", "8.59"), ("20У", "18.40"), ("30У", "31.80"), ("40У", "48.30")]
        elif "Лист" in prof:
            data = [("Лист t=2мм (1500х6000)", "141.3"), ("Лист t=4мм (1500х6000)", "282.6"), ("Лист t=10мм (2000х6000)", "942.0"), ("Лист t=20мм (2000х6000)", "1884.0")]
        else:
            data = [
                ("∅57х3.5", "4.62"), ("∅89х4", "8.38"), ("∅108х4", "10.26"), ("∅159х5", "18.99"), 
                ("∅219х6", "31.52"), ("∅273х7", "45.92"), ("∅325х8", "62.54"), ("∅426х9", "92.55"), 
                ("∅530х10", "128.24"), ("∅630х10", "152.90"), ("∅720х10", "175.10"), ("∅820х10", "199.76"), 
                ("∅920х10", "224.42"), ("∅1024х10", "250.07"), ("∅1220х12", "357.50"), ("∅1420х14", "499.20")
            ]
        for item in data: self.sort_tree.insert("", "end", values=item)

    def calculate_sortament_weight(self):
        rho = self.get_density(); prof = self.sort_profile.get()
        sel = self.sort_tree.focus()
        if not sel: messagebox.showwarning("Внимание", "Выберите строку сортамента в таблице!"); return
        val = self.sort_tree.item(sel, "values")
        try: L = float(self.sort_length.get())
        except: L = 12.0
        total = float(val) * (rho / 7.85) * L
        res = f"📊 РЕЗУЛЬТАТ РАСЧЕТА СОРТАМЕНТА:\n• Профиль: {prof} ({val})\n• Расчетная длина: {L} м\n▶ ИТОГОВЫЙ СМЕТНЫЙ ВЕС ПАРТИИ: {total:.3f} кг\n"
        self.sort_output.delete("1.0", tk.END); self.sort_output.insert("1.0", res)
    def init_detali_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔧 Детали трубопроводов")
        left = ttk.LabelFrame(tab, text=" Параметры арматуры ")
        left.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        
        ttk.Label(left, text="Элемент теплосети:").pack(anchor="w", padx=10, pady=2)
        self.det_type = ttk.Combobox(left, values=["Отвод 90° ГОСТ 17375-2001", "Фланец ГОСТ 33259-2015"], state="readonly", width=30)
        self.det_type.set("Отвод 90° ГОСТ 17375-2001"); self.det_type.pack(fill="x", padx=10, pady=4)
        
        ttk.Label(left, text="Типоразмер Ду (DN):").pack(anchor="w", padx=10, pady=2)
        self.det_dy = ttk.Combobox(left, values=[
            "Ду50 (∅57)", "Ду80 (∅89)", "Ду100 (∅108)", "Ду150 (∅159)", 
            "Ду200 (∅219)", "Ду250 (∅273)", "Ду300 (∅325)", "Ду400 (∅426)", 
            "Ду500 (∅530)", "Ду600 (∅630)", "Ду700 (∅720)", "Ду800 (∅820)", 
            "Ду900 (∅920)", "Ду1000 (∅1024)"
        ], state="readonly")
        self.det_dy.set("Ду150 (∅159)"); self.det_dy.pack(fill="x", padx=10, pady=4)
        
        ttk.Label(left, text="Количество деталей, шт:").pack(anchor="w", padx=10, pady=2)
        self.det_cnt = ttk.Entry(left); self.det_cnt.insert(0, "10"); self.det_cnt.pack(fill="x", padx=10, pady=4)
        ttk.Button(left, text="Посчитать массу фасонины", command=self.proc_detali_calc).pack(fill="x", padx=10, pady=10)
        
        self.det_output = tk.Text(tab, bg="#ffffff", font=("Consolas", 10), bd=1, relief="solid")
        self.det_output.pack(side="right", fill="both", expand=True, padx=15, pady=15)

    def proc_detali_calc(self):
        t, d = self.det_type.get(), self.det_dy.get()
        try: c = float(self.det_cnt.get())
        except: c = 1.0
        w_map = {
            "Ду50": 0.7, "Ду80": 2.1, "Ду100": 3.3, "Ду150": 8.1, "Ду200": 17.2, "Ду250": 33.5, 
            "Ду300": 51.4, "Ду400": 98.6, "Ду500": 173.0, "Ду600": 248.0, "Ду700": 345.0, 
            "Ду800": 482.0, "Ду900": 634.0, "Ду1000": 810.0
        }
        prefix = d.split(" ")[0]
        w = w_map.get(prefix, 8.1)
        total = w * c * (self.get_density() / 7.85)
        self.det_output.delete("1.0", "end")
        self.det_output.insert("1.0", f"🔧 ВЕДОМОСТЬ ФАСОННЫХ ЭЛЕМЕНТОВ СГК:\n• Элемент: {t}\n• Типоразмер: {d}\n• Паспортная масса 1 ед.: {w:.2f} кг\n• Количество: {int(c)} шт\n----------------------------------------\n▶ ИТОГОВАЯ МАССА ПАРТИИ: {total:.2f} кг\n")
    def init_metiz_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔩 Метизы")
        
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=1)
        
        # ---------------------------------------------------------------------
        # БЛОК 1: БОЛТЫ (ГОСТ 7798, Высокопрочные 52644, Крупные 10602)
        # ---------------------------------------------------------------------
        f1 = ttk.LabelFrame(tab, text=" БОЛТЫ ЭНЕРГЕТИЧЕСКИЕ ")
        f1.grid(row=0, column=0, padx=10, pady=8, sticky="nsew")
        
        self.b_gost = ttk.Combobox(f1, values=["ГОСТ 7798-70 шестигранные", "ГОСТ R 52644-2006 высокопрочные", "ГОСТ 10602-94 крупные (от М42)"], state="readonly")
        self.b_gost.set("ГОСТ 7798-70 шестигранные"); self.b_gost.pack(fill="x", padx=8, pady=3)
        self.b_mat = ttk.Combobox(f1, values=["Материал-сталь", "Материал-нержавейка", "Материал-латунь"], state="readonly")
        self.b_mat.set("Материал-сталь"); self.b_mat.pack(fill="x", padx=8, pady=3)
        
        g1 = ttk.Frame(f1); g1.pack(fill="x", padx=8, pady=5)
        ttk.Label(g1, text="n штук", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, padx=2)
        ttk.Label(g1, text="диаметр", font=("Segoe UI", 9, "bold")).grid(row=0, column=1, padx=2)
        ttk.Label(g1, text="Длина", font=("Segoe UI", 9, "bold")).grid(row=0, column=2, padx=2)
        ttk.Label(g1, text="Масса ед.", font=("Segoe UI", 9, "bold")).grid(row=0, column=3, padx=2)
        ttk.Label(g1, text="Общая масса, кг", font=("Segoe UI", 9, "bold")).grid(row=0, column=4, padx=2)
        
        self.b_pcs = tk.Entry(g1, width=7, bg="#fff2cc", justify="center"); self.b_pcs.insert(0, "8"); self.b_pcs.grid(row=1, column=0, pady=2)
        self.b_d = ttk.Combobox(g1, values=["М10", "М12", "М16", "М20", "М24", "М30", "М36", "М42", "М48"], width=7, state="readonly"); self.b_d.set("М16"); self.b_d.grid(row=1, column=1, pady=2)
        self.b_l = ttk.Combobox(g1, values=[str(x) for x in range(40, 161, 10)] + [str(x) for x in range(180, 301, 20)], width=6, state="readonly"); self.b_l.set("50"); self.b_l.grid(row=1, column=2, pady=2)
        self.b_one = tk.Entry(g1, width=9, justify="center"); self.b_one.grid(row=1, column=3, pady=2)
        self.b_tot = tk.Entry(g1, width=10, justify="center"); self.b_tot.grid(row=1, column=4, pady=2)
        
        g1_rev = ttk.Frame(f1); g1_rev.pack(fill="x", padx=8, pady=5)
        ttk.Label(g1_rev, text="кг", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, padx=2)
        ttk.Label(g1_rev, text="диаметр", font=("Segoe UI", 9, "bold")).grid(row=0, column=1, padx=2)
        ttk.Label(g1_rev, text="Длина", font=("Segoe UI", 9, "bold")).grid(row=0, column=2, padx=2)
        ttk.Label(g1_rev, text="Кол-во шт.", font=("Segoe UI", 9, "bold")).grid(row=0, column=3, padx=2)
        
        self.b_kg_rev = tk.Entry(g1_rev, width=7, bg="#fff2cc", justify="center"); self.b_kg_rev.insert(0, "1"); self.b_kg_rev.grid(row=1, column=0, pady=2)
        self.b_d_rev = ttk.Combobox(g1_rev, values=["М10", "М12", "М16", "М20", "М24", "М30", "М36", "М42", "М48"], width=7, state="readonly"); self.b_d_rev.set("М16"); self.b_d_rev.grid(row=1, column=1, pady=2)
        self.b_l_rev = ttk.Combobox(g1_rev, values=[str(x) for x in range(40, 161, 10)] + [str(x) for x in range(180, 301, 20)], width=6, state="readonly"); self.b_l_rev.set("50"); self.b_l_rev.grid(row=1, column=2, pady=2)
        self.b_pcs_rev = tk.Entry(g1_rev, width=10, justify="center"); self.b_pcs_rev.grid(row=1, column=3, pady=2)

        # ---------------------------------------------------------------------
        # БЛОК 2: ГАЙКИ (ГОСТ 5915, Фланцевые высокотемпературные 9064)
        # ---------------------------------------------------------------------
        f2 = ttk.LabelFrame(tab, text=" ГАЙКИ МАГИСТРАЛЬНЫЕ ")
        f2.grid(row=0, column=1, padx=10, pady=8, sticky="nsew")
        
        self.n_gost = ttk.Combobox(f2, values=["ГОСТ 5915-70 класс точности Б", "ГОСТ 9064-75 фланцевые для ТЭЦ (до 650°С)", "ГОСТ R 52645-2006 высокопрочные"], state="readonly")
        self.n_gost.set("ГОСТ 5915-70 класс точности Б"); self.n_gost.pack(fill="x", padx=8, pady=3)
        self.n_mat = ttk.Combobox(f2, values=["Материал-сталь", "Материал-нержавейка"], state="readonly")
        self.n_mat.set("Материал-сталь"); self.n_mat.pack(fill="x", padx=8, pady=3)
        
        g2 = ttk.Frame(f2); g2.pack(fill="x", padx=8, pady=5)
        ttk.Label(g2, text="n штук", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, padx=2)
        ttk.Label(g2, text="диаметр", font=("Segoe UI", 9, "bold")).grid(row=0, column=1, padx=2)
        ttk.Label(g2, text="Масса ед.", font=("Segoe UI", 9, "bold")).grid(row=0, column=2, padx=2)
        ttk.Label(g2, text="Общая масса, кг", font=("Segoe UI", 9, "bold")).grid(row=0, column=3, padx=2)
        
        self.n_pcs = tk.Entry(g2, width=7, bg="#fff2cc", justify="center"); self.n_pcs.insert(0, "8"); self.n_pcs.grid(row=1, column=0, pady=2)
        self.n_d = ttk.Combobox(g2, values=["М10", "М12", "М16", "М20", "М24", "М30", "М36", "М42", "М48"], width=8, state="readonly"); self.n_d.set("М16"); self.n_d.grid(row=1, column=1, pady=2)
        self.n_one = tk.Entry(g2, width=10, justify="center"); self.n_one.grid(row=1, column=2, pady=2)
        self.n_tot = tk.Entry(g2, width=12, justify="center"); self.n_tot.grid(row=1, column=3, pady=2)
        
        g2_rev = ttk.Frame(f2); g2_rev.pack(fill="x", padx=8, pady=5)
        ttk.Label(g2_rev, text="кг", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, padx=2)
        ttk.Label(g2_rev, text="диаметр", font=("Segoe UI", 9, "bold")).grid(row=0, column=1, padx=2)
        ttk.Label(g2_rev, text="Кол-во шт.", font=("Segoe UI", 9, "bold")).grid(row=0, column=2, padx=2)
        
        self.n_kg_rev = tk.Entry(g2_rev, width=7, bg="#fff2cc", justify="center"); self.n_kg_rev.insert(0, "1"); self.n_kg_rev.grid(row=1, column=0, pady=2)
        self.n_d_rev = ttk.Combobox(g2_rev, values=["М10", "М12", "М16", "М20", "М24", "М30", "М36", "М42", "М48"], width=8, state="readonly"); self.n_d_rev.set("М16"); self.n_d_rev.grid(row=1, column=1, pady=2)
        self.n_pcs_rev = tk.Entry(g2_rev, width=12, justify="center"); self.n_pcs_rev.grid(row=1, column=2, pady=2)
        # ---------------------------------------------------------------------
        # БЛОК 3: ШАЙБЫ (ГОСТ 11371, Фланцевые 9065, Гроверные 6402)
        # ---------------------------------------------------------------------
        f3 = ttk.LabelFrame(tab, text=" ШАЙБЫ И ГРОВЕРЫ ")
        f3.grid(row=1, column=0, padx=10, pady=8, sticky="nsew")
        
        self.w_gost = ttk.Combobox(f3, values=["ГОСТ 11371-78 плоские класс А", "ГОСТ 9065-75 фланцевые уплотнительные", "ГОСТ 6402-70 пружинные гроверные"], state="readonly")
        self.w_gost.set("ГОСТ 11371-78 плоские класс А"); self.w_gost.pack(fill="x", padx=8, pady=3)
        self.w_mat = ttk.Combobox(f3, values=["Материал-сталь", "Материал-нержавейка"], state="readonly")
        self.w_mat.set("Материал-сталь"); self.w_mat.pack(fill="x", padx=8, pady=3)
        
        g3 = ttk.Frame(f3); g3.pack(fill="x", padx=8, pady=5)
        ttk.Label(g3, text="n штук", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, padx=2)
        ttk.Label(g3, text="тип (размер)", font=("Segoe UI", 9, "bold")).grid(row=0, column=1, padx=2)
        ttk.Label(g3, text="Масса ед.", font=("Segoe UI", 9, "bold")).grid(row=0, column=2, padx=2)
        ttk.Label(g3, text="Общая масса, кг", font=("Segoe UI", 9, "bold")).grid(row=0, column=3, padx=2)
        
        self.w_pcs = tk.Entry(g3, width=7, bg="#fff2cc", justify="center"); self.w_pcs.insert(0, "100"); self.w_pcs.grid(row=1, column=0, pady=2)
        self.w_size = ttk.Combobox(g3, values=["М10", "М12", "М16", "М20", "М24", "М30", "М36", "М42", "М48"], width=9, state="readonly"); self.w_size.set("М16"); self.w_size.grid(row=1, column=1, pady=2)
        self.w_one = tk.Entry(g3, width=10, justify="center"); self.w_one.grid(row=1, column=2, pady=2)
        self.w_tot = tk.Entry(g3, width=12, justify="center"); self.w_tot.grid(row=1, column=3, pady=2)
        
        g3_rev = ttk.Frame(f3); g3_rev.pack(fill="x", padx=8, pady=5)
        ttk.Label(g3_rev, text="кг", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, padx=2)
        ttk.Label(g3_rev, text="диаметр", font=("Segoe UI", 9, "bold")).grid(row=0, column=1, padx=2)
        ttk.Label(g3_rev, text="Кол-во шт.", font=("Segoe UI", 9, "bold")).grid(row=0, column=2, padx=2)
        
        self.w_kg_rev = tk.Entry(g3_rev, width=7, bg="#fff2cc", justify="center"); self.w_kg_rev.insert(0, "1"); self.w_kg_rev.grid(row=1, column=0, pady=2)
        self.w_size_rev = ttk.Combobox(g3_rev, values=["М10", "М12", "М16", "М20", "М24", "М30", "М36", "М42", "М48"], width=9, state="readonly"); self.w_size_rev.set("М16"); self.w_size_rev.grid(row=1, column=1, pady=2)
        self.w_pcs_rev = tk.Entry(g3_rev, width=12, justify="center"); self.w_pcs_rev.grid(row=1, column=2, pady=2)

        # ---------------------------------------------------------------------
        # БЛОК 4: ШПИЛЬКИ И САМОРЕЗЫ (ГОСТ 9066 высокого давления, ГОСТ 10619)
        # ---------------------------------------------------------------------
        f4 = ttk.LabelFrame(tab, text=" ШПИЛЬКИ ТЕПЛОСЕТЕЙ И САМОРЕЗЫ ")
        f4.grid(row=1, column=1, padx=10, pady=8, sticky="nsew")
        
        self.s_gost = ttk.Combobox(f4, values=["ГОСТ 9066-75 фланцевые шпильки ТЭЦ", "ГОСТ 22032-76 с ввинчиваемым концом", "ГОСТ 10619-80 саморезы потайные"], state="readonly")
        self.s_gost.set("ГОСТ 9066-75 фланцевые шпильки ТЭЦ"); self.s_gost.pack(fill="x", padx=8, pady=3)
        self.s_mat = ttk.Combobox(f4, values=["Материал-сталь", "Материал-нержавейка"], state="readonly")
        self.s_mat.set("Материал-сталь"); self.s_mat.pack(fill="x", padx=8, pady=3)
        
        g4 = ttk.Frame(f4); g4.pack(fill="x", padx=8, pady=5)
        ttk.Label(g4, text="n штук", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, padx=2)
        ttk.Label(g4, text="dxL (размер)", font=("Segoe UI", 9, "bold")).grid(row=0, column=1, padx=2)
        ttk.Label(g4, text="Масса ед.", font=("Segoe UI", 9, "bold")).grid(row=0, column=2, padx=2)
        ttk.Label(g4, text="Общая масса, кг", font=("Segoe UI", 9, "bold")).grid(row=0, column=3, padx=2)
        
        self.s_pcs = tk.Entry(g4, width=7, bg="#fff2cc", justify="center"); self.s_pcs.insert(0, "100"); self.s_pcs.grid(row=1, column=0, pady=2)
        self.s_size = ttk.Combobox(f4, values=["М12х60", "М16х90", "М20x110", "М24x130", "М30x150", "М36x180", "М42x220", "М48x260", "2.5x16", "4.2x25"], width=12, state="readonly"); self.s_size.set("М16х90"); self.s_size.grid(row=1, column=1, pady=2)
        self.s_one = tk.Entry(g4, width=10, justify="center"); self.s_one.grid(row=1, column=2, pady=2)
        self.s_tot = tk.Entry(g4, width=12, justify="center"); self.s_tot.grid(row=1, column=3, pady=2)
        
        g4_rev = ttk.Frame(f4); g4_rev.pack(fill="x", padx=8, pady=5)
        ttk.Label(g4_rev, text="кг", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, padx=2)
        ttk.Label(g4_rev, text="dxL (размер)", font=("Segoe UI", 9, "bold")).grid(row=0, column=1, padx=2)
        ttk.Label(g4_rev, text="Кол-во шт.", font=("Segoe UI", 9, "bold")).grid(row=0, column=2, padx=2)
        
        self.s_kg_rev = tk.Entry(g4_rev, width=7, bg="#fff2cc", justify="center"); self.s_kg_rev.insert(0, "1"); self.s_kg_rev.grid(row=1, column=0, pady=2)
        self.s_size_rev = ttk.Combobox(f4, values=["М12х60", "М16х90", "М20x110", "М24x130", "М30x150", "М36x180", "М42x220", "М48x260", "2.5x16", "4.2x25"], width=12, state="readonly"); self.s_size_rev.set("М16х90"); self.s_size_rev.grid(row=1, column=2, pady=2)
        self.s_pcs_rev = tk.Entry(g4_rev, width=12, justify="center"); self.s_pcs_rev.grid(row=1, column=3, pady=2)
        
        self.bind_metiz_auto_calculation()
    def bind_metiz_auto_calculation(self):
        for e in [self.b_pcs, self.b_kg_rev, self.n_pcs, self.n_kg_rev, self.w_pcs, self.w_kg_rev, self.s_pcs, self.s_kg_rev]:
            e.bind("<KeyRelease>", lambda event: self.proc_all_metiz_logic())
        for c in [self.b_d, self.b_l, self.b_d_rev, self.b_l_rev, self.b_gost, self.b_mat,
                  self.n_d, self.n_d_rev, self.n_gost, self.n_mat,
                  self.w_size, self.w_size_rev, self.w_gost, self.w_mat,
                  self.s_size, self.s_size_rev, self.s_gost, self.s_mat]:
            c.bind("<<ComboboxSelected>>", lambda event: self.proc_all_metiz_logic())
        self.proc_all_metiz_logic()

    def proc_all_metiz_logic(self):
        rho_coeff = self.get_density() / 7.85

        # --- 1. РАСЧЕТ БОЛТОВ ---
        base_bolt = {"М10": 0.068, "М12": 0.102, "М16": 0.198, "М20": 0.342, "М24": 0.564, "М30": 0.985, "М36": 1.540, "М42": 2.280, "М48": 3.120}
        bd = self.b_d.get(); bl = float(self.b_l.get()); b_g = self.b_gost.get()
        w_b_base = base_bolt.get(bd, 0.198) * (bl / 90.0)
        if "52644" in b_g: w_b_base *= 1.15
        w_b_one = w_b_base * rho_coeff
        
        self.b_one.config(state="normal"); self.b_one.delete(0, "end"); self.b_one.insert(0, f"{w_b_one:.3f}"); self.b_one.config(state="readonly")
        try:
            bp = float(self.b_pcs.get())
            self.b_tot.config(state="normal"); self.b_tot.delete(0, "end"); self.b_tot.insert(0, f"{bp * w_b_one:.2f}"); self.b_tot.config(state="readonly")
        except: pass
        try:
            b_kg = float(self.b_kg_rev.get())
            bd_r = self.b_d_rev.get(); bl_r = float(self.b_l_rev.get())
            w_br_base = base_bolt.get(bd_r, 0.198) * (bl_r / 90.0)
            if "52644" in b_g: w_br_base *= 1.15
            pcs_r = int(b_kg / (w_br_base * rho_coeff)) if (w_br_base * rho_coeff) > 0 else 0
            self.b_pcs_rev.config(state="normal"); self.b_pcs_rev.delete(0, "end"); self.b_pcs_rev.insert(0, str(pcs_r)); self.b_pcs_rev.config(state="readonly")
        except: pass

        # --- 2. РАСЧЕТ ГАЕК ---
        base_nut = {"М10": 0.011, "М12": 0.015, "М16": 0.033, "М20": 0.064, "М24": 0.110, "М30": 0.230, "М36": 0.390, "М42": 0.620, "М48": 0.960}
        nd = self.n_d.get(); n_g = self.n_gost.get()
        w_n_base = base_nut.get(nd, 0.033)
        if "9064" in n_g: w_n_base *= 1.25
        w_n_one = w_n_base * rho_coeff
        
        self.n_one.config(state="normal"); self.n_one.delete(0, "end"); self.n_one.insert(0, f"{w_n_one:.4f}"); self.n_one.config(state="readonly")
        try:
            np = float(self.n_pcs.get())
            self.n_tot.config(state="normal"); self.n_tot.delete(0, "end"); self.n_tot.insert(0, f"{np * w_n_one:.2f}"); self.n_tot.config(state="readonly")
        except: pass
        try:
            n_kg = float(self.n_kg_rev.get())
            nd_r = self.n_d_rev.get()
            w_nr_base = base_nut.get(nd_r, 0.033)
            if "9064" in n_g: w_nr_base *= 1.25
            pcs_r = int(n_kg / (w_nr_base * rho_coeff)) if (w_nr_base * rho_coeff) > 0 else 0
            self.n_pcs_rev.config(state="normal"); self.n_pcs_rev.delete(0, "end"); self.n_pcs_rev.insert(0, str(pcs_r)); self.n_pcs_rev.config(state="readonly")
        except: pass

        # --- 3. РАСЧЕТ ШАЙБ ---
        base_washer = {"М10": 0.004, "М12": 0.006, "М16": 0.011, "М20": 0.017, "М24": 0.032, "М30": 0.054, "М36": 0.092, "М42": 0.182, "М48": 0.274}
        ws = self.w_size.get(); w_g = self.w_gost.get()
        w_w_base = base_washer.get(ws, 0.011)
        if "9065" in w_g: w_w_base *= 1.4
        elif "6402" in w_g: w_w_base *= 0.7
        w_w_one = w_w_base * rho_coeff
        
        self.w_one.config(state="normal"); self.w_one.delete(0, "end"); self.w_one.insert(0, f"{w_w_one:.5f}"); self.w_one.config(state="readonly")
        try:
            wp = float(self.w_pcs.get())
            self.w_tot.config(state="normal"); self.w_tot.delete(0, "end"); self.w_tot.insert(0, f"{wp * w_w_one:.2f}"); self.w_tot.config(state="readonly")
        except: pass
        try:
            w_kg = float(self.w_kg_rev.get())
            ws_r = self.w_size_rev.get()
            w_wr_base = base_washer.get(ws_r, 0.011)
            if "9065" in w_g: w_wr_base *= 1.4
            elif "6402" in w_g: w_wr_base *= 0.7
            pcs_r = int(w_kg / (w_wr_base * rho_coeff)) if (w_wr_base * rho_coeff) > 0 else 0
            self.w_pcs_rev.config(state="normal"); self.w_pcs_rev.delete(0, "end"); self.w_pcs_rev.insert(0, str(pcs_r)); self.w_pcs_rev.config(state="readonly")
        except: pass

        # --- 4. РАСЧЕТ ШПИЛЕК И САМОРЕЗОВ ---
        ss = self.s_size.get()
        w_s_base = 0.00049
        if "М" in ss:
            parts = ss.replace("М", "").split("х")
            sd_d = "М" + parts[0]
            sd_l = float(parts[1]) if len(parts) > 1 else 90.0
            weights_stud_90 = {"М12": 0.080, "М16": 0.142, "М20": 0.246, "М24": 0.395, "М30": 0.670, "М36": 1.020, "М42": 1.480, "М48": 2.050}
            w_s_base = weights_stud_90.get(sd_d, 0.142) * (sd_l / 90.0)
        else:
            if "2.5x16" in ss: w_s_base = 0.00049
            elif "4.2x25" in ss: w_s_base = 0.00180
        w_s_one = w_s_base * rho_coeff
        
        self.s_one.config(state="normal"); self.s_one.delete(0, "end"); self.s_one.insert(0, f"{w_s_one:.5f}"); self.s_one.config(state="readonly")
        try:
            sp = float(self.s_pcs.get())
            self.s_tot.config(state="normal"); self.s_tot.delete(0, "end"); self.s_tot.insert(0, f"{sp * w_s_one:.2f}"); self.s_tot.config(state="readonly")
        except: pass
        try:
            s_kg = float(self.s_kg_rev.get())
            ss_r = self.s_size_rev.get()
            if "М" in ss_r:
                parts_r = ss_r.replace("М", "").split("х")
                sdr_d = "М" + parts_r[0]
                sdr_l = float(parts_r[1]) if len(parts_r) > 1 else 90.0
                weights_stud_90 = {"М12": 0.080, "М16": 0.142, "М20": 0.246, "М24": 0.395, "М30": 0.670, "М36": 1.020, "М42": 1.480, "М48": 2.050}
                w_sr_base = weights_stud_90.get(sdr_d, 0.142) * (sdr_l / 90.0)
            else:
                w_sr_base = 0.00049 if "2.5x16" in ss_r else 0.00180
            pcs_r = int(s_kg / (w_sr_base * rho_coeff)) if (w_sr_base * rho_coeff) > 0 else 0
            self.s_pcs_rev.config(state="normal"); self.s_pcs_rev.delete(0, "end"); self.s_pcs_rev.insert(0, str(pcs_r)); self.s_pcs_rev.config(state="readonly")
        except: pass
    def init_welding_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="⚡ Сварка")
        
        top_f = ttk.Frame(tab)
        top_f.pack(fill="x", padx=15, pady=5)
        
        in_box = ttk.LabelFrame(top_f, text=" Исходные данные ")
        in_box.pack(side="left", fill="both", expand=True, padx=(0,10))
        
        ttk.Label(in_box, text="соединение").grid(row=0, column=0, padx=5, pady=3, sticky="w")
        self.w_joint_type = ttk.Combobox(in_box, values=[
            "C2", "C8", "C17", "У5", "У7", "У8", 
            "Листы Н1", "Листы Н2", "Листы Т1", "Листы Т3", "Листы У4", "Листы У5"
        ], state="readonly", width=10)
        self.w_joint_type.set("C17"); self.w_joint_type.grid(row=0, column=1, padx=5, pady=3, sticky="w")
        self.w_joint_type.bind("<<ComboboxSelected>>", self.rebuild_weld_grid)
        
        ttk.Label(in_box, text="Материал").grid(row=1, column=0, padx=5, pady=3, sticky="w")
        self.w_mat_type = ttk.Combobox(in_box, values=["Сталь", "Нержавеющая сталь", "Алюминий", "Бронза", "Латунь", "Медь", "Никель", "Чугун"], state="readonly", width=18)
        self.w_mat_type.set("Сталь"); self.w_mat_type.grid(row=1, column=1, padx=5, pady=3, sticky="w")
        self.w_mat_type.bind("<<ComboboxSelected>>", self.sync_welding_tab_electrodes)
        
        ttk.Label(in_box, text="Положение шва").grid(row=2, column=0, padx=5, pady=3, sticky="w")
        self.w_pos_type = ttk.Combobox(in_box, values=["Нижнее", "Вертикальное", "Потолочное"], state="readonly", width=15)
        self.w_pos_type.set("Нижнее"); self.w_pos_type.grid(row=2, column=1, padx=5, pady=3, sticky="w")
        self.w_pos_type.bind("<<ComboboxSelected>>", lambda event: self.proc_welding_current_and_rates())
        
        self.dyn_grid_frame = ttk.Frame(in_box)
        self.dyn_grid_frame.grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")
        self.w_inputs = {}
        
        self.w_canvas = tk.Canvas(top_f, bg="#ffffff", width=440, height=240, bd=1, relief="solid")
        self.w_canvas.pack(side="right", fill="both", expand=True)
        
        ttk.Button(in_box, text="Считать", command=self.process_gost_welding_calculations).grid(row=4, column=1, padx=5, pady=5, sticky="e")
        
        mid_f = ttk.Frame(tab)
        mid_f.pack(fill="x", padx=15, pady=5)
        
        el_box = ttk.LabelFrame(mid_f, text=" Выбор сварочного материала (РОС-ЭЛЕКТРОД) ")
        el_box.pack(fill="x", pady=2)
        
        self.w_el_cat = ttk.Combobox(el_box, values=[
            "Углеродистая и низколегированная сталь", "Легированная конструкционная сталь", 
            "Теплоустойчивая сталь по ГОСТ 9467", "Высоколегированная сталь (Нержавеющая)",
            "Сплавы алюминия (ОЗА)", "Медь и сплавы (Бронза/Латунь)", "Чугун и его ремонт (ЦЧ-4)"
        ], state="readonly", width=38)
        self.w_el_cat.set("Углеродистая и низколегированная сталь"); self.w_el_cat.pack(side="left", padx=10, pady=5)
        self.w_el_cat.bind("<<ComboboxSelected>>", self.update_welding_marks_list)
        
        self.w_el_mark = ttk.Combobox(el_box, values=[], state="readonly", width=15)
        self.w_el_mark.pack(side="left", padx=5, pady=5)
        self.w_el_mark.bind("<<ComboboxSelected>>", lambda event: self.proc_welding_current_and_rates())
        
        ttk.Label(el_box, text="Диаметр электрода, мм:").pack(side="left", padx=10)
        self.w_el_dia = ttk.Combobox(el_box, values=["2.0", "2.5", "3.0", "4.0", "5.0", "6.0"], width=6, state="readonly")
        self.w_el_dia.set("3.0"); self.w_el_dia.pack(side="left", padx=5, pady=5)
        self.w_el_dia.bind("<<ComboboxSelected>>", lambda event: self.proc_welding_current_and_rates())
        
        res_box = ttk.LabelFrame(tab, text=" Расчетные сметные показатели ")
        res_box.pack(fill="x", padx=15, pady=5)
        
        f_r1 = ttk.Frame(res_box); f_r1.pack(fill="x", pady=4)
        self.out_e = ttk.Entry(f_r1, width=10, font=("Consolas", 10, "bold"), justify="center"); self.out_e.pack(side="left", padx=10)
        ttk.Label(f_r1, text="- нормативная ширина шва (e), мм").pack(side="left")
        
        ttk.Label(f_r1, text="РЕКОМЕНДУЕМЫЙ ТОК:").pack(side="right", padx=5)
        self.out_current = ttk.Entry(f_r1, width=15, font=("Consolas", 10, "bold"), justify="center"); self.out_current.pack(side="right", padx=15)
        
        f_r2 = ttk.Frame(res_box); f_r2.pack(fill="x", pady=4)
        self.out_el_mass = ttk.Entry(f_r2, width=10, font=("Consolas", 10, "bold"), justify="center"); self.out_el_mass.pack(side="left", padx=10)
        ttk.Label(f_r2, text="- расход электродов, кг (с учетом марки)").pack(side="left")
        
        btn_exit = ttk.Button(f_r2, text="Выход", command=self.root.quit)
        btn_exit.pack(side="right", padx=15)
        
        self.rebuild_weld_grid()
        self.sync_welding_tab_electrodes()

    def sync_welding_tab_electrodes(self, event=None):
        mat = self.w_mat_type.get()
        if mat == "Сталь": self.w_el_cat.set("Углеродистая и низколегированная сталь")
        elif mat == "Нержавеющая сталь": self.w_el_cat.set("Высоколегированная сталь (Нержавеющая)")
        elif mat == "Алюминий": self.w_el_cat.set("Сплавы алюминия (ОЗА)")
        elif mat in ["Медь", "Бронза", "Латунь"]: self.w_el_cat.set("Медь и сплавы (Бронза/Латунь)")
        elif mat == "Чугун": self.w_el_cat.set("Чугун и его ремонт (ЦЧ-4)")
        self.update_welding_marks_list()

    def update_welding_marks_list(self, event=None):
        cat = self.w_el_cat.get()
        if "Углеродистая" in cat: marks = ["ТМУ-21У", "ОЗС-4", "ОЗС-6", "ОЗС-12", "АНО-4", "УОНИ-13/45", "УОНИ-13/55", "МР-3"]
        elif "Легированная" in cat: marks = ["АНО-ТМ70", "АНП-1", "УОНИ-13/85", "ЦЛ-18", "ЦЛ-19"]
        elif "Теплоустойчивая" in cat: marks = ["ЦЛ-6", "ЦУ-2М", "ТМЛ-1", "ТМЛ-3У", "ЦЛ-39"]
        elif "Высоколегированная" in cat: marks = ["ОЗЛ-6", "ОЗЛ-8", "ЦЛ-11", "ЦТ-15", "КТИ-9А"]
        elif "алюминия" in cat: marks = ["ОЗА-1", "ОЗА-2"]
        elif "Медь" in cat: marks = ["«КОМСОМОЛЕЦ-100»", "АНЦ/ОЗМ-2", "АНЦ/ОЗМ-3"]
        else: marks = ["ЦЧ-4", "АНЧ-1", "ОЗЧ-2", "ОЗЧ-6"]
        self.w_el_mark['values'] = marks; self.w_el_mark.set(marks if marks else "")
        self.proc_welding_current_and_rates()

    def proc_welding_current_and_rates(self, event=None):
        mark = self.w_el_mark.get(); pos = self.w_pos_type.get(); dia = self.w_el_dia.get()
        current_map = {
            "УОНИ-13/45": {"2.0": {"Нижнее": "40-60", "Вертикальное": "35-55", "Потолочное": "35-55"},
                           "2.5": {"Нижнее": "50-75", "Вертикальное": "40-65", "Потолочное": "40-65"},
                           "3.0": {"Нижнее": "80-100", "Вертикальное": "70-90", "Потолочное": "70-90"},
                           "4.0": {"Нижнее": "130-150", "Вертикальное": "130-140", "Потолочное": "130-140"}},
            "УОНИ-13/55": {"2.0": {"Нижнее": "40-60", "Вертикальное": "35-55", "Потолочное": "35-55"},
                           "2.5": {"Нижнее": "50-75", "Вертикальное": "40-65", "Потолочное": "40-65"},
                           "3.0": {"Нижнее": "80-100", "Вертикальное": "70-90", "Потолочное": "70-90"},
                           "4.0": {"Нижнее": "130-160", "Вертикальное": "130-140", "Потолочное": "130-140"}},
            "АНО-4":      {"3.0": {"Нижнее": "100-140", "Вертикальное": "90-110", "Потолочное": "100-120"},
                           "4.0": {"Нижнее": "170-210", "Вертикальное": "140-150", "Потолочное": "140-170"}},
            "МР-3":       {"3.0": {"Нижнее": "140-180", "Вертикальное": "120-160", "Потолочное": "120-160"},
                           "4.0": {"Нижнее": "160-200", "Вертикальное": "140-180", "Потолочное": "140-180"}},
            "ОЗС-4":      {"3.0": {"Нижнее": "90-100", "Вертикальное": "80-90", "Потолочное": "70-90"},
                           "4.0": {"Нижнее": "140-170", "Вертикальное": "130-160", "Потолочное": "140-160"}},
            "ОЗС-6":      {"3.0": {"Нижнее": "80-110", "Вертикальное": "60-90", "Потолочное": "70-100"},
                           "4.0": {"Нижнее": "170-220", "Вертикальное": "130-150", "Потолочное": "140-170"}}
        }
        tok = "140-160 A"
        if mark in current_map and dia in current_map[mark]: tok = current_map[mark][dia].get(pos, "130-150 A")
        self.out_current.config(state="normal"); self.out_current.delete(0, "end"); self.out_current.insert(0, tok); self.out_current.config(state="readonly")

    def rebuild_weld_grid(self, event=None):
        for w in self.dyn_grid_frame.winfo_children(): w.destroy()
        self.w_inputs.clear()
        joint = self.w_joint_type.get()
        if joint in ["C2", "C8"]:
            fields = [("кол-во св. швов", "1"), ("диаметр трубы (D), мм", "60"), ("толщина стенки (S), мм", "3"), ("зазор после прихватки (b), мм", "1"), ("притупление кромки (c), мм", "0.5"), ("выпуклость шва (g), мм", "2"), ("угол фаски (A°)", "50")]
        elif joint == "C17":
            fields = [("кол-во св. швов", "1"), ("диаметр трубы (D), мм", "20"), ("толщина стенки (S), мм", "3"), ("зазор после прихватки (b), мм", "1"), ("притупление кромки (c), мм", "0.5"), ("выпуклость шва (g), мм", "2"), ("угол фаски (A°)", "30")]
        elif joint in ["У5", "У7", "У8"]:
            fields = [("кол-во св. швов", "1"), ("диаметр трубы (D), мм", "108"), ("толщина стенки (S), мм", "4"), ("толщина фланца (S1), мм", "4"), ("зазор после прихватки (b), мм", "0.5"), ("выпуклость шва (g), мм", "1")]
        else:
            fields = [("толщина листа (S), мм", "5"), ("Длина шва, мм", "1000"), ("Катет шва (k), мм", "5"), ("выпуклость шва (g), мм", "1")]
        for r, (lbl, val) in enumerate(fields):
            e = ttk.Entry(self.dyn_grid_frame, width=8, justify="center"); e.insert(0, val); e.grid(row=r, column=0, padx=5, pady=2)
            ttk.Label(self.dyn_grid_frame, text=f"- {lbl}").grid(row=r, column=1, padx=2, pady=2, sticky="w")
    def init_welding_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="⚡ Сварка")
        
        top_f = ttk.Frame(tab)
        top_f.pack(fill="x", padx=15, pady=5)
        
        in_box = ttk.LabelFrame(top_f, text=" Исходные данные ")
        in_box.pack(side="left", fill="both", expand=True, padx=(0,10))
        
        ttk.Label(in_box, text="соединение").grid(row=0, column=0, padx=5, pady=3, sticky="w")
        self.w_joint_type = ttk.Combobox(in_box, values=[
            "C2", "C8", "C17", "У5", "У7", "У8", 
            "Листы Н1", "Листы Н2", "Листы Т1", "Листы Т3", "Листы У4", "Листы У5"
        ], state="readonly", width=10)
        self.w_joint_type.set("C17"); self.w_joint_type.grid(row=0, column=1, padx=5, pady=3, sticky="w")
        self.w_joint_type.bind("<<ComboboxSelected>>", self.rebuild_weld_grid)
        
        ttk.Label(in_box, text="Материал").grid(row=1, column=0, padx=5, pady=3, sticky="w")
        self.w_mat_type = ttk.Combobox(in_box, values=["Сталь", "Нержавеющая сталь", "Алюминий", "Бронза", "Латунь", "Медь", "Никель", "Чугун"], state="readonly", width=18)
        self.w_mat_type.set("Сталь"); self.w_mat_type.grid(row=1, column=1, padx=5, pady=3, sticky="w")
        self.w_mat_type.bind("<<ComboboxSelected>>", self.sync_welding_tab_electrodes)
        
        ttk.Label(in_box, text="Положение шва").grid(row=2, column=0, padx=5, pady=3, sticky="w")
        self.w_pos_type = ttk.Combobox(in_box, values=["Нижнее", "Вертикальное", "Потолочное"], state="readonly", width=15)
        self.w_pos_type.set("Нижнее"); self.w_pos_type.grid(row=2, column=1, padx=5, pady=3, sticky="w")
        self.w_pos_type.bind("<<ComboboxSelected>>", lambda event: self.proc_welding_current_and_rates())
        
        self.dyn_grid_frame = ttk.Frame(in_box)
        self.dyn_grid_frame.grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")
        self.w_inputs = {}
        
        self.w_canvas = tk.Canvas(top_f, bg="#ffffff", width=440, height=240, bd=1, relief="solid")
        self.w_canvas.pack(side="right", fill="both", expand=True)
        
        ttk.Button(in_box, text="Считать", command=self.process_gost_welding_calculations).grid(row=4, column=1, padx=5, pady=5, sticky="e")
        
        mid_f = ttk.Frame(tab)
        mid_f.pack(fill="x", padx=15, pady=5)
        
        el_box = ttk.LabelFrame(mid_f, text=" Выбор сварочного материала (РОС-ЭЛЕКТРОД) ")
        el_box.pack(fill="x", pady=2)
        
        self.w_el_cat = ttk.Combobox(el_box, values=[
            "Углеродистая и низколегированная сталь", "Легированная конструкционная сталь", 
            "Теплоустойчивая сталь по ГОСТ 9467", "Высоколегированная сталь (Нержавеющая)",
            "Сплавы алюминия (ОЗА)", "Медь и сплавы (Бронза/Латунь)", "Чугун и его ремонт (ЦЧ-4)"
        ], state="readonly", width=38)
        self.w_el_cat.set("Углеродистая и низколегированная сталь"); self.w_el_cat.pack(side="left", padx=10, pady=5)
        self.w_el_cat.bind("<<ComboboxSelected>>", self.update_welding_marks_list)
        
        self.w_el_mark = ttk.Combobox(el_box, values=[], state="readonly", width=15)
        self.w_el_mark.pack(side="left", padx=5, pady=5)
        self.w_el_mark.bind("<<ComboboxSelected>>", lambda event: self.proc_welding_current_and_rates())
        
        ttk.Label(el_box, text="Диаметр электрода, мм:").pack(side="left", padx=10)
        self.w_el_dia = ttk.Combobox(el_box, values=["2.0", "2.5", "3.0", "4.0", "5.0", "6.0"], width=6, state="readonly")
        self.w_el_dia.set("3.0"); self.w_el_dia.pack(side="left", padx=5, pady=5)
        self.w_el_dia.bind("<<ComboboxSelected>>", lambda event: self.proc_welding_current_and_rates())
        
        res_box = ttk.LabelFrame(tab, text=" Расчетные сметные показатели ")
        res_box.pack(fill="x", padx=15, pady=5)
        
        f_r1 = ttk.Frame(res_box); f_r1.pack(fill="x", pady=4)
        self.out_e = ttk.Entry(f_r1, width=10, font=("Consolas", 10, "bold"), justify="center"); self.out_e.pack(side="left", padx=10)
        ttk.Label(f_r1, text="- нормативная ширина шва (e), мм").pack(side="left")
        
        ttk.Label(f_r1, text="РЕКОМЕНДУЕМЫЙ ТОК:").pack(side="right", padx=5)
        self.out_current = ttk.Entry(f_r1, width=15, font=("Consolas", 10, "bold"), justify="center"); self.out_current.pack(side="right", padx=15)
        
        f_r2 = ttk.Frame(res_box); f_r2.pack(fill="x", pady=4)
        self.out_el_mass = ttk.Entry(f_r2, width=10, font=("Consolas", 10, "bold"), justify="center"); self.out_el_mass.pack(side="left", padx=10)
        ttk.Label(f_r2, text="- расход электродов, кг (с учетом марки)").pack(side="left")
        
        btn_exit = ttk.Button(f_r2, text="Выход", command=self.root.quit)
        btn_exit.pack(side="right", padx=15)
        
        self.rebuild_weld_grid()
        self.sync_welding_tab_electrodes()
    def sync_welding_tab_electrodes(self, event=None):
        mat = self.w_mat_type.get()
        if mat == "Сталь": self.w_el_cat.set("Углеродистая и низколегированная сталь")
        elif mat == "Нержавеющая сталь": self.w_el_cat.set("Высоколегированная сталь (Нержавеющая)")
        elif mat == "Алюминий": self.w_el_cat.set("Сплавы алюминия (ОЗА)")
        elif mat in ["Медь", "Бронза", "Латунь"]: self.w_el_cat.set("Медь и сплавы (Бронза/Латунь)")
        elif mat == "Чугун": self.w_el_cat.set("Чугун и его ремонт (ЦЧ-4)")
        self.update_welding_marks_list()

    def update_welding_marks_list(self, event=None):
        cat = self.w_el_cat.get()
        if "Углеродистая" in cat: marks = ["ТМУ-21У", "ОЗС-4", "ОЗС-6", "ОЗС-12", "АНО-4", "УОНИ-13/45", "УОНИ-13/55", "МР-3"]
        elif "Легированная" in cat: marks = ["АНО-ТМ70", "АНП-1", "УОНИ-13/85", "ЦЛ-18", "ЦЛ-19"]
        elif "Теплоустойчивая" in cat: marks = ["ЦЛ-6", "ЦУ-2М", "ТМЛ-1", "ТМЛ-3У", "ЦЛ-39"]
        elif "Высоколегированная" in cat: marks = ["ОЗЛ-6", "ОЗЛ-8", "ЦЛ-11", "ЦТ-15", "КТИ-9А"]
        elif "алюминия" in cat: marks = ["ОЗА-1", "ОЗА-2"]
        elif "Медь" in cat: marks = ["«КОМСОМОЛЕЦ-100»", "АНЦ/ОЗМ-2", "АНЦ/ОЗМ-3"]
        else: marks = ["ЦЧ-4", "АНЧ-1", "ОЗЧ-2", "ОЗЧ-6"]
        self.w_el_mark['values'] = marks; self.w_el_mark.set(marks if marks else "")
        self.proc_welding_current_and_rates()

    def proc_welding_current_and_rates(self, event=None):
        mark = self.w_el_mark.get(); pos = self.w_pos_type.get(); dia = self.w_el_dia.get()
        current_map = {
            "УОНИ-13/45": {"2.0": {"Нижнее": "40-60", "Вертикальное": "35-55", "Потолочное": "35-55"},
                           "2.5": {"Нижнее": "50-75", "Вертикальное": "40-65", "Потолочное": "40-65"},
                           "3.0": {"Нижнее": "80-100", "Вертикальное": "70-90", "Потолочное": "70-90"},
                           "4.0": {"Нижнее": "130-150", "Вертикальное": "130-140", "Потолочное": "130-140"}},
            "УОНИ-13/55": {"2.0": {"Нижнее": "40-60", "Вертикальное": "35-55", "Потолочное": "35-55"},
                           "2.5": {"Нижнее": "50-75", "Вертикальное": "40-65", "Потолочное": "40-65"},
                           "3.0": {"Нижнее": "80-100", "Вертикальное": "70-90", "Потолочное": "70-90"},
                           "4.0": {"Нижнее": "130-160", "Вертикальное": "130-140", "Потолочное": "130-140"}},
            "АНО-4":      {"3.0": {"Нижнее": "100-140", "Вертикальное": "90-110", "Потолочное": "100-120"},
                           "4.0": {"Нижнее": "170-210", "Вертикальное": "140-150", "Потолочное": "140-170"}},
            "МР-3":       {"3.0": {"Нижнее": "140-180", "Вертикальное": "120-160", "Потолочное": "120-160"},
                           "4.0": {"Нижнее": "160-200", "Вертикальное": "140-180", "Потолочное": "140-180"}},
            "ОЗС-4":      {"3.0": {"Нижнее": "90-100", "Вертикальное": "80-90", "Потолочное": "70-90"},
                           "4.0": {"Нижнее": "140-170", "Вертикальное": "130-160", "Потолочное": "140-160"}},
            "ОЗС-6":      {"3.0": {"Нижнее": "80-110", "Вертикальное": "60-90", "Потолочное": "70-100"},
                           "4.0": {"Нижнее": "170-220", "Вертикальное": "130-150", "Потолочное": "140-170"}}
        }
        tok = "140-160 A"
        if mark in current_map and dia in current_map[mark]: tok = current_map[mark][dia].get(pos, "130-150 A")
        self.out_current.config(state="normal"); self.out_current.delete(0, "end"); self.out_current.insert(0, tok); self.out_current.config(state="readonly")

    def rebuild_weld_grid(self, event=None):
        for w in self.dyn_grid_frame.winfo_children(): w.destroy()
        self.w_inputs.clear(); joint = self.w_joint_type.get()
        if joint in ["C2", "C8"]:
            fields = [("кол-во св. швов", "1"), ("диаметр трубы (D), мм", "60"), ("толщина стенки (S), мм", "3"), ("зазор после прихватки (b), мм", "1"), ("притупление кромки (c), мм", "0.5"), ("выпуклость шва (g), мм", "2"), ("угол фаски (A°)", "50")]
        elif joint == "C17":
            fields = [("кол-во св. швов", "1"), ("диаметр трубы (D), мм", "20"), ("толщина стенки (S), мм", "3"), ("зазор после прихватки (b), мм", "1"), ("притупление кромки (c), мм", "0.5"), ("выпуклость шва (g), мм", "2"), ("угол фаски (A°)", "30")]
        elif joint in ["У5", "У7", "У8"]:
            fields = [("кол-во св. швов", "1"), ("диаметр трубы (D), мм", "108"), ("толщина стенки (S), мм", "4"), ("толщина фланца (S1), мм", "4"), ("зазор после прихватки (b), мм", "0.5"), ("выпуклость шва (g), мм", "1")]
        else:
            fields = [("толщина листа (S), мм", "5"), ("Длина шва, мм", "1000"), ("Катет шва (k), мм", "5"), ("выпуклость шва (g), мм", "1")]
        for r, (lbl, val) in enumerate(fields):
            e = ttk.Entry(self.dyn_grid_frame, width=8, justify="center"); e.insert(0, val); e.grid(row=r, column=0, padx=5, pady=2)
            ttk.Label(self.dyn_grid_frame, text=f"- {lbl}").grid(row=r, column=1, padx=2, pady=2, sticky="w")
            self.w_inputs[lbl] = e
        self.redraw_gost_canvas_shapes()
    def redraw_gost_canvas_shapes(self):
        self.w_canvas.delete("all"); joint = self.w_joint_type.get(); cx, cy = 220, 110
        def draw_arrow(x1, y1, x2, y2, label="", txt_x=0, txt_y=0):
            self.w_canvas.create_line(x1, y1, x2, y2, fill="#130f40", width=1, arrow="both", arrowshape=(8,10,3))
            if label: self.w_canvas.create_text(txt_x if txt_x else (x1+x2)/2, txt_y if txt_y else (y1+y2)/2-10, text=label, font=("Segoe UI", 9, "bold"), fill="#2c3e50")
        if joint in ["C2", "C8"]:
            self.w_canvas.create_rectangle(40, cy-15, 185, cy+15, fill="#dcdde1", outline="#7f8c8d", width=1.5)
            self.w_canvas.create_rectangle(235, cy-15, 380, cy+15, fill="#dcdde1", outline="#7f8c8d", width=1.5)
            self.w_canvas.create_oval(175, cy-22, 245, cy+12, fill="#ff8c00", outline="#d35400", width=1.5)
            draw_arrow(185, cy+28, 235, cy+28, "b"); draw_arrow(175, cy-32, 245, cy-32, "e")
            draw_arrow(210, cy-22, 210, cy-15, "g", txt_x=225, txt_y=cy-25); draw_arrow(390, cy-15, 390, cy+15, "S", txt_x=405)
            self.w_canvas.create_line(40, cy, 380, cy, fill="#7f8c8d", dash=(6,4)); draw_arrow(50, cy-50, 50, cy, "D", txt_x=65, txt_y=cy-25)
        elif joint == "C17":
            self.w_canvas.create_polygon(40,cy-20, 150,cy-20, 180,cy+20, 40,cy+20, fill="#dcdde1", outline="#7f8c8d", width=1.5)
            self.w_canvas.create_polygon(380,cy-20, 270,cy-20, 240,cy+20, 380,cy+20, fill="#dcdde1", outline="#7f8c8d", width=1.5)
            self.w_canvas.create_oval(165, cy-28, 255, cy+15, fill="#ff8c00", outline="#d35400", width=1.5)
            draw_arrow(180, cy+32, 240, cy+32, "b"); draw_arrow(165, cy-38, 255, cy-38, "e"); draw_arrow(390, cy-20, 390, cy+20, "S", txt_x=405)
            self.w_canvas.create_arc(130, cy-35, 190, cy+5, start=315, extent=45, style="arc", outline="red", width=1.5)
            self.w_canvas.create_text(135, cy-10, text="A°", font=("Segoe UI", 9, "bold"), fill="red")
        elif joint in ["У5", "У7", "У8"]:
            self.w_canvas.create_rectangle(210, cy-70, 320, cy+70, fill="#b2bec3", outline="#7f8c8d", width=1.5)
            self.w_canvas.create_rectangle(60, cy-20, 210, cy+20, fill="#dcdde1", outline="#7f8c8d", width=1.5)
            self.w_canvas.create_polygon(210,cy-20, 210,cy-50, 175,cy-20, fill="#ff8c00", outline="#d35400", width=1.5)
            self.w_canvas.create_polygon(210,cy+20, 210,cy+50, 175,cy+20, fill="#ff8c00", outline="#d35400", width=1.5)
            draw_arrow(335, cy-70, 335, cy+70, "S1", txt_x=355); draw_arrow(45, cy-20, 45, cy+20, "S", txt_x=30)
        else:
            self.w_canvas.create_rectangle(60, cy-25, 240, cy, fill="#dcdde1", outline="#7f8c8d", width=1.5)
            self.w_canvas.create_rectangle(150, cy, 340, cy+25, fill="#b2bec3", outline="#7f8c8d", width=1.5)
            self.w_canvas.create_polygon(150,cy, 150,cy-25, 120,cy, fill="#ff8c00", outline="#d35400", width=1.5)
            draw_arrow(160, cy-20, 160, cy, "k", txt_x=175)

    def process_gost_welding_calculations(self):
        joint = self.w_joint_type.get(); rho = self.get_density()
        self.out_e.delete(0, "end"); self.out_el_mass.delete(0, "end")
        try:
            if joint in ["C2", "C8"]:
                n = float(self.w_inputs["кол-во св. швов"].get()); D = float(self.w_inputs["диаметр трубы (D), мм"].get()); S = float(self.w_inputs["толщина стенки (S), мм"].get()); b = float(self.w_inputs["зазор после прихватки (b), мм"].get()); g = float(self.w_inputs["выпуклость шва (g), мм"].get())
                c = float(self.w_inputs["притупление кромки (c), мм"].get()) if "притупление кромки (c), мм" in self.w_inputs else 0.5
                A = float(self.w_inputs["угол фаски (A°)"].get()) if "угол фаски (A°)" in self.w_inputs else 50.0
                e = b + 2 * (S - c) * math.tan(math.radians(A)) + 2
                F_w = ((b + (e - 2)) / 2) * (S - c) + (b * c) + (2 / 3 * e * g)
                L_w = math.pi * (D - S); m_dep = (F_w * L_w * rho / 1000000) * n
            elif joint == "C17":
                n = float(self.w_inputs["кол-во св. швов"].get()); D = float(self.w_inputs["диаметр трубы (D), мм"].get()); S = float(self.w_inputs["толщина стенки (S), мм"].get()); b = float(self.w_inputs["зазор после прихватки (b), мм"].get()); c = float(self.w_inputs["притупление кромки (c), мм"].get()); g = float(self.w_inputs["выпуклость шва (g), мм"].get()); A = float(self.w_inputs["угол фаски (A°)"].get())
                e = b + 2 * (S - c) * math.tan(math.radians(A)) + 2; F_w = ((b + (e - 2)) / 2) * (S - c) + (b * c) + (2 / 3 * e * g)
                L_w = math.pi * (D - S); m_dep = (F_w * L_w * rho / 1000000) * n
            elif joint in ["У5", "У7", "У8"]:
                n = float(self.w_inputs["кол-во св. швов"].get()); D = float(self.w_inputs["диаметр трубы (D), мм"].get()); S = float(self.w_inputs["толщина стенки (S), мм"].get()); S1 = float(self.w_inputs["толщина фланца (S1), мм"].get()); b = float(self.w_inputs["зазор после прихватки (b), мм"].get()); g = float(self.w_inputs["выпуклость шва (g), мм"].get())
                e = S + S1 + b + 1.5; K = S + 1; K1 = S1 + 1; F_w = (0.5 * K * K1) + (2 / 3 * max(K, K1) * g)
                L_w = math.pi * D; m_dep = (F_w * L_w * rho / 1000000) * n
            else:
                S = float(self.w_inputs["толщина листа (S), мм"].get()); L_w = float(self.w_inputs["Длина шва, мм"].get()); k = float(self.w_inputs["Катет шва (k), мм"].get()); g = float(self.w_inputs["выпуклость шва (g), мм"].get())
                e = k + 2; F_w = (0.5 * k * k) + (2 / 3 * e * g); m_dep = (F_w * L_w * rho / 1000000)
            mark = self.w_el_mark.get(); rate_coeff = 1.62
            if mark in ["УОНИ-13/45", "ОЗС-4"]: rate_coeff = 1.60
            elif mark in ["МР-3", "АНО-4"]: rate_coeff = 1.70
            elif mark == "ОЗС-6": rate_coeff = 1.50
            self.out_e.insert(0, f"{round(e, 1)}"); self.out_el_mass.insert(0, f"{m_dep * rate_coeff:.3f}")
        except Exception: messagebox.showerror("Ошибка", "Проверить параметры!")
    def init_electrodes_tab(self):
        tab = ttk.Frame(self.notebook); self.notebook.add(tab, text="📖 Справочник электродов")
        ttk.Label(tab, text="Выбор марки электрода в зависимости от свариваемого материала конструкции", font=("Segoe UI", 11, "bold")).pack(pady=8, anchor="w", padx=15)
        f_top = ttk.LabelFrame(tab, text=" 1. Выберите категорию сталей/сплавов по ГОСТ "); f_top.pack(fill="x", padx=15, pady=5)
        self.el_cat_box = tk.Listbox(f_top, height=5, font=("Segoe UI", 10)); self.el_cat_box.pack(fill="x", padx=10, pady=5)
        cats = ["Углеродистые и низколегированные конструкционные стали (до 0.25% углерода)", "Легированные конструкционные стали повышенной и высокой прочности", "Легированные теплоустойчивые стали котельных и тепловых сетей по ГОСТ 9467", "Высоколегированные коррозионно-стойкие и жаропрочные стали (Нержавеющие сплавы)", "Сварка чугуна, цветных металлов (Алюминий, Медь, Бронза, Латунь) и наплавка"]
        for c in cats: self.el_cat_box.insert("end", c)
        f_bot = ttk.Frame(tab); f_bot.pack(fill="both", expand=True, padx=15, pady=5)
        f_left = ttk.LabelFrame(f_bot, text=" 2. Совместимые марки электродов "); f_left.pack(side="left", fill="both", expand=True, padx=(0,5), pady=5)
        self.el_mark_box = tk.Listbox(f_left, font=("Consolas", 10, "bold")); self.el_mark_box.pack(fill="both", expand=True, padx=5, pady=5)
        f_right = ttk.Frame(f_bot); f_right.pack(side="right", fill="both", expand=True, padx=(5,0), pady=5)
        f_all = ttk.LabelFrame(f_right, text=" Перечень всех марок в выбранной группе "); f_all.pack(fill="x", pady=(5,5))
        self.el_all_text = tk.Text(f_all, bg="#ffffff", height=2, font=("Consolas", 10)); self.el_all_text.pack(fill="x", padx=5, pady=5)
        f_desc = ttk.LabelFrame(f_right, text=" Техническое назначение и сметное описание "); f_desc.pack(fill="both", expand=True, pady=(5,5))
        self.el_desc_text = tk.Text(f_desc, bg="#f8f9fa", font=("Segoe UI", 10)); self.el_desc_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.el_cat_box.bind("<<ListboxSelect>>", self.on_main_electrode_category_change); self.el_cat_box.select_set(0); self.on_main_electrode_category_change(None)

    def on_main_electrode_category_change(self, event=None):
        sel = self.el_cat_box.curselection()
        if not sel: return
        idx = sel[0]; self.el_mark_box.delete(0, "end")
        if idx == 0:
            mar = ["ТМУ-21У", "ОЗС-4", "ОЗС-6", "ОЗС-12", "АНО-4", "УОНИ-13/45", "УОНИ-13/55", "МР-3"]
            txt = "ТМУ-21У, ОЗС-4, ОЗС-6, ОЗС-12, АНО-4, УОНИ-13/45, УОНИ-13/55, МР-3"
            desc = "ГОСТ 9467: Типы Э42, Э46, Э50. Для ручной дуговой сварки особо ответственных металлоконструкций и трубопроводов пара и горячей воды."
        elif idx == 1:
            mar = ["АНО-ТМ70", "АНП-1", "АНП-2", "УОНИ-13/85", "ЦЛ-18", "ЦЛ-19"]
            txt = "АНО-ТМ70, АНП-1, АНП-2, УОНИ-13/85, ЦЛ-18, ЦЛ-19"
            desc = "Для сварки легированных конструкционных сталей повышенной и высокой прочности."
        elif idx == 2:
            mar = ["ЦЛ-6", "ЦУ-2М", "УОНИ-13ХМ", "ТМЛ-1", "ТМЛ-3У", "ЦЛ-39", "ЦЛ-17", "ЦЛ-21", "ЦЛ-57"]
            txt = "ЦЛ-6, ЦУ-2М, УОНИ-13ХМ, ТМЛ-1, ТМЛ-3У, ЦЛ-39, ЦЛ-17, ЦЛ-21, ЦЛ-57"
            desc = "ГОСТ 9467: Типы Э-09Х1М, Э-09Х1МФ, Э-10Х5МФ. Для сварки элементов котельного оборудования и паропроводов тепловых сетей ТЭЦ."
        elif idx == 3:
            mar = ["ОЗЛ-6", "ОЗЛ-8", "ЦЛ-11", "ЦТ-15", "КТИ-5", "АНЖ-2", "НЖ-13", "ЭА-400/13", "ОЗЛ-17У", "ОЗЛ-22"]
            txt = "ОЗЛ-6, ОЗЛ-8, ЦЛ-11, ЦТ-15, КТИ-5, АНЖ-2, НЖ-13, ЭА-400/13, ОЗЛ-17У, ОЗЛ-22"
            desc = "Для высоколегированных сталей аустенитного класса (нержавейки). Защита шва от межкристаллитной коррозии (МКК)."
        else:
            mar = ["ЦЧ-4", "АНЧ-1", "ОЗА-1", "ОЗА-2", "«КОМСОМОЛЕЦ-100»", "АНЦ/ОЗМ-2", "ОЗБ-2М", "Т-590", "Т-620", "ОЗН-300М"]
            txt = "ЦЧ-4, АНЧ-1 (Чугун); ОЗА-1, ОЗА-2 (Алюминий); «КОМСОМОЛЕЦ-100», АНЦ/ОЗМ-2 (Медь); ОЗБ-2М (Бронза); Т-590, Т-620 (Наплавка)"
            desc = "Специализированные марки. Заварка свищей, трещин и дефектов литья в чугунной арматуре, сварка цветных металлов и сплавов."
        for m in mar: self.el_mark_box.insert("end", m)
        self.el_all_text.delete("1.0", "end"); self.el_all_text.insert("1.0", txt)
        self.el_desc_text.delete("1.0", "end"); self.el_desc_text.insert("1.0", desc)
    def init_designation_tab(self):
        tab = ttk.Frame(self.notebook); self.notebook.add(tab, text="📝 Обозначение швов (ГОСТ)")
        tk.Label(tab, text="Структура условного обозначения стандартного сварного шва по ГОСТ 2.312-72", font=("Segoe UI", 11, "bold"), fg="#8e44ad").pack(pady=10, anchor="w", padx=20)
        f_arrow = ttk.LabelFrame(tab, text=" 📊 Схема расположения знаков на линии выноски чертежа "); f_arrow.pack(fill="x", padx=20, pady=5)
        f_fields = ttk.Frame(f_arrow); f_fields.pack(pady=10)
        fields_desc = ["1. Стандарт", "2. Тип соединения", "3. Способ сварки", "4. Катет шва", "5. Особая длина", "6. Вспом. знаки"]
        for i, f_lbl in enumerate(fields_desc):
            ttk.Label(f_fields, text=f" {f_lbl} ", font=("Segoe UI", 9, "bold")).pack(side="left", padx=5)
            e = ttk.Entry(f_fields, width=10, justify="center"); e.insert(0, f"[{i+1}]"); e.pack(side="left", padx=2)
        f_znaki = ttk.LabelFrame(tab, text=" Вспомогательные технологические знаки (Поле 6) "); f_znaki.pack(fill="x", padx=20, pady=5)
        self.znak_var = tk.StringVar(value="𝓞 По замкнутому контуру")
        znaks = [("𝓞 По замкнутому контуру", "Шов по замкнутой линии"), ("⌿  Монтажный шов", "Сварка при монтаже"), ("⎓ Усиление снять", "Снять выпуклость механически"), (" Плавный переход", "Плавное сопряжение")]
        f_r = ttk.Frame(f_znaki); f_r.pack(pady=5)
        for z_txt, _ in znaks: ttk.Radiobutton(f_r, text=z_txt, variable=self.znak_var, value=z_txt, command=self.update_gost_text_info).pack(side="left", padx=10)
        f_gosts = ttk.LabelFrame(tab, text=" 1. Стандарты на типы и конструктивные элементы швов соединений "); f_gosts.pack(fill="both", expand=True, padx=20, pady=5)
        self.gost_lb = tk.Listbox(f_gosts, font=("Segoe UI", 10), height=4); self.gost_lb.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        g_data = ["ГОСТ 16037-80 — Соединения сварные стальных трубопроводов.", "ГОСТ 5264-80 — Ручная дуговая сварка. Соединения сварные сталей.", "ГОСТ 14771-76 — Дуговая сварка в защитном газе.", "ГОСТ 8713-79 — Автоматическая и полуавтоматическая сварка под флюсом."]
        for g in g_data: self.gost_lb.insert("end", g)
        self.gost_desc_txt = tk.Text(f_gosts, bg="#f8f9fa", font=("Segoe UI", 10), width=45); self.gost_desc_txt.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        self.gost_lb.bind("<<ListboxSelect>>", self.update_gost_text_info); self.gost_lb.select_set(0); self.update_gost_text_info()

    def update_gost_text_info(self, event=None):
        self.gost_desc_txt.delete("1.0", "end"); sel = self.gost_lb.curselection(); gost_info = ""
        if sel:
            idx = sel[0]
            if idx == 0: gost_info = "ГОСТ 16037-80:\nПрименяется для стальных технологических трубопроводов, магистральных сетей пара и горячей воды (ТЭЦ). Регламентирует типы швов С2, С8, С17, У5, У7, У8.\n\n"
            elif idx == 1: gost_info = "ГОСТ 5264-80:\nОсновной стандарт на ручную дуговую сварку листовых металлоконструкций, балок, рам оборудования и резервуаров из сталей.\n\n"
            elif idx == 2: gost_info = "ГОСТ 14771-76:\nРегламентирует дуговую сварку в защитных газах (аргон, углекислый газ). Применяется для нержавеющих и легированных конструкций.\n\n"
            else: gost_info = "ГОСТ 8713-79:\nАвтоматическая и полуавтоматическая сварка под флюсом на сварочных тракторах. Высокая производительность для толстого металла.\n\n"
        znak_info = f"Выбранный вспомогательный знак:\n{self.znak_var.get()}\n"; self.gost_desc_txt.insert("1.0", gost_info + znak_info)
    def init_insulation_tab(self):
        tab = ttk.Frame(self.notebook); self.notebook.add(tab, text="环 Изоляция")
        inputs = ttk.LabelFrame(tab, text=" Геометрический расчет объемов теплоизоляции по схеме "); inputs.pack(fill="x", padx=15, pady=10)
        ttk.Label(inputs, text="Тип прокладки сети:").grid(row=0, column=0, padx=5, pady=6, sticky="w")
        self.iso_calc_type = ttk.Combobox(inputs, values=["Одна труба", "Несколько труб (Группа в оболочке)"], state="readonly", width=30)
        self.iso_calc_type.set("Одна труба"); self.iso_calc_type.grid(row=0, column=1, padx=5, pady=6, sticky="w")
        self.iso_calc_type.bind("<<ComboboxSelected>>", self.on_iso_calc_type_change)
        self.iso_inputs_frame = ttk.Frame(inputs); self.iso_inputs_frame.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky="ew")
        self.iso_entries = {}
        btn_frame = ttk.Frame(inputs); btn_frame.grid(row=2, column=0, columnspan=4, pady=10, sticky="ew")
        ttk.Button(btn_frame, text="⚡ Рассчитать геометрические объемы изоляции", command=self.calculate_only_insulation, width=45).pack(side="left", padx=5)
        self.iso_output = tk.Text(tab, bg="#ffffff", font=("Courier", 10), height=14, bd=1, relief="solid"); self.iso_output.pack(fill="both", expand=True, padx=15, pady=10)
        self.on_iso_calc_type_change()

    def on_iso_calc_type_change(self, event=None):
        for w in self.iso_inputs_frame.winfo_children(): w.destroy()
        self.iso_entries.clear(); itype = self.iso_calc_type.get()
        if itype == "Одна труба": fields = [("Диаметр трубы D, м", "1.024"), ("Толщина изоляции t, м", "0.1"), ("Длина участка L, м", "100")]
        else: fields = [("Диаметр крайних D1, м", "1.024"), ("Диаметр средних D2, м", "0.720"), ("Толщина изоляции t, м", "0.1"), ("Зазор труб p, м", "0.15"), ("Длина участка L, м", "50")]
        for idx, (lbl, val) in enumerate(fields):
            ttk.Label(self.iso_inputs_frame, text=lbl).grid(row=0, column=idx*2, padx=4, pady=4, sticky="w")
            e = ttk.Entry(self.iso_inputs_frame, width=10); e.insert(0, val); e.grid(row=0, column=idx*2+1, padx=4, pady=4); self.iso_entries[lbl] = e

    def calculate_only_insulation(self):
        try:
            itype = self.iso_calc_type.get()
            if itype == "Одна труба":
                D = float(self.iso_entries["Диаметр трубы D, м"].get()); t = float(self.iso_entries["Толщина изоляции t, м"].get()); L = float(self.iso_entries["Длина участка L, м"].get())
                S_r = math.pi * D * L; S_pi = math.pi * (D + 2 * t) * L; V_i = (math.pi / 4) * (((D + 2 * t) ** 2) - (D ** 2)) * L
                res = f"📝 ВЕДОМОСТЬ ОБЪЕМОВ ИЗОЛЯЦИОННЫХ РАБОТ СГК (ОДНОТРУБНЫЙ УЧАСТОК):\n--------------------------------------------------\n▶ Площадь обертывания (окраски) Sr:        {S_r:.6f} м²\n▶ Площадь покровного слоя Spi:             {S_pi:.6f} м²\n▶ ИТОГОВЫЙ ОБЪЕМ ТЕПЛОИЗОЛЯЦИИ Vi:         {V_i:.6f} м³\n"
            else:
                D1 = float(self.iso_entries["Диаметр крайних D1, м"].get()); D2 = float(self.iso_entries["Диаметр средних D2, м"].get()); t = float(self.iso_entries["Толщина изоляции t, м"].get()); p = float(self.iso_entries["Зазор труб p, м"].get()); L = float(self.iso_entries["Длина участка L, м"].get())
                M = D1 + D2 + (p * 2); B = (D1 * 2) + D2 + (p * 2) + (t * 2); S_r = ((math.pi * D1) + (M * 2)) * L; S_pi = ((math.pi * (D1 + 2 * t)) + (M * 2)) * L; V_i = (((math.pi / 4) * ((D1 + 2 * t) ** 2 - D1 ** 2)) + (M * 2 * t)) * L
                res = f"📝 ВЕДОМОСТЬ ОБЪЕМОВ ИЗОЛЯЦИОННЫХ РАБОТ СГК (ГРУППОВАЯ ОСЬ):\n--------------------------------------------------\n• Габаритная ширина блока B:               {B:.3f} м\n--------------------------------------------------\n▶ Площадь обертывания (окраски) Sr:        {S_r:.6f} м²\n▶ Площадь покровного слоя Spi:             {S_pi:.6f} м²\n▶ ИТОГОВЫЙ ОБЪЕМ ТЕПЛОИЗОЛЯЦИИ Vi:         {V_i:.6f} м³\n"
        except Exception as e: res = f"❌ Ошибка: {e}"
        self.iso_output.delete("1.0", tk.END); self.iso_output.insert("1.0", res)

if __name__ == "__main__":
    root = tk.Tk()
    app = MetallistProApp(root)
    root.mainloop()
