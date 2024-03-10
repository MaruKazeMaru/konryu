# SPDX-FileCopyrightText: 2024 ShinagwaKazemaru
# SPDX-License-Identifier: MIT License

from __future__ import annotations

import pathlib

from ._dir_maker import DirMaker
from ._constants import *
from .exceptions import UnknownRule, TooManyEqual, NotSetDstDir

RULE_STR_RENDER = "RENDER"
RULE_STR_COPY = "COPY"
RULE_STR_LINKH = "LINKH"
RULE_STR_LINKS = "LINKS"
RULE_STR_IGNORE = "IGNORE"

VAR_STR_SRC_DIR = "SRC_DIR"
VAR_STR_DST_DIR = "DST_DIR"

def parse_plan(path:str) -> DirMaker:
    p = pathlib.Path(path).resolve(strict=True)
    src_dir_path = p.parent
    dst_dir_path = None
    manifests = []
    with open(p, mode='r') as f:
        i = 0
        while True:
            l = f.readline()
            if not l:
                break
            i += 1
            m = l.split('#')[0].strip() # method ?
            # empty or only comment line
            if m == "":
                continue
            v = m.split('=') # variable ?
            len_v = len(v)

            # method
            if len_v == 1:
                ms = m.split()
                if len(ms) == 1:
                    continue

                rule_str = ms[0].upper()
                if rule_str == RULE_STR_RENDER:
                    rule = RULE_RENDER
                elif rule_str == RULE_STR_COPY:
                    rule = RULE_COPY
                elif rule_str == RULE_STR_LINKH:
                    rule = RULE_LINKH
                elif rule_str == RULE_STR_LINKS:
                    rule = RULE_LINKS
                elif rule_str == RULE_STR_IGNORE:
                    rule = RULE_IGNORE
                else:
                    raise UnknownRule(ms[0], path, i)

                for pattern_str in ms[1:]:
                    manifests.append((rule, pattern_str))
            # variable
            elif len_v == 2:
                name = v[0].strip().upper()
                val = v[1].strip()
                if name == VAR_STR_SRC_DIR:
                    src_dir_path = pathlib.Path(val)
                    if not src_dir_path.is_absolute():
                        src_dir_path = p.parent / src_dir_path
                elif name == VAR_STR_DST_DIR:
                    dst_dir_path = pathlib.Path(val)
                    if not dst_dir_path.is_absolute():
                        dst_dir_path = p.parent / dst_dir_path
            else:
                raise TooManyEqual(path, i)

    if not dst_dir_path:
        raise NotSetDstDir(path)

    for i, m in enumerate(manifests):
        pattern_path = pathlib.Path(m[1])
        if not pattern_path.is_absolute():
            pattern_path = src_dir_path / pattern_path
        manifests[i] = (m[0], pattern_path)

    return DirMaker(manifests, src_dir_path.resolve(), dst_dir_path.resolve())
