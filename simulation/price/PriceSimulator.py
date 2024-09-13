import random

from simulation.instruments.Instrument import Instrument
from simulation.price.PriceManager import PriceManager


class PriceSimulator(PriceManager):
    def __init__(self, instruments: list[Instrument], price=100, step=0.1):
        self.prices = {i.instrument_id: price for i in instruments}

        self.start_price = price
        self.step = step

    def update_price_all(self, instruments: list[Instrument]) -> bool:
        for i in instruments:
            i_id = i.instrument_id
            if i_id not in self.prices:
                self.prices[i_id] = self.start_price

            change = self.step * random.randint(-10, 10)

            if self.prices[i_id] + change > 0:
                self.prices[i_id] += change

        return True

    def get_price_all(self, instruments: list[Instrument]) -> dict[str, float]:
        res = {}
        for i in instruments:
            i_id = i.instrument_id
            if i_id not in self.prices:
                self.prices[i_id] = self.start_price

            res[i_id] = self.prices[i_id]

        return res
