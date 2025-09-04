import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from logic import MarriageLogic
from population_logic import PopulationLogic

class DataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Анализ данных")
        self.root.geometry("900x600")

        # --- Верхняя панель ---
        top_frame = tk.Frame(root)
        top_frame.pack(pady=10)

        self.btn_open = tk.Button(top_frame, text="Открыть файл", command=self.open_file)
        self.btn_open.pack(side=tk.LEFT, padx=5)

        tk.Label(top_frame, text="Прогноз на N лет:").pack(side=tk.LEFT, padx=5)
        self.entry_years = tk.Entry(top_frame, width=5)
        self.entry_years.pack(side=tk.LEFT, padx=5)

        self.btn_plot = tk.Button(top_frame, text="Построить графики", command=self.plot_data)
        self.btn_plot.pack(side=tk.LEFT, padx=5)

        self.btn_forecast = tk.Button(top_frame, text="Прогноз", command=self.forecast)
        self.btn_forecast.pack(side=tk.LEFT, padx=5)

        # --- Таблица данных ---
        self.tree = ttk.Treeview(root)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

        # --- Панель для графиков ---
        self.fig, self.ax = plt.subplots(figsize=(6,4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Переменные
        self.logic = None
        self.data = None
        self.variant = None  # "marriage" или "population"

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files","*.csv"),("Excel Files","*.xlsx")])
        if not file_path:
            return
        # Загружаем данные и определяем вариант
        temp_data = MarriageLogic.load_file(file_path)
        if 'Браки' in temp_data.columns and 'Разводы' in temp_data.columns:
            self.variant = "marriage"
            self.logic = MarriageLogic
        elif 'Население' in temp_data.columns:
            self.variant = "population"
            self.logic = PopulationLogic
        else:
            messagebox.showerror("Ошибка", "Неизвестный формат файла")
            return
        self.data = temp_data
        self.show_table()

        # Вывод статистики
        if self.variant == "marriage":
            ages = self.logic.most_common_age(self.data)
            print("Возрастные статистики:", ages)
        elif self.variant == "population":
            stats = self.logic.max_growth_decline(self.data)
            print("Максимальный прирост/убыль населения:", stats)

    def show_table(self):
        if self.data is None or self.data.empty:
            return
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = list(self.data.columns)
        self.tree["show"] = "headings"
        for col in self.data.columns:
            self.tree.heading(col, text=col)
        for _, row in self.data.iterrows():
            self.tree.insert("", "end", values=list(row))

    def plot_data(self):
        if self.data is None or self.logic is None or self.data.empty:
            messagebox.showerror("Ошибка", "Нет данных для построения графика")
            return
        self.ax.clear()
        if self.variant == "marriage":
            if all(col in self.data.columns for col in ['Год', 'Браки', 'Разводы']):
                self.ax.set_title("Браки и разводы по годам")
                self.ax.set_xlabel("Год")
                self.ax.set_ylabel("Количество")
                self.ax.plot(self.data['Год'], self.data['Браки'], label='Браки', marker='o')
                self.ax.plot(self.data['Год'], self.data['Разводы'], label='Разводы', marker='o')
                self.ax.legend()
            else:
                messagebox.showerror("Ошибка", "Файл должен содержать колонки: 'Год', 'Браки', 'Разводы'")
        elif self.variant == "population":
            if all(col in self.data.columns for col in ['Год', 'Население']):
                self.ax.set_title("Численность населения по годам")
                self.ax.set_xlabel("Год")
                self.ax.set_ylabel("Население")
                self.ax.plot(self.data['Год'], self.data['Население'], label='Население', marker='o')
                self.ax.legend()
            else:
                messagebox.showerror("Ошибка", "Файл должен содержать колонки: 'Год', 'Население'")
        self.canvas.draw()

    def forecast(self):
        if self.data is None or self.logic is None or self.data.empty:
            messagebox.showerror("Ошибка", "Нет данных для прогноза")
            return
        try:
            N = int(self.entry_years.get())
        except ValueError:
            N = 15  # по умолчанию
        self.ax.clear()
        if self.variant == "marriage":
            if 'Год' in self.data.columns and 'Браки' in self.data.columns:
                self.ax.set_title(f"Прогноз браков на {N} лет (скользящая средняя последних 15 лет)")
                self.ax.set_xlabel("Год")
                self.ax.set_ylabel("Количество")
                forecast = self.logic.moving_average_forecast_last_15_years(self.data['Браки'], N)
                years_forecast = [self.data['Год'].iloc[-1]+i+1 for i in range(N)]
                self.ax.plot(self.data['Год'], self.data['Браки'], label='Браки', marker='o')
                self.ax.plot(years_forecast, forecast, label='Прогноз', linestyle='--', marker='x', color='red')
                self.ax.legend()
            else:
                messagebox.showerror("Ошибка", "Файл должен содержать колонки: 'Год', 'Браки'")
        elif self.variant == "population":
            if 'Год' in self.data.columns and 'Население' in self.data.columns:
                self.ax.set_title(f"Прогноз численности населения на {N} лет (скользящая средняя последних 15 лет)")
                self.ax.set_xlabel("Год")
                self.ax.set_ylabel("Население")
                forecast = self.logic.moving_average_forecast_last_15_years(self.data['Население'], N)
                years_forecast = [self.data['Год'].iloc[-1]+i+1 for i in range(N)]
                self.ax.plot(self.data['Год'], self.data['Население'], label='Население', marker='o')
                self.ax.plot(years_forecast, forecast, label='Прогноз', linestyle='--', marker='x', color='red')
                self.ax.legend()
            else:
                messagebox.showerror("Ошибка", "Файл должен содержать колонки: 'Год', 'Население'")
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = DataApp(root)
    root.mainloop()
