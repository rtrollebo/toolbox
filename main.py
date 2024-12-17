
import argparse

from userstat.main import main


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="ToolBox")
    parser.add_argument('tool')
    parser.add_argument('--args', nargs='+', help='Optional tool arguments', default=[])
    args = parser.parse_args()
    print(args.args)
    match args.tool:
        case 'userstat':
            main(args.args)
        case _:
            print(f"Unknown tool: {args.tool}")