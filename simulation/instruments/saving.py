from builtins import Exception

from simulation.instruments.Instrument import Instrument


def save_all(path: str, instruments: list[Instrument]) -> bool:
    json_data = Instrument.schema().dumps(instruments, many=True)
    try:
        with open(path, "w") as f:
            f.write(json_data)
            return True
    except Exception as er:
        print(er)
        return False


def load_all(path: str) -> list[Instrument]:
    with open(path, "r") as f:
        return Instrument.schema().loads(f.read(), many=True)


def save(path: str, instrument: Instrument) -> bool:
    return save_all(path, [instrument])


def load(path: str) -> Instrument:
    return load_all(path)[0]
