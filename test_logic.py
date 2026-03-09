def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

def test_failing():
    # Uncomment this to see what a failure looks like in GitHub Actions
    assert add(2, 2) == 5