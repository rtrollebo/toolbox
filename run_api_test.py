import argparse

from apitester.testsequence import TestSequence

def run_tests(filename):
    test_seq = TestSequence(filename)
    test_seq.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="run_api_test")
    parser.add_argument('filename')
    args = parser.parse_args()
    run_tests(args.filename)

