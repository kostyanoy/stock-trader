import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import creds
from simulation.accounts.AccountTinkoff import AccountTinkoff
from simulation.bots.BotFlat import BotFlat
from simulation.instruments import saving
from simulation.instruments.Instrument import Instrument
from simulation.instruments.logging import log_csv, log_txt
from simulation.price.PriceShare import PriceShare

# LOG_TXT_FILE = "../simulation/logs/trur_trader_fixed_step/log.txt"
LOG_CSV_FILE = os.path.dirname(__file__) + "/../simulation/logs/trur_trader_fixed_step/log.csv"
LOGGING_MODE = "csv"
SAVES_PATH = os.path.dirname(__file__) + "/../simulation/saves/trur_trader_fixed_step"  # list of tracked shares
HISTORY_LOGGING = True
BOT_LOGGING = True
STEP = 0.03  # change amount for one step

TOKEN = creds.TEST_TOKEN  # token for account access
ACCOUNT_ID = creds.TEST_ACCOUNT_ID


def main():
    price_manager = PriceShare(TOKEN)
    account = AccountTinkoff(price_manager, TOKEN, ACCOUNT_ID)
    save_files = [f"{SAVES_PATH}/{f}" for f in os.listdir(SAVES_PATH) if os.path.isfile(f"{SAVES_PATH}/{f}")]
    instruments = [saving.load(f) for f in save_files]
    price_manager.update_price_all(instruments)

    for ind, instrument in enumerate(instruments):
        if instrument.mode == "trade":
            res, amount = trade(account, instrument, save_files[ind])
        # elif instrument.mode == "track":
        #     res, amount = track(account, instrument, save_files[ind])
        else:
            raise AttributeError("No such instrument mode")

        if HISTORY_LOGGING:
            if LOGGING_MODE == "csv":
                log_csv(TOKEN, ACCOUNT_ID, LOG_CSV_FILE, price_manager, instrument, amount, str(res))
            # elif LOGGING_MODE == "txt":
            #     log_txt(TOKEN, ACCOUNT_ID, LOG_TXT_FILE, price_manager, instrument, amount, str(res))
            else:
                raise AttributeError("No such logging mode")


def trade(account: AccountTinkoff, instrument: Instrument, save_file: str):
    # bot = BotProportional(account, instrument, STEP, BOT_LOGGING)
    # res, amount = bot.trade()
    # if res:
    #     saving.save(save_file, instrument)
    #
    # return res, amount

    bot = BotFlat(account, instrument, STEP, BOT_LOGGING)
    bot.set_step(STEP)
    res, amount = bot.trade()
    if res:
        saving.save(save_file, instrument)

    return res, amount


# def track(account: AccountTinkoff, instrument: Instrument, save_file: str):
#     bot = BotProportional(account, instrument, STEP, BOT_LOGGING)
#     amount = bot.track()
#     saving.save(save_file, instrument)
#
#     return "Track", amount


if __name__ == "__main__":
    main()
