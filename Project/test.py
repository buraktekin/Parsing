import unittest
from parser import is_cnf

class TestIsCnf(unittest.TestCase):
    def test_is_cnf(self):
        res = is_cnf(
            {'S': ['AB'], 'A': ['CD', 'CF'], 'B': ['c', 'EB'], 'C': ['a'], 'D': ['b'], 'E': ['c'], 'F': ['AD']}
        )
        print("Result: ", res)
        self.assertEqual(res, True)


if __name__ == '__main__':
    unittest.main()