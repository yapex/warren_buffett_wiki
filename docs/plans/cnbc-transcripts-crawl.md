# CNBC 巴菲特股东大会文字稿爬取计划

> **For Hermes:** Use browser tools to extract transcript data from CNBC, then use file tools to save as Markdown. Execute task-by-task.

**Goal:** 爬取 1994-2025 年全部 32 年伯克希尔股东大会完整文字稿（上午场 + 下午场）

**Architecture:** 按优先级分批次爬取，每年生成 3 个文件（上午场、下午场、元数据），保持与 2022 年相同的文件结构和编码处理。

**Tech Stack:** browser_navigate, browser_console, execute_code, write_file

---

## ⚠️ 注意事项与踩坑记录（2026-04-18 更新）

### 1. 编码问题（重要！）

**问题：** CNBC 页面提取的文本包含错误的编码字符，特别是：
- em dash (`—`, UTF-8: `e2 80 94`) 被错误用于替代 apostrophe
- 例如：`o—clock` 应为 `o'clock`，`it—s` 应为 `it's`

**解决方案：** 保存后必须运行编码修复脚本：

```python
from pathlib import Path
import re

file_path = Path("raw/shareholders_meeting/en/2024-morning-session.md")

with open(file_path, "rb") as f:
    content = f.read()

em_dash = b'\xe2\x80\x94'      # —
right_quote = b'\xe2\x80\x99'  # '

# 1. o—clock -> o'clock
content = content.replace(b"o" + em_dash + b"clock", b"o" + right_quote + b"clock")

# 2. 代词 + — + 缩写后缀 -> 代词 + ' + 缩写后缀
def fix_possessive(match):
    return match.group(1) + right_quote + match.group(2)

pattern = rb'(\w)' + em_dash + rb'(s|re|ll|d|ve|t|m)\b'
content = re.sub(pattern, fix_possessive, content)

with open(file_path, "wb") as f:
    f.write(content)

print(f"Fixed: em dash count = {content.count(em_dash)}")
```

**验证方法：**
```bash
# 检查是否还有 em dash 乱码
grep -n "—" raw/shareholders_meeting/en/2024-morning-session.md | head -10
# 应该只出现在 URL 中，不应该出现在 o'clock、it's 等位置
```

### 2. 2025 年文字稿尚未发布

**状态：** CNBC 页面中 `transcript: null`，只有视频片段摘要

**检测代码：**
```javascript
const html = document.documentElement.outerHTML;
const hasTranscript = html.includes('"transcript":"') || html.includes('"text":"');
console.log({ hasTranscript });
```

**处理方案：**
- 跳过 2025 年，等 CNBC 发布完整文字稿后再补充
- 或只保存会议简介和视频片段列表作为占位符

### 3. 页面结构差异

**有完整文字稿的年份（2022-2024）：**
- 页面包含 "Key Chapters" 章节
- 有 `button` 元素包含章节标题和段落
- `document.querySelectorAll('p')` 可提取 700-800 个段落

**无完整文字稿的年份（2025）：**
- 页面只有视频播放器
- 只有简介段落（1-2 个）
- 需要等待 CNBC 更新

### 4. 提取代码（已验证）

```javascript
// 在 browser_console 中运行
const paragraphs = [];
document.querySelectorAll('p').forEach(p => {
    const text = p.textContent?.trim();
    if (text && text.length > 5) {
        paragraphs.push(text);
    }
});
JSON.stringify({ count: paragraphs.length, paragraphs: paragraphs });
```

**预期结果：**
- 上午场：700-800 段落（约 120-150KB）
- 下午场：600-700 段落（约 100-120KB）

### 5. 文件提交规范

```bash
cd ~/workspace/warren_buffett_wiki
git add raw/shareholders_meeting/en/2024-morning-session.md
git commit -m "feat: add 2024 morning session transcript"
# 如有编码修复
git commit -m "fix: correct encoding issues in 2024 morning session (em dash -> apostrophe)"
```

