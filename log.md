# 📋 Changelog / 更新日志

<!-- Append-only log. Format: ## [YYYY-MM-DD] action | description -->

## [2026-04-07] ingest | 1982 Berkshire Shareholder Letter (ClawTeam tmux+subprocess pi --no-session)
- Raw sources: EN from juliuschun/eco-moat-ai, ZH from buffett-letters-eir.pages.dev (pre-existing)
- Pipeline: ClawTeam with tmux pi (aligner) + subprocess pi (extractor, summarizer, verifier, wikier) workers
- Created: [1982-letter](letters/1982-letter.md), [1982-summary](letters/1982-summary.md), [entities-1982.md](tmp/entities-1982.md)
- QA result: ✅ PASS — 6/6 sections present, all chapter headers match, signature/date present
- Created companies: [GEICO](companies/GEICO.md), [General-Foods](companies/General-Foods.md)
- Link verification: Partial — some links use English filenames (GEICO, Blue Chip Stamps) but actual files use Chinese (盖可保险, 蓝筹印花)
- New pages: 3 (1982-letter, 1982-summary, 2 company pages)
- Updated pages: 0

## [2026-04-07] ingest | 1981 Berkshire Shareholder Letter (ClawTeam subprocess pi -p mode)
- Raw sources: EN from juliuschun/eco-moat-ai, ZH from buffett-letters-eir.pages.dev (pre-existing)
- Pipeline: ClawTeam with subprocess pi -p --no-session workers
- Created: [1981-letter](letters/1981-letter.md), [1981-summary](letters/1981-summary.md), [tmp/1981-entities.json](tmp/1981-entities.json)
- QA findings: broken link 沃伦·巴菲特 (page not created), relative paths in summary (companies/ -> ../companies/), wrong link: 罗兰·米勒->乔治·扬
- QA result: ✅ PASS after fixes — 22 links verified, all sections present
- Created concepts: [无控制权持股收益](concepts/无控制权持股收益.md)
- Created companies: [雷诺烟草](companies/雷诺烟草.md), [平克顿安保](companies/平克顿安保.md)
- Created people: [沃伦·巴菲特](people/沃伦·巴菲特.md), [本·海涅曼](people/本·海涅曼.md), [亨利·辛格尔顿](people/亨利·辛格尔顿.md), [埃尔文·扎班](people/埃尔文·扎班.md), [汤姆·墨菲](people/汤姆·墨菲.md)
- Updated entities: 菲尔·利舍 (1981 ref), 乔治·扬 (1981 ref), 留存收益 (1981 ref)
- Link verification: ✅ All links pass after fixes — 22 links verified
- New pages: 8
- Updated pages: 3

## [2026-04-07] ingest | 1980 Berkshire Shareholder Letter (ClawTeam pilot)
- Raw sources: EN from juliuschun/eco-moat-ai, ZH from buffett-letters-eir.pages.dev (pre-existing)
- Pipeline: ClawTeam with 1 content worker (pi) + 1 QA worker (pi)
- Created: [1980-letter](letters/1980-letter.md), [1980-summary](letters/1980-summary.md), [tmp/1980-entities.json](tmp/1980-entities.json)
- QA findings: 6 broken wiki links fixed (韦斯科金融→韦斯科金融公司, 互助储贷→互助储贷公司, 国民保险→国民保险公司, 赛普拉斯保险→Cypress保险)
- QA result: ✅ PASS — all checks passed (40/40 callout pairs, all sections present, 11 links verified)
- Created concepts: [收益冰山理论](concepts/收益冰山理论.md), [真正的指数化](concepts/真正的指数化.md), [现金流承保](concepts/现金流承保.md), [权益法](concepts/权益法.md), [持久竞争优势](concepts/持久竞争优势.md)
- Created companies: [丘博保险](companies/丘博保险.md)
- Created people: [杰克·伯恩](people/杰克·伯恩.md), [丹·格罗斯曼](people/丹·格罗斯曼.md), [乔治·扬](people/乔治·扬.md), [芭芭拉·斯图尔特](people/芭芭拉·斯图尔特.md)
- Updated entities: 吉恩·阿贝格, 菲尔·利舍, 弗兰克·德纳尔多, 米尔特·桑顿, 留存收益 (1980 reference added)
- Link verification: ✅ All links pass — 11 links verified
- New pages: 10
- Updated pages: 5

