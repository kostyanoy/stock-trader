import pandas as pd

from simulation.price.PriceManager import PriceManager


class PriceData(PriceManager):
    def __init__(self, file, column, per_lot=1):
        self.column = column
        self.per_lot = per_lot

        self.data = pd.read_csv(file)

        self.index = 0
        self.data_length = len(self.data)
        self.price = self.data[column][0]

    def update_price_all(self, instruments) -> bool:
        if self.index < self.data_length - 1:
            self.index += 1
            self.price = self.data[self.column][self.index]
            return True
        return False

    def get_price_all(self, instruments) -> dict[str, float]:
        return {instruments[0].instrument_id: self.price * self.per_lot}