**注意：** 变更不在 `wiki/` 目录下，不会触发索引更新。

---

## 优先级分组

| 优先级 | 年份 | 数量 | 说明 |
|--------|------|------|------|
| **P0** | 2020, 2021, 2023, 2024, 2025 | 5 年 | 近 6 年（2022 已完成）|
| **P1** | 2015-2019 | 5 年 | 近 10 年 |
| **P2** | 2010-2014 | 5 年 | 中期数据 |
| **P3** | 2000-2009 | 10 年 | 早期数据 |
| **P4** | 1994-1999 | 6 年 | 最早期 |

---

## P0 优先级：2025 年

### Task 1: 爬取 2025 年上午场

**Objective:** 从 CNBC 提取 2025 年股东大会上午场完整文字稿

**Files:**
- 访问：https://buffett.cnbc.com/2025-berkshire-hathaway-annual-meeting/
- 输出：`raw/shareholders_meeting/en/2025-morning-session.md`
- 元数据：`raw/shareholders_meeting/en/2025-metadata.json`

**Step 1: 访问 2025 年会议页面**

使用 browser_navigate 访问：
```
https://buffett.cnbc.com/2025-berkshire-hathaway-annual-meeting/
```

**Step 2: 找到上午场视频链接**

在页面中找到上午场视频链接（格式：`/video/2025/*/morning-session---2025-meeting.html`）

**Step 3: 访问上午场视频页面**

使用 browser_navigate 访问上午场页面。

**Step 4: 提取文字内容**

在 browser_console 中运行：
```javascript
const paragraphs = [];
document.querySelectorAll('p').forEach(p => {
    const text = p.textContent?.trim();
    if (text && text.length > 5) {
        paragraphs.push(text);
    }
});
JSON.stringify({
    session: 'morning',
    year: 2025,
    count: paragraphs.length,
    paragraphs: paragraphs
});
```

**Step 5: 保存为 Markdown**

使用 execute_code 处理并保存：
```python
import json
from pathlib import Path

# 读取提取的数据（从 browser_console 结果）
data = {...}  # 粘贴 Step 4 的 JSON 输出

def clean_text(text):
    import re
    text = re.sub(r'â"[-\x80-\x9f]*', '—', text)
    text = re.sub(r'â€"[-\x80-\x9f]*', '—', text)
    text = re.sub(r'â[-\x80-\x9f]*', '—', text)
    text = text.replace('â€™', "'")
    text = text.replace('â€˜', "'")
    text = text.replace('â€œ', '"')
    text = text.replace('â€"', '"')
    text = re.sub(r'[\x80-\x9f]', '', text)
    return text

output_dir = Path("/Users/yapex/workspace/warren_buffett_wiki/raw/shareholders_meeting/en")
output_dir.mkdir(parents=True, exist_ok=True)

md_content = f"""# 2025 Berkshire Hathaway Annual Meeting - Morning Session

**Source**: CNBC Warren Buffett Archive  
**Date**: May 3, 2025  
**Location**: Omaha, Nebraska  
**Duration**: ~2h30m  
**URL**: https://buffett.cnbc.com/video/2025/05/05/morning-session---2025-meeting.html

---

"""

for para in data['paragraphs']:
    md_content += clean_text(para) + "\n\n"

output_file = output_dir / "2025-morning-session.md"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(md_content)

print(f"✅ 保存：{output_file} ({len(data['paragraphs'])} 段落)")
```

**Step 6: 验证文件**

使用 read_file 检查前 30 行，确认编码正确。

**Step 7: 提交**

```bash
cd ~/workspace/warren_buffett_wiki
git add raw/shareholders_meeting/en/2025-morning-session.md
git commit -m "feat: add 2025 morning session transcript"
```

---

### Task 2: 爬取 2025 年下午场

**Objective:** 从 CNBC 提取 2025 年股东大会下午场完整文字稿

