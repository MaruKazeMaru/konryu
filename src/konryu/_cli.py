import argparse

from ._plan import parse_plan

def make():
    parser = argparse.ArgumentParser(description="Jinja2 CLI tool")
    parser.add_argument("planpath", help="path of plan file", type=str, default="plan.txt")
    args = parser.parse_args()

    maker = parse_plan(args.planpath)
    maker.make()


if __name__ == "__main__":
    make()
