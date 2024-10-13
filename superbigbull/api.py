from .trader.fake_trader import FakeTrader

def use(trader_name):
    if trader_name == 'fake':
        return FakeTrader()
    else:
        raise NotImplementedError("We have fake_trader only, you have no other choice.")
