import os
from functions.run_python_file import run_python_file


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    calculator_dir = os.path.join(base_dir, "calculator")

    test_cases = [
        ("calculator usage", calculator_dir, os.path.join(calculator_dir, "main.py")),
        (
            "calculator with expression",
            calculator_dir,
            os.path.join(calculator_dir, "main.py"),
            ["3 + 5"],
        ),
        ("calculator tests", calculator_dir, os.path.join(calculator_dir, "tests.py")),
        (
            "outside directory error",
            calculator_dir,
            "../main.py",
        ),
        (
            "nonexistent file error",
            calculator_dir,
            os.path.join(calculator_dir, "nonexistent.py"),
        ),
        (
            "not python file error",
            calculator_dir,
            os.path.join(calculator_dir, "lorem.txt"),
        ),
    ]

    for test_name, working_dir, file_path, *args in test_cases:
        print(f"\n{'=' * 50}")
        print(f"Test: {test_name}")
        print(f"{'=' * 50}")
        result = run_python_file(working_dir, file_path, args[0] if args else None)
        print(result)


if __name__ == "__main__":
    main()
