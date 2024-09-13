from simulation.accounts.Account import Account
from simulation.bots.Bot import Bot
from simulation.instruments.Instrument import Instrument

# Bot with floating step where each  step is percent from price
class BotProportional(Bot):
    def __init__(self, account: Account, instrument: Instrument, step_percent: float, logging: bool = False):
        super().__init__(account, instrument, logging)
        self.step = step_percent

    def check_market(self) -> int:
        last_price = self.instrument.get_last_price()
        cur_price = self.account.get_price([self.instrument])[self.instrument.instrument_id]
        sign = -1 if cur_price >= last_price else 1
        amount = int(abs(round(cur_price - last_price, 2)) / max(last_price, cur_price) * 100 // self.step)

        return sign * amount

    def update_last_price(self, step_amount: int) -> float:
        cur_price = self.account.get_price([self.instrument])[self.instrument.instrument_id]
        last_price = self.instrument.get_last_price()
        price = last_price - (self.step * step_amount / 100) * max(last_price, cur_price)
        self.instrument.set_last_price(price)
        return price
