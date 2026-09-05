# bug-hunter 测试报告 — codeplan-hub（boke）

> 终局报告 · 2026-09-04 · 模式：自动修复（用户确认）
> 目标：纯静态单文件站 index.html + data 生成管线（Python3 stdlib）

## 总览

| 指标 | 值 |
|---|---|
| 存活轮数 | 10 轮（R1–R10） |
| 累计发现 | **17 项**（计命）+ 1 项同根因去重（R10 死 CSS 第二轮） |
| 修复状态 | **18 项全部 fixed**（0 unfixed / 0 不可修复 / 0 欺诈） |
| 寿命终点 | life=8（初值 1，净 +7） |
| 模块覆盖 | **8/8 = 100%**（全部「已覆盖」） |
| 提交 | 每轮独立提交：b2049e7 / 9717b22 / 50fd669 / 71062e1 / 5760982 / e5e8021 / aaea61c / 181f105 / bce283a 等，全部已推送 origin/main |

## 发现清单（按严重度排序）

### 安全级（2）

**11. esc 纪律契约违规（潜在 XSS）** — fixed · R6 · e5e8021
- 证据：index.html 自声明「所有 JSON 数据插入 innerHTML 必须经过 esc」，但 `m.concurrency` / `m.calls`(×2) / `prov.rating` / `plan.inputPricePerMillion` 五处插槽漏转义
- 红：注入 `<img src=x onerror>` 载荷后 DOM 出现真实 img 元素（data-id 可被页面内验证）
- 绿：补 esc/Number 约束后同载荷仅显示为文本；README 明确邀请用户直接编辑 JSON，数据面不可信，防御纵深成立

**15/16. 错误路径与存储访问加固** — fixed · R8 · 181f105
- 15：catch 分支 `e.message` 未转义，JSON 解析错误消息嵌响应体原文——损坏数据文件可注入（绿测试：载荷以转义文本显示，onerror 不触发）
- 16：主脚本 `initTheme/toggleTheme` 裸访问 localStorage（头部内联脚本有 try/catch、主脚本没有），隐私加固配置下整段主脚本死亡（fetch/事件绑定全不执行）。两函数兜底后回归 dark↔light 切换与持久化正确

### 功能级（5）

**1. 促销价语义颠倒** — fixed · R1 · b2049e7
- 15 条套餐 originalPrice 误存首月促销价，页面渲染「现价¥40 + 划线~~¥7.9~~」；源头置 None（促销信息保留在 benefits），红测试 15→0 转绿，Live 复验「¥40 仅月付」无错误划线、稳明正确划线（¥30 ~~¥99~~）保留

**2. 移动端整页横向溢出** — fixed · R1 · b2049e7
- 375px 视口 scrollWidth 442>375（67px），根因 `.billing-tabs` 无响应式处理（同族 `.cat-tabs` 有 overflow-x 而 billing 遗漏）；@media≤860px flex-wrap 后 Live 复验溢出=false

**3. hash 路由单向** — fixed · R1 · b2049e7
- switchCategory 写 location.hash 无 hashchange 监听，后退后 URL=#token 页面停留 video；补监听后后退/前进双向回归通过

**9. 「当前：undefined」上屏** — fixed · R5 · 5760982
- catNames 映射缺 discontinued 键；改复用 CAT_LABELS 单一来源，6 分类绿测试全过、全页无 undefined

**10. 周付订阅误标买断价** — fixed · R5 · 5760982
- OpenStarry 星序版(周) 三处显示「一次性」（¥9.9 会被误读为永久买断）；build_billing_note 按 billingLabel 区分「仅周付」，稳明限购活动语义不变

### 契约/语义级（4）

**5. 季/年付列口径歧义** — fixed · R2 · 9717b22
- 列值是月均价（$4.50=$5×0.9）但列头「季付均价」可读成季总价（3 倍偏差）；列头/筛选器/README 统一「季付折月均/年付折月均」

**6. headline 与 plans 数据脱节** — fixed · R3 · 50fd669
- 腾讯 Token「8档/¥28起」实际 4 档 ¥39 起；Kimi「¥39起」为已废弃首月价（实际 ¥49）；修复后 56 家起步价全量审计 PASS

