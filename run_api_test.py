import argparse

from apitester.testsequence import TestSequence

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="run_api_test")
    parser.add_argument('filename')
    args = parser.parse_args()
    test_seq = TestSequence(args.filename)
    test_seq.run()

