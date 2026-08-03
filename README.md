# CodePlan·比价

> 中立、免费的 AI 套餐对比站。覆盖 Coding、Token、视频、图片、音频五大场景，55 家平台、89 个套餐档位，一个页面全搞定。

**2026 持续更新** · 人工核对 · 非爬虫抓取 · 深/浅主题

---

## ✨ 特性

- **6 大分类 + 已下架归档**：Coding / Token / Video / Image / Audio / 中转站 / 已下架，分类 tab 切换
- **卡片概览**：每家平台一张卡片，星级评分 + 编辑点评 + 支持模型 + 最低价，点击卡片筛选下方对比表
- **12 列对比大表**：平台 / 方案 / 开通 / 月付 / 季付均价 / 年付均价 / 5h请求数 / 周请求数 / 月总请求数 / 支持模型 / 额外权益 / 备注
- **多维度筛选**：平台下拉、模型下拉、月付/季付/年付上限、计费方式（全部/Coding/Token），组合生效
- **跨币种折算**：美元套餐自动按 7.2 汇率折算人民币参与排序和价格筛选，显示 `$20 ≈¥144`
- **排行徽章**：入门 / 性价比 / 进阶 / 旗舰 / 活动 / 免费 / 按量，同分内可置顶 featured 平台
- **深 / 浅主题**：跟随系统 + 手动切换，localStorage 持久化
- **响应式**：桌面 3 列卡片，移动单列；分类 tab 栏横向滑动；对比表横向滚动不撑爆
- **纯静态**：单文件 HTML + JSON 数据，无构建工具，无后端

## 📂 分类与覆盖

| 分类 | 平台数 | 说明 |
|---|---|---|
| 💻 Coding | 26 | 按次订阅的编程套餐（智谱/稳明/字节方舟/Kimi/百度/腾讯…） |
| 🎫 Token | 9 | 按 token 计费（阿里/小米/方舟/腾讯/TaoToken…） |
| 🎬 Video | 8 | 视频生成平台概览（可灵/即梦/Vidu/海螺…） |
| 🖼️ Image | 6 | 图片生成平台概览（Midjourney/即梦/Liblib…） |
| 🎵 Audio | 4 | 音频生成平台概览（Suno/Udio/Ace Studio…） |
| 📦 已下架 | 1 | 停服平台归档（京东云） |

Video / Image / Audio / 已下架 类别暂仅含平台概览，无套餐明细，数据持续整理中。

## 🛠 技术栈

- 纯静态单文件 `index.html`（HTML + 内联 CSS + 原生 JS，无框架）
- 数据：`data/providers.json`（平台）+ `data/plans.json`（套餐）
- 数据由 `data/_generate_data.py` 生成，`data/_add_reviews.py` 补充编辑点评
- 字体：Inter + JetBrains Mono（Google Fonts）
- CSS 变量驱动主题，`color-mix()` 实现深浅色自适应

## 🚀 本地开发

无需构建，任意静态服务器即可：

```bash
python3 -m http.server 8765
# 打开 http://localhost:8765
```

或直接用 VS Code Live Server / `npx serve` 等。

## 📁 项目结构

```
codeplan-hub/
├── index.html                  # 站点主体（HTML + CSS + JS 单文件）
├── data/
│   ├── providers.json          # 55 家平台数据
│   ├── plans.json              # 89 个套餐档位
│   ├── _generate_data.py       # 数据生成脚本（源）
│   └── _add_reviews.py         # 编辑点评补充脚本
├── docs/
│   └── AIPlanHub-幻境MirageAI-技术分析文档.md
├── .gitignore
└── README.md
```

## 📊 数据结构

### providers.json

