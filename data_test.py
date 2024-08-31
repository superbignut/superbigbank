import superbigdata
import unittest


class TestSuperbigData(unittest.TestCase):
    def test_stock_code_with_prefix(self):
        cases = ['sina', 'qq']
        for src in cases:
            q = superbigdata.use(src)
            # data



if __name__ == "__main__":
    unittest.main()


