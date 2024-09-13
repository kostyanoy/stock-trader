from tinkoff.invest import Quotation, Client, AssetInstrument, PositionsResponse, InstrumentIdType, InstrumentResponse, \
    MoneyValue

from simulation.instruments.Instrument import Instrument


def quotation_to_float(quotation: Quotation | MoneyValue) -> float:
    """
    Convert Quotation, MoneyValue class to float
    :param quotation: tinkoff class
    :return: float result
    """
    return quotation.units + quotation.nano / 1e9


def ticker_info(token: str, ticker: str) -> AssetInstrument:
    """
    Get short info by ticker
    :param token: any token to access stocks
    :param ticker: string ticker of share
    :return: short info
    """
    with Client(token) as client:
        r = client.instruments.get_assets()
        for i in r.assets:
            for j in i.instruments:
                if j.ticker == ticker:
                    return j


def instrument_info(token: str, instrument_id) -> InstrumentResponse:
    """
    Get full info about instrument based on instrument id
    :param token: any token to access stocks
    :param instrument_id: id of instrument
    :return: full info
    """
    with Client(token) as client:
        r = client.instruments.get_instrument_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_UID, id=instrument_id)
    return r


def instrument_from_ticker(token: str, ticker: str) -> Instrument | None:
    """
    Get Instrument class from ticker string
    :param token: any token to access stocks
    :param ticker: string ticker
    :return: Instrument class
    """
    info = ticker_info(token, ticker)
    if info is None:
        return None
    instrument = Instrument(info.uid, info.ticker, info.class_code)
    return instrument


def get_positions(token: str, account_id: str, _client=Client) -> PositionsResponse:
    """
    Get positions of account
    :param token: token to access account
    :param account_id: corresponding id
    :return: positions of account
    """
    with _client(token) as client:
        r = client.operations.get_positions(account_id=account_id)
        return r


def get_account_balance(token: str, account_id: str, _client=Client) -> float:
    """
    Get total
    :param token: token to access account
    :param account_id: corresponding id
    :return: total money of a portfolio
    """
    with _client(token) as client:
        r = client.operations.get_portfolio(account_id=account_id).total_amount_portfolio
        return quotation_to_float(r)

def get_instruments_prices(token: str, instrument_ids: list, _client=Client):
    with _client(token) as client:
        resp = client.market_data.get_last_prices(instrument_id=instrument_ids)
        return resp