## [2026-04-07] ingest | 1979 Berkshire Shareholder Letter
- Raw sources: EN from juliuschun/eco-moat-ai, ZH from buffett-letters-eir.pages.dev (pre-existing)
- Bilingual letter and summary already existed; verified completeness: all 9 sections present
- Created concepts: [投资人痛苦指数](concepts/投资人痛苦指数.md), [长期固定利率债券](concepts/长期固定利率债券.md), [困境反转](concepts/困境反转.md)
- Created companies: [联合出版公司](companies/联合出版公司.md), [阿美拉达·赫斯](companies/阿美拉达·赫斯.md), [通用食品](companies/通用食品.md), [汉迪哈曼](companies/汉迪哈曼.md), [媒体综合](companies/媒体综合.md), [奥美国际](companies/奥美国际.md), [伍尔沃斯](companies/伍尔沃斯.md), [Cypress保险](companies/Cypress保险.md), [互助储贷公司](companies/互助储贷公司.md), [精密钢铁](companies/精密钢铁.md)
- Created people: [菲利普·费雪](people/菲利普·费雪.md)
- Updated concepts: [股本回报率](concepts/股本回报率.md), [承保纪律](concepts/承保纪律.md), [综合比率](concepts/综合比率.md), [留存收益](concepts/留存收益.md), [保险浮存金](concepts/保险浮存金.md)
- Updated companies: [盖可保险](companies/盖可保险.md), [华盛顿邮报](companies/华盛顿邮报.md), [伊利诺伊国民银行](companies/伊利诺伊国民银行.md), [国民保险公司](companies/国民保险公司.md), [喜诗糖果](companies/喜诗糖果.md), [布法罗晚报](companies/布法罗晚报.md), [蓝筹印花](companies/蓝筹印花.md), [SAFECO公司](companies/SAFECO公司.md), [韦斯科金融公司](companies/韦斯科金融公司.md), [联合零售商店](companies/联合零售商店.md), [美国广播公司](companies/美国广播公司.md), [英特帕布利克集团](companies/英特帕布利克集团.md), [凯撒铝化学公司](companies/凯撒铝化学公司.md)
- Updated people: [菲尔·利舍](people/菲尔·利舍.md), [吉恩·阿贝格](people/吉恩·阿贝格.md), [本·罗斯纳](people/本·罗斯纳.md), [路易斯·文森蒂](people/路易斯·文森蒂.md), [杰克·林沃尔特](people/杰克·林沃尔特.md), [约翰·林沃尔特](people/约翰·林沃尔特.md), [弗洛伊德·泰勒](people/弗洛伊德·泰勒.md), [米尔特·桑顿](people/米尔特·桑顿.md), [弗兰克·德纳尔多](people/弗兰克·德纳尔多.md), [彼得·杰弗里](people/彼得·杰弗里.md)
- Link verification: ✅ All links pass — zero broken links
- New pages: 14
- Updated pages: 23

