#!/usr/bin/env python

from typing import List
from pathlib import Path
import os

PROJECT_NAME = "determined"
root = Path(os.getenv('PROJECT_ROOT', os.getcwd())).absolute()
if not str(root).endswith(PROJECT_NAME):
    print("Please run this script from the root of the project or set it using " +
    "PROJECT_ROOT env variable")
    exit(1)
os.chdir(root)


rules = {
  root/'harness': 'make -j fmt; make -j check; make -j build',
  root/'proto': '''make build fmt check && make -C ../bindings build && make -C ../webui/react bindings-copy-over''',
  root/'webui'/'react': '''make -j fmt; make -j check && make -j build; make test''',
  root/'master': '''make -C ../proto build && make -j fmt; make -j check && make -j build;''',
}

# get a list of paths to dirty and staged files from git
def get_git_status() -> List[Path]:
    git_status = os.popen('git status --porcelain').read()
    git_status_list = git_status.split('\n')
    git_status_list = [x for x in git_status_list if x]
    files = [Path(x.split()[1]).absolute() for x in git_status_list]
    return files

# check if path a child of another path
def is_child(path: Path, parent: Path) -> bool:
    assert path.is_absolute()
    assert parent.is_absolute()
    cur_path = path
    while cur_path != parent and cur_path != root:
        cur_path = cur_path.parent
        if cur_path == parent:
            return True
    return False

# check if path is the same or child of one of the rules and execute the rule as 
# subprocess
def run_rules(dirty_path: Path):
    for rule_path, rule in rules.items():
        if is_child(dirty_path, rule_path):
            os.chdir(rule_path)
            print(f'in {rule_path.relative_to(root)} run {rule}')
            os.system(rule)


# print('dirty files', get_git_status())
for dirty_path in get_git_status():
    run_rules(dirty_path)