**Files:**
- 访问：找到下午场视频链接
- 输出：`raw/shareholders_meeting/en/2025-afternoon-session.md`

**Step 1: 访问下午场视频页面**

URL 格式：`https://buffett.cnbc.com/video/2025/05/05/afternoon-session---2025-meeting.html`

**Step 2: 提取文字内容**

使用与 Task 1 Step 4 相同的 JavaScript 代码，但 `session: 'afternoon'`

**Step 3: 保存为 Markdown**

```python
# 与 Task 1 Step 5 类似，修改：
# - session 为 afternoon
# - 输出文件为 2025-afternoon-session.md
# - URL 为 afternoon-session---2025-meeting.html
```

**Step 4: 验证文件**

**Step 5: 提交**

```bash
git add raw/shareholders_meeting/en/2025-afternoon-session.md
git commit -m "feat: add 2025 afternoon session transcript"
```

---

### Task 3: 生成 2025 年元数据

**Objective:** 创建 2025 年元数据文件

**Files:**
- Create: `raw/shareholders_meeting/en/2025-metadata.json`

**Step 1: 生成元数据**

```python
import json
from pathlib import Path
from datetime import datetime

metadata = {
    "year": 2025,
    "company": "Berkshire Hathaway",
    "event": "Annual Shareholders Meeting",
    "date": "May 3, 2025",
    "location": "Omaha, Nebraska",
    "source": "CNBC Warren Buffett Archive",
    "crawled_at": datetime.now().isoformat(),
    "urls": {
        "morning": "https://buffett.cnbc.com/video/2025/05/05/morning-session---2025-meeting.html",
        "afternoon": "https://buffett.cnbc.com/video/2025/05/05/afternoon-session---2025-meeting.html",
        "meeting_page": "https://buffett.cnbc.com/2025-berkshire-hathaway-annual-meeting/"
    },
    "files": {
        "morning_session": "2025-morning-session.md",
        "afternoon_session": "2025-afternoon-session.md"
    },
    "statistics": {
        "morning_paragraphs": 0,  # 从实际文件统计
        "afternoon_paragraphs": 0,
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

output_dir = Path("/Users/yapex/workspace/warren_buffett_wiki/raw/shareholders_meeting/en")
with open(output_dir / "2025-metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2, ensure_ascii=False)

print("✅ 生成 2025-metadata.json")
```

**Step 2: 提交**

```bash
git add raw/shareholders_meeting/en/2025-metadata.json
git commit -m "docs: add 2025 metadata"
```

---

### Task 4: 验证 2025 年数据

**Objective:** 验证 2025 年文件完整性和编码

**Files:**
- Verify: `raw/shareholders_meeting/en/2025-*.md`

**Step 1: 检查文件大小**

```bash
ls -lh raw/shareholders_meeting/en/2025-*.md
```

Expected: 每个文件 100-200KB

**Step 2: 检查行数**

```bash
wc -l raw/shareholders_meeting/en/2025-*.md
```

Expected: 每个文件 1000-2000 行

**Step 3: 检查编码**

使用 read_file 读取前 30 行，确认无乱码（特别是 em dash `—` 和引号）。

**Step 4: 统计段落**

```python
import json
from pathlib import Path

output_dir = Path("/Users/yapex/workspace/warren_buffett_wiki/raw/shareholders_meeting/en")

# 更新元数据中的段落数
with open(output_dir / "2025-metadata.json", "r") as f:
    metadata = json.load(f)

# 统计实际段落（简化：数空行）
for session in ["morning", "afternoon"]:
    with open(output_dir / f"2025-{session}-session.md", "r") as f:
        content = f.read()
    paragraphs = len([l for l in content.split("\n\n") if l.strip()])
    metadata["statistics"][f"{session}_paragraphs"] = paragraphs

with open(output_dir / "2025-metadata.json", "w") as f:
    json.dump(metadata, f, indent=2, ensure_ascii=False)

print(f"✅ 2025 年验证完成")
print(f"   上午场：{metadata['statistics']['morning_paragraphs']} 段落")
print(f"   下午场：{metadata['statistics']['afternoon_paragraphs']} 段落")
```

