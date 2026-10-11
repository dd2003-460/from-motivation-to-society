# search-log.md — 检索式、渠道与结果

> 研究执行日期：2026-10-11（UTC）。
> 检索渠道：OpenAlex API、Semantic Scholar API、arXiv、Google Scholar（经 web 检索）、Nature / PNAS / Science / ACM DL / PubMed 官方页面、HuggingFace Datasets、Reuters Institute 官方页。

---

## 一、可用渠道（本沙箱实测）

| 渠道 | 可用 | 用法 | 备注 |
|---|---|---|---|
| **OpenAlex API** | ✅ | `https://api.openalex.org/works?filter=doi:<DOI>&select=id,doi,title,publication_year,biblio` | **核验 DOI / 卷期 / 年份的主力渠道**。用 `select=` 限制字段，否则返回体巨大 |
| **Semantic Scholar API** | ✅ | `https://api.semanticscholar.org/graph/v1/paper/DOI:<DOI>?fields=title,abstract,year,venue,externalIds` | **拿摘要最快**。部分出版社会 elide abstract（如 JMR） |
| **arXiv** | ✅ | `https://arxiv.org/abs/<id>` | 可拿全文（HTML / PDF） |
| **PMC / PubMed** | ✅ | `https://pmc.ncbi.nlm.nih.gov/articles/PMC<id>/` | 可拿全文，含 Table 数字 |
| **Nature / Science / PNAS / Wiley / ACM DL** | ✅ | 直接取页面 | 摘要与部分正文可读 |
| **Google Scholar** | 🟡 间接 | 经 web 检索命中 Scholar 索引的页面 | 无直连 API |
| **HuggingFace Datasets** | 🟡 间接 | 经 web 检索命中数据集卡片 | **本沙箱网络白名单不含 huggingface.co**，只能靠检索工具取卡片摘要 |
| **Papers-with-Code** | ❌ | 未直接取到 | 本议题的数据集多不在 PwC 上 |

**沙箱网络限制**：bash 侧仅允许 `github.com` / `codeload.github.com` / `api.github.com` / `registry.npmjs.org` / `pypi.org` / `files.pythonhosted.org`。
→ 所有文献检索**必须走 fetch_page / web_search 工具**（服务端），**不能**用 `curl` 直接打 OpenAlex / arXiv / Semantic Scholar API。
→ 已实测：`curl` 到 `api.openalex.org` 不通；`fetch_page` 到同一 URL 通。

---

## 二、按研究问题的检索式与结果

### Q1 · 观念接受与变形

| 检索式 | 渠道 | 结果 |
|---|---|---|
| `information evolution in social networks Adamic Lento Adar Ng Facebook memes mutation rate Yule process` | web | ✅ 命中 E01（WSDM 2016 / arXiv:1402.6792） |
| `Leskovec Backstrom Kleinberg "Meme-tracking and the dynamics of the news cycle" KDD 2009 dataset quotes MemeTracker` | web | ✅ 命中 E02 主论文 + 变异分析子集数字 |
| `"Memes Online: Extracted, Subtracted, Injected, and Recollected" ICWSM 2011 Simmons Adamic Adar quote mutation` | web | ✅ 命中；并由引文串出 E01（"Information Evolution in Social Networks", WSDM 2016） |
| `Zannettou "On the Origins of Memes by Means of Fringe Web Communities" IMC 2018 dataset 160 million memes 4chan Reddit` | web + arXiv | ✅ 命中 E03（160M 图 / 2.6B 帖 / 13 个月） |
| `serial reproduction large scale N>=1000 cultural transmission chain experiment` | OpenAlex / web | ❌ **未找到** N≥1,000 的受控传递链实验 |
| `Bartlett War of the Ghosts serial reproduction number of participants` | web | 🟡 仅广泛转述（N≈20），**未核到 1932 原文** → 标 E25 **弱 / 待核实** |
| `curiosity gap clickbait headline sharing large sample study experiment information gap virality` | web | ✅ **意外命中** E08（Qiu 2024，10 万+ 微信文章）与 E09（Molina CHI 2021 反证）—— 转归 Q2 |