```jsonc
{
  "id": "coding-wenming",          // {category}-{slug}
  "category": "coding",            // coding/token/video/image/audio/relay/discontinued
  "name": "稳明光语纪",
  "type": "aggregator",            // vendor 厂商 / aggregator 聚合 / relay 中转
  "url": "https://...",            // 官网/开通链接
  "blurb": "一句话简介",
  "rating": 4.0,                   // 主观评分 0-5
  "headline": "¥29.9 起 · ...",
  "tags": ["按次", "按 token"],
  "review": "编辑点评正文",          // 卡片主体内容
  "featured": false,               // true 则同分内置顶
  "asOf": "2026-07-31"
}
```

### plans.json

```jsonc
{
  "id": "coding-wenming-pro",
  "providerId": "coding-wenming",
  "planName": "Pro",
  "tier": "PRO",                   // 可空
  "billingMode": "CALL",           // CALL 按次 / TOKEN 按量
  "billingLabel": "月度按次",
  "price": 125,                    // 主价格
  "currency": "CNY",               // CNY / USD
  "originalPrice": null,
  "periodDays": 30,
  "billingCycles": { "monthly": 125, "quarterly": null, "annual": null, "note": "仅月付" },
  "usageWindow": { "fiveHour": null, "weekly": null, "monthly": null, "totalTokens": null },
  "models": [{ "code": "glm-5.2", "version": "5.2", "context": "1M", "concurrency": "...", "calls": 5000, "isBonus": false }],
  "benefits": ["每月5000次", "赠送 DeepSeek-V4-Flash"],
  "badge": "性价比",               // 入门/性价比/进阶/旗舰/活动/免费/按量
  "highlight": "日常使用，高性价比",
  "subscribeUrl": "https://...",
  "source": "https://...",
  "sourceType": "manual",          // manual 手动 / api 接口同步
  "isPlaceholder": false,
  "asOf": "2026-07-31"
}
```

**橙色「待核实」** 标记表示该字段接口未提供或待人工核实，非最终值。

## 🔗 开通链接策略

本站中立，邀请链接策略透明：

- **5 个平台使用站方邀请码**：稳明光语纪、智谱 AI、字节·方舟、Kimi、OpenStarry
- **其余平台一律官方直链**，不带任何第三方邀请码
- **ChatGPT** 指向官方定价页 `openai.com/chatgpt/pricing`（美元计价，自动折算人民币对比）

如需更改邀请链接，修改 `data/_generate_data.py` 对应记录后重新生成，或直接改 `data/providers.json` / `data/plans.json` 的 `subscribeUrl` / `url` 字段。

## 🎨 设计要点

- **卡片交互**：点卡片 = 选中该平台筛选对比表（单选）；卡片右下角外链图标 = 新标签打开官网，两动作分离
- **编辑点评为核心**：每张卡片有一段人工撰写的 `review` 文本，强调人声音而非纯数据罗列
- **color-mix 主题自适应**：卡片字母标、hover 边框用 `color-mix(in srgb, var(--c) N%, var(--surface))`，深浅主题自动适配
- **URL hash 路由**：分类切换写 `location.hash`，刷新可恢复、可分享
- **对比表防撑高**：模型列无规格时流式排列 chip + 一条「规格待核实」，不逐模型逐规格占行

## 📝 数据来源

- 部分平台结构与信息参考 [AIPlanHub](https://ai.hsnb.fun/aiplanhub) 开源项目
- 模型规格（版本/上下文/并发）据各厂商官方文档核实，如智谱 GLM-5.2（1M 上下文）、DeepSeek-V4-Flash（1M/并发 2500）
- 价格与用量均为公开信息，**橙圈**标记为待核实占位

## ⚠️ 免责声明

- 卡片评分为**主观印象**（满分 5），仅代表编辑综合判断，非客观数据
- 聚合平台套餐为模型二次转售，计费单位各异，实际成本受模型档位、缓存、限速影响
- 本站**不售卖任何套餐**，仅提供信息对比，以各厂商官方页面为准
- 数据仅供参考，不构成购买建议

## 📄 License

数据与代码可自由使用，请注明来源。各平台名称、商标归各自所有。
