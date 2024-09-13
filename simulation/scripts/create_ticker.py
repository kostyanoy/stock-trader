import creds
from simulation.instruments import saving
from simulation.instruments.utils import instrument_from_ticker
from simulation.price.PriceShare import PriceShare

TOKEN = creds.SANDBOX_TOKEN
SAVE_PATH = "../saves/trur_trader_fixed_step/"


def main():
    # init
    price_manager = PriceShare(TOKEN)

    # get ticker
    ticker = input("Input ticker: ").upper()
    instrument = instrument_from_ticker(TOKEN, ticker)
    if instrument is None:
        print("Sorry, can't find ticker")
        return

    # get price
    if not price_manager.update_price(instrument):
        print("Sorry, can't get price")
        return
    instrument.set_last_price(price_manager.get_price(instrument))
    instrument.update_last_changed()

    # get stock per step
    inp = input("Please, set stock per step (1 is default): ")
    stock = int(inp) if inp else 1
    instrument.stock_per_step = stock

    # get ticker mode
    mode = input("Please, set trading mode: track (default) or trade: ").strip().lower()
    if mode == "trade":
        instrument.mode = "trade"
    else:
        instrument.mode = "track"

    name = f"{SAVE_PATH}{ticker}.txt"
    saving.save(name, instrument)
    print("Saving: " + name)


if __name__ == "__main__":
    main()
