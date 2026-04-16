from functions.get_file_content import get_file_content


def main():
    test_cases = [
        ("non-existent file", "calculator", "lorem.txt"),
        ("large file (truncated)", "functions", "lorem.txt"),
        ("path outside working directory", "functions", "../test_get_files_info.py"),
        ("non-existent file in functions", "functions", "nonexistent.txt"),
        ("small file", "functions", "get_files_info.py"),
        ("calculator main.py", "calculator", "main.py"),
        ("calculator module", "calculator", "pkg/calculator.py"),
        ("absolute path error", "calculator", "/bin/cat"),
        ("nested non-existent file", "calculator", "pkg/does_not_exist.py"),
    ]

    for test_name, project, file_path in test_cases:
        print(f"\n{'=' * 50}")
        print(f"Test: {test_name}")
        print(f"{'=' * 50}")
        result = get_file_content(project, file_path)
        print(f"Content length: {len(result)}")
        if "truncated" in result:
            print("File was truncated")
            print(f"Last 100 chars: ...{result[-100:]}")
        elif len(result) > 200:
            print("First 200 chars:")
            print(result[:200])
        else:
            print(result)


if __name__ == "__main__":
    main()
