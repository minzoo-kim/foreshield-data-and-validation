"""Tests for public reconstructions, not the private team's integration suite."""

import json
import unittest

from examples.pattern_dedup import unique_variants
from examples.strict_json import parse_strict_json


class StrictJsonTests(unittest.TestCase):
    def test_valid_utf8_and_nested_data(self):
        payload = {"region": "예시지역", "values": [0.25, None, True]}
        self.assertEqual(
            parse_strict_json(json.dumps(payload, ensure_ascii=False).encode("utf-8")),
            payload,
        )

    def test_duplicate_keys_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "Duplicate object keys"):
            parse_strict_json(b'{"score": 0.25, "score": 0.75}')

    def test_invalid_utf8_and_bom_are_rejected(self):
        with self.assertRaises(UnicodeDecodeError):
            parse_strict_json(b'{"id": "\xff"}')
        with self.assertRaises(ValueError):
            parse_strict_json(b"\xef\xbb\xbf" + b'{"id": 1}')

    def test_non_finite_numbers_are_rejected(self):
        for value in ("NaN", "Infinity", "-Infinity", "1e999"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_strict_json((f'{{"score": {value}}}').encode())


class PatternTests(unittest.TestCase):
    def test_order_is_preserved_while_duplicates_are_removed(self):
        self.assertEqual(
            unique_variants("original", ["z", "original", "a", "z", "b"]),
            ["z", "a", "b"],
        )

    def test_independent_groups_do_not_erase_each_other(self):
        first = unique_variants("first", ["shared"])
        second = unique_variants("second", ["shared"])
        self.assertEqual(first, ["shared"])
        self.assertEqual(second, ["shared"])


if __name__ == "__main__":
    unittest.main()
