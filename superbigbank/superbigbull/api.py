from .trader.fake_trader import FakeTrader
from .trader.ths_trader import THSTrader

def use(trader_name, log=None):
    if trader_name == 'fake':
        return FakeTrader(log=log)
    elif trader_name == 'ths':
        return THSTrader()
    else:
        raise NotImplementedError("We have fake_trader only, you have no other choice.")
