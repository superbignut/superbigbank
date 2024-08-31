


class A:
    def __init__(self):
        self._word = 1

    @property
    def func(self):
        return self._word

    
    # func = property(fget=func)
    print(type(func))


if __name__ == '__main__':
    a = A()

    print(a.func)


