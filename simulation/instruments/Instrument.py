import time
from ctypes import ArgumentError
from dataclasses import dataclass

from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Instrument:
    instrument_id: str
    ticker: str
    class_code: str
    last_price: float | None = None
    last_changed: float | None = None
    stock_per_step: int = 1
    mode: str = "track"
    rolling_amount: int = 0

    def get_last_price(self):
        return self.last_price

    def set_last_price(self, price: float):
        if price <= 0:
            raise ArgumentError("Price must be more than 0")

        self.last_price = price

    def set_last_changed(self, timestamp: float):
        self.last_changed = timestamp

    def get_last_changed(self) -> float:
        return self.last_changed

    def update_last_changed(self):
        self.last_changed = time.time()

    def update_rolling_amount(self, is_buy: bool):
        if is_buy:
            self.rolling_amount = max(self.rolling_amount, 0) + 1
        else:
            self.rolling_amount = min(self.rolling_amount, 0) - 1
