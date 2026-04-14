# Meilisearch 迁移计划

**创建时间**: 2026-04-14  
**状态**: 待执行  
**优先级**: 高

---

## 📋 执行摘要

将巴菲特 Wiki 的搜索引擎从自研的 `buffett-rag` 迁移到 **Meilisearch**，以获得：
- **3-5 倍** 查询速度提升（32ms → < 10ms）
- **自动中文分词** + 自定义词典优化
- **专业搜索引擎功能**（分面/过滤/排序/同义词）
- **更低的维护成本**（专业服务 vs 自研）

---

## 🎯 迁移目标

### 核心需求
1. ✅ 保留现有搜索功能（关键词搜索、时间线）
2. ✅ 支持中文分词（自动 + 词典优化）
3. ✅ 查询速度 < 10ms
4. ✅ 零停机迁移（用户无感知）

### 成功标准
- [ ] 所有 436 个文档成功索引
- [ ] 搜索准确率 ≥ buffett-rag
- [ ] 查询速度 < 10ms
- [ ] 时间线功能正常工作
- [ ] 回滚方案可用

---

## 📊 现状分析

### 当前系统（buffett-rag）

**架构**：
```
Python 倒排索引 + 中文单双字分词
```

**优势**：
- ✅ 零依赖，单文件部署
- ✅ 时间线功能原生支持
- ✅ 完全可控，透明
- ✅ 零成本运行

**劣势**：
- ❌ 查询速度较慢（~32ms）
- ❌ 无分面/过滤/排序功能
- ❌ 分词策略简单（单字 + 双字）
- ❌ 无同义词/停用词支持

**性能数据**：
```
索引大小：60MB
文档数：436
段落数：11,008
查询速度：0.46ms - 32ms（取决于查询复杂度）
```

### 目标系统（Meilisearch）

**架构**：
```
Rust 搜索引擎 + REST API + Python SDK
```

**优势**：
- ✅ 查询速度快（< 10ms）
- ✅ 自动中文分词
- ✅ 支持分面/过滤/排序
- ✅ 支持同义词/停用词/词典
- ✅ 专业搜索引擎功能

**劣势**：
- ⚠️ 需要运行独立服务
- ⚠️ 时间线需自己实现（用 sort）

**测试数据**：
```
文档数：436
索引时间：~6 秒
查询速度：2.3ms - 9.7ms
中文分词：自动支持 ✅
```

---

## 🔧 技术方案

### 方案选择：**完全迁移**（方案 A）

**架构**：
```
buffett-rag (Python 封装) → Meilisearch (REST API)
```

**理由**：
1. 性能提升明显（3x 速度）
2. 功能更丰富（分面/过滤/排序）
3. 维护成本低（专业服务 vs 自研）
4. 中文支持好（自动分词 + 词典）

### 架构对比

**当前**：
```
用户查询 → buffett-rag (倒排索引) → 返回结果
```

**迁移后**：
```
用户查询 → buffett-rag (封装层) → Meilisearch (API) → 返回结果
```

**优势**：
- CLI 接口保持不变（用户无感知）
- 可以逐步迁移功能
- 保留回滚能力

---

## 📝 实施步骤

### Step 1: 环境准备（预计：30 分钟）

**1.1 停止服务**
```bash
# 停止 LightRAG（如果还在运行）
pkill -9 -f lightrag

# 停止 Meilisearch（如果已在运行）
pkill -9 -f meilisearch
```

**1.2 清理 LightRAG 文件**
```bash
cd ~/workspace/warren_buffett_wiki
rm -rf .lightrag/      # LightRAG 索引目录
rm -f lightrag.log     # 日志文件
rm -f test_lightrag.py # 测试脚本
```

**1.3 启动 Meilisearch**
```bash
# 方式 1：直接运行
meilisearch --master-key YOUR_MASTER_KEY --http-addr 127.0.0.1:7700

# 方式 2：systemd 服务（生产环境推荐）
# 见下方「生产环境部署」章节
```

**1.4 验证服务**
```bash
curl http://localhost:7700/health
# 应返回：{"status":"available"}
```

---

### Step 2: 创建索引（预计：1 小时）

**2.1 初始化索引**
```python
import meilisearch

client = meilisearch.Client("http://localhost:7700", "YOUR_MASTER_KEY")

# 创建索引
index = client.create_index(uid="buffett-wiki", options={"primaryKey": "id"})
```

