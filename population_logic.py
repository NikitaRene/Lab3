import pandas as pd

class PopulationLogic:
    @staticmethod
    def load_file(file_path):
        """Загрузить CSV или Excel и вернуть DataFrame"""
        if file_path.endswith(".csv"):
            data = pd.read_csv(file_path)
        else:
            data = pd.read_excel(file_path)
        return data

    @staticmethod
    def max_growth_decline(data):
        """
        Вычисляет максимальный процент прироста и убыли населения за год.
        Предполагаем колонку 'Население'.
        """
        data = data.copy()
        data['Процент_изменения'] = data['Население'].pct_change() * 100
        max_growth = data['Процент_изменения'].max()
        max_decline = data['Процент_изменения'].min()
        year_max_growth = data.loc[data['Процент_изменения'].idxmax(), 'Год']
        year_max_decline = data.loc[data['Процент_изменения'].idxmin(), 'Год']
        return {
            'Макс. прирост (%)': max_growth,
            'Год макс. прироста': year_max_growth,
            'Макс. убыли (%)': max_decline,
            'Год макс. убыли': year_max_decline
        }

    @staticmethod
    def moving_average_forecast_last_15_years(series, N):
        """
        Прогноз методом скользящей средней по последним 15 годам.
        series: pd.Series с данными (например, численность населения)
        N: количество лет для прогноза
        """
        last_15 = series.tail(15)               # берём последние 15 лет
        ma = last_15.rolling(window=3).mean()   # скользящая средняя за 3 года
        last_ma = ma.iloc[-1]                   # последнее значение средней
        forecast = [last_ma] * N                # прогноз на N лет
        return forecast
