from hypothesis.utils.conventions import not_set

def accept(f):
    def test_parse(self, l=not_set):
        return f(self, l)
    return test_parse