**Q1 结论**：大样本证据全部来自**自然数据**（E01/E02/E03），无受控实验的大样本版本。

---

### Q2 · 共鸣触发机制

| 检索式 | 渠道 | 结果 |
|---|---|---|
| `Berger Milkman "What Makes Online Content Viral?" Journal of Marketing Research sample New York Times articles N` | web + OpenAlex + S2 | ✅ E05（近 7,000 篇 NYT / 3 个月） |
| `Brady Wills Van Bavel "Emotion shapes the diffusion of moralized content" PNAS 2017 sample size tweets N` | web + PNAS | ✅ E06（563,312 条推文）；另命中一个复现报告（313,002 条推文语料，IRR=1.21） |
| `Muchnik Aral Taylor "social influence bias: a randomized experiment" Science 2013 sample size comments page views N` | web + S2 | ✅ E07（101,281 条评论 / 1,000 万浏览 / 308,515 次评分） |
| `Pennycook Rand "Lazy, not biased" PNAS 2019 sample size participants cognitive reflection` | web + PubMed | ✅ 但**期刊是 Cognition 不是 PNAS**（N=3,446）→ E18 |
| `curiosity gap clickbait headline sharing large sample study experiment information gap virality` | web | ✅ E08（Qiu 2024）+ E09（Molina CHI 2021，反证） |
| `scarcity virality sharing large-scale natural data` / `scarcity information diffusion experiment N` | OpenAlex / S2 / web | ❌ **未找到** N≥1,000、以分享/扩散为因变量的自然数据研究 → **E10 标"无"** |

**Q2 结论**：情绪唤醒、身份/道德化、社会证明、信息缺口、新颖性**均有证据**；**稀缺性无证据**；clickbait 有**反证**。

---

### Q3 · K 因子 / 基本再生数

| 检索式 | 渠道 | 结果 |
|---|---|---|
| `Goel Anderson Hofman Watts "structural virality" online diffusion Management Science dataset size how many events` | web | ✅ **E11**（10 亿事件；平均级联 1.3–1.4；219,855 条大级联） |
| `estimating basic reproduction number R0 information diffusion social media hashtags large scale empirical` | web | ✅ **命中两条关键文献**：E12（Cinelli 2020，五平台 R₀）与 **E13**（Luo 2026，微博 R₀ = 0.179–0.246） |
| `Vosoughi Roy Aral "The spread of true and false news online" Science 2018 sample 126,000 stories` | web + S2 | ✅ E14（126,000 故事 / 300 万人 / 450 万次转发） |
| `Bakshy Rosenn Marlow Adamic "The role of social networks in information diffusion" WWW 2012 253 million Facebook users weak ties` | web + OpenAlex | ✅ E15（2.53 亿人 RCT） |

**Q3 关键发现（检索后才看清）**：`R0` 的检索同时返回 **>1** 与 **<1** 的文献。
→ 逐条核对后发现差异源于**层级不同**（话题级 vs 内容级），这是本次研究最重要的一个结论，已写入 synthesis §〇 与 §Q3。

---

### Q4 · 人群差异

| 检索式 | 渠道 | 结果 |
|---|---|---|
| `Grinberg Joseph Friedland "Fake news on Twitter during the 2016 U.S. presidential election" Science 2019 sample size tweets users age` | web + S2 | ✅ E16（16,442 账号；1%/80%、0.1%/80%；年龄系数 0.02***） |
| `Guess Nagler Tucker "Less than you think" Science Advances 2019 sample N users age` | web + S2 | ✅ 摘要拿到，但**摘要不含 N** → 再检索 `Guess Nagler Tucker 2019 Facebook fake news study "2,525"` → ✅ N=2,525（E17） |
| `Pennycook Rand "Lazy, not biased" sample size` | PubMed | ✅ E18（N=3,446） |
| `Reuters Institute Digital News Report 2024 sample size respondents countries methodology` | web | ✅ E19（>95,000 / 47 市场 / 2024 年 1–2 月） |
| `students vs office workers vs experts differences in sharing behavior large sample` | OpenAlex / S2 | ❌ **未找到**以四分类为自变量的 N≥1,000 研究 → 诚实标注 |

