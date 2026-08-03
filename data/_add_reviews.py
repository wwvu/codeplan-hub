#!/usr/bin/env python3
"""给 providers.json 添加 AIPlanHub 的点评(review)数据"""
import json

REVIEWS = {
    # === Coding 平台 ===
    "coding-chatgpt": "OpenAI 官方，GPT-5.4/Codex/Image-2 全覆盖。Plus 月付 ¥26.6（走幻境代付渠道，非官方原价）",
    "coding-sensenova": "商汤自研 SenseNova 6.7 Flash-Lite / U1 Fast，免费公测中，性价比极高，编程体验优秀",
    "coding-zhipu": "⚠️ 新版积分制价格大幅上调：Lite ¥118 / Pro ¥538 / Max ¥1078；MCP 与模型共享额度，OpenClaw 采用次级调度，当前性价比很差",
    "coding-wenming": "AI 应用商城转售，GLM-5.2 + DeepSeek-V4-Flash 双线并行，按次和按 token 两种套餐可切换，新用户 ¥29.9 活动价有竞争力",
    "coding-bytedance": "⚠️ 双层计费：名义按调用次数，实际 Token 消耗大会被按 2-3 次甚至更多次扣费，计费不透明，无用量明细（蓝点网/V2EX/微博多源证实）",
    "coding-charm": "海外聚合平台，含免费档和 Bundle 充值，$0/$5/$10/$20 多档，适合美元结算用户",
    "coding-meituan": "美团出品，免费版需下载客户端，公司内部接入较方便",
    "coding-kimi": "月之暗面四档方案（Andante/Moderato/Allegretto/Allegro），网友反馈额度消耗较快，¥39 起",
    "coding-aliyun": "Pro 专属 Qwen3.6-Plus，Pro 固定 ¥200/月，每周 45,000 次请求，模型单一但稳定",
    "coding-lanyun": "高峰与非高峰差异化扣额，GLM-5.1 没有 429 限流但调用速度较慢，¥49 起三档",
    "coding-tencent": "腾讯云出品，GLM-5/Kimi-K2.5/MiniMax-M2.5 三模型，首月 ¥7.9 优惠价吸引新用户",
    "coding-baidu": "百度千帆，GLM/DeepSeek/Kimi 全系，¥4.9 起四档，按 Token 量计费而非按次",
    "coding-iflytek": "讯飞星辰平台，GLM-5.2/Spark X2 Agent/Kimi-K2.7-Code，高效版 ¥199 起",
    "coding-jieyue": "阶跃星辰自研 Step-3.5-Flash-2603，四档从 ¥49 到 ¥699，低端性价比不错",
    "coding-kuaishou": "快手 StreamLake 平台，KAT-Coder-Pro V2.5，按 Prompts 计费（非标准 Token），¥29 起四档",
    "coding-ollama": "开源本地部署平台，GLM-5.1/DeepSeek-V4-Flash/MiniMax-M2.7，免费档适合自建",
    "coding-atomcode": "GLM-5.2/DeepSeek-V4-Flash，三档含免费，起步门槛低",
    "coding-zai": "⚠️ GLM-5.1 国际版，2026.04.11 价格暴涨：月付涨至 $18 / $72 / $160，美元计费后性价比明显下降",
    "coding-minimax": "2026.06.01 全面升级 M3 体系，Plus ¥49/Max ¥119/Ultra ¥469 三档（年付立省2月），M2.7 参考 1500/4500/15000 次/5h，月 6~55 亿 token",
    "coding-liantong": "⚠️ 当前资源紧张 GLM-5.1 很慢 + 429 限流；支持 DeepSeek-V4 全系列；测试发现多数模型调用工具有问题，默认关闭思考模式；没有异常扣费挺耐用；禁止 API 调用",
    "coding-taotoken": "GLM-5.2 为主，Lite/Pro/Max 三档，¥39 起，聚合平台性价比一般",
    "coding-yidong": "⚠️ 已支持 MiniMax-M2.5 与 GLM-5.1；GLM-5.1 按 4x 抵扣额度消耗更快；支持华北-呼和浩特/湖北-武汉/华南-广州资源池；Coding Plan 禁止 API 调用",
    "coding-supercomp": "国家超算互联网平台，MiniMax-M2.5/Qwen3-235B，¥20 起 Lite/Pro 双档，性价比突出",
    "coding-youyun": "模型最多：GLM-5.2/DeepSeek-V4-Pro/Flash/Qwen3.6-Plus/MiniMax-M2.7/Kimi-K2.6 全系，¥49 起六档",
    "coding-openstarry": "含免费档，模型覆盖广（GLM/Kimi/DeepSeek/MiniMax/Qwen），但评分最低，稳定性存疑",
    "coding-opencode": "OpenCode Go 平台，Grok-4.5/GLM-5.2/GPT-5.6-Luna/Kimi-K3/Hy3 等 17 款模型，$10/月起，按量计费",
    "coding-jdcloud": "⚠️ Coding Plan 已于 2026.07.29 停止新购、续费及升级；已购套餐有效期内可用，历史套餐见站内「已下架」页面",

    # === Token 平台 ===
    "token-chatgpt": "OpenAI 官方 Token 方案，GPT-5.4/Image-2/Codex，¥28.8/月，暂时售罄",
    "token-opencode": "OpenCode Go，GLM-5.2/GPT-5.6-Luna/DeepSeek-V4-Pro/Kimi-K2.6 等 17 款，$10/月起",
    "token-aliyun": "按坐席订阅，qwen3.8-max/Qwen3.7-Max/DeepSeek-V4-Pro/GLM-5.2/Kimi-K2.6，Credits 统一计量，不支持退款；标准坐席 ¥150 限时 10 倍加量，尊享坐席 ¥1,398",
    "token-taotoken": "DeepSeek-V4-Pro/Kimi-K3/GLM-5.2，¥59 起按 Credits 计费，三档含加油包",
    "token-fangzhou": "AFP 积分制，覆盖文本/向量/图像/视频与联网搜索 Harness，兼容编程和 Agent 工具，¥40 起四档",
    "token-tencent": "⚠️ 仅限 AI 工具（Cursor/Claude Code 等）使用，禁止 API 调用（违者封禁）；暂不支持多模态；8 档方案 ¥28 起，但无公开用量计算器透明度差",
    "token-tianyi": "⚠️ 高阶 GLM 模型在高峰期按 3 倍、非高峰期按 2 倍抵扣额度，实际可用量明显低于表面档位；当前页面长期显示售罄/补货",
    "token-alaya": "Alaya Code，GLM-5.2/GLM-5.1/DeepSeek-V4-Flash，¥199 起三档",
    "token-xiaomi": "⚠️ Credit ≠ Token！MiMo-V2.5-Pro 输入/输出按 300/600 Credits 抵扣，属于 Token Plan 不进入 Coding 请求数表；¥39 起四档",

    # === Video 平台 ===
    "video-kling": "快手可灵 Kling 3.0 Omni，国产视频生成标杆，五档含免费",
    "video-vidu": "Vidu 视频生成，四档含免费，效果好但额度消耗快",
    "video-hailuo": "海螺AI，Hailuo 2.3/Seedance 2.0 双引擎，年付 ¥55/月起",
    "video-paivideo": "PixVerse 平台，五档含免费",
    "video-jimeng": "字节即梦，Seedance 2.0/2.0 Mini 双引擎，季度首购价优惠",
    "video-tongyi": "阿里通义万相 2.6，三档含免费",
    "video-runninghub": "云端 ComfyUI 工作流平台，10 档方案，团队优惠/进阶版月价下调",
    "video-hunyuan": "腾讯混元视频 API，四档方案",

    # === Image 平台 ===
    "image-jimeng": "字节即梦 Seedance 2.0，¥69/月起四档",
    "image-midjourney": "MJ V7，$10/月起（≈¥70），Cloudflare 拦截严重但 Zendesk API 可确认价格",
    "image-liblib": "Liblib AI，WebUI/ComfyUI/Kling/Seedream 多引擎，年付 ¥429/年起，新增 Seedance 2.5 预售限时赠送",
    "image-tongyi": "阿里通义万相 2.6，¥72/月起三档",
    "image-runninghub": "云端 ComfyUI 工作流平台",
    "image-duiyou": "堆友，国风/设计风格，年付 ¥399/年起",

    # === Audio 平台 ===
    "audio-suno": "Suno v5.5 AI 音乐生成，三档含免费，口碑最好的 AI 音乐平台",
    "audio-udio": "Udio AI 音乐生成，三档含免费",
    "audio-acestudio": "Ace Studio AI 歌声合成，年付制",
    "audio-hailuo": "海螺AI，Music 2.6/Speech 2.8 双引擎，五档含免费",

    # === 中转站 ===
    "relay-mirage": "gpt-5.4/deepseek-v4-pro/gemini-2.5-flash/agnes-2.0-flash 等 37 款模型，按量充值半公益中转站，基于 New API 统一协议，pay.ldxp.cn 充值",
}

with open('providers.json', 'r') as f:
    providers = json.load(f)

updated = 0
for p in providers:
    if p['id'] in REVIEWS:
        p['review'] = REVIEWS[p['id']]
        updated += 1
    else:
        p['review'] = ''  # 空字符串表示无特殊点评

with open('providers.json', 'w') as f:
    json.dump(providers, f, ensure_ascii=False, indent=2)

print(f'Updated {updated}/{len(providers)} providers with review data')
print('Done.')
