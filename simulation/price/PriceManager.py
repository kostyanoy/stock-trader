from abc import abstractmethod, ABC

from simulation.instruments.Instrument import Instrument


class PriceManager(ABC):
    @abstractmethod
    def get_price_all(self, instruments: list[Instrument]) -> dict[str, float]:
        pass

    @abstractmethod
    def update_price_all(self, instruments: list[Instrument]) -> bool:
        pass

    def get_price(self, instrument: Instrument) -> float:
        price = self.get_price_all([instrument])[instrument.instrument_id]
        return price

    def update_price(self, instrument: Instrument) -> bool:
        res = self.update_price_all([instrument])
        return res
