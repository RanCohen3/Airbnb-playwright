import pytest


def main():
    test_case_one = "tests/test_case_one.py"
    pytest.main([test_case_one, "--headed"])


if __name__ == "__main__":
    main()
