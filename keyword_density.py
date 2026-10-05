#!/usr/bin/env python3
"""keyword_density —— 关键词密度分析（命令行）。

分词后统计每个词 / 二元短语的出现次数与占比（密度），支持停用词过滤，
输出按密度降序的密度表。零第三方依赖。
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter

_CJK = re.compile(r"[\u4e00-\u9fff]")
_WORD = re.compile(r"[a-z0-9][a-z0-9]*")

STOPWORDS = {
    "的", "了", "是", "在", "我", "你", "他", "她", "和", "与", "及", "或",
    "这", "那", "有", "也", "都", "就", "而", "把", "被", "从", "到", "对",
    "the", "a", "an", "and", "or", "of", "to", "in", "is", "are", "it",
}


def tokenize(text: str, with_bigrams: bool = True) -> list[str]:
    toks = [w for w in _WORD.findall(text.lower()) if w not in STOPWORDS and len(w) > 1]
    buf: list[str] = []

    def flush():
        if with_bigrams and len(buf) >= 2:
            for i in range(len(buf) - 1):
                toks.append(buf[i] + buf[i + 1])
        buf.clear()

    for ch in text:
        if _CJK.match(ch):
            buf.append(ch)
        else:
            flush()
    flush()
    return toks


def density_table(text: str, min_count: int = 1, filter_stop: bool = True) -> list[dict]:
    toks = tokenize(text)
    total = len(toks)
    counter = Counter(toks)
    rows = []
    for word, cnt in counter.items():
        if cnt < min_count:
            continue
        rows.append({"keyword": word, "count": cnt, "density": round(cnt / total, 4) if total else 0.0})
    rows.sort(key=lambda r: (-r["count"], r["keyword"]))
    return rows


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="关键词密度分析")
    p.add_argument("--file", help="读取该文本文件；不传则读标准输入")
    p.add_argument("--top", type=int, default=10, help="只显示前 N 行，默认 10")
    p.add_argument("--min-count", type=int, default=1)
    args = p.parse_args(argv)
    text = open(args.file, encoding="utf-8").read() if args.file else sys.stdin.read()
    rows = density_table(text, min_count=args.min_count)
    if not rows:
        print("（无有效词）")
        return 0
    print(f"{'关键词':<12}{'次数':>6}{'密度':>10}")
    for r in rows[:args.top]:
        print(f"{r['keyword']:<12}{r['count']:>6}{r['density']:>10.2%}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
