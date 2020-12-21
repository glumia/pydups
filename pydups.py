import argparse
import ast
import os
from ast import *  # noqa - required by `eval`
from collections import defaultdict

import astunparse


class Visitor(ast.NodeVisitor):
    def __init__(self, functions, module_path):
        self.functions = functions
        self.module_path = module_path
        self.class_name = None

    def visit_FunctionDef(self, node):
        args_map = {arg.arg: f"x{i}" for i, arg in enumerate(node.args.args)}
        hash = ast.dump(node)
        hash = hash.replace(
            f"name='{node.name}'", "name='f'"
        )  # Function name doesn't matter
        for arg in args_map:
            hash = hash.replace(
                f"'{arg}'", f"'{args_map[arg]}'"
            )  # Args name doesn't matter
        self.functions[hash].append(
            f"{self.module_path}::{self.class_name+'.' if self.class_name else ''}{node.name}"
        )
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.class_name = node.name
        super().generic_visit(node)
        self.class_name = None


def analyze_module(path):
    functions = defaultdict(lambda: [])
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if not filename.endswith("py"):
                continue
            path = os.path.join(dirpath, filename)
            with open(path, "r") as fp:
                tree = ast.parse(fp.read(), mode="exec")
            visitor = Visitor(functions, path)
            visitor.visit(tree)

    duplicates = {k: v for k, v in functions.items() if len(v) > 1}
    if duplicates:
        print("Found duplicates 💥\n")
        for hash, paths in duplicates.items():
            print("=" * 80 + "\n")
            print(astunparse.unparse(eval(hash)).lstrip("\n"))
            print("\n".join(paths))
            print("")
    else:
        print("No duplicates! ✨")


def main():
    parser = argparse.ArgumentParser(
        description="Search for duplicate functions looking at code's AST."
    )
    parser.add_argument("path", type=str, help="path of the python module to inspect")
    args = parser.parse_args()
    analyze_module(args.path)


if __name__ == "__main__":
    main()
