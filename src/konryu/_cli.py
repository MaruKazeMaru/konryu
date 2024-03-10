import argparse

from ._plan import parse_plan

def make():
    parser = argparse.ArgumentParser(description="Jinja2 CLI tool")
    parser.add_argument("planpath", help="path of plan file", type=str, default="plan.txt")
    parser.add_argument("-l", "--log", help="show log", action="store_true")
    args = parser.parse_args()

    maker = parse_plan(args.planpath)
    if args.log:
        maker.logging = True
    maker.make()


if __name__ == "__main__":
    make()
