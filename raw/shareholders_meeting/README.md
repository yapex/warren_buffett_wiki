# CNBC 巴菲特股东大会文字稿数据

本目录包含从 CNBC Warren Buffett Archive 爬取的伯克希尔股东大会完整文字稿。

## 数据来源

- **来源**: [CNBC Warren Buffett Archive](https://buffett.cnbc.com/annual-meetings/)
- **官方说明**: 32 届股东大会（1994-2025），145 小时视频，3000 页文字稿
- **爬取方式**: 通过浏览器控制台提取页面文本内容

## 文件结构

```
en/
├── YYYY-full-meeting.md       # 完整版本（上午场 + 下午场）
└── YYYY-metadata.json         # 元数据
```

## 2022 年数据

### 基本信息
- **日期**: 2022 年 4 月 30 日
- **地点**: 内布拉斯加州奥马哈
- **时长**: 约 6 小时（上午 2h40m + 下午 3h30m）
- **参与者**: 
  - Warren Buffett (CEO)
  - Charlie Munger (Vice Chairman)
  - Greg Abel (Vice Chairman, Non-Insurance Operations)
  - Ajit Jain (Vice Chairman, Insurance Operations)

### 文件
- `2022-full-meeting.md` (280KB, 1420 段) - 包含上午场 + 下午场
- `2022-metadata.json`

### 关键话题
- 3 月份 400 亿美元紧急买入
- Alleghany 保险公司收购
- 西方石油公司持股
- 股票回购
- 通货膨胀
- 比特币批评（25 美元不买全部比特币）
- 政治中立立场
- 指数基金影响力

## 数据格式

### Markdown 文件
```markdown
# 2022 Berkshire Hathaway Annual Meeting - Morning Session

**Source**: CNBC Warren Buffett Archive  
**Date**: April 30, 2022  
**Location**: Omaha, Nebraska  
**URL**: https://buffett.cnbc.com/video/2022/05/02/morning-session---2022-meeting.html

---

WARREN BUFFETT: (Applause) Thank you.

I don't hear anything from the index funds. Where are they? (Laughter)

CHARLIE MUNGER: It's worked so far.
```

### 元数据 (JSON)
```json
{
  "year": 2022,
  "company": "Berkshire Hathaway",
  "source": "CNBC Warren Buffett Archive",
  "statistics": {
    "morning_paragraphs": 759,
    "afternoon_paragraphs": 661,
    "total_paragraphs": 1420
  }
}
```

## 爬取方法

### 手动提取（当前使用）
1. 打开 CNBC 股东大会页面
2. 按 F12 打开开发者控制台
3. 运行提取脚本：
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
    year: 2022,
    count: paragraphs.length,
    paragraphs: paragraphs
});
```
4. 保存 JSON 输出
5. 用 Python 脚本处理为 Markdown 格式

### 自动化爬取（待实现）
- 使用 Selenium/Playwright 自动访问页面
- 提取文本内容
- 保存为结构化格式

## 注意事项

1. **原始数据**: 文件保持原汁原味，未做任何编辑或整理
2. **特殊字符**: 包含 `(Laughter)`, `(Applause)`, `(unintelligible)` 等现场标记
3. **发言人标记**: 格式为 `WARREN BUFFETT:`, `CHARLIE MUNGER:`, 等
4. **版权问题**: 数据仅供个人学习研究使用

## 后续计划

- [ ] 爬取所有年份（1994-2025）
- [ ] 添加中文翻译版本
- [ ] 按话题分类整理
- [ ] 与现有 Wiki 索引整合

## 相关资源

- [巴菲特 Wiki 项目](../README.md)
- [CNBC 巴菲特档案](https://buffett.cnbc.com/)
- [伯克希尔官网](https://berkshirehathaway.com/)
