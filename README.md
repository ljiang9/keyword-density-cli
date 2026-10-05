# keyword-density-cli

**关键词密度分析**命令行工具：分词后统计每个词 / 二元短语的出现次数与占比（密度），
内置停用词过滤，输出按次数降序的密度表。零第三方依赖。

## 功能简介

- 混合分词：英文小写单词 + 中文相邻字二元组；
- 内置中英文停用词表，自动过滤无意义词；
- `density_table(text)` 输出 `[{keyword, count, density}, ...]`；
- 支持 `--min-count` 过滤低频词、`--top` 限制行数。

## 快速开始

环境：Python 3.10+，零依赖。

```bash
printf '机器学习 机器学习 自然语言 自然语言 自然语言' | python3 keyword_density.py --top 5
```

分析文件：

```bash
python3 keyword_density.py --file article.txt --top 10 --min-count 2
```

作为库：

```python
from keyword_density import density_table
for row in density_table("苹果 苹果 香蕉"):
    print(row)
```

## 使用示例（真实命令）

```bash
$ printf '机器学习 机器学习 自然语言 自然语言 自然语言' | python3 keyword_density.py --top 3
关键词             次数        密度
然语               3   20.00%
自然               3   20.00%
语言               3   20.00%
```

## 无 API key 如何运行

纯本地统计，**不需要任何 API key**，不联网。

## 目录结构

```
keyword-density-cli/
├── keyword_density.py            # 分词 + 密度表 + CLI
├── tests/
│   └── test_keyword_density.py   # unittest
├── README.md
├── LICENSE
└── .gitignore
```

## 运行测试

```bash
python3 -m unittest discover -s tests -v
```

## 许可证

[MIT](./LICENSE) © 2026 ljiang9
