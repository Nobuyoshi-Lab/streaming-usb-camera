import os
from pathlib import Path
import pathspec

def read_gitignore(gitignore_path):
    with open(gitignore_path, "r") as gitignore_file:
        gitignore_rules = gitignore_file.readlines()
    return gitignore_rules

def compile_gitignore_rules(gitignore_rules, base_path):
    gitignore_rules.append(".git/")
    pathspec_obj = pathspec.PathSpec.from_lines(pathspec.patterns.GitWildMatchPattern, gitignore_rules)
    pathspec_obj.base = base_path
    return pathspec_obj

def generate_structure_diagram(working_dir, pathspec_obj):
    structure_diagram = []

    def traverse_directory(current_dir, prefix):
        for entry in sorted(os.listdir(current_dir)):
            file_or_dir_path = current_dir / entry
            relative_file_or_dir_path = file_or_dir_path.relative_to(working_dir)

            if pathspec_obj.match_file(str(relative_file_or_dir_path)):
                continue

            if file_or_dir_path.is_dir():
                structure_diagram.append(f"{prefix}+-- {entry}")
                traverse_directory(file_or_dir_path, f"{prefix}{' ' * 4}")
            else:
                structure_diagram.append(f"{prefix}+-- {entry}")

    traverse_directory(working_dir, "")
    return "\n".join(structure_diagram)

def main():
    script_path = Path(__file__).resolve()
    working_dir = script_path.parent
    gitignore_path = working_dir / ".gitignore"

    if gitignore_path.is_file():
        gitignore_rules = read_gitignore(gitignore_path)
        pathspec_obj = compile_gitignore_rules(gitignore_rules, working_dir)
    else:
        pathspec_obj = pathspec.PathSpec.from_lines(pathspec.patterns.GitWildMatchPattern, [])

    structure_diagram = generate_structure_diagram(working_dir, pathspec_obj)

    with open("structure_diagram.txt", "w") as diagram_file:
        diagram_file.write(structure_diagram)

if __name__ == "__main__":
    main()
