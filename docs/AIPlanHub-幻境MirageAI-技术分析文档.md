# AIPlanHub（幻境 MirageAI）技术分析文档

> ⚠️ **外部参考资料 / 调研存档**：本文档是对外部站点 ai.hsnb.fun 的分析记录，**非本项目（CodePlan·比价）代码文档**。本项目仅参考其中的平台与数据信息，代码与实现见 `index.html` 与 `data/`。

> **分析日期**: 2026-08-01  
> **目标站点**: https://ai.hsnb.fun  
> **分析页面**: /aiplanhub（订阅方案对比页）  
> **开源项目**: [QuantumNous/new-api](https://github.com/QuantumNous/new-api) (基于 One API 二次开发)  
> **当前版本**: v1.0.0-rc.22

---

## 一、项目概述

### 1.1 项目定位

**幻境 MirageAI** 是一个 AI API 聚合中转站（AI API Gateway），核心业务模式是：
- 聚合上游 AI 平台（OpenAI、Claude、Gemini、DeepSeek、GLM 等）的 API
- 统一转换为 **OpenAI 兼容格式**对外提供
- 通过批量采购/免费额度套利赚取差价
- 提供用户管理、计费、充值、订阅等全套管理系统

### 1.2 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| **后端** | Go + Gin | API 网关与管理后台 |
| **数据库** | SQLite / MySQL | 二选一 |
| **前端** | React + TypeScript | SPA 应用 |
| **构建工具** | Rsbuild (rspack) | 高性能 Rust 构建 |
| **包管理** | Bun | 快速 JS 运行时 |
| **UI 框架** | shadcn/ui | 组件库 |
| **状态管理** | React Query (TanStack Query) | 服务端状态 |
| **表单** | react-hook-form | 表单管理 |
| **CSS** | Tailwind CSS | 实用优先样式 |
| **部署** | Docker / Docker Compose | 容器化部署 |
| **CDN/代理** | 腾讯 EdgeOne + Cloudflare | 双线加速 |

### 1.3 运行环境

- **主域名**: `https://ai.hsnb.fun` (腾讯 EdgeOne 线路)
- **备用域名**: `https://ai-cf.hsnb.fun` (Cloudflare 线路)
- **服务器**: 阿里云北京节点 (39.104.123.54)
- **部署方式**: Docker Compose

---

## 二、系统架构

### 2.1 总体架构图

```
┌──────────────────────────────────────────────────────┐
│                    客户端 (Client)                     │
│  Cherry Studio / LobeChat / DeepChat / OpenCat / ...  │
└────────────────────┬─────────────────────────────────┘
                     │ OpenAI 格式 API (/v1/...)
                     ▼
┌──────────────────────────────────────────────────────┐
│              EdgeOne / Cloudflare (CDN)               │
└────────────────────┬─────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────┐
│              幻境 MirageAI (Go Backend)               │
│                                                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐    │
│  │ API 网关  │  │ 管理后台  │  │ 认证/授权 (JWT)   │    │
│  │ (Relay)  │  │ (Admin)  │  │ + OAuth + Passkey │    │
│  └────┬─────┘  └────┬─────┘  └──────────────────┘    │
│       │             │                                  │
│  ┌────▼─────────────▼─────────────────────────────┐   │
│  │              渠道层 (Channel Layer)              │   │
│  │  - OpenAI / Azure / Anthropic / Google / ...    │   │
│  │  - 负载均衡 / 重试 / 故障转移                     │   │
│  │  - 配额管理 / 限流 / 计费                         │   │
│  └────┬────────────────────────────────────────────┘   │
└───────┼────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────────┐
│              上游 AI 服务商                             │
│  OpenAI │ Anthropic │ Google │ DeepSeek │ 智谱 │ ...   │
└──────────────────────────────────────────────────────┘
```

### 2.2 核心模块

| 模块 | 说明 |
|------|------|
| **Relay（中继）** | 核心转发引擎，将请求转发到上游并返回结果 |
| **Channel（渠道）** | 管理上游 API key 和供应商配置 |
| **Token（令牌）** | 用户 API Key 管理，用于客户端调用认证 |
| **Billing（计费）** | Token 消耗统计、按量计费、模型定价 |
| **Subscription（订阅）** | 订阅套餐管理、自动续费 |
| **TopUp（充值）** | 在线充值（易支付/Stripe/Creem/Waffo） |
| **Log（日志）** | 请求日志、用量统计 |
| **Model（模型）** | 模型元数据管理、上游模型同步 |

---

## 三、API 接口全览

### 3.1 Relay 中继接口（对外 API，使用 Token 认证）

这些接口是用户实际调用 AI 模型的接口，通过 `Authorization: Bearer {token}` 认证：

| 方法 | 路径 | 功能 |
|------|------|------|
| GET | `/v1/models` | 获取可用模型列表 |
| GET | `/v1/models/:model` | 获取模型详情 |
| POST | `/v1/chat/completions` | Chat 对话（OpenAI 格式） |
| POST | `/v1/completions` | 文本补全 |
| POST | `/v1/messages` | Claude Messages 格式 |
| POST | `/v1/responses` | OpenAI Responses API |
| POST | `/v1/embeddings` | 文本向量化 |
| POST | `/v1/images/generations` | 图片生成 |
| POST | `/v1/images/edits` | 图片编辑 |
| POST | `/v1/audio/transcriptions` | 语音转文字 |
| POST | `/v1/audio/translations` | 语音翻译 |
| POST | `/v1/audio/speech` | 文字转语音 |
| POST | `/v1/rerank` | 重排序 (Rerank) |
| POST | `/v1/moderations` | 内容审核 |
| GET | `/v1/realtime` | OpenAI Realtime (WebSocket) |
| POST | `/v1beta/models/*path` | Gemini 格式 API |
| POST | `/suno/submit/:action` | Suno 音乐生成 |
| POST | `/suno/fetch` | Suno 任务查询 |
| POST | `/mj/submit/*` | Midjourney 图片生成 |
| GET | `/mj/task/:id/fetch` | MJ 任务查询 |
| GET | `/mj/image/:id` | MJ 图片获取 |

### 3.2 管理后台 API（公开接口）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/status` | 站点状态、公告、配置 |
| GET | `/api/setup` | 初始化状态 |
| GET | `/api/notice` | 系统通知 |
| GET | `/api/pricing` | 定价信息 |
| GET | `/api/rankings` | 排行榜 |
| GET | `/api/models` | 模型列表 |
| GET | `/api/home_page_content` | 首页内容 |
| GET | `/api/about` | 关于页面 |
| GET | `/api/user-agreement` | 用户协议 |
| GET | `/api/privacy-policy` | 隐私政策 |
| GET | `/api/ratio_config` | 倍率配置 |

> **重要更正**: 之前标注"需登录"的错误——aiplanhub 页面上的 AI 对比数据来自开源仓库 [HsMirage/AIPlanHub](https://github.com/HsMirage/AIPlanHub)，完全公开无需登录。数据以 Markdown 格式存储在 GitHub README 中，网站直接渲染展示。

### 3.3 管理后台 API（用户接口，需 UserAuth）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/user/register` | 用户注册 |
| POST | `/api/user/login` | 用户登录 |
| POST | `/api/user/auth/refresh` | 刷新令牌 |
| POST | `/api/user/auth/logout` | 登出 |
| GET | `/api/user/self` | 获取个人信息 |
| PUT | `/api/user/self` | 更新个人信息 |
| DELETE | `/api/user/self` | 删除账号 |
| GET | `/api/user/token` | 生成 API Token |
| GET | `/api/user/models` | 用户可用模型 |
| GET | `/api/user/groups` | 用户分组 |
| GET | `/api/user/topup/self` | 充值记录 |
| POST | `/api/user/topup` | 提交充值 |
| POST | `/api/user/pay` | 发起支付（易支付） |
| POST | `/api/user/stripe/pay` | 发起支付（Stripe） |
| GET | `/api/user/aff` | 推广码 |
| POST | `/api/user/aff_transfer` | 推广额度划转 |
| GET | `/api/user/checkin` | 签到状态 |
| POST | `/api/user/checkin` | 签到 |
| GET | `/api/log/self` | 自己的日志 |
| GET | `/api/log/self/stat` | 自己的统计 |
| GET | `/api/data/self` | 自己的数据图表 |
| GET | `/api/mj/self` | 自己的 MJ 任务 |
| GET | `/api/task/self` | 自己的异步任务 |

### 3.4 Token 管理接口（需 UserAuth）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/token/` | Token 列表 |
| GET | `/api/token/search` | 搜索 Token |
| GET | `/api/token/:id` | Token 详情 |
| POST | `/api/token/:id/key` | 查看 Token Key |
| POST | `/api/token/` | 创建 Token |
| PUT | `/api/token/` | 更新 Token |
| DELETE | `/api/token/:id` | 删除 Token |
| POST | `/api/token/batch` | 批量删除 |
| POST | `/api/token/batch/keys` | 批量获取 Key |

### 3.5 订阅接口（需 UserAuth）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/subscription/plans` | 套餐列表 |
| GET | `/api/subscription/self` | 我的订阅 |
| PUT | `/api/subscription/self/preference` | 偏好设置 |
| POST | `/api/subscription/balance/pay` | 余额支付 |
| POST | `/api/subscription/epay/pay` | 易支付支付 |
| POST | `/api/subscription/stripe/pay` | Stripe 支付 |

### 3.6 管理后台 API（管理员接口，需 AdminAuth）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/user/` | 用户列表 |
| GET | `/api/user/search` | 搜索用户 |
| POST | `/api/user/` | 创建用户 |
| PUT | `/api/user/` | 更新用户 |
| DELETE | `/api/user/:id` | 删除用户 |
| GET | `/api/channel/` | 渠道列表 |
| POST | `/api/channel/` | 创建渠道 |
| PUT | `/api/channel/` | 更新渠道 |
| DELETE | `/api/channel/:id` | 删除渠道 |
| POST | `/api/channel/test` | 测试渠道 |
| GET | `/api/log/` | 全部日志 |
| GET | `/api/log/stat` | 日志统计 |
| GET | `/api/data/` | 数据看板 |
| GET | `/api/redemption/` | 兑换码管理 |
| GET | `/api/group/` | 分组管理 |
| GET | `/api/vendors/` | 供应商管理 |

### 3.7 系统设置接口（需 RootAuth）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/option/` | 系统配置 |
| PUT | `/api/option/` | 更新配置 |
| POST | `/api/option/rest_model_ratio` | 重置模型倍率 |
| POST | `/api/system-task/log-cleanup` | 日志清理任务 |
| GET | `/api/performance/stats` | 性能统计 |
| POST | `/api/performance/gc` | 强制 GC |
| GET | `/api/ratio_sync/channels` | 获取可同步渠道 |
| POST | `/api/ratio_sync/fetch` | 同步上游倍率 |

### 3.8 支付回调接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST/GET | `/api/user/epay/notify` | 易支付回调 |
| POST | `/api/stripe/webhook` | Stripe Webhook |
| POST | `/api/creem/webhook` | Creem Webhook |
| POST | `/api/waffo/webhook` | Waffo Webhook |
| POST | `/api/subscription/epay/notify` | 订阅易支付回调 |

### 3.9 OAuth 认证接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/oauth/state` | 生成 OAuth 状态码 |
| GET | `/api/oauth/:provider` | OAuth 登录回调 |
| GET | `/api/oauth/github` | GitHub 登录 |
| GET | `/api/oauth/wechat` | 微信登录 |
| GET | `/api/oauth/telegram/login` | Telegram 登录 |
| POST | `/api/oauth/email/bind` | 邮箱绑定 |
| POST | `/api/user/passkey/login/begin` | Passkey 登录开始 |
| POST | `/api/user/passkey/login/finish` | Passkey 登录完成 |

---

## 四、前端路由结构

### 4.1 导航模块

站点使用**自定义 Section-based 路由系统**（非 React Router）。

**顶部导航 (HeaderNavModules)**:
```
├── 首页 (home)           - /
├── AI方案对比 (aiplanhub) - /aiplanhub (公开，无需登录)
├── 控制台 (console)       - /dashboard
├── 定价 (pricing)         - /pricing
├── 排行榜 (rankings)      - /rankings
├── 文档 (docs)            - 已禁用
└── 关于 (about)           - 已禁用
```

**侧边栏 (SidebarModulesAdmin)**:
```
├── 控制台 (console)
│   ├── 概览 (detail)
│   ├── 令牌 (token)       - Token 管理
│   └── 日志 (log)         - 请求日志
├── 个人中心 (personal)
│   ├── 充值 (topup)
│   └── 个人设置 (personal)
└── 管理 (admin)
    ├── 渠道 (channel)     - 上游渠道管理
    ├── 模型 (models)      - 模型元数据
    ├── 部署 (deployment)  - 模型部署
    ├── 兑换 (redemption)  - 兑换码
    ├── 用户 (user)        - 用户管理
    ├── 订阅 (subscription)- 订阅管理
    └── 设置 (setting)     - 系统设置
```

### 4.2 Dashboard 路由 (Section-based)

| Section ID | 标题 | 权限 |
|------------|------|------|
| `overview` | Overview | 所有用户 |
| `models` | Model Call Analytics | 所有用户 |
| `flow` | Flow | 所有用户 |
| `users` | User Analytics | 仅管理员 |

### 4.3 Models 路由

| Section ID | 标题 |
|------------|------|
| `metadata` | Metadata |
| `deployments` | Deployments |

### 4.4 系统设置 - 认证路由

| Section ID | 标题 |
|------------|------|
| `basic-auth` | Basic Authentication |
| `oauth` | OAuth Integrations |
| `passkey` | Passkey Authentication |
| `bot-protection` | Bot Protection |
| `custom-oauth` | Custom OAuth |

---

## 五、业务逻辑关键点

### 5.1 渠道 (Channel) 管理逻辑

- **渠道类型**: OpenAI、Azure、Anthropic、Google、DeepSeek、GLM、Dify、Midjourney-Proxy、Suno、自定义等
- **负载均衡**: 支持加权随机负载均衡
- **健康检查**: 自动检测渠道可用性，失败自动切换
- **多 Key 管理**: 一个渠道可配置多个 API Key，自动轮换
- **模型映射**: 将上游模型名映射为统一模型名

### 5.2 计费 (Billing) 逻辑

- **按量计费**: 根据 Token 消耗量计费
- **倍率系统**: 不同模型设置不同价格倍率
- **分组倍率**: 不同用户分组可设置不同倍率
- **缓存计费**: 命中缓存时可设置打折比例（如 50%）
- **按次收费**: 部分模型支持按次数收费
- **计费因子**: `倍率 × 分组倍率 × Token数量 / 配额单位`
- **配额单位**: 1 USD = 500,000 配额 (quota_per_unit)
- **汇率**: 1 USD = 7 CNY (可配置)
- **价格**: $7/500K tokens（当前定价）

### 5.3 订阅 (Subscription) 逻辑

- 用户可购买订阅套餐
- 套餐定义月配额额度、价格、有效期
- 支持自动续费（余额/Stripe/Creem 支付）
- 到期自动降级或暂停
- 管理员可手动绑定、重置订阅

### 5.4 充值 (TopUp) 逻辑

支持的支付渠道：
- **易支付**: 国内第三方支付（支付宝/微信）
- **Stripe**: 国际信用卡支付
- **Creem**: 国际支付
- **Waffo / Waffo-Pancake**: 加密货币支付

### 5.5 认证体系

| 认证方式 | 状态 |
|----------|------|
| 密码登录 | ✅ 已启用 |
| 密码注册 | ❌ 已关闭 |
| 邮箱验证 | ❌ 已关闭 |
| GitHub OAuth | ✅ 已启用 |
| LinuxDO OAuth | ✅ 已启用 (Trust Level ≥ 2) |
| Telegram OAuth | ❌ 未启用 |
| 微信登录 | ❌ 未启用 |
| OIDC 通用 | ❌ 未启用 |
| Discord | ❌ 未启用 |
| Passkey | ❌ 未启用 |
| Turnstile 验证 | ❌ 未启用 |

### 5.6 限流与安全

- **全局 API 限流** (`GlobalAPIRateLimit`)
- **模型级限流** (`ModelRequestRateLimit`)：可设置总请求数和成功请求数限制
- **关键操作限流** (`CriticalRateLimit`)：登录/注册/重置密码
- **匿名请求体大小限制** (`AnonymousRequestBodyLimit`)
- **Session Cookie Origin Guard**：防止 CSRF
- **用户会话限制**：每用户最多 50 个活跃会话

### 5.7 Token 认证流程

1. 客户端使用 `Authorization: Bearer {token}` 调用 `/v1/...`
2. 后端验证 Token 有效性、余额、权限
3. 根据智能路由选择最优渠道
4. 转发请求到上游，流式返回结果
5. 实时统计 Token 消耗并扣费

---

## 六、站点实际配置（从 /api/status 获取）

| 配置项 | 值 |
|--------|-----|
| 站点名称 | 幻境 MirageAI |
| 版本 | v1.0.0-rc.22 |
| 注册功能 | 开启（密码注册关闭，OAuth 可用） |
| 签到功能 | 关闭 |
| 自用模式 | 关闭 |
| 数据导出 | 开启 |
| 批量更新 | 关闭 |
| 任务系统 | 开启 |
| 画图功能 | 开启 |
| 配额显示方式 | USD |
| 货币单位 | 1 USD = 7 CNY |
| 基础价格 | $7 / 500K tokens |
| 公告系统 | 开启 |
| Uptime Kuma 监控 | 开启 |
| 演示站点 | 关闭 |

### 当前公告（2026-08-01）

1. "openai暗降额度，plus只有5-60刀额度，特价分组目前全是plus。暂时涨价到0.2x倍率。如果不是特别复制的问题，建议用terra或者luna"
2. "账号涨价严重，特价分组暂时改为0.2X"

---

## 七、前端技术细节

### 7.1 JS Bundle 分析

| Bundle | 大小 | 内容 |
|--------|------|------|
| `vendor-ui-primitives.b17b3046c5.js` | - | UI 基础库 (Radix/Headless UI) |
| `vendor-tanstack.74c48f25c5.js` | - | TanStack Query + Table |
| `lib-react.064bab1680.js` | - | React 核心库 |
| `4590.35f3f271c1.js` | ~782KB | 第三方库 (dayjs, markdown, react-aria) |
| `index.3be1001fd3.js` | ~384KB | 主应用代码 |
| CSS: `4590.10e003a7e2.css` | - | 第三方库样式 |
| CSS: `index.78c12a68e7.css` | ~408KB | 主应用样式 (Tailwind) |

### 7.2 关键前端技术

- **图表**: 使用自定义 Dashboard 组件（带数据导出功能）
- **编辑器**: 支持 Markdown 渲染（marked 库 + KaTeX 数学公式）
- **主题**: 支持 dark mode（通过 Tailwind dark: 语法）
- **国际化**: 5 种语言支持（简中、繁中、英、法、日）——框架已就位，翻译待完善
- **代码分割**: 大型页面组件通过 rspack code-splitting 异步加载

### 7.3 支持的客户端一键配置

平台内置了主流 AI 客户端的 Deep Link 配置：

| 客户端 | 协议格式 |
|--------|---------|
| Cherry Studio | `cherrystudio://providers/api-keys` |
| AionUI | `aionui://provider/add` |
| DeepChat | `deepchat://provider/install` |
| Lobe Chat | Web URL 参数 |
| AI as Workspace | Web URL 参数 |
| AMA 问天 | `ama://set-api-key` |
| OpenCat | `opencat://team/join` |
| 流畅阅读 | 浏览器插件 |
| CC Switch | 浏览器插件 |

---

## 八、数据部署要点

### 8.1 部署命令（Docker Compose）

```bash
git clone https://github.com/QuantumNous/new-api.git
cd new-api
# 编辑 docker-compose.yml 配置数据库
docker-compose up -d
# 访问 http://localhost:3000
```

### 8.2 关键环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `SQL_DSN` | 数据库连接串（SQLite 或 MySQL） | - |
| `SESSION_SECRET` | 会话密钥 | 随机生成 |
| `INITIAL_ROOT_TOKEN` | 初始管理员 Token | - |
| `STREAMING_TIMEOUT` | 流式响应超时（秒） | 120 |
| `FORCE_STREAM_OPTION` | 强制返回 usage 信息 | true |
| `GET_MEDIA_TOKEN` | 统计图片 token | true |
| `GENERATE_DEFAULT_TOKEN` | 新用户默认生成 Token | false |
| `FRONTEND_BASE_URL` | 前后端分离时的前端地址 | - |
| `TZ` | 时区 | Asia/Shanghai |

### 8.3 数据库

- 默认使用 SQLite（`one-api.db`）
- 可直接使用原版 One API 的数据库
- 也支持 MySQL / PostgreSQL

---

## 九、aiplanhub 页面 — AI 订阅方案对比（数据完全公开）

### 9.1 页面概述

`/aiplanhub` 是一个**完全公开**的 AI 订阅方案一站式对比页面，数据来源为开源仓库 [HsMirage/AIPlanHub](https://github.com/HsMirage/AIPlanHub)，**任何人无需登录即可查看全部数据**。

- **站点**: https://ai.hsnb.fun/aiplanhub
- **仓库**: https://github.com/HsMirage/AIPlanHub
- **数据更新**: 每日人工核实（最后更新 2026.08.01）
- **数据格式**: Markdown（README.md），网站直接渲染

### 9.2 页面功能

| 功能 | 说明 |
|------|------|
| 多分类对比 | Coding · Token · Video · Image · Audio 五大场景独立页面（Hash 路由） |
| 多维度筛选 + 排序 | 按价格、评分、平台等维度筛选 |
| 直达开通链接 | 每条方案附带官方开通链接，部分含邀请折扣 |
| 深色/亮色主题切换 | 全站支持 |
| 响应式布局 | 支持移动端浏览 |
| 价格对比 | Token 性价比专用对比页（2026.07.06 新增） |
| 已下架套餐归档 | 保留历史套餐数据供查档 |

### 9.3 Coding 平台对比（27 家）

#### 平台总览

| 平台 | 代表模型 | 方案数 | 月付起 | 评分 |
|------|----------|--------|--------|------|
| ChatGPT | GPT-5.4 / GPT-Image-2 / GPT-5.3-Codex | 2 | ¥26.6 | ★★★★★ |
| 商汤SenseNova | SenseNova 6.7 Flash-Lite / SenseNova U1 Fast | 1 | 免费 | ★★★★★ |
| 智谱AI | GLM-5.2 / GLM-5-Turbo / GLM-4.7 | 3 | ¥49 | ★ |
| 稳明光语纪 | GLM-5.2 / DeepSeek-V4-Flash | 5 | ¥29.9 | ★★★★ |
| 字节·方舟 | GLM-5.2 / Doubao-Seed-2.1-turbo / Kimi-K2.7 | 2 | ¥40 | ★★★★ |
| Charm Hyper | DeepSeek-V4-Flash / DeepSeek-V4-Pro / GLM-5.2 | 5 | $0 | ★★★½ |
| Meituan CatPaw | — | 1 | 免费 | ★★★★ |
| Kimi | Kimi-K3 / Kimi-K2.7-Code | 4 | ¥39 | ★★★ |
| 阿里·百炼 | Qwen3.6-Plus | 1 | ¥200 | ★★★ |
| 蓝耘元生代云 | GLM-5.1 | 3 | ¥49 | ★★★ |
| 腾讯·Coding | GLM-5 / Kimi-K2.5 / MiniMax-M2.5 | 2 | ¥40 | ★★★ |
| 百度·千帆 | GLM / DeepSeek / Kimi | 4 | ¥4.9 | ★★★ |
| 讯飞星辰 | GLM-5.2 / Spark X2 Agent / Kimi-K2.7-Code | 2 | ¥199 | ★★★ |
| 阶跃星辰 | Step-3.5-Flash-2603 | 4 | ¥49 | ★★★ |
| 快手 StreamLake | KAT-Coder-Pro V2.5 | 4 | ¥29 | ★★★ |
| Ollama | GLM-5.1 / DeepSeek-V4-Flash / MiniMax-M2.7 | 3 | $0 | ★★★ |
| AtomCode | GLM-5.2 / DeepSeek-V4-Flash | 3 | 免费 | ★★★ |
| z.ai | GLM-5.1（国际版） | 3 | $18 | ★ |
| MiniMax | MiniMax-M3 / M2.7 | 3 | ¥49 | ★★ |
| 联通云 | DeepSeek-V4-Pro / Kimi-K2.6 / Qwen3.6-27B | 2 | ¥40 | ★★ |
| TaoToken | GLM-5.2 | 3 | ¥39 | ★★ |
| 移动云 | MiniMax-M2.5 | 2 | ¥40 | ★★ |
| 国家超算互联网 | MiniMax-M2.5 / Qwen3-235B-A22B | 2 | ¥20 | ★★ |
| 优云智算 | GLM-5.2 / DeepSeek-V4-Pro / DeepSeek-V4-Flash / Qwen3.6-Plus / MiniMax-M2.7 / Kimi-K2.6 | 6 | ¥49 | ★★ |
| OpenStarry | GLM-5.2 / Kimi-K3 / DeepSeek-V4-Pro / MiniMax-M3 / Kimi-K2.7-Code / Qwen3.7-Max | 4(含免费) | ¥0(免费) | ★ |

#### 入门级（月付 ≤ ¥50）部分方案示例

| 平台 | 方案 | 月付 | 5h请求数 |
|------|------|------|----------|
| ChatGPT | Plus | ¥26.6 | — |
| 百度·千帆 | Mini | ¥4.9 | 1000万 Tokens/月 |
| 腾讯·Coding | Lite | ¥40（首月¥7.9） | 1,200 |
| 字节·方舟 | Lite | ¥40（首月¥9.9） | 1,200 |
| Kimi | Andante | ¥49（首月¥39） | — |
| 快手 StreamLake | Mini | ¥29 | 40 Prompts |
| 阶跃星辰 | Flash Mini | ¥49 | 1,500 |
| MiniMax | Plus | ¥49 | 1,500 |
| Meituan CatPaw | 免费版 | 免费 | — |

#### 高阶级（月付 ≥ ¥200）部分方案示例

| 平台 | 方案 | 月付 | 5h请求数 |
|------|------|------|----------|
| 阿里·百炼 | Pro | ¥200 | 6,000 |
| 腾讯·Coding | Pro | ¥200（首月¥39.9） | 6,000 |
| MiniMax | Ultra | ¥469 | 15,000 |
| 阶跃星辰 | Flash Max | ¥699 | 75,000 |
| Kimi | Allegro | ¥699 | — |
| 百度·千帆 | Max | ¥299.9 | 7亿 Tokens/月 |

### 9.4 Token 平台对比（9 家）

| 平台 | 代表模型 | 方案数 | 月付起 | 评分 |
|------|----------|--------|--------|------|
| ChatGPT | GPT-5.4 / GPT-Image-2 / GPT-5.3-Codex | 1 | ¥28.8 | ★★★★★ |
| OpenCode Go | GLM-5.2 / GPT-5.6-Luna / DeepSeek-V4-Pro / Kimi-K2.6 | 1 | $10 | ★★★★ |
| 阿里·Token Plan | qwen3.8-max-preview / Qwen3.7-Max / DeepSeek-V4-Pro / GLM-5.2 / Kimi-K2.6 | 7 | ¥39 | ★★★ |
| TaoToken | DeepSeek-V4-Pro / Kimi-K3 / GLM-5.2 | 3 | ¥59 | ★★ |
| 方舟 Agent Plan | DeepSeek-V4-Pro / GLM-5.1 / Kimi-K2.6 | 4 | ¥40 | ★★ |
| 腾讯·Token | Auto / DeepSeek-V4-Flash/Pro / GLM-5.1 / Kimi-K2.5 / Hy3 / Hy3 preview | 8 | ¥28 | ★ |
| 天翼云·Token | GLM-5 / DeepSeek-V3.2 | 5 | ¥29 | ★ |
| Alaya Code | GLM-5.2 / GLM-5.1 / DeepSeek-V4-Flash | 3 | ¥199 | ★ |
| 小米·MiMo | MiMo-V2.5-Pro / MiMo-V2.5 | 4 | ¥39 | ★ |

> Token 平台的关键区别：每家 Credits/Token 计算方式不同，有些平台的高阶模型按 2-4 倍抵扣额度。

### 9.5 Video 平台对比（8 家）

| 平台 | 方案数 | 月付起 | 核心模型 | 评分 |
|------|--------|--------|----------|------|
| 快手可灵 | 5 | ¥0 | Kling 3.0 Omni | ★★★★★ |
| Vidu | 4 | ¥0 | Vidu | ★★★★ |
| 海螺AI | 5 | ¥55/月(年付) | Hailuo 2.3·Seedance 2.0 | ★★★★ |
| pai.video | 5 | ¥0 | PixVerse | ★★★★ |
| 即梦 | 5 | ¥0 | Seedance 2.0·2.0 Mini | ★★★★ |
| 通义万相 | 3 | ¥0 | 万相 2.6 | ★★★★ |
| RunningHub | 10 | ¥29 | 云端ComfyUI | ★★★ |
| 腾讯混元 | 4 | — | 混元视频(API) | ★★★ |

### 9.6 Image 平台对比（6 家）

| 平台 | 方案数 | 月付起 | 核心模型 | 评分 |
|------|--------|--------|----------|------|
| 即梦 | 4 | ¥69 | Seedance 2.0 | ★★★★★ |
| Midjourney | 4 | ¥70($10) | MJ V7 | ★★★★★ |
| Liblib AI | 6 | ¥429/年 | WebUI/ComfyUI/Kling/Seedream | ★★★★★ |
| 通义万相 | 3 | ¥72 | 万相 2.6 | ★★★★ |
| RunningHub | 10 | ¥29 | 云端ComfyUI | ★★★ |
| 堆友 | 1 | ¥399/年 | 国风/设计 | ★★★ |

### 9.7 Audio 平台对比（4 家）

| 平台 | 方案数 | 月付起 | 核心模型 | 评分 |
|------|--------|--------|----------|------|
| Suno | 3 | ¥0 | v5.5 | ★★★★★ |
| Udio | 3 | ¥0 | Udio | ★★★★ |
| Ace Studio | 2 | —/年付 | AI歌声合成 | ★★★ |
| 海螺AI | 5 | ¥0 | Music 2.6 / Speech 2.8 | ★★★ |

### 9.8 中转站（API 中继，1 家）

| 平台 | 代表模型 | 计费方式 | 特点 | 评分 |
|------|----------|----------|------|------|
| 幻境MirageAI | gpt-5.4 / deepseek-v4-pro / gemini-2.5-flash / agnes-2.0-flash 等 37 款 | 按量计费·充值制 | 半公益中转·New API 统一协议·pay.ldxp.cn 充值 | ★★★★ |

### 9.9 关键警告与提醒（原文收录）

- **z.ai**: 2026.04.11 价格暴涨，月付涨至 $18/$72/$160，性价比明显下降
- **智谱AI**: 新版积分制价格大幅上调，Lite ¥118/Pro ¥538/Max ¥1078，性价比差，降为 1 星
- **字节·方舟**: 双层计费——名义按调用次数，实际 Token 消耗大会被按 2-3 次扣费，计费不透明
- **天翼云**: 高阶 GLM 模型高峰期按 3 倍抵扣额度
- **京东云**: Coding Plan 已于 2026.07.29 停止新购
- **联通云**: 资源紧张，GLM-5.1 慢+429限流，禁止 API 调用
- **移动云**: GLM-5.1 按 4x 抵扣，同样禁止 API 调用

### 9.10 数据架构

这个页面的数据流非常简单：

```
HsMirage/AIPlanHub (GitHub)
    └── README.md (Markdown 数据源, 318 行)
         └── 网站 /aiplanhub 直接渲染 (Hash 路由)
              ├── #home    → 首页概览
              ├── #coding  → Coding 平台对比
              ├── #token   → Token 平台对比
              ├── #video   → 视频平台对比
              ├── #image   → 图片平台对比
              ├── #audio   → 音频平台对比
              └── #compare → 价格/Token 效率对比
```

说明：网站可能将 README.md 作为静态资源加载，也可能预先编译为 JSON 数据；无论哪种方式，**数据来源都是 GitHub 上的公开 README**，完全不涉及后端 API 认证。

---

## 十、开发同类型网站的核心要点

如果开发类似网站，需要实现以下核心功能模块：

### 必选功能
1. ✅ **API 中继引擎**: 将上游 API 转为 OpenAI 格式，支持流式响应
2. ✅ **多租户管理**: 用户注册、Token 管理、配额控制
3. ✅ **渠道管理**: 上游 API Key 池化管理、负载均衡、健康检查
4. ✅ **计费系统**: Token 消耗统计、模型定价、倍率系统
5. ✅ **充值系统**: 至少接入一种支付方式
6. ✅ **日志系统**: 请求日志、消费明细、异常监控

### 进阶功能
7. 🔧 **订阅套餐**: 灵活定义月/年套餐
8. 🔧 **数据看板**: Token 消耗趋势、用户分析
9. 🔧 **OAuth 登录**: GitHub/微信/Telegram 等第三方登录
10. 🔧 **模型管理**: 上游模型同步、自定义模型映射
11. 🔧 **异步任务**: Midjourney/Suno 等非流式任务支持
12. 🔧 **CDN 加速**: EdgeOne + Cloudflare 双线部署

### 法律合规注意事项
- 需完成**算法备案**
- 需取得 **ICP 许可证**
- 需取得 **EDI 许可证**（在线数据处理与交易处理）
- 在中国境内提供生成式 AI 服务需完成备案
- 不得未经授权转售境外 AI 平台服务

---

## 附录：API 接口总数统计

| 分类 | 接口数量 |
|------|----------|
| Relay 中继接口 | ~30+ |
| 管理后台 - 公开 | ~12 |
| 管理后台 - 用户 | ~50 |
| 管理后台 - 管理员 | ~35 |
| 管理后台 - Root | ~20 |
| 支付回调 | ~6 |
| OAuth 认证 | ~10 |
| **总计** | **~163** |

---

> 本文档基于对 ai.hsnb.fun 网站的公开信息抓取和开源项目 QuantumNous/new-api 的代码分析整理。数据仅供参考，以官方实际为准。
