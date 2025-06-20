
import argparse
from enum import Enum

from userstat.main import main


class Tool(Enum):
    USERSTAT = "userstat"
    APITESTER = "apitester"


class ToolBox:
    """

    """
    def __init__(self, tool: Tool, required_parameters=None, mainFunc=None):
        if required_parameters is None:
            required_parameters = []
        self.tool = tool
        self.required_parameters = required_parameters
        self.mainFunc = mainFunc

    def execute(self, *args):
        self.mainFunc(*args)


if __name__ == '__main__':
    toolboxes = {Tool.USERSTAT.value: ToolBox(tool=Tool.USERSTAT, required_parameters=[], mainFunc=main)}


    parser = argparse.ArgumentParser(prog="ToolBox")
    parser.add_argument('tool')
    parser.add_argument('--args', nargs='+', help='Optional tool arguments', default=[])
    args = parser.parse_args()
    print(args.args)
    match args.tool:
        case Tool.USERSTAT.value:
            toolboxes[Tool.USERSTAT.value].execute(args.args)
        case Tool.APITESTER.value:
            print("TBD")
        case _:
            print(f"Unknown tool: {args.tool}")