**13. 数据加载失败错误路径不完整** — fixed · R7 · aaea61c
- 404 时提示难懂 SyntaxError 且误导；空筛选栏/计费 tab 在错误态残留。fetchJSON 加 r.ok 检查、catch 隐藏控件；黑盒复验 404 提示真因+控件隐藏

**4. sitemap 6 条 hash URL 无效** — fixed · R2 · 9717b22
- 搜索引擎忽略 fragment，等于首页重复声明 6 次；精简为唯一可索引首页

### 一致性/文档级（4）

**7. badge 枚举映射缺口** — fixed · R3 · 50fd669：售罄/团队无映射 fallback 灰色，补 b-soldout（红）/b-team（青）含深色主题
**12. fReset 状态矛盾** — fixed · R6 · e5e8021：重置按钮能清 billing 却在 billing-only 时禁用；active 判定补 billing
**14. .gitignore 资产陷阱** — fixed · R7 · aaea61c：`*.png` 会静默忽略规划中的 og-image.png，加 `!og-image.png` 例外
**17. README 徽章枚举失真** — fixed · R9 · bce283a：7 种 vs 实际 9 种，补全

### 死代码（2）

**8. 死 CSS 64 行**（13 组选择器）— fixed · R4 · 71062e1 前身
**18. 死 CSS 残留 5 行**（.rm/.add-hint/.model-spec/.k）— fixed · R10 · 71062e1（R4 同根因去重不计命）
- 全量 141 class 使用率扫描死类清零；index.html 1110 → 1055 行

## 模块覆盖清单（终局校验）

| 模块 | 状态 | 发现数 |
|---|---|---|
| index.html/JS 渲染与状态机 | 已覆盖 | 3（Bug3/9/12） |
| index.html/价格与数字处理 | 已覆盖 | 2（Bug1/5） |
| index.html/CSS 布局与响应式 | 已覆盖 | 2（Bug2/8+18） |
| index.html/SEO meta 与结构 | 已覆盖 | 1（Bug4） |
| data/_generate_data.py | 已覆盖 | 2（Bug1/6/10 相关） |
| data/_add_reviews.py | 已覆盖 | 0 |
| data JSON 一致性 | 已覆盖 | 3（Bug6/7/17 相关） |
| robots/sitemap/LICENSE/README/.gitignore | 已覆盖 | 2（Bug14/17） |

**已覆盖 8/8 = 100%**

## 测试覆盖情况

- 白盒：JS 全部渲染函数/状态机/映射表逐插槽审计；Python 生成管线逐函数审查
- 黑盒 UI：browser-use 活体验证——6 分类循环、筛选组合（平台/模型/计费/价格上限含负数/小数/科学计数法/NaN 边界）、卡片单击/双击/键盘 Enter、hash 后退/前进、主题切换持久化、375/768/1024/1440 四断点溢出检测、暗色对比度抽检、404 降级路径
- 模糊：畸形数据 14 项变异矩阵（4 项 THROW 均安全降级到错误卡）
- 每项修复：红测试（或红复现）→ 修复 → 绿测试 → 浏览器 Live 复验原场景 → 全量回归

## 遗留风险与未修复项

无未修复 bug。两项**需用户决策**的已知事项（非 bug）：
1. `codeplan.example.com` 占位域名 + `og-image.png` 尚未制作——上线时统一替换（.gitignore 已留例外，og-image.png 可直接入库）
2. AtomCode、京东云（已下架）两个空官网链接，卡片外链指向 `#`
3. 设计灰区备忘：暗色主题辅助文字（ink-3/ink-4）对比度 3.7–4.0，AA 大字达标、正文级不达标——属编辑取舍，如需无障碍认证需调色

## 下次重启建议

- 错题集 `.zcode/agent/mistake-book.md` 已沉淀 17 条根因模式（双头映射漏键 ×3、摘要与明细脱节 ×3、esc 纪律、错误路径收尾、响应式同族排查等），复用价值高于重挖
- 数据变动时跑一致性探针：headline 起步价 vs plans 最低价、originalPrice>price、badge 枚举 vs BADGE_CLASS
- 外部基线：`export BH_PRE_BASELINE='{"life": 1, "found_total": 0, "round": 1, "rounds_completed": 0, "alive": true, "mode": null, "history": []}'`
