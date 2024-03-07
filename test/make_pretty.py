import sys
from konryu import parse_plan

if __name__ == "__main__":
    maker = parse_plan(sys.argv[1])
    maker.make()