**Step 5: 提交验证结果**

```bash
git add raw/shareholders_meeting/en/2025-metadata.json
git commit -m "chore: update 2025 statistics"
```

---

## P0 优先级：2024 年

### Task 5: 爬取 2024 年上午场

**Objective:** 从 CNBC 提取 2024 年股东大会上午场完整文字稿

**Files:**
- 访问：https://buffett.cnbc.com/2024-berkshire-hathaway-annual-meeting/
- 输出：`raw/shareholders_meeting/en/2024-morning-session.md`

**Step 1-7:** 与 Task 1 相同，修改年份为 2024

**URL:**
- Meeting: `https://buffett.cnbc.com/2024-berkshire-hathaway-annual-meeting/`
- Morning: `https://buffett.cnbc.com/video/2024/05/06/morning-session---2024-meeting.html`

---

### Task 6: 爬取 2024 年下午场

**Objective:** 从 CNBC 提取 2024 年股东大会下午场完整文字稿

**Files:**
- 输出：`raw/shareholders_meeting/en/2024-afternoon-session.md`

**Step 1-5:** 与 Task 2 相同，修改年份为 2024

---

### Task 7: 生成 2024 年元数据

**Objective:** 创建 2024 年元数据文件

**Files:**
- Create: `raw/shareholders_meeting/en/2024-metadata.json`

**Step 1-2:** 与 Task 3 相同，修改年份为 2024

---

### Task 8: 验证 2024 年数据

**Objective:** 验证 2024 年文件完整性和编码

**Files:**
- Verify: `raw/shareholders_meeting/en/2024-*.md`

**Step 1-5:** 与 Task 4 相同，修改年份为 2024

---

## P0 优先级：2023 年

### Task 9: 爬取 2023 年上午场

**Objective:** 从 CNBC 提取 2023 年股东大会上午场完整文字稿

**URL:**
- Meeting: `https://buffett.cnbc.com/2023-berkshire-hathaway-annual-meeting/`
- Morning: `https://buffett.cnbc.com/video/2023/05/08/morning-session---2023-meeting.html`

**Step 1-7:** 与 Task 1 相同，修改年份为 2023

---

### Task 10: 爬取 2023 年下午场

**Objective:** 从 CNBC 提取 2023 年股东大会下午场完整文字稿

**Step 1-5:** 与 Task 2 相同，修改年份为 2023

---

### Task 11: 生成 2023 年元数据

**Objective:** 创建 2023 年元数据文件

**Step 1-2:** 与 Task 3 相同，修改年份为 2023

---

### Task 12: 验证 2023 年数据

**Objective:** 验证 2023 年文件完整性和编码

**Step 1-5:** 与 Task 4 相同，修改年份为 2023

---

## P0 优先级：2021 年

### Task 13: 爬取 2021 年上午场

**Objective:** 从 CNBC 提取 2021 年股东大会上午场完整文字稿

**URL:**
- Meeting: `https://buffett.cnbc.com/2021-berkshire-hathaway-annual-meeting/`
- Morning: `https://buffett.cnbc.com/video/2021/05/03/morning-session---2021-meeting.html`

**Step 1-7:** 与 Task 1 相同，修改年份为 2021

---

### Task 14: 爬取 2021 年下午场

**Objective:** 从 CNBC 提取 2021 年股东大会下午场完整文字稿

**Step 1-5:** 与 Task 2 相同，修改年份为 2021

---

### Task 15: 生成 2021 年元数据

**Objective:** 创建 2021 年元数据文件

**Step 1-2:** 与 Task 3 相同，修改年份为 2021

---

### Task 16: 验证 2021 年数据

**Objective:** 验证 2021 年文件完整性和编码

