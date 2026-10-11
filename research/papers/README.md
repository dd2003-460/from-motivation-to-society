# papers/ — 关键论文引用 + 摘要笔记

> 本目录只放**引用与笔记**，不放 PDF（除非明确可合法获取且体积小）。
> 所有元数据经 OpenAlex API / Semantic Scholar API 核验。
> 详细笔记按研究问题分文件：`notes-q1-mutation.md` … `notes-q5-history.md`。

---

## 一、快速引用索引（按研究问题）

| # | 引用 | 一句话结论 | 对应 inventory |
|---|---|---|---|
| **Q1** | Adamic, Lento, Adar & Ng (2016). Information Evolution in Social Networks. *WSDM '16*, 473–482. DOI [10.1145/2835776.2835827](https://doi.org/10.1145/2835776.2835827)（arXiv:1402.6792） | Facebook 4.6 亿次复述：变异率服从 Yule 过程，级联距离越远编辑距离越大 | **E01** |
| **Q1** | Leskovec, Backstrom & Kleinberg (2009). Meme-tracking and the Dynamics of the News Cycle. *KDD '09*, 497–506. DOI [10.1145/1557019.1557077](https://doi.org/10.1145/1557019.1557077) | 9000 万文章 / 160 万站点的引语变异轨迹（MemeTracker 数据集） | **E02 / E23** |
| **Q1** | Simmons, Adamic & Adar (2011). Memes Online: Extracted, Subtracted, Injected, and Recollected. *ICWSM 2011* | 引语在转载中被裁剪 / 替换 / 加料；文本 meme 趋于缩写 | **E02** |
| **Q1** | Zannettou et al. (2018). On the Origins of Memes by Means of Fringe Web Communities. *ACM IMC 2018*. arXiv:[1805.12512](https://arxiv.org/abs/1805.12512) | 1.6 亿图 / 26 亿帖；meme 从边缘社区流向主流平台 | **E03** |
| **Q1/Q2** | Brady, McLoughlin, Doan & Crockett (2021). How social learning amplifies moral outrage expression in online social networks. *Science Advances* 7(33), eabe5641. DOI [10.1126/sciadv.abe5641](https://doi.org/10.1126/sciadv.abe5641) | 7,331 用户 / 1,270 万推文：社会反馈放大愤怒表达，规范学习盖过强化学习 | **E04** |
| **Q1** | Bartlett, F. C. (1932). *Remembering*. Cambridge University Press. | 「幽灵之战」系列再生：缩短 + 合理化（N≈20，**弱**） | **E25** |
| **Q2** | Berger & Milkman (2012). What Makes Online Content Viral? *JMR* 49(2), 192–205. DOI [10.1509/jmr.10.0353](https://doi.org/10.1509/jmr.10.0353) | 近 7,000 篇 NYT：高唤醒（敬畏/愤怒/焦虑）提升传播，悲伤降低 | **E05** |
| **Q2** | Brady, Wills, Jost, Tucker & Van Bavel (2017). Emotion shapes the diffusion of moralized content in social networks. *PNAS* 114(28), 7313–7318. DOI [10.1073/pnas.1618923114](https://doi.org/10.1073/pnas.1618923114) | 563,312 条推文：道德—情绪词每多一个，扩散 +20%；且受群体边界约束 | **E06** |
| **Q2** | Muchnik, Aral & Taylor (2013). Social Influence Bias: A Randomized Experiment. *Science* 341(6146), 647–651. DOI [10.1126/science.1240466](https://doi.org/10.1126/science.1240466) | 101,281 条评论随机化：一个赞 → 后续点赞概率 +32%，5 个月不衰减 | **E07** |
| **Q2** | Qiu (2024). Curiosity in news consumption. *Applied Cognitive Psychology*. DOI [10.1002/acp.4195](https://doi.org/10.1002/acp.4195) | 10 万+ 微信文章：问句标题阅读量 +3.4%；出人意料程度正向 | **E08** |
| **Q2** | Molina, Sundar, Rony, Hassan, Le & Lee (2021). Does Clickbait Actually Attract More Clicks? *CHI '21*, Art. 234. DOI [10.1145/3411764.3445753](https://doi.org/10.1145/3411764.3445753) | 12,000 条标题真实分享数据：clickbait **未**引发更多好奇 / 点击（**反证**） | **E09** |
| **Q3** | Goel, Anderson, Hofman & Watts (2016). The Structural Virality of Online Diffusion. *Management Science* 62(1), 180–196. DOI [10.1287/mnsc.2015.2158](https://doi.org/10.1287/mnsc.2015.2158) | 10 亿扩散事件：平均级联 1.3–1.4（等效 K≈0.3–0.4）；热度靠广播而非病毒 | **E11** |
| **Q3** | Cinelli et al. (2020). The COVID-19 social media infodemic. *Scientific Reports* 10, 16598. DOI [10.1038/s41598-020-73510-5](https://doi.org/10.1038/s41598-020-73510-5) | 134 万帖 / 374 万用户：**话题级** R₀：Gab 1.42–1.52 … Instagram 2.02–2.64 | **E12** |
| **Q3** | Luo, Hu & Sun (2026). Characterizing Information Propagation in Social Media with Branching Processes. *Entropy* 28(5), 493. DOI [10.3390/e28050493](https://doi.org/10.3390/e28050493) | 微博最多 8,979 万帖：**内容级** R₀ = 0.179–0.246，全部亚临界 | **E13** |
| **Q3** | Vosoughi, Roy & Aral (2018). The spread of true and false news online. *Science* 359(6380), 1146–1151. DOI [10.1126/science.aap9559](https://doi.org/10.1126/science.aap9559) | 126,000 故事 / 300 万人 / 450 万次转发：假新闻更快更远，因更新颖 | **E14** |
| **Q3/Q4** | Bakshy, Rosenn, Marlow & Adamic (2012). The role of social networks in information diffusion. *WWW '12*, 519–528. DOI [10.1145/2187836.2187907](https://doi.org/10.1145/2187836.2187907) | 2.53 亿人 RCT：强连接单条更强，但**弱连接**承担新信息传播 | **E15** |
| **Q4** | Grinberg, Joseph, Friedland, Swire-Thompson & Lazer (2019). Fake news on Twitter during the 2016 U.S. presidential election. *Science* 363(6425), 374–378. DOI [10.1126/science.aau2706](https://doi.org/10.1126/science.aau2706) | 16,442 账号：1% 占 80% 曝光，0.1% 占近 80% 分享；年龄效应显著 | **E16** |
| **Q4** | Guess, Nagler & Tucker (2019). Less than you think… *Science Advances* 5(1), eaau4586. DOI [10.1126/sciadv.aau4586](https://doi.org/10.1126/sciadv.aau4586) | 2,525 人调查 × 真实 FB 分享：65+ 分享假新闻约为 18–29 岁的 7 倍 | **E17** |
| **Q4** | Pennycook & Rand (2019). Lazy, not biased… *Cognition* 188, 39–50. DOI [10.1016/j.cognition.2018.06.011](https://doi.org/10.1016/j.cognition.2018.06.011) | N=3,446：分析型思维（CRT）预测真假新闻辨别力 | **E18** |
| **Q4** | Reuters Institute (2024). *Digital News Report 2024*. <https://reutersinstitute.politics.ox.ac.uk/digital-news-report/2024> | 47 个市场、95,000+ 人：新闻接触与平台使用的跨国年龄基线 | **E19** |
| **Q5** | Cantoni (2012). Adopting a New Religion: The Case of Protestantism in 16th Century Germany. *The Economic Journal* 122(560), 502–531. DOI [10.1111/j.1468-0297.2012.02495.x](https://doi.org/10.1111/j.1468-0297.2012.02495.x) | 119 领地 / 249 城：**到维滕贝格的距离**预测新教采纳 | **E20** |
| **Q5** | Bonnasse-Gahot et al. (2018). Epidemiological modelling of the 2005 French riots. *Scientific Reports* 8, 107. DOI [10.1038/s41598-017-18093-4](https://doi.org/10.1038/s41598-017-18093-4) | 6,877 事件 / 853 市镇 / 44 天：SIR 类模型拟合线下骚乱传播波 | **E21** |
| **Q5** | Banerjee, Chandrasekhar, Duflo & Jackson (2019). Using Gossips to Spread Information. *REStud* 86(6), 2453–2490. DOI [10.1093/restud/rdz008](https://doi.org/10.1093/restud/rdz008) | 213 村 RCT：换更好的种子有效，但增益 +3.65 通电话（p=0.19，不显著） | **E22** |

---

## 二、数据集索引

| 数据集 | 规模 | 获取方式 | 对应 |
|---|---|---|---|
| **MemeTracker**（memetracker.org / SNAP `memetracker9`） | 9,000 万文章 / 160 万站点（2008 大选期约 3 个月）；变异子集 685 万博客 → 309,730 引语 → 71,344 簇 | <http://memetracker.org> · <https://snap.stanford.edu/data/memetracker9.html> | E02 / E23 |
| **HuggingFace `easytpp/retweet`** | 24,000 行带时间戳的转发事件序列（47 MB，Apache-2.0） | <https://huggingface.co/datasets/easytpp/retweet> | E24 |
| **Cantoni 宗教改革复刻数据**（Harvard Dataverse） | 119 领地 / 249 城市，1300–1900 年人口 | DOI [10.7910/dvn/kqblle](https://doi.org/10.7910/dvn/kqblle) | E20 |

> 说明：E01（Facebook 460M 实例）、E11（Twitter 10 亿事件）、E16（Twitter 面板）等为**平台内部数据**，
> 未公开原始数据；其数字只能引自论文，无法二次复现。已在 inventory 中标注。

---

## 三、核验状态总表

| 条目 | 元数据核验 | 规模数字来源 | 状态 |
|---|---|---|---|
| E01 | ✅ OpenAlex | 论文 PDF（作者主页） | 已核实 |
| E02 | ✅ OpenAlex + 作者 PDF | 论文正文 | 已核实 |
| E03 | ✅ arXiv + KCL Pure | 论文摘要 | 已核实 |
| E04 | ✅ PMC / Science Advances | 摘要 | 已核实 |
| E05 | ✅ OpenAlex + S2 | 论文 PDF 正文 | 已核实 |
| E06 | ✅ PNAS 页面 | 摘要 + Results | 已核实 |
| E07 | ✅ S2 + Wikipedia 转述 | 摘要 | 已核实 |
| E08 | ✅ Wiley 页面 | 摘要 + 正文 | 已核实 |
| E09 | ✅ OpenAlex（含全部作者） | 论文 PDF 正文 | 已核实 |
| E11 | ✅ INFORMS + 两份 PDF | 正文（草稿与定稿数字略有差异，已在条目内注明） | 已核实 |
| E12 | ✅ PMC + arXiv | Table 1 / Table 4 | 已核实 |
| E13 | ✅ PMC 全文 | Table 1 + §3.1 | 已核实 |
| E14 | ✅ Science + S2 | 摘要 | 已核实 |
| E15 | ✅ OpenAlex | 摘要 | 已核实 |
| E16 | ✅ S2 摘要 | 摘要 + 论文 PDF | 已核实 |
| E17 | ✅ S2 + Science Advances | 摘要 + Results | 已核实 |
| E18 | ✅ PubMed | 摘要 | 已核实 |
| E19 | ✅ 官方页面 | Methodology | 已核实 |
| E20 | ✅ OpenAxex（DOI 已更正为 02495.x） | 论文 PDF | 已核实 |
| E21 | ✅ Nature 页面 | 正文 | 已核实 |
| E22 | ✅ OpenAlex | arXiv PDF 正文 | 已核实 |
| E25 | ⚠️ 未核原始文本 | 广泛转述 | **待核实（等级：弱，不影响结论）** |
