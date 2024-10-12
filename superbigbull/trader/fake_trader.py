"""
    这是一个假的 交易对象， 提供基本的买卖函数， 先越简单越好，

"""
BULL= {'BUY':0, "SELL":1} # 买卖方向

class OneDeal:
    # 一笔交易的类型， 时间，名字，数量，买卖方向
    def __init__(self, time, name, num, direction):
        pass

class FakeTrader:
    # 虚假的交易商， 会扣除你非常多的手续费
    def __init__(self, init_money=0):
        # 初始资金
        pass

    def buy(self, name, num):
        # 买 num 个 name
        pass

    def sell(self, name, num):
        # 卖 num 个 name
        pass

    def check_position(self):
        # 查看股票持仓情况（持有情况）
        pass

    def check_cost_money(self):
        # 查看总共向账户投入的钱
        pass

    def add_money_to_account(self):
        # 继续向账户中投钱
        pass

    def get_today_deal(self):
        # 返回当日的所有交易
        pass


