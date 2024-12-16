
import argparse

from userstat.main import main


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="ToolBox")
    parser.add_argument('tool')
    args = parser.parse_args()
    match args.tool:
        case 'userstat':
            main()
        case _:
            print(f"Unknown tool: {args.tool}")