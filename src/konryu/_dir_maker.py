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


    def make(self) -> None:
        self.rec_make(self.src_dir_path)


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
                    os.makedirs(dst_path.parent, mode=755)

                if rule_hit == RULE_RENDER:
                    self.render(src_path, dst_path)
                elif rule_hit == RULE_COPY:
                    shutil.copy(src_path, dst_path)
                elif rule_hit == RULE_LINKH:
                    os.link(src_path, dst_path)
                elif rule_hit == RULE_LINKS:
                    os.symlink(src_path, dst_path)


    def render(self, src_path:str|pathlib.Path, dst_path:str|pathlib.Path) -> None:
        with open(dst_path, 'w') as f:
            f.write(jinja2.Template(src_path).render())


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
