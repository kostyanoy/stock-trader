import time
from abc import ABC, abstractmethod

from simulation.accounts.Account import Account
from simulation.instruments.Instrument import Instrument

# Abstract Bot class with default methods
class Bot(ABC):
    def __init__(self, account: Account, instrument: Instrument, is_logging: bool):
        self.account = account # managing operations
        self.instrument = instrument # share
        self.logging = is_logging # logging mode

        if instrument.get_last_price() is None:
            instrument.set_last_price(account.get_price([instrument])[instrument.instrument_id])

    # how much shares to buy/sell
    @abstractmethod
    def check_market(self) -> int:
        pass

    # how the instrument changes from amount
    @abstractmethod
    def update_instrument(self, amount: int) -> float:
        pass

    # try buy/sell shares with account
    def update_stock(self, amount: int, buy: bool) -> bool:
        if amount == 0:
            res = False
        elif buy:
            res = self.account.buy_stock(self.instrument, amount)
        else:
            res = self.account.sell_stock(self.instrument, amount)
        return res

    # print log in console
    def print_log(self, amount: int, buy: bool, res: str):
        last_price = self.instrument.get_last_price()
        cur_price = self.account.get_price([self.instrument])[self.instrument.instrument_id]
        if amount == 0:
            print(f"{self.instrument.ticker}: Doing nothing. Last price: {last_price} Current: {cur_price}")
        elif buy:
            print(f"{self.instrument.ticker}: Trying to buy {amount}: {res}. Last price: {last_price} Current: {cur_price}")
        else:
            print(f"{self.instrument.ticker}: Trying to sell {amount}: {res}. Last price: {last_price} Current: {cur_price}")

    # compute buy/sell operation
    def trade(self) -> tuple[bool, int]:
        steps_amount = self.check_market()
        shares_amount = steps_amount * self.instrument.stock_per_step
        res = self.update_stock(abs(shares_amount), shares_amount > 0)
        if self.logging:
            self.print_log(abs(shares_amount), shares_amount > 0, str(res))
        if res:
            self.update_instrument(steps_amount)
            self.instrument.update_last_changed()
        return res, shares_amount

    # simulate buy/sell operation
    def track(self) -> int:
        steps_amount = self.check_market()
        shares_amount = steps_amount * self.instrument.stock_per_step
        if self.logging:
            self.print_log(abs(shares_amount), shares_amount > 0, "Tracking")
        self.update_instrument(steps_amount)
        self.instrument.update_last_changed()
        return shares_amount
