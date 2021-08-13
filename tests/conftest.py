from random import randint

def pytest_generate_tests(metafunc):
    if "n" in metafunc.fixturenames:
        metafunc.parametrize("n", [randint(1,500) for _ in range(5)])
