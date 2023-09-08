import pandas as pd

class BarCodeMatching:
    def __init__(self, base_path='base_matching.csv') -> None:
        self.base = []
        self.base_path = base_path

    def load_base(self) -> None:
        self.base = pd.read_csv(self.base_path)

    def get_match(self, barcode: str, match_by_first_symbols=7):
        '''
        barcode: баркод для мэтчинга
        match_by_first_symbols: до скольки символов мэтчить, если длина больше 13

        return: ошибка (0 - успешно найдено по 13, 1 - найдено по 7, 2 - ничего не найдено), 
                pd.Series - запись в базе
        '''
        if len(barcode) == 13:
            output = self.base[self.base.barcode == barcode]
            if output.shape[0] > 0:
                error = 0
            else:
                error = 2
        else:
            output = self.base[self.base.barcode.str.startswith(barcode[:match_by_first_symbols], na=False)]
            if output.shape[0] > 0:
                error = 1
            else:
                error = 2

        return error, self.base[self.base.barcode == barcode]
    
    def append_to_base(self, **fileds):
        self.base = self.base.append(fileds)
        self.base.to_csv(self.base_path)
