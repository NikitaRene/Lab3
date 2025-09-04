import tkinter as tk
from tkinter import ttk, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from logic import MarriageLogic

class MarriageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Анализ браков и разводов")
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

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files","*.csv"),("Excel Files","*.xlsx")])
        if file_path:
            self.data = MarriageLogic.load_file(file_path)
            self.show_table()
            # вывод возраста
            ages = MarriageLogic.most_common_age(self.data)
            print("Возрастные статистики:", ages)

    def show_table(self):
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = list(self.data.columns)
        self.tree["show"] = "headings"
        for col in self.data.columns:
            self.tree.heading(col, text=col)
        for _, row in self.data.iterrows():
            self.tree.insert("", "end", values=list(row))

    def plot_data(self):
        if hasattr(self, 'data'):
            self.ax.clear()
            self.ax.set_title("Браки и разводы по годам")
            self.ax.set_xlabel("Год")
            self.ax.set_ylabel("Количество")
            if 'Год' in self.data.columns and 'Браки' in self.data.columns and 'Разводы' in self.data.columns:
                self.ax.plot(self.data['Год'], self.data['Браки'], label='Браки', marker='o')
                self.ax.plot(self.data['Год'], self.data['Разводы'], label='Разводы', marker='o')
                self.ax.legend()
            self.canvas.draw()

    def forecast(self):
        if hasattr(self, 'data'):
            # Получаем N лет из поля ввода
            try:
                N = int(self.entry_years.get())
            except ValueError:
                N = 15  # по умолчанию, если не введено число
            self.ax.clear()
            self.ax.set_title(f"Прогноз по скользящей средней (последние 15 лет) на {N} лет")
            self.ax.set_xlabel("Год")
            self.ax.set_ylabel("Количество")
            if 'Год' in self.data.columns and 'Браки' in self.data.columns:
                forecast = MarriageLogic.moving_average_forecast_last_15_years(self.data['Браки'], N)
                years_forecast = [self.data['Год'].iloc[-1]+i+1 for i in range(N)]
                self.ax.plot(self.data['Год'], self.data['Браки'], label='Браки', marker='o')
                self.ax.plot(years_forecast, forecast, label='Прогноз', linestyle='--', marker='x')
                self.ax.legend()
            self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = MarriageApp(root)
    root.mainloop()