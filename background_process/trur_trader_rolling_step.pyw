import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import creds
from simulation.accounts.AccountTinkoff import AccountTinkoff
from simulation.bots.BotRollingFlat import BotRollingFlat
from simulation.instruments import saving
from simulation.instruments.Instrument import Instrument
from simulation.instruments.logging import log_csv
from simulation.price.PriceShare import PriceShare
from simulation.instruments.utils import ensure_dirs_exist

# path
BASE_DIR = os.path.dirname(__file__)
LOG_CSV_FILE = BASE_DIR + "/../simulation/logs/trur_trader_rolling_step/log.csv"
SAVES_PATH = BASE_DIR + "/../simulation/saves/trur_trader_rolling_step/"  # list of tracked shares

# parameters
LOGGING_MODE = "csv"
HISTORY_LOGGING = True
BOT_LOGGING = True
STEP_FLAT = 0.03  # change amount for one step
ROLLING_STRENGTH = 1  # additional amount per repeating operation

# tokens
TOKEN = creds.TEST_TOKEN  # token for account access
ACCOUNT_ID = creds.TEST_ACCOUNT_ID


def main():
    # create folders
    ensure_dirs_exist([LOG_CSV_FILE, SAVES_PATH])

    price_manager = PriceShare(TOKEN)
    account = AccountTinkoff(price_manager, TOKEN, ACCOUNT_ID)
    save_files = [f"{SAVES_PATH}/{f}" for f in os.listdir(SAVES_PATH) if os.path.isfile(f"{SAVES_PATH}/{f}")]
    instruments = [saving.load(f) for f in save_files]
    price_manager.update_price_all(instruments)

    for ind, instrument in enumerate(instruments):
        if instrument.mode == "trade":
            res, amount = trade(account, instrument, save_files[ind])
        else:
            raise AttributeError("No such instrument mode")

        if HISTORY_LOGGING:
            if LOGGING_MODE == "csv":
                log_csv(TOKEN, ACCOUNT_ID, LOG_CSV_FILE, price_manager, instrument, amount, str(res))
            else:
                raise AttributeError("No such logging mode")


def trade(account: AccountTinkoff, instrument: Instrument, save_file: str):
    bot = BotRollingFlat(account, instrument, 0, BOT_LOGGING, rolling_strength=ROLLING_STRENGTH)
    bot.set_step(STEP_FLAT)
    res, amount = bot.trade()
    if res:
        saving.save(save_file, instrument)

    return res, amount


if __name__ == "__main__":
    main()
