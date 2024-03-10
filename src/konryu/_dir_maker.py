# SPDX-FileCopyrightText: 2024 ShinagwaKazemaru
# SPDX-License-Identifier: MIT License

from __future__ import annotations

import fnmatch
import glob
import os
import pathlib
import re
import shutil

import jinja2

from ._constants import *

class DirMaker:
    def __init__(self, manifests:list[tuple[bytes, str|pathlib.Path]], src_dir_path:str|pathlib.Path, dst_dir_path:str|pathlib.Path) -> None:
        self.src_dir_path = src_dir_path # must be absolute path
        self.dst_dir_path = dst_dir_path # must be absolute path
        self.manifests = manifests
        self.logging = False
        loader = jinja2.FileSystemLoader(str(self.src_dir_path))
        self.env = jinja2.Environment(loader=loader)


    def make(self) -> None:
        self.rec_make(self.src_dir_path)


    def _info(self, msg:str):
        if self.logging:
            print(msg)


    def rec_make(self, src_path:str) -> None:
        if os.path.isdir(src_path):
            for child_path in glob.glob(os.path.join(src_path, '*')):
                self.rec_make(child_path)
        else:
            rule_hit = RULE_IGNORE
            for rule, pattern in self.manifests:
                if fnmatch.fnmatch(src_path, pattern):
                    rule_hit = rule

            if not rule_hit == RULE_IGNORE:
                name = pathlib.Path(src_path).relative_to(self.src_dir_path)
                dst_path = self.dst_dir_path / name

                # prepare directory
                if not os.path.exists(dst_path.parent):
                    os.makedirs(dst_path.parent, mode=0o775)

                if rule_hit == RULE_RENDER:
                    self._render_file(src_path, dst_path)
                elif rule_hit == RULE_COPY:
                    self._copy_file(src_path, dst_path)
                elif rule_hit == RULE_LINKH:
                    self._linkh_file(src_path, dst_path)
                elif rule_hit == RULE_LINKS:
                    self._links_file(src_path, dst_path)


    def _render_file(self, src_path:str|pathlib.Path, dst_path:str|pathlib.Path) -> None:
        p = pathlib.Path(src_path).relative_to(self.src_dir_path)
        template = self.env.get_template(str(p))
        with open(dst_path, 'w') as f:
            f.write(template.render())
        self._info("rendered : {} -> {}".format(src_path, dst_path))


    def _copy_file(self, src_path:str|pathlib.Path, dst_path:str|pathlib.Path):
        if (not os.path.exists(dst_path)) or (os.path.getmtime(dst_path) < os.path.getmtime(src_path)):
            shutil.copy(src_path, dst_path)
            self._info("copy : {} -> {}".format(src_path, dst_path))


    def _linkh_file(self, src_path:str|pathlib.Path, dst_path:str|pathlib.Path):
        if os.path.exists(dst_path):
            os.remove(dst_path)
        os.link(src_path, dst_path)
        self._info("create hard link : {} -> {}".format(src_path, dst_path))


    def _links_file(self, src_path:str|pathlib.Path, dst_path:str|pathlib.Path):
        if os.path.exists(dst_path):
            os.remove(dst_path)
        os.symlink(src_path, dst_path)
        self._info("create symbolic link : {} -> {}".format(src_path, dst_path))


    def __str__(self) -> str:
        s = "manifests:\n"
        s = s + "| RULE   | PATTERN\n"
        s = s + "+--------+----------\n"
        for rule, pattern in self.manifests:
            if rule == RULE_RENDER:
                s = s + "| RENDER"
            elif rule == RULE_COPY:
                s = s + "| COPY  "
            elif rule == RULE_LINKH:
                s = s + "| LINKH "
            elif rule == RULE_LINKS:
                s = s + "| LINKS "
            elif rule == RULE_IGNORE:
                s = s + "| IGNORE"

            s = s + " | {}\n".format(pattern)

        return \
        s + \
        "src_dir:{}\n".format(self.src_dir_path) + \
        "dst_dir:{}".format(self.dst_dir_path)
