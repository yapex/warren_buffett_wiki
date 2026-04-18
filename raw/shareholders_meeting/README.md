# CNBC 巴菲特股东大会文字稿数据

本目录包含从 CNBC Warren Buffett Archive 爬取的伯克希尔股东大会完整文字稿。

## 数据来源

- **来源**: [CNBC Warren Buffett Archive](https://buffett.cnbc.com/annual-meetings/)
- **爬取完成**: 2026-04-18
- **覆盖年份**: 1996-2024（29 年，57 场会议）
- **总数据量**: 43,904 段落，约 6.5 MB

## 文件结构

```
raw/shareholders_meeting/
├── README.md
└── en/
    ├── YYYY-morning-session.md    # 上午场原始文字稿
    ├── YYYY-afternoon-session.md  # 下午场原始文字稿
    └── YYYY-metadata.json         # 元数据
```

**说明**: 保持 CNBC 原始结构，不合并为完整版本。

## 完成统计

| 优先级 | 年份范围 | 会议场次 | 段落总数 | 状态 |
|--------|----------|----------|----------|------|
| P0 | 2020-2024 | 9 场 | 5,623 段 | ✅ |
| P1 | 2015-2019 | 10 场 | 6,983 段 | ✅ |
| P2 | 2010-2014 | 10 场 | 8,621 段 | ✅ |
| P3 | 2000-2009 | 20 场 | 15,905 段 | ✅ |
| P4 | 1996-1999 | 8 场 | 6,772 段 | ✅ |
| **总计** | **1996-2024** | **57 场** | **43,904 段** | **✅** |

## 数据格式

### Markdown 文件

```markdown
# 2024 Berkshire Hathaway Annual Meeting - Morning Session

**Source**: CNBC Warren Buffett Archive  
**Date**: May 6, 2024  
**Location**: Omaha, Nebraska  
**Duration**: ~2h30m  
**URL**: https://buffett.cnbc.com/video/2024/05/06/morning-session---2024-meeting.html

---

WARREN BUFFETT: Good morning.

(Applause)
```

### 元数据 (JSON)

```json
{
  "year": 2024,
  "company": "Berkshire Hathaway",
  "event": "Annual Shareholders Meeting",
  "date": "May 6, 2024",
  "location": "Omaha, Nebraska",
  "source": "CNBC Warren Buffett Archive",
  "statistics": {
    "morning_paragraphs": 802,
    "afternoon_paragraphs": 636,
    "morning_duration": "~2h30m",
    "afternoon_duration": "~3h30m"
  },
  "participants": [
    "Warren Buffett (CEO)",
    "Charlie Munger (Vice Chairman)",
    "Greg Abel (Vice Chairman, Non-Insurance Operations)",
    "Ajit Jain (Vice Chairman, Insurance Operations)"
  ]
}
```

## 爬取方法

### 高效下载流程（已验证）

```bash
# 1. 下载 HTML
curl -s -A "Mozilla/5.0" [URL] -o /tmp/year_session.html

# 2. Python 解析并保存
python3 << 'EOF'
import re
from pathlib import Path

with open("/tmp/year_session.html", "r") as f:
    html = f.read()

paragraphs = []
for match in re.finditer(r'<p[^>]*>(.*?)</p>', html, re.DOTALL | re.IGNORECASE):
    text = re.sub(r'<[^>]+>', '', match.group(1)).strip()
    if text and len(text) > 5:
        paragraphs.append(text)

# 生成 Markdown 并保存
EOF

# 3. 编码修复（em dash → apostrophe）
# 4. Git 提交
```

### URL 格式差异

| 年份 | URL 格式 | 示例 |
|------|----------|------|
| 2020-2024 | 三减号 `---` + 简化后缀 | `morning-session---2024-meeting.html` |
| 2017-2019 | 三减号 `---` + 完整后缀 | `morning-session---2019-berkshire-hathaway-annual-meeting.html` |
| 2015-2016 | 双减号 `--` 或三减号 `---` + 完整后缀 | `morning-session--2016-berkshire-hathaway-annual-meeting.html` |
| 2000-2014 | 三减号 `---` + 完整后缀 | `morning-session---2010-berkshire-hathaway-annual-meeting.html` |
| 1996-1999 | 三减号 `---` + 完整后缀 | `morning-session---1999-berkshire-hathaway-annual-meeting.html` |

**确认方法**: 先访问年份主页获取正确 URL 格式。

## 注意事项

1. **原始数据**: 文件保持原汁原味，未做任何编辑或整理
2. **特殊字符**: 包含 `(Laughter)`, `(Applause)`, `(unintelligible)` 等现场标记
3. **发言人标记**: 格式为 `WARREN BUFFETT:`, `CHARLIE MUNGER:`, 等
4. **编码修复**: 已处理 em dash (`—`) 误用为 apostrophe (`'`) 的问题
5. **版权问题**: 数据仅供个人学习研究使用

## 未包含年份

| 年份 | 状态 | 说明 |
|------|------|------|
| 2025 | ⏳ 等待中 | CNBC 尚未发布完整文字稿 |
| 1995 | ⚠️ 无记录 | CNBC archive 只有视频片段 |
| 1994 | ⚠️ 无记录 | CNBC archive 只有视频片段 |

## 后续计划

- [ ] 监测 2025 年 CNBC 发布（预计 2026 年 5 月后）
- [ ] 与现有 Wiki 索引整合
- [ ] 按话题分类整理
- [ ] 添加中文翻译版本（可选）

## 相关资源

- [巴菲特 Wiki 项目](../README.md)
- [CNBC 巴菲特档案](https://buffett.cnbc.com/)
- [伯克希尔官网](https://berkshirehathaway.com/)
- [爬取计划文档](../docs/plans/cnbc-transcripts-crawl.md)
