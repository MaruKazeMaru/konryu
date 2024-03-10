# SPDX-FileCopyrightText: 2024 ShinagwaKazemaru
# SPDX-License-Identifier: MIT License

class PlanSyntaxError(SyntaxError):
    pass

class UnknownRule(PlanSyntaxError):
    def __init__(self, rule:str, path:str, line:int) -> None:
        super().__init__("can't parse {} in {}, line {}".format(rule, path, line))


class TooManyEqual(PlanSyntaxError):
    def __init__(self, path:str, line:int) -> None:
        super().__init__("too many '=' in {}, line {}".format(path, line))


class NotSetDstDir(PlanSyntaxError):
    def __init__(self, path:str) -> None:
        super().__init__("destination directory is not set in {}".format(path))
