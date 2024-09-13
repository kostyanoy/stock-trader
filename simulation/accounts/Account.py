from abc import ABC, abstractmethod

from simulation.instruments.Instrument import Instrument
from simulation.price.PriceManager import PriceManager

# Abstract class for doing buy/sell operations
class Account(ABC):
    def __init__(self, price_manager: PriceManager):
        self.price_manager = price_manager

    # buy shares amount
    @abstractmethod
    def buy_stock(self, instrument: Instrument, amount: int) -> bool:
        pass

    # sell shares amount
    @abstractmethod
    def sell_stock(self, instrument: Instrument, amount: int) -> bool:
        pass

    # get amount of shares on the account
    @abstractmethod
    def get_amount(self, instruments: list[Instrument]) -> dict[str, int]:
        pass

    # update prices for shares in this class
    def update_price(self, instruments: list[Instrument]) -> bool:
        return self.price_manager.update_price_all(instruments)

    # get prices for shares from this class
    def get_price(self, instruments: list[Instrument]) -> dict[str, float]:
        return self.price_manager.get_price_all(instruments)
