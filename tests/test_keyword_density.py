import unittest

from keyword_density import density_table, tokenize, STOPWORDS


class TestTokenize(unittest.TestCase):
    def test_stopwords_filtered(self):
        toks = tokenize("我喜欢自然语言")
        self.assertNotIn("我", toks)
        self.assertIn("自然", toks)

    def test_english(self):
        toks = tokenize("machine learning and python")
        self.assertIn("machine", toks)
        self.assertNotIn("and", toks)


class TestDensity(unittest.TestCase):
    def test_density_sum(self):
        rows = density_table("苹果 苹果 香蕉 香蕉 香蕉")
        d = {r["keyword"]: r for r in rows}
        self.assertGreater(d["香蕉"]["count"], d["苹果"]["count"])
        self.assertAlmostEqual(d["香蕉"]["density"] + d["苹果"]["density"], 1.0, places=1)

    def test_sorted_desc(self):
        rows = density_table("a a a b b c 数据 数据")
        counts = [r["count"] for r in rows]
        self.assertEqual(counts, sorted(counts, reverse=True))

    def test_min_count(self):
        rows = density_table("唯一词 重复 重复", min_count=2)
        words = [r["keyword"] for r in rows]
        self.assertNotIn("唯一词", words)

    def test_empty(self):
        self.assertEqual(density_table(""), [])


if __name__ == "__main__":
    unittest.main()
