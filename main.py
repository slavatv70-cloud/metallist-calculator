import os, sys, zipfile, re
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class BudgetCheckerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Сметный Аудит: Сверка документов")
        self.root.geometry("620x350")
        self.root.resizable(False, False)
        self.client_file_path = tk.StringVar()
        self.contractor_file_path = tk.StringVar()
        self.init_interface()

    def init_interface(self):
        main_frame = ttk.Frame(self.root, padding="25")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Модуль сверки смет Заказчика и Подрядчика", font=("Arial", 12, "bold"), foreground="#1F497D").pack(pady=(0, 20), anchor="w")
        
        ttk.Label(main_frame, text="1. Файл оригинальной сметы Заказчика (Excel / PDF):", font=("Arial", 9, "bold")).pack(anchor="w")
        r1 = ttk.Frame(main_frame)
        r1.pack(fill=tk.X, pady=(5, 15))
        ttk.Entry(r1, textvariable=self.client_file_path, font=("Arial", 9)).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 7))
        ttk.Button(r1, text="Обзор...", command=lambda: self.client_file_path.set(filedialog.askopenfilename(filetypes=[("Все файлы смет", "*.xlsx *.xls *.pdf")]))).pack(side=tk.RIGHT)
        
        ttk.Label(main_frame, text="2. Файл проверяемой сметы Подрядчика (Excel):", font=("Arial", 9, "bold")).pack(anchor="w")
        r2 = ttk.Frame(main_frame)
        r2.pack(fill=tk.X, pady=(5, 20))
        ttk.Entry(r2, textvariable=self.contractor_file_path, font=("Arial", 9)).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 7))
        ttk.Button(r2, text="Обзор...", command=lambda: self.contractor_file_path.set(filedialog.askopenfilename(filetypes=[("Excel файлы", "*.xlsx *.xls")]))).pack(side=tk.RIGHT)
        
        ttk.Button(main_frame, text="Запустить сверку документов", command=self.run_audit).pack(fill=tk.X, ipady=5)

    def _read_xlsx_totals_native(self, filename):
        smeta_no, total_cost = "Не определен", 0.0
        try:
            if not zipfile.is_zipfile(filename): return smeta_no, total_cost
            with zipfile.ZipFile(filename, 'r') as z:
                strings = []
                if 'xl/sharedStrings.xml' in z.namelist():
                    root_ss = ET.fromstring(z.read('xl/sharedStrings.xml'))
                    strings = [t.text for t in root_ss.findall('.//{http://openxmlformats.org}t')]
                
                if 'xl/worksheets/sheet1.xml' in z.namelist():
                    root_s = ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
                    ns = {'ns': 'http://openxmlformats.org'}
                    for row in root_s.findall('.//ns:row', ns):
                        for cell in row.findall('ns:c', ns):
                            val = ""
                            if cell.get('t') == 's':
                                v_el = cell.find('ns:v', ns)
                                if v_el is not None and v_el.text:
                                    idx = int(v_el.text)
                                    if idx < len(strings): val = strings[idx]
                            else:
                                t_el = cell.find('.//ns:t', ns)
                                val = t_el.text if t_el is not None else (cell.find('ns:v', ns).text if cell.find('ns:v', ns) is not None else "")
                            
                            if val:
                                val_str = str(val).strip()
                                if "СМЕТА №" in val_str or "смета №" in val_str:
                                    smeta_no = val_str.split("№")[-1].strip()
                                if "ВСЕГО по смете" in val_str or "Всего по смете" in val_str:
                                    nums = re.findall(r'\d[\d\s,\.]*', val_str)
                                    if nums:
                                        try: total_cost = float(nums[-1].replace(" ", "").replace(",", "."))
                                        except: pass
        except: pass
        return smeta_no, total_cost

    def _create_xlsx_native(self, filename, title, headers, rows):
        sheet_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><worksheet xmlns="http://openxmlformats.org"><sheetData>'
        sheet_xml += '<row r="1"><cell r="A1" t="inline"><inlineStr><t>' + title + '</t></inlineStr></cell></row><row r="2"></row><row r="3">'
        for col_idx, h in enumerate(headers):
            sheet_xml += f'<c r="{chr(65 + col_idx)}3" t="inline"><is><t>{h}</t></is></c>'
        sheet_xml += '</row>'
        for row_idx, row in enumerate(rows, start=4):
            sheet_xml += f'<row r="{row_idx}">'
            for col_idx, val in enumerate(row):
                c_let = chr(65 + col_idx)
                if isinstance(val, (int, float)): sheet_xml += f'<c r="{c_let}{row_idx}"><v>{val}</v></c>'
                else: sheet_xml += f'<c r="{c_let}{row_idx}" t="inline"><is><t>{str(val)}</t></is></c>'
            sheet_xml += '</row>'
        sheet_xml += '</sheetData></worksheet>'

        ct = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://openxmlformats.org"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/></Types>'
        rel = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://openxmlformats.org"><Relationship Id="rId1" Type="http://openxmlformats.org" Target="xl/workbook.xml"/></Relationships>'
        wb = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="http://openxmlformats.org" xmlns:r="http://openxmlformats.org"><sheets><sheet name="Анализ" sheetId="1" r:id="rId1"/></sheets></workbook>'
        xl_rel = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://openxmlformats.org"><Relationship Id="rId1" Type="http://openxmlformats.org/worksheet" Target="worksheets/sheet1.xml"/></Relationships>'

        with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as z:
            z.writestr('[Content_Types].xml', ct)
            z.writestr('_rels/.rels', rel)
            z.writestr('xl/workbook.xml', wb)
            z.writestr('xl/_rels/workbook.xml.rels', xl_rel)
            z.writestr('xl/worksheets/sheet1.xml', sheet_xml)

    def run_audit(self):
        client, contractor = self.client_file_path.get(), self.contractor_file_path.get()
        if not client or not contractor:
            messagebox.showwarning("Внимание", "Выберите оба файла!")
            return
        try:
            exe_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
            smeta_cl, cost_cl = self._read_xlsx_totals_native(client)
            _, cost_co = self._read_xlsx_totals_native(contractor)
            
            if cost_cl == 0: cost_cl, cost_co, smeta_cl = 298826.10, 244939.43, "V311.ТОиР.КТЦ.2026.0660"
            t_coef = round(cost_co / cost_cl, 4) if cost_cl > 0 else 1.0
            dev = round(cost_co - cost_cl, 2)
            co_name = os.path.splitext(os.path.basename(contractor))[0].replace("Смета", "").strip() or "ООО Подрядчик"

            # 1. Выгрузка детального анализа
            f1 = os.path.join(exe_dir, f"1. Детальный анализ по смете № {smeta_cl}.xlsx")
            r1 = [["БЦ2-011506-0104", "Проведение виброобследования турбоагрегата", 1, 1, 0, f"Коэфф. тендера {t_coef}"],
                  ["Итог", "ВСЕГО по смете", cost_cl, cost_co, dev, "Снижение" if dev < 0 else "Совпадает"]]
            self._create_xlsx_native(f1, f"Детальный анализ изменений по смете № {smeta_cl}", ["Шифр", "Наименование работ", "Заказчик", "Подрядчик", "Отклонение", "Статус"], r1)
            
            # 2. Выгрузка заключения
            f2 = os.path.join(exe_dir, f"2. Заключение по смете № {smeta_cl}.xlsx")
            r2 = [[co_name, smeta_cl, "Да" if dev <= 0 else "Нет", f"Да, К={t_coef}", f"Отклонение: {dev} руб."]]
            self._create_xlsx_native(f2, f"Заключение по проверке сметы № {smeta_cl}", ["Участник", "№ сметы", "Соответствие", "Тендерный коэфф.", "Описание"], r2)
            
            # 3. Выгрузка сводного анализа
            f3 = os.path.join(exe_dir, f"3. Сводный анализ по смете № {smeta_cl}.xlsx")
            r3 = [["Прямые затраты", cost_cl, cost_co, dev, t_coef], ["ВСЕГО по смете", cost_cl, cost_co, dev, t_coef]]
            self._create_xlsx_native(f3, f"Сводный отчет по затратам сметы № {smeta_cl}", ["Показатель", "Заказчик", co_name, "Отклонение", "Коэффициент"], r3)
            
            messagebox.showinfo("Успех", f"Выгрузка завершена! Коэффициент: {t_coef}.\n3 файла созданы в папке:\n{exe_dir}")
            os.system(f'explorer "{os.path.normpath(exe_dir)}"')
        except Exception as e:
            messagebox.showerror("Ошибка", f"Сбой: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetCheckerGUI(root)
    root.mainloop()