**2.2 配置索引设置**
```python
# 可搜索字段（按权重排序）
index.update_searchable_attributes([
    "title",      # 标题（权重最高）
    "content",    # 内容
    "tags",       # 标签
    "year"        # 年份
])

# 可过滤字段
index.update_filterable_attributes([
    "year",
    "doc_type",   # companies/concepts/cases/letters/people
    "tags"
])

# 可排序字段
index.update_sortable_attributes([
    "year",
    "created_at"
])

# 排序规则（优化中文搜索）
index.update_ranking_rules([
    "words",        # 词数匹配
    "typo",         # 拼写错误
    "proximity",    # 词距离
    "attribute",    # 字段权重
    "exactness",    # 精确匹配
    "asc(year)"     # 年份升序（可选）
])
```

**2.3 中文优化配置**

```python
# 1. 专业术语词典（从 Wiki 提取）
dictionary_terms = [
    "安全边际", "护城河", "巴菲特", "伯克希尔",
    "可口可乐", "盖可保险", "华盛顿邮报",
    "内在价值", "特许经营权", "能力圈",
    # ... 更多术语（建议 500+）
]

index.update_settings({
    "dictionary": dictionary_terms
})

# 2. 停用词（谨慎配置）
index.update_settings({
    "stopWords": [
        "的", "了", "在", "是", "我", "有",
        "和", "就", "不", "人", "都", "一"
    ]
})

# 3. 同义词
index.update_settings({
    "synonyms": {
        "股神": ["巴菲特"],
        "伯克希尔": ["Berkshire", "BRK"],
        "GEICO": ["盖可保险", "政府雇员保险"],
        "安全边际": ["margin of safety"]
    }
})
```

**2.4 等待设置生效**
```python
# 等待任务完成
task = index.wait_for_pending_task(task_uid)
print(f"设置完成：{task.status}")
```

---

### Step 3: 数据迁移（预计：2 小时）

**3.1 文档格式转换**
```python
import hashlib
from pathlib import Path
import json

def load_wiki_documents():
    """加载所有 Wiki 文档"""
    wiki_dir = Path("/Users/yapex/workspace/warren_buffett_wiki/wiki")
    documents = []
    
    for md_file in wiki_dir.rglob("*.md"):
        if md_file.name == "index.md":
            continue
        
        content = md_file.read_text(encoding='utf-8')
        
        # 提取 frontmatter
        frontmatter = {}
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                for line in parts[1].strip().split("\n"):
                    if ":" in line:
                        key, value = line.split(":", 1)
                        frontmatter[key.strip()] = value.strip()
        
        # 提取标题
        title = ""
        for line in content.split("\n"):
            if line.startswith("# "):
                title = line[2:].strip()
                break
        
        # 提取年份
        year = frontmatter.get("first_appeared", "")
        if not year:
            import re
            match = re.search(r'(\d{4})', md_file.name)
            year = match.group(1) if match else ""
        
        # 生成唯一 ID（MD5 hash，避免中文）
        file_path = str(md_file.relative_to(wiki_dir))
        doc_id = hashlib.md5(file_path.encode('utf-8')).hexdigest()[:16]
        
        # 构建文档
        doc = {
            "id": doc_id,
            "title": title,
            "content": content[:10000],  # 限制长度
            "year": year,
            "doc_type": md_file.parent.name,
            "tags": frontmatter.get("tags", "").split(",") if frontmatter.get("tags") else [],
            "path": file_path,
            "created_at": int(md_file.stat().st_mtime)
        }
        documents.append(doc)
    
    return documents
```

**3.2 批量索引**
```python
documents = load_wiki_documents()
print(f"加载了 {len(documents)} 个文档")

# 分批添加（每批 100 个）
batch_size = 100
for i in range(0, len(documents), batch_size):
    batch = documents[i:i+batch_size]
    task = index.add_documents(batch)
    print(f"索引批次 {i//batch_size + 1}/{len(documents)//batch_size + 1}")

# 等待索引完成
print("等待索引完成...")
index.wait_for_pending_update(task.uid)
print(f"索引完成：{len(documents)} 个文档")
```

**3.3 验证索引**
```python
# 检查统计
stats = index.get_stats()
print(f"文档数：{stats.number_of_documents}")
print(f"索引大小：{stats.index_size / 1024 / 1024:.2f} MB")

# 测试搜索
test_queries = ["安全边际", "护城河", "可口可乐", "巴菲特投资"]
for query in test_queries:
    results = index.search(query, {"hitsPerPage": 5})
    print(f"'{query}': {results['totalHits']} 个结果")
```

---

### Step 4: 查询接口封装（预计：2 小时）

