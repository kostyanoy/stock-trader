from tinkoff.invest import Client
from tinkoff.invest.sandbox.client import SandboxClient

import creds
from simulation.instruments.utils import get_positions, instrument_info, instrument_from_ticker, get_instruments_prices, \
    quotation_to_float

# TOKEN = creds.SANDBOX_TOKEN
# ACCOUNT_ID = creds.SANDBOX_ACCOUNT_ID
# SAVE_PATH = "../saves/sandbox_trader/"
# CLIENT = SandboxClient

TOKEN = creds.TEST_TOKEN
ACCOUNT_ID = creds.TEST_ACCOUNT_ID
SAVE_PATH = "../saves/trur_trader_fixed_step/"
CLIENT = Client


def main():
    res1 = get_positions(TOKEN, ACCOUNT_ID, CLIENT)
    for money in res1.money:
        print(f"{money.currency.upper()}: {quotation_to_float(money)}")

    ids = [i.instrument_uid for i in res1.securities]
    res2 = get_instruments_prices(TOKEN, ids, CLIENT).last_prices

    for ind, share in enumerate(res2):
        instrument = instrument_info(TOKEN, share.instrument_uid).instrument
        ticker = instrument.ticker
        balance = res1.securities[ind].balance
        per_share = quotation_to_float(share.price)
        total = round(balance * per_share, 2)
        print(f"{ticker}: {balance} штук по {per_share}: {total}")


if __name__ == "__main__":
    main()
