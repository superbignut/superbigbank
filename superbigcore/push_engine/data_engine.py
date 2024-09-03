import superbigdata
from base_engine import BaseEngine

class DefaultDataEngine(BaseEngine):

    EventType = 'superbigdata'

    def __init__(self):
        super().__init__()
        self.source = None

    def init(self):
        # 这个函数没看懂
        self.source = superbigdata.use('sina')

    def fetch_data(self):
        return self.source.all_market()