**Q4 结论**：年龄（两项独立研究、两个平台、两种方法一致）与分析型思维有证据；**四分类本身无证据**。

---

### Q5 · 跨时空共通框架

| 检索式 | 渠道 | 结果 |
|---|---|---|
| `Cantoni "Adopting a New Religion: The Case of Protestantism in Sixteenth-Century Germany" Economic Journal 2012 number of cities` | web | ✅ 命中论文 PDF（119 领地 / 249 城市） |
| — DOI 初次猜测 `10.1111/j.1468-0297.2012.02534.x` | OpenAlex | ❌ **DOI 错误**（该 DOI 是另一篇"Two-Tier Labour Markets in the Great Recession"）→ 用 `title.search` 重新查 → ✅ 正确 DOI **10.1111/j.1468-0297.2012.02495.x**，并**额外发现 Harvard Dataverse 复刻包** DOI 10.7910/dvn/kqblle |
| `Bonnasse-Gahot "Epidemiological modelling of the 2005 French riots" PNAS 2018 number of events towns` | web | ✅ 但**期刊是 Scientific Reports 不是 PNAS**（8:107；6,877 事件 / 853 市镇 / 44 天）→ E21 |
| `Banerjee Chandrasekhar Duflo Jackson gossips spread information randomized controlled trial villages` | OpenAlex | ✅ 但**正式题名是 "…from Two Randomized Controlled Trials"**（REStud 86(6):2453–2490）→ E22 |
| `quantitative study diffusion of ideas along the Silk Road large dataset Buddhism spread network analysis archaeology` | web | ❌ **仅返回定性 / 史料综述** → **E26 标"无"** |
| `quantitative diffusion dataset Wang Anshi reform Song dynasty adoption` | OpenAlex / S2 | ❌ **无结果** → **E27 标"无"** |

---

## 三、失败与纠错记录（保留，供复现）

1. **Cantoni DOI 猜错**：凭记忆写的 `…02534.x` 指向完全无关的论文。**教训：DOI 必须过 OpenAlex 核验，不能凭记忆。**
2. **Bonnasse-Gahot 期刊记错**：记忆中是 PNAS，实际是 *Scientific Reports* 8:107。**教训：期刊 / 年份同样要核验。**
3. **Pennycook & Rand 期刊记错**：记忆中是 PNAS 2019，实际是 *Cognition* 188:39–50（2019，线上 2018）。**教训：同名作者有多篇相似论文，必须核 DOI。**
4. **Banerjee et al. 题名记错**：arXiv 版本叫 "…from a Randomized Controlled Trial"，正式发表版改为 "…from **Two** Randomized Controlled Trials"。
5. **Goel et al. 的数字有两个版本**：预印本（6.22 亿内容 / 12 亿采纳）与正式版（7.5 亿 / 14 亿）略有差异；**平均级联规模也有 1.3 与 1.4 两种表述**。已在 E11 中并列标注，不取单一值。
6. **Bartlett (1932) 的 N 未核到原文**：N≈20 为广泛转述值。**已降级为"弱"并标"待核实"**，且明确声明它**不是** Q1 的证据主力。
7. **HuggingFace 数据集检索质量低**：`HuggingFace dataset meme diffusion retweet cascade dataset size` 返回的多是 <1,000 行的个人上传集。最终只保留了 `easytpp/retweet`（24,000 行，属标准基准集）。

---

## 四、可复现的检索模板（下次直接用）

```
# 1. 用 DOI 核验元数据
https://api.openalex.org/works?filter=doi:<DOI>&select=id,doi,title,publication_year,biblio

# 2. 用题名查 DOI（DOI 记不准时）
https://api.openalex.org/works?filter=title.search:<Title>&select=id,doi,title,publication_year,biblio,authorships&per-page=3

# 3. 拿摘要
https://api.semanticscholar.org/graph/v1/paper/DOI:<DOI>?fields=title,abstract,year,venue,externalIds

# 4. 拿全文（开放获取）
https://pmc.ncbi.nlm.nih.gov/articles/PMC<id>/
https://arxiv.org/abs/<id>
```