## [2026-04-06] ingest | 1978 Berkshire Shareholder Letter
- Raw sources: EN from juliuschun/eco-moat-ai (`markdown/buffett-letter-1978.md`), ZH from buffett-letters-eir.pages.dev
- Created: [1978-letter](letters/1978-letter.md), [1978-summary](letters/1978-summary.md)
- Created concepts: [集中投资](concepts/集中投资.md), [留存收益](concepts/留存收益.md)
- Created companies: [SAFECO公司](companies/SAFECO公司.md), [布法罗晚报](companies/布法罗晚报.md), [美国广播公司](companies/美国广播公司.md), [英特帕布利克集团](companies/英特帕布利克集团.md), [凯撒铝化学公司](companies/凯撒铝化学公司.md), [骑士报业公司](companies/骑士报业公司.md), [联合零售商店](companies/联合零售商店.md)
- Created people: [杰克·林沃尔特](people/杰克·林沃尔特.md), [本·罗斯纳](people/本·罗斯纳.md), [弗兰克·德纳尔多](people/弗兰克·德纳尔多.md), [米尔特·桑顿](people/米尔特·桑顿.md), [弗洛伊德·泰勒](people/弗洛伊德·泰勒.md), [约翰·林沃尔特](people/约翰·林沃尔特.md)
- Updated: [盖可保险](companies/盖可保险.md) (1978 持仓数据), [华盛顿邮报](companies/华盛顿邮报.md) (1978 市值 $43.4M), [蓝筹印花](companies/蓝筹印花.md) (持股提升至 ~58%), [伊利诺伊国民银行](companies/伊利诺伊国民银行.md) (1978 收益 $4.3M), [韦斯科金融公司](companies/韦斯科金融公司.md) (1978 数据), [国民保险公司](companies/国民保险公司.md) (1978 承保利润 ~$11M), [喜诗糖果](companies/喜诗糖果.md) (1978 数据), [菲尔·利舍](people/菲尔·利舍.md) (1978 业绩), [吉恩·阿贝格](people/吉恩·阿贝格.md) (1978 数据), [彼得·杰弗里](people/彼得·杰弗里.md) (1978 数据), [路易斯·文森蒂](people/路易斯·文森蒂.md) (1978 数据), [股本回报率](concepts/股本回报率.md) (added 1978 source), [承保纪律](concepts/承保纪律.md) (added 1978 source), [综合比率](concepts/综合比率.md) (added 1978 source), [顺风与逆风行业](concepts/顺风与逆风行业.md) (added 1978 source), [保险浮存金](concepts/保险浮存金.md) (added 1978 source), [社会通胀](concepts/社会通胀.md) (added 1978 source)
- Link verification: ✅ All 17 new/updated files pass — zero broken links
- New pages: 17
- Updated pages: 16

<!-- Append-only log. Format: ## [YYYY-MM-DD] action | description -->

## [2026-04-06] ingest | 1977 Berkshire Shareholder Letter
- Raw sources: EN from juliuschun/eco-moat-ai, ZH from buffett-letters-eir.pages.dev
- Created: [1977-letter](letters/1977-letter.md), [1977-summary](letters/1977-summary.md)
- Created concepts: [股本回报率](concepts/股本回报率.md), [顺风与逆风行业](concepts/顺风与逆风行业.md), [承保纪律](concepts/承保纪律.md), [社会通胀](concepts/社会通胀.md), [综合比率](concepts/综合比率.md), [保险浮存金](concepts/保险浮存金.md)
- Created companies: [盖可保险](companies/盖可保险.md), [华盛顿邮报](companies/华盛顿邮报.md), [蓝筹印花](companies/蓝筹印花.md), [大都会通讯公司](companies/大都会通讯公司.md), [伊利诺伊国民银行](companies/伊利诺伊国民银行.md), [韦斯科金融公司](companies/韦斯科金融公司.md), [国民保险公司](companies/国民保险公司.md)
- Created people: [菲尔·利舍](people/菲尔·利舍.md), [吉恩·阿贝格](people/吉恩·阿贝格.md), [肯尼思·蔡斯](people/肯尼思·蔡斯.md), [路易斯·文森蒂](people/路易斯·文森蒂.md), [彼得·杰弗里](people/彼得·杰弗里.md), [查克·哈金斯](people/查克·哈金斯.md)
- Updated: [喜诗糖果](companies/喜诗糖果.md) (added 1977 earnings data, added to Blue Chip Stamps context)
- New pages: 19
- Updated pages: 1

## [2026-04-06] ingest | 1989 Berkshire Shareholder Letter
- Raw source: `raw/berkshire/1989-letter.md` (from github.com/juliuschun/eco-moat-ai, original berkshirehathaway.com PDF returns 404)
- Created: [1989-summary](letters/1989-summary.md)
- Created concepts: [内在价值](concepts/内在价值.md), [透视收益](concepts/透视收益.md), [烟蒂投资法](concepts/烟蒂投资法.md), [制度惯性](concepts/制度惯性.md), [递延税](concepts/递延税.md), [Rip Van Winkle投资法](concepts/Rip Van Winkle投资法.md)
- Created companies: [可口可乐](companies/可口可乐.md), [波仙珠宝](companies/波仙珠宝.md), [吉列](companies/吉列.md), [喜诗糖果](companies/喜诗糖果.md), [内布拉斯加家具商场](companies/内布拉斯加家具商场.md)
- Created people: [查理·芒格](people/查理·芒格.md), [B夫人](people/B夫人.md), [Ike Friedman](people/Ike Friedman.md), [Roberto Goizueta](people/Roberto Goizueta.md)
- New pages: 16
- Updated pages: 0
