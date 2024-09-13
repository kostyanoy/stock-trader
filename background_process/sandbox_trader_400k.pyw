import os

from tinkoff.invest.sandbox.client import SandboxClient

import creds
from simulation.accounts.AccountTinkoff import AccountTinkoff
from simulation.bots.BotProportional import BotProportional
from simulation.instruments import saving
from simulation.instruments.Instrument import Instrument
from simulation.instruments.logging import log_csv
from simulation.price.PriceShare import PriceShare

LOG_CSV_FILE = "../simulation/logs/sandbox_trader/log.csv"
SAVES_PATH = "../simulation/saves/sandbox_trader"  # list of tracked shares
HISTORY_LOGGING = True
BOT_LOGGING = True
STEP = 2  # percent for step

TOKEN = creds.SANDBOX_TOKEN  # token for account access
ACCOUNT_ID = creds.SANDBOX_ACCOUNT_ID


def main():
    price_manager = PriceShare(TOKEN)
    account = AccountTinkoff(price_manager, TOKEN, ACCOUNT_ID, SandboxClient)
    save_files = [f"{SAVES_PATH}/{f}" for f in os.listdir(SAVES_PATH) if os.path.isfile(f"{SAVES_PATH}/{f}")]
    instruments = [saving.load(f) for f in save_files]
    price_manager.update_price_all(instruments)

    for ind, instrument in enumerate(instruments):
        res, amount = trade(account, instrument, save_files[ind])
        if HISTORY_LOGGING:
            log_csv(TOKEN, ACCOUNT_ID, LOG_CSV_FILE, price_manager, instrument, amount, str(res), SandboxClient)


def trade(account: AccountTinkoff, instrument: Instrument, save_file: str):
    bot = BotProportional(account, instrument, STEP, BOT_LOGGING)
    res, amount = bot.trade()
    if res:
        saving.save(save_file, instrument)

    return res, amount


if __name__ == "__main__":
    main()
