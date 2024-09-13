from simulation.instruments.Instrument import Instrument
from simulation.accounts.Account import Account
from simulation.price.PriceManager import PriceManager


class AccountStub(Account):
    def __init__(self, price_manager: PriceManager, money: float, commission=0):
        super().__init__(price_manager)
        self.money = money
        self.commission = commission

        self.stock = dict[str, int]()

    def buy_stock(self, instrument: Instrument, amount: int) -> bool:
        prices = self.price_manager.get_price_all([instrument])
        total = prices[instrument.instrument_id] * amount * (1 + self.commission)
        if self.money < total:
            return False

        if instrument.instrument_id not in self.stock:
            self.stock[instrument.instrument_id] = 0

        self.stock[instrument.instrument_id] += amount
        self.money -= total
        return True

    def sell_stock(self, instrument: Instrument, amount: int) -> bool:
        if instrument.instrument_id not in self.stock or self.stock[instrument.instrument_id] < amount:
            return False

        prices = self.price_manager.get_price_all([instrument])

        self.stock[instrument.instrument_id] -= amount
        self.money += prices[instrument.instrument_id] * amount
        return True

    def get_amount(self, instruments: list[Instrument]) -> dict[str, int]:
        res = {}
        for inst in instruments:
            i_id = inst.instrument_id
            if i_id in self.stock:
                res[i_id] = self.stock[i_id]
            else:
                res[i_id] = 0
        return res



