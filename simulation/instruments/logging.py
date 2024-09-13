import csv
import datetime

from tinkoff.invest import Client

from simulation.instruments import utils
from simulation.instruments.Instrument import Instrument
from simulation.price.PriceManager import PriceManager


def get_date():
    return datetime.datetime.now()


def get_portfolio_cost(token: str, account_id: str, _client=Client):
    return utils.get_account_balance(token, account_id, _client)


def get_money_left(token: str, account_id: str, _client=Client):
    return utils.quotation_to_float(utils.get_positions(token, account_id, _client).money[0])


def log_txt(token: str, account_id: str, file: str, price_manager: PriceManager, instrument: Instrument, amount: int,
            res: str, _client=Client):
    with open(file, "a") as f:
        date = get_date()
        portfolio_cost = get_portfolio_cost(token, account_id, _client)
        money_left = get_money_left(token, account_id, _client)
        cost = price_manager.get_price(instrument)

        f.write(
            f"{date} {instrument.ticker} ({cost}) - amount: {amount}. {res}. Total cost: {portfolio_cost}. Money left: {money_left}\n")


def log_csv(token: str, account_id: str, file: str, price_manager: PriceManager, instrument: Instrument, amount: int,
            res: str, _client=Client):
    with open(file, "a", newline="") as f:
        date = get_date()
        portfolio_cost = get_portfolio_cost(token, account_id, _client)
        money_left = get_money_left(token, account_id, _client)
        cost = price_manager.get_price(instrument)

        writer = csv.writer(f)
        writer.writerow([date, instrument.ticker, cost, amount, res, portfolio_cost, money_left])
