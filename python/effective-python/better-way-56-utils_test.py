from unittest import TestCase, main
from .utils import to_str


class UtilsTestCase(TestCase):
    def test_to_str_bytes(self):
        self.assertEqual("hello", to_str(b"hello"))

    def test_to_str_str(self):
        self.assertEqual("hello", to_str("hello"))

    def to_str_bad(self):
        self.assertRaises(TypeError, to_str, object())


if __name__ == '__main__':
    main()