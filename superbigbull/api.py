from .trader.fake_trader import FakeTrader

def use(trader_name, log=None):
    if trader_name == 'fake':
        return FakeTrader(log=log)
    else:
        raise NotImplementedError("We have fake_trader only, you have no other choice.")
