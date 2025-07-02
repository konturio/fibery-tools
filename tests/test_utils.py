import utils


def test_slugify_basic():
    assert utils.slugify('Hello World') == 'hello-world'


def test_slugify_repeated_symbols():
    assert utils.slugify('A---B') == 'a-b'
