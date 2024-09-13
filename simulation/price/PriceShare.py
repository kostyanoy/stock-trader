from tinkoff.invest import RequestError
from tinkoff.invest.clients import Client

from simulation.instruments.Instrument import Instrument
from simulation.price.PriceManager import PriceManager
from simulation.instruments.utils import quotation_to_float


class PriceShare(PriceManager):
    def __init__(self, token: str):
        self.token = token

        self.prices = dict[str, float]()

    def get_price_all(self, instruments: list[Instrument]) -> dict[str, float]:
        res = {}
        for i in instruments:
            i_id = i.instrument_id
            if i_id in self.prices:
                res[i_id] = self.prices[i_id]
        return res

    def update_price_all(self, instruments: list[Instrument]) -> bool:
        try:
            with Client(self.token) as client:
                ids = [i.instrument_id for i in instruments]
                resp = client.market_data.get_last_prices(instrument_id=ids)
            for i in resp.last_prices:
                self.prices[i.instrument_uid] = quotation_to_float(i.price)
            return True
        except RequestError as er:
            print(er)
            return False