**Step 1-5:** 与 Task 4 相同，修改年份为 2021

---

## P0 优先级：2020 年

### Task 17: 爬取 2020 年上午场

**Objective:** 从 CNBC 提取 2020 年股东大会上午场完整文字稿

**Note:** 2020 年为疫情特别场，线上举行

**URL:**
- Meeting: `https://buffett.cnbc.com/2020-berkshire-hathaway-annual-meeting/`
- Morning: `https://buffett.cnbc.com/video/2020/05/04/berkshire-hathaway-annual-meeting--may-02-2020.html`

**Step 1-7:** 与 Task 1 相同，修改年份为 2020

---

### Task 18: 爬取 2020 年下午场

**Objective:** 从 CNBC 提取 2020 年股东大会下午场完整文字稿

**URL:**
- Afternoon: `https://buffett.cnbc.com/video/2020/05/04/berkshire-hathaway-annual-meeting-qa---may-02-2020.html`

**Step 1-5:** 与 Task 2 相同，修改年份为 2020

---

### Task 19: 生成 2020 年元数据

**Objective:** 创建 2020 年元数据文件

**Step 1-2:** 与 Task 3 相同，修改年份为 2020

---

### Task 20: 验证 2020 年数据

**Objective:** 验证 2020 年文件完整性和编码

**Step 1-5:** 与 Task 4 相同，修改年份为 2020

---

## P1 优先级：2015-2019 年

### Task 21-40: 爬取 2015-2019 年

**Objective:** 爬取 5 年共 10 场会议

**Pattern:** 每年 4 个任务（上午场、下午场、元数据、验证）

**URL Pattern:**
```
https://buffett.cnbc.com/YYYY-berkshire-hathaway-annual-meeting/
https://buffett.cnbc.com/video/YYYY/MM/DD/morning-session---YYYY-meeting.html
https://buffett.cnbc.com/video/YYYY/MM/DD/afternoon-session---YYYY-meeting.html
```

---

## P2 优先级：2010-2014 年

### Task 41-60: 爬取 2010-2014 年

**Objective:** 爬取 5 年共 10 场会议

**Pattern:** 与 P1 相同

---

## P3 优先级：2000-2009 年

### Task 61-100: 爬取 2000-2009 年

**Objective:** 爬取 10 年共 20 场会议

**Note:** 早期年份可能只有单场，需要验证

---

## P4 优先级：1994-1999 年

### Task 101-120: 爬取 1994-1999 年

**Objective:** 爬取 6 年共 12 场会议

**Note:** 
- 1994-1996 可能无视频记录
- 需要验证 CNBC 是否有数据

---

## 完成标准

### 文件结构
```
raw/shareholders_meeting/en/
├── YYYY-morning-session.md    (100-200KB, 1000-2000 行)
├── YYYY-afternoon-session.md  (100-200KB, 1000-2000 行)
└── YYYY-metadata.json         (元数据)
```

### 质量要求
- [ ] 所有文件 UTF-8 编码
- [ ] 无乱码（em dash、引号正确）
- [ ] 元数据完整
- [ ] 每个年份通过验证

### 提交要求
- 每完成 1 年提交一次（3-4 个 commit）
- 或每完成 P0/P1/P2 组提交一次
- Commit message 清晰

---

## 预计时间

| 阶段 | 任务数 | 预计时间 |
|------|--------|----------|
| P0 (2020-2025) | Task 1-20 | 2-3 小时 |
| P1 (2015-2019) | Task 21-40 | 2-3 小时 |
| P2 (2010-2014) | Task 41-60 | 2-3 小时 |
| P3 (2000-2009) | Task 61-100 | 4-5 小时 |
| P4 (1994-1999) | Task 101-120 | 2-3 小时 |
| **总计** | **120 任务** | **12-17 小时** |

---

## 下一步

**Ready to execute P0 priority (2020-2025)?**

Start with Task 1: 爬取 2025 年上午场