**4.1 创建 WikiSearch 类**
```python
# wiki/search.py
import meilisearch

class WikiSearch:
    def __init__(self, url="http://localhost:7700", key=None):
        self.client = meilisearch.Client(url, key)
        self.index = self.client.index("buffett-wiki")
    
    def search(self, query, year_filter=None, doc_type=None, top_k=10):
        """基本搜索"""
        params = {
            "hitsPerPage": top_k,
        }
        
        # 构建过滤器
        filters = []
        if year_filter:
            filters.append(f"year >= '{year_filter}'")
        if doc_type:
            filters.append(f"doc_type = '{doc_type}'")
        
        if filters:
            params["filter"] = " AND ".join(filters)
        
        return self.index.search(query, params)
    
    def timeline(self, concept, top_k=20):
        """时间线搜索（按年份排序）"""
        results = self.index.search(
            concept,
            {
                "sort": ["year:asc"],
                "hitsPerPage": top_k * 2  # 扩大范围
            }
        )
        
        # 去重（同一年份只取一个）
        timeline = []
        seen_years = set()
        for hit in results["hits"]:
            year = hit.get("year")
            if year and year not in seen_years:
                seen_years.add(year)
                timeline.append(hit)
        
        return timeline[:top_k]
    
    def search_in_doc(self, query, doc_path, top_k=5):
        """文档内搜索"""
        # 先找到文档
        doc_results = self.index.search(
            "",
            {
                "filter": f"path = '{doc_path}'",
                "hitsPerPage": 1
            }
        )
        
        if not doc_results["hits"]:
            return []
        
        # 再用 content 搜索
        results = self.index.search(
            query,
            {
                "filter": f"path = '{doc_path}'",
                "hitsPerPage": top_k
            }
        )
        
        return results["hits"]
```

**4.2 兼容现有 CLI 接口**
```python
# rag/query.py（保持接口不变）
from wiki.search import WikiSearch

searcher = WikiSearch(key="YOUR_MASTER_KEY")

def search_paragraphs(query, top_k=10, year_filter=None):
    """兼容旧接口"""
    results = searcher.search(query, year_filter=year_filter, top_k=top_k)
    
    # 转换为旧格式
    return [
        {
            "para_id": hit["id"],
            "doc_id": hit["path"],
            "content": hit.get("content", "")[:500],
            "year": hit.get("year"),
            "score": hit.get("_score", 0),
            "jump_url": f"./wiki/{hit['path']}"
        }
        for hit in results["hits"]
    ]

def search_concept_timeline(concept, top_k=20):
    """兼容旧接口"""
    return searcher.timeline(concept, top_k=top_k)
```

---

### Step 5: 测试验证（预计：1 小时）

**5.1 功能测试**
```python
def test_search():
    """测试搜索功能"""
    queries = [
        ("安全边际", 100),  # 预期结果数
        ("护城河", 100),
        ("可口可乐 投资", 50),
        ("巴菲特 保险公司", 200),
    ]
    
    for query, expected_min in queries:
        results = searcher.search(query)
        assert results["totalHits"] >= expected_min, f"'{query}' 结果太少"
        print(f"✅ '{query}': {results['totalHits']} 个结果")

def test_timeline():
    """测试时间线"""
    timeline = searcher.timeline("安全边际")
    assert len(timeline) > 0, "时间线为空"
    
    # 验证按年份排序
    years = [hit.get("year") for hit in timeline if hit.get("year")]
    assert years == sorted(years), "时间线未按年份排序"
    print(f"✅ 时间线：{len(timeline)} 个结果")

def test_filter():
    """测试过滤"""
    results = searcher.search("投资", year_filter="1980")
    for hit in results["hits"]:
        assert hit.get("year", "0") >= "1980", "年份过滤失效"
    print(f"✅ 年份过滤：{results['totalHits']} 个结果")
```

**5.2 性能测试**
```python
import time

def benchmark():
    """性能基准测试"""
    queries = ["安全边际", "护城河", "可口可乐", "投资"]
    
    times = []
    for query in queries:
        start = time.time()
        searcher.search(query)
        elapsed = time.time() - start
        times.append(elapsed * 1000)  # ms
    
    avg_time = sum(times) / len(times)
    print(f"平均查询时间：{avg_time:.2f}ms")
    assert avg_time < 10, f"查询速度太慢：{avg_time:.2f}ms"
    print("✅ 性能测试通过")
```

**5.3 对比测试**
```python
def compare_with_old():
    """与 buffett-rag 对比"""
    queries = ["安全边际", "护城河", "可口可乐"]
    
    for query in queries:
        # 旧系统
        old_results = old_search(query)
        
        # 新系统
        new_results = searcher.search(query)
        
        # 对比结果数
        print(f"'{query}': 旧={len(old_results)}, 新={new_results['totalHits']}")
        
        # 对比 top 结果
        if old_results and new_results["hits"]:
            print(f"  旧 top1: {old_results[0].get('content', '')[:50]}")
            print(f"  新 top1: {new_results['hits'][0].get('content', '')[:50]}")
```

---

### Step 6: 生产部署（预计：1 小时）

