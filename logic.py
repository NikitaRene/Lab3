import pandas as pd

class MarriageLogic:
    @staticmethod
    def load_file(file_path):
        """Загрузить CSV или Excel и вернуть DataFrame"""
        if file_path.endswith(".csv"):
            data = pd.read_csv(file_path)
        else:
            data = pd.read_excel(file_path)
        return data

    @staticmethod
    def most_common_age(data):
        """
        Вычисляет возраст, когда чаще женились/разводились.
        Предполагаем колонки:
        'Возраст_мужчины_женитьба', 'Возраст_женщины_замужество',
        'Возраст_мужчины_развод', 'Возраст_женщины_развод'
        """
        result = {}
        if 'Возраст_мужчины_женитьба' in data.columns:
            result['Мужчины женились чаще всего'] = data['Возраст_мужчины_женитьба'].mode()[0]
        if 'Возраст_женщины_замужество' in data.columns:
            result['Женщины выходили замуж чаще всего'] = data['Возраст_женщины_замужество'].mode()[0]
        if 'Возраст_мужчины_развод' in data.columns:
            result['Мужчины разводились чаще всего'] = data['Возраст_мужчины_развод'].mode()[0]
        if 'Возраст_женщины_развод' in data.columns:
            result['Женщины разводились чаще всего'] = data['Возраст_женщины_развод'].mode()[0]
        return result

    @staticmethod
    def moving_average_forecast_last_15_years(series, N):
        """
        Прогноз методом скользящей средней по последним 15 годам.
        series: pd.Series с данными (например, количество браков)
        N: количество лет для прогноза
        """
        last_15 = series.tail(15)               # берём последние 15 лет
        ma = last_15.rolling(window=3).mean()   # скользящая средняя за 3 года
        last_ma = ma.iloc[-1]                   # последнее значение средней
        forecast = [last_ma] * N                # прогноз на N лет
        return forecast
