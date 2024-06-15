import unittest

def run_tests():
    loader = unittest.TestLoader()
    suite = loader.discover('tests')

    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == "__main__":
    run_tests()
