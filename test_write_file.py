from functions.write_file import write_file


def main():
    test_cases = [
        (
            "write to calculator directory",
            "calculator",
            "lorem.txt",
            "wait, this isn't lorem ipsum",
        ),
        (
            "write to nested directory",
            "calculator",
            "pkg/morelorem.txt",
            "lorem ipsum dolor sit amet",
        ),
        (
            "outside directory error",
            "calculator",
            "/tmp/temp.txt",
            "this should not be allowed",
        ),
    ]

    for test_name, project, file_path, content in test_cases:
        print(f"\n{'=' * 50}")
        print(f"Test: {test_name}")
        print(f"{'=' * 50}")
        result = write_file(project, file_path, content)
        print(result)


if __name__ == "__main__":
    main()
