import os
from konryu import *

def _get_dir():
    return os.path.join(os.path.dirname(__file__), "data")    


def test_parse_plan():
    dir = _get_dir()

    maker = parse_plan(os.path.join(dir, "plan_s1.txt"))
    assert len(maker.manifests) == 6
    maker = parse_plan(os.path.join(dir, "plan_s2.txt"))
    assert len(maker.manifests) == 3

    try:
        parse_plan(os.path.join(dir, "plan_f1.txt"))
    except NotSetDstDir: pass
    try:
        parse_plan(os.path.join(dir, "plan_f2.txt"))
    except UnknownRule: pass
    try:
        parse_plan(os.path.join(dir, "plan_f3.txt"))
    except TooManyEqual: pass


def test_dir_maker():
    maker = parse_plan(os.path.join(_get_dir(), "plan.txt"))
    s = str(maker)
    maker.make()


if __name__ == "__main__":
    test_parse_plan()
    test_dir_maker()
