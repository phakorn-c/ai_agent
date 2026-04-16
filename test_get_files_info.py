from functions.get_files_info import get_files_info


def main():
    test_cases = [
        ("current directory", "calculator", "."),
        ("nested directory", "calculator", "pkg"),
        ("absolute path error", "calculator", "/bin"),
        ("parent directory error", "calculator", "../"),
    ]

    for test_name, project, directory in test_cases:
        print(f"\n{'=' * 50}")
        print(f"Test: {test_name}")
        print(f"{'=' * 50}")
        result = get_files_info(project, directory)
        print(result)


if __name__ == "__main__":
    main()
