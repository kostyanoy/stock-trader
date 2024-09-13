from tinkoff.invest import OrderType, OrderDirection, RequestError, Client

from simulation.accounts.Account import Account
from simulation.instruments.Instrument import Instrument
from simulation.price.PriceManager import PriceManager


class AccountTinkoff(Account):
    def __init__(self, price_manager: PriceManager, token: str, account_id: str, client=Client):
        super().__init__(price_manager)
        self.token = token
        self.account_id = account_id
        self.client = client

    def buy_stock(self, instrument: Instrument, amount: int) -> bool:
        try:
            with self.client(self.token) as client:
                order = client.orders.post_order(account_id=self.account_id,
                                                 instrument_id=instrument.instrument_id,
                                                 quantity=amount,
                                                 order_type=OrderType.ORDER_TYPE_MARKET,
                                                 direction=OrderDirection.ORDER_DIRECTION_BUY)

                return client.orders.get_order_state(account_id=self.account_id,
                                                     order_id=order.order_id).execution_report_status == 1
        except RequestError as er:
            print(er)
            return False

    def sell_stock(self, instrument: Instrument, amount: int) -> bool:
        try:
            with self.client(self.token) as client:
                order = client.orders.post_order(account_id=self.account_id,
                                                 instrument_id=instrument.instrument_id,
                                                 quantity=amount,
                                                 order_type=OrderType.ORDER_TYPE_MARKET,
                                                 direction=OrderDirection.ORDER_DIRECTION_SELL)

                return client.orders.get_order_state(account_id=self.account_id,
                                                     order_id=order.order_id).execution_report_status == 1
        except RequestError as er:
            print(er)
            return False

    def get_amount(self, instruments: list[Instrument]) -> dict[str, int]:
        res = {i.instrument_id: 0 for i in instruments}
        try:
            with Client(self.token) as client:
                r = client.operations.get_positions(account_id=self.account_id)

                for i in r.securities:
                    if i.instrument_uid in res:
                        res[i.instrument_uid] = i.balance
        except RequestError as er:
            print(er)

        return res
