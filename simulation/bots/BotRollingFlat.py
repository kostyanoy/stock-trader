import math

from simulation.accounts.Account import Account
from simulation.bots.BotFlat import BotFlat
from simulation.instruments.Instrument import Instrument


# Bot with fixed step for buying shares
class BotRollingFlat(BotFlat):
    def __init__(self, account: Account, instrument: Instrument, step_percent: float, is_logging: bool = False,
                 rolling_strength: int = 0):
        super().__init__(account, instrument, step_percent, is_logging)
        self.rolling_strength = rolling_strength

    def get_rolling_amount(self, shares_amount):
        if self.instrument.rolling_amount * shares_amount > 0:
            return self.instrument.rolling_amount * self.rolling_strength
        else:
            return 0

    def check_market(self) -> int:
        signed_amount = super().check_market()
        signed_amount += self.get_rolling_amount(signed_amount)

        return signed_amount

    def update_instrument(self, amount: int) -> float:
        signed_amount = amount - self.get_rolling_amount(amount)
        price = self.instrument.get_last_price() - signed_amount * self.step

        self.instrument.set_last_price(price)
        self.instrument.update_rolling_amount(signed_amount > 0)

        return price

    def set_rolling_strength(self, strength):
        self.rolling_strength = strength
