from . import sina, tencent

def use(source):
    if source in ["sina"]:
        return sina.Sina()
    if source in ["qq", "tencent"]:
        return tencent.Tencent()
    raise NotImplementedError