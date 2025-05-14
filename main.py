import pytest


def main():
    test_case_one = ["tests/test_case_one.py", "--headed"]
    test_case_two = ["tests/test_case_two.py", "--headed"]
    tests = [
        # test_case_one,
        test_case_two
             ]
    for test in tests:
        pytest.main(test)


if __name__ == "__main__":
    main()
