"""
    本来是想要去雪球的web上做虚拟交易的，但是仔细想想没这个必要
"""

from .follower import BaseFollower


class XqFollower(BaseFollower):
    LOGIN_PAGE = "www.xueqiu.com"
    LOGIN_API = "https://www.xueqiu.com/snowman/login"

    def __init__(self):
        super().__init__()
        pass
