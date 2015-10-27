from hypothesis.utils.conventions import not_set

def accept(f):
    def test_STLParser(self, n=not_set):
        return f(self, n)
    return test_STLParser