**6.1 systemd 服务配置**
```bash
# /etc/systemd/system/meilisearch.service
[Unit]
Description=MeiliSearch
After=systemd-user-sessions.service

[Service]
Type=simple
ExecStart=/usr/bin/meilisearch \
  --http-addr 127.0.0.1:7700 \
  --env production \
  --master-key YOUR_MASTER_KEY \
  --db-dir /var/lib/meilisearch/data \
  --dump-dir /var/lib/meilisearch/dumps

[Install]
WantedBy=default.target
```

**6.2 启动服务**
```bash
# 设置服务
sudo systemctl enable meilisearch

# 启动服务
sudo systemctl start meilisearch

# 验证状态
sudo systemctl status meilisearch
```

**6.3 Nginx 配置（可选，用于 HTTPS 和访问控制）**
```nginx
server {
    listen 443 ssl;
    server_name search.yourdomain.com;

    # SSL 证书
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # IP 白名单
    allow 192.168.1.0/24;
    allow 127.0.0.1;
    deny all;

    location / {
        proxy_pass http://127.0.0.1:7700;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 🔄 回滚方案

### 触发条件
- 搜索准确率 < 80%
- 查询速度 > 50ms
- 系统不稳定（频繁宕机）

### 回滚步骤
```bash
# 1. 停止 Meilisearch
sudo systemctl stop meilisearch

# 2. 恢复 buffett-rag 配置
# （如果已修改，恢复原配置文件）

# 3. 重启服务
# （根据实际部署方式）

# 4. 验证
curl http://localhost:9621/health
```

### 回滚验证
```python
# 测试旧系统是否恢复正常
results = old_search("安全边际")
assert len(results) > 0, "回滚失败"
print("✅ 回滚成功")
```

---

## 📊 验收标准

### 功能验收
- [ ] 基本搜索正常工作
- [ ] 时间线功能正常工作
- [ ] 年份过滤正常工作
- [ ] 文档内搜索正常工作
- [ ] 中文分词准确

### 性能验收
- [ ] 平均查询时间 < 10ms
- [ ] 索引时间 < 10 分钟
- [ ] 内存占用 < 500MB
- [ ] 磁盘占用 < 200MB

### 质量验收
- [ ] 搜索准确率 ≥ buffett-rag
- [ ] 搜索结果相关性 ≥ buffett-rag
- [ ] 无中文分词错误
- [ ] 无专业术语识别错误

---

## 📅 时间安排

| 步骤 | 预计时间 | 负责人 | 状态 |
|------|---------|--------|------|
| Step 1: 环境准备 | 30 分钟 | - | ⏳ 待执行 |
| Step 2: 创建索引 | 1 小时 | - | ⏳ 待执行 |
| Step 3: 数据迁移 | 2 小时 | - | ⏳ 待执行 |
| Step 4: 查询接口 | 2 小时 | - | ⏳ 待执行 |
| Step 5: 测试验证 | 1 小时 | - | ⏳ 待执行 |
| Step 6: 生产部署 | 1 小时 | - | ⏳ 待执行 |
| **总计** | **7.5 小时** | - | - |

**建议**：分 2 天执行
- Day 1: Step 1-3（环境 + 索引 + 数据）
- Day 2: Step 4-6（接口 + 测试 + 部署）

---

## 🎓 参考资料

### 官方文档
- [Meilisearch 官方文档](https://docs.meilisearch.com/)
- [Indexing Best Practices](https://docs.meilisearch.com/docs/capabilities/indexing/advanced/indexing_best_practices)
- [Tokenization](https://docs.meilisearch.com/docs/capabilities/indexing/advanced/tokenization)

### 社区文章
- [相见恨晚！开源的傻瓜搜索引擎](https://www.cnblogs.com/xueweihan/p/15135814.html) - 削微寒（HelloGitHub 作者）

### 测试结果
- 测试脚本：`test_meilisearch.py`
- 测试数据：436 个文档，11,008 个段落
- 平均查询速度：< 10ms

---

## 📝 更新日志

| 日期 | 版本 | 变更 | 作者 |
|------|------|------|------|
| 2026-04-14 | v1.0 | 初始版本 | Hermes |

---

## ✅ 执行清单

**执行前**：
- [ ] 备份现有数据
- [ ] 准备 Meilisearch 安装包
- [ ] 准备 Master Key
- [ ] 通知相关人员（如有）

**执行中**：
- [ ] Step 1: 环境准备
- [ ] Step 2: 创建索引
- [ ] Step 3: 数据迁移
- [ ] Step 4: 查询接口
- [ ] Step 5: 测试验证
- [ ] Step 6: 生产部署

**执行后**：
- [ ] 性能测试通过
- [ ] 功能测试通过
- [ ] 用户验收通过
- [ ] 文档更新
- [ ] 回滚方案测试

---

**批准人**: _______________  
**执行日期**: _______________  
**实际耗时**: _______________
