"""
    superbigdata 的接口部分，负责返回不同的数据对象子类
"""


from . import sina, tencent

def use(source):
    if source in ["sina"]:
        return sina.Sina()
    if source in ["qq", "tencent"]:
        return tencent.Tencent()
    raise NotImplementedError