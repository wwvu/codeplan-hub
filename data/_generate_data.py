#!/usr/bin/env python3
"""从 AIPlanHub README 数据生成 providers.json 和 plans.json"""
import json, re
from pathlib import Path

# 所有读写都基于本脚本所在目录（data/），不依赖 CWD
BASE_DIR = Path(__file__).resolve().parent

# ============ Providers ============
PROVIDERS = [
    # ---- Coding 编程 (27) ----
    {"id": "coding-chatgpt", "category": "coding", "name": "ChatGPT", "type": "vendor", "url": "https://openai.com/chatgpt/pricing/", "blurb": "OpenAI 官方 AI 编程平台，GPT-5.4/Codex/Image-2 多模态全覆盖", "rating": 5.0, "headline": "$20/月起 · Plus/Team 双档", "tags": ["多模态", "Coding", "图片生成"], "asOf": "2026-07-31"},
    {"id": "coding-sensenova", "category": "coding", "name": "商汤SenseNova", "type": "vendor", "url": "https://www.sensenova.cn/token-plan", "blurb": "商汤自研 SenseNova 6.7 Flash-Lite / U1 Fast，免费公测中", "rating": 5.0, "headline": "免费公测 · 1500次/5h", "tags": ["免费", "自研模型"], "asOf": "2026-07-31"},
    {"id": "coding-zhipu", "category": "coding", "name": "智谱AI", "type": "vendor", "url": "https://www.bigmodel.cn/invite?icode=naEahtDGpOp7hfCi6MPFVunfet45IvM%2BqDogImfeLyI%3D", "blurb": "GLM-5.2/GLM-5-Turbo/GLM-4.7 三档方案，新版积分制价格大幅上调，性价比差", "rating": 1.0, "headline": "¥49起 · 积分制大涨价", "tags": ["GLM", "积分制", "涨价"], "asOf": "2026-07-31"},
    {"id": "coding-wenming", "category": "coding", "name": "稳明光语纪", "type": "aggregator", "url": "https://wenming7.cn/sales?ref=6FRFQW2D", "blurb": "AI 应用商城，转售 GLM-5.2 / DeepSeek-V4-Flash，按次与按 token 两种套餐并行", "rating": 4.0, "headline": "¥29.9 起 · 5000 万 token 限时", "tags": ["按次", "按 token", "新用户低价"], "featured": True, "asOf": "2026-07-31"},
    {"id": "coding-bytedance", "category": "coding", "name": "字节·方舟", "type": "vendor", "url": "https://volcengine.com/L/RYnDeTYySYQ/", "blurb": "GLM-5.2 / Doubao-Seed-2.1-turbo / Kimi-K2.7，双层计费不透明", "rating": 4.0, "headline": "¥40/月起 · 计费不透明", "tags": ["双层计费", "Doubao", "不透明"], "asOf": "2026-07-31"},
    {"id": "coding-charm", "category": "coding", "name": "Charm Hyper", "type": "aggregator", "url": "https://hyper.charm.land/", "blurb": "DeepSeek-V4-Flash/Pro + GLM-5.2，含免费档和Bundle充值", "rating": 3.5, "headline": "$0 起 · 美元计费", "tags": ["免费档", "Bundle充值", "美元"], "asOf": "2026-07-31"},
    {"id": "coding-meituan", "category": "coding", "name": "Meituan CatPaw", "type": "vendor", "url": "https://catpaw.meituan.com/", "blurb": "美团出品，Coding Plan 免费版，需下载客户端", "rating": 4.0, "headline": "免费 · 需下载客户端", "tags": ["免费", "美团"], "asOf": "2026-07-31"},
    {"id": "coding-kimi", "category": "coding", "name": "Kimi", "type": "vendor", "url": "https://kimi-bot.com/activities/zh-cn/invite/share?scenario=invite&from=share_poster&invitation_code=22K28A", "blurb": "月之暗面，Kimi-K3/K2.7-Code，四档方案，额度消耗较快", "rating": 3.0, "headline": "¥39/月起 · 四档方案", "tags": ["Kimi", "Coding"], "asOf": "2026-07-31"},
    {"id": "coding-aliyun", "category": "coding", "name": "阿里·百炼", "type": "vendor", "url": "https://bailian.console.aliyun.com/", "blurb": "Qwen3.6-Plus 专属，每周 45,000 次请求，Pro 固定 ¥200/月", "rating": 3.0, "headline": "¥200/月 · Qwen3.6-Plus", "tags": ["Qwen", "按量"], "asOf": "2026-07-31"},
    {"id": "coding-lanyun", "category": "coding", "name": "蓝耘元生代云", "type": "aggregator", "url": "https://console.lanyun.net/#/register", "blurb": "GLM-5.1 三档方案，高峰/非高峰差异化扣额，调用速度较慢", "rating": 3.0, "headline": "¥49起 · 差异化扣额", "tags": ["GLM", "差异化扣额", "高峰期限流"], "asOf": "2026-07-31"},
    {"id": "coding-tencent", "category": "coding", "name": "腾讯·Coding", "type": "vendor", "url": "https://console.cloud.tencent.cn/tokenhub/codingplan?regionId=1", "blurb": "GLM-5 / Kimi-K2.5 / MiniMax-M2.5，Lite/Pro 双档", "rating": 3.0, "headline": "¥40/月起 · 首月¥7.9", "tags": ["GLM", "Kimi", "MiniMax"], "asOf": "2026-07-31"},
    {"id": "coding-baidu", "category": "coding", "name": "百度·千帆", "type": "vendor", "url": "https://cloud.baidu.com/product/codingplan.html", "blurb": "GLM / DeepSeek / Kimi，四档方案，按 Token 计费", "rating": 3.0, "headline": "¥4.9/月起 · Token 计费", "tags": ["GLM", "DeepSeek", "Kimi", "Token计费"], "asOf": "2026-07-31"},
    {"id": "coding-iflytek", "category": "coding", "name": "讯飞星辰", "type": "vendor", "url": "https://maas.xfyun.cn/packageSubscription", "blurb": "GLM-5.2 / Spark X2 Agent / Kimi-K2.7-Code，高效/速通双档", "rating": 3.0, "headline": "¥199/月起 · Spark赋能", "tags": ["Spark", "GLM", "Kimi"], "asOf": "2026-07-31"},
    {"id": "coding-jieyue", "category": "coding", "name": "阶跃星辰", "type": "vendor", "url": "https://platform.stepfun.com", "blurb": "Step-3.5-Flash-2603，四档方案 (Mini/Plus/Pro/Max)", "rating": 3.0, "headline": "¥49/月起 · 四档定价", "tags": ["Step", "四档"], "asOf": "2026-07-31"},
    {"id": "coding-kuaishou", "category": "coding", "name": "快手StreamLake", "type": "vendor", "url": "https://www.streamlake.com/marketing/coding-plan", "blurb": "KAT-Coder-Pro V2.5，四档方案，按 Prompts 计费", "rating": 3.0, "headline": "¥29/月起 · 按Prompts计", "tags": ["KAT", "Prompts计费"], "asOf": "2026-07-31"},
    {"id": "coding-ollama", "category": "coding", "name": "Ollama", "type": "vendor", "url": "https://ollama.com/pricing", "blurb": "GLM-5.1 / DeepSeek-V4-Flash / MiniMax-M2.7，含免费档", "rating": 3.0, "headline": "$0起 · 本地部署友好", "tags": ["免费", "本地部署"], "asOf": "2026-07-31"},
    {"id": "coding-atomcode", "category": "coding", "name": "AtomCode", "type": "aggregator", "url": "", "blurb": "GLM-5.2 / DeepSeek-V4-Flash，三档方案含免费", "rating": 3.0, "headline": "免费起 · 三档", "tags": ["免费", "GLM", "DeepSeek"], "asOf": "2026-07-31"},
    {"id": "coding-zai", "category": "coding", "name": "z.ai", "type": "aggregator", "url": "https://z.ai/subscribe", "blurb": "GLM-5.1 国际版，2026.04.11 价格暴涨，美元计费后性价比明显下降", "rating": 1.0, "headline": "$18/月起 · 暴涨", "tags": ["GLM国际版", "美元", "涨价"], "asOf": "2026-07-31"},
    {"id": "coding-minimax", "category": "coding", "name": "MiniMax", "type": "vendor", "url": "https://platform.minimaxi.com/subscribe/token-plan", "blurb": "M3 体系：Plus/Max/Ultra 三档，2026.06.01 全面升级", "rating": 2.0, "headline": "¥49/月起 · M3体系", "tags": ["MiniMax", "M3"], "asOf": "2026-07-31"},
    {"id": "coding-liantong", "category": "coding", "name": "联通云", "type": "vendor", "url": "https://support.cucloud.cn/document/127/591/2357.html?id=2357&arcid=7015", "blurb": "DeepSeek-V4-Pro / Kimi-K2.6 / Qwen3.6-27B，资源紧张、429限流", "rating": 2.0, "headline": "¥40/月起 · 资源紧张", "tags": ["资源紧张", "429限流", "禁止API"], "asOf": "2026-07-31"},
    {"id": "coding-taotoken", "category": "coding", "name": "TaoToken", "type": "aggregator", "url": "https://taotoken.net/", "blurb": "GLM-5.2，三档方案（Lite/Pro/Max）", "rating": 2.0, "headline": "¥39/月起 · 三档", "tags": ["GLM"], "asOf": "2026-07-31"},
    {"id": "coding-yidong", "category": "coding", "name": "移动云", "type": "vendor", "url": "https://ecloud.10086.cn/portal/act/codingplan", "blurb": "MiniMax-M2.5，两档方案，GLM-5.1 按 4x 抵扣", "rating": 2.0, "headline": "¥40/月起 · GLM 4x抵扣", "tags": ["MiniMax", "4x抵扣", "禁止API"], "asOf": "2026-07-31"},
    {"id": "coding-supercomp", "category": "coding", "name": "国家超算互联网", "type": "vendor", "url": "https://www.scnet.cn/ac/openapi/doc/2.0/moduleapi/codingplan/subscriptionnotice.html", "blurb": "MiniMax-M2.5 / Qwen3-235B-A22B，Lite/Pro 双档", "rating": 2.0, "headline": "¥20/月起 · 双档", "tags": ["MiniMax", "Qwen"], "asOf": "2026-07-31"},
    {"id": "coding-youyun", "category": "coding", "name": "优云智算", "type": "aggregator", "url": "https://passport.compshare.cn/register", "blurb": "GLM-5.2 / DeepSeek-V4-Pro / DeepSeek-V4-Flash / Qwen3.6-Plus / MiniMax-M2.7 / Kimi-K2.6，六档方案", "rating": 2.0, "headline": "¥49/月起 · 六档", "tags": ["GLM", "DeepSeek", "Qwen", "MiniMax", "Kimi"], "asOf": "2026-07-31"},
    {"id": "coding-openstarry", "category": "coding", "name": "OpenStarry", "type": "aggregator", "url": "https://api.openstarry.com/auth?mode=register&aff=X6K8", "blurb": "GLM-5.2 / Kimi-K3 / DeepSeek-V4-Pro / MiniMax-M3 / Kimi-K2.7-Code / Qwen3.7-Max，含免费档", "rating": 1.0, "headline": "免费起 · 含免费档", "tags": ["免费", "GLM", "DeepSeek", "Kimi", "Qwen"], "asOf": "2026-07-31"},
    {"id": "coding-opencode", "category": "coding", "name": "OpenCode Go", "type": "aggregator", "url": "https://opencode.ai/", "blurb": "Grok-4.5 / GLM-5.2 / GPT-5.6-Luna / Kimi-K3 / Hy3 等17款模型，按量计费", "rating": 4.0, "headline": "$10/月起 · 17款模型", "tags": ["多模型", "美元", "Grok"], "asOf": "2026-07-31", "featured": True},
    {"id": "coding-xkiro", "category": "coding", "name": "xKiro", "type": "aggregator", "url": "https://xkiro.com/ref/3Y9VZSF", "blurb": "AI 路由聚合平台，50+ 模型 / 6 供应商 / 1 API key，OpenAI & Anthropic SDK 兼容，比直连省 50–70%", "rating": 4.5, "headline": "$0 起 · 6 档 · 年付 -20%", "tags": ["多模型", "美元", "路由聚合"], "featured": False, "asOf": "2026-08-06"},
    {"id": "discontinued-jdcloud", "category": "discontinued", "name": "京东云（已下架）", "type": "vendor", "url": "", "blurb": "Coding Plan 已于2026.07.29停止新购、续费及升级；已购套餐有效期内可用", "rating": 1.0, "headline": "已下架 · 仅存量可用", "tags": ["已下架"], "asOf": "2026-07-31"},

    # ---- Token 平台 (9) ----
    {"id": "token-chatgpt", "category": "token", "name": "ChatGPT", "type": "vendor", "url": "https://openai.com/chatgpt/pricing/", "blurb": "GPT-5.4 / GPT-Image-2 / GPT-5.3-Codex，Token 方案暂时售罄", "rating": 5.0, "headline": "$100 · 暂时售罄", "tags": ["Token", "暂时售罄"], "asOf": "2026-08-01"},
    {"id": "token-opencode", "category": "token", "name": "OpenCode Go", "type": "aggregator", "url": "https://opencode.ai/", "blurb": "GLM-5.2 / GPT-5.6-Luna / DeepSeek-V4-Pro / Kimi-K2.6，17款模型按量计费", "rating": 4.0, "headline": "$10/月起 · 17款模型", "tags": ["多模型", "美元", "按量"], "asOf": "2026-08-01"},
    {"id": "token-aliyun", "category": "token", "name": "阿里·Token Plan", "type": "vendor", "url": "https://common-buy.aliyun.com/token-plan", "blurb": "qwen3.8-max-preview / Qwen3.7-Max / DeepSeek-V4-Pro / GLM-5.2 / Kimi-K2.6，7档坐席制", "rating": 3.0, "headline": "¥150/月起 · 坐席制", "tags": ["坐席制", "多模型", "按 Credits"], "asOf": "2026-08-01"},
    {"id": "token-taotoken", "category": "token", "name": "TaoToken", "type": "aggregator", "url": "https://taotoken.net/", "blurb": "DeepSeek-V4-Pro / Kimi-K3 / GLM-5.2，三档方案含加油包", "rating": 2.0, "headline": "¥59/月起 · 按 Credits", "tags": ["Credits", "GLM", "DeepSeek", "Kimi"], "asOf": "2026-08-01"},
    {"id": "token-fangzhou", "category": "token", "name": "方舟 Agent Plan", "type": "vendor", "url": "https://www.volcengine.com/docs/82379/2366394?lang=zh", "blurb": "DeepSeek-V4-Pro / GLM-5.1 / Kimi-K2.6，AFP 积分制四档", "rating": 2.0, "headline": "¥40/月起 · AFP积分制", "tags": ["AFP", "积分制", "四档"], "asOf": "2026-08-01"},
    {"id": "token-tencent", "category": "token", "name": "腾讯·Token", "type": "vendor", "url": "https://console.cloud.tencent.cn/tokenhub/", "blurb": "Auto / DeepSeek-V4-Flash/Pro / GLM-5.1 / Kimi-K2.5 / Hy3 / Hy3 preview，8档方案", "rating": 1.0, "headline": "¥28/月起 · 8档方案", "tags": ["多模型", "8档", "禁止API"], "asOf": "2026-08-01"},
    {"id": "token-tianyi", "category": "token", "name": "天翼云·Token", "type": "vendor", "url": "https://www.ctyun.cn/act/AI/zhuanxiang", "blurb": "GLM-5 / DeepSeek-V3.2，5档方案，高阶模型高峰期3倍抵扣", "rating": 1.0, "headline": "¥29/月起 · 高峰期3x抵扣", "tags": ["GLM", "DeepSeek", "3x抵扣"], "asOf": "2026-08-01"},
    {"id": "token-alaya", "category": "token", "name": "Alaya Code", "type": "aggregator", "url": "https://codingplan.alayanew.com/docs/billing", "blurb": "GLM-5.2 / GLM-5.1 / DeepSeek-V4-Flash，三档方案", "rating": 1.0, "headline": "¥199/月起 · 三档", "tags": ["GLM", "DeepSeek"], "asOf": "2026-08-01"},
    {"id": "token-xiaomi", "category": "token", "name": "小米·MiMo", "type": "vendor", "url": "https://platform.xiaomimimo.com/#/token-plan", "blurb": "MiMo-V2.5-Pro / MiMo-V2.5，四档方案，Credit ≠ Token", "rating": 1.0, "headline": "¥39/月起 · Credit 倍率", "tags": ["MiMo", "Credit≠Token", "四档"], "asOf": "2026-08-01"},

    # ---- Video (8) ----
    {"id": "video-kling", "category": "video", "name": "快手可灵", "type": "vendor", "url": "https://kling.kuaishou.com/", "blurb": "Kling 3.0 Omni，五档方案含免费档，国产视频生成标杆", "rating": 5.0, "headline": "¥0起 · 5档方案", "tags": ["Kling", "免费档", "视频生成"], "asOf": "2026-08-01"},
    {"id": "video-vidu", "category": "video", "name": "Vidu", "type": "vendor", "url": "https://www.vidu.com/", "blurb": "Vidu 视频生成平台，四档方案含免费档", "rating": 4.0, "headline": "¥0起 · 4档方案", "tags": ["Vidu", "免费档"], "asOf": "2026-08-01"},
    {"id": "video-hailuo", "category": "video", "name": "海螺AI", "type": "vendor", "url": "https://hailuo.ai/", "blurb": "Hailuo 2.3 / Seedance 2.0，五档方案，年付¥55/月起", "rating": 4.0, "headline": "¥55/月起(年付) · 5档", "tags": ["Hailuo", "Seedance", "年付优惠"], "asOf": "2026-08-01"},
    {"id": "video-paivideo", "category": "video", "name": "pai.video", "type": "vendor", "url": "https://pai.video/", "blurb": "PixVerse 视频生成平台，五档方案含免费档", "rating": 4.0, "headline": "¥0起 · 5档方案", "tags": ["PixVerse", "免费档"], "asOf": "2026-08-01"},
    {"id": "video-jimeng", "category": "video", "name": "即梦", "type": "vendor", "url": "https://jimeng.jianying.com/", "blurb": "Seedance 2.0 / 2.0 Mini，五档方案含免费档，字节旗下", "rating": 4.0, "headline": "¥0起 · 5档方案", "tags": ["Seedance", "免费档", "字节"], "asOf": "2026-08-01"},
    {"id": "video-tongyi", "category": "video", "name": "通义万相", "type": "vendor", "url": "https://tongyi.aliyun.com/wanxiang/", "blurb": "万相 2.6，三档方案含免费档，阿里系", "rating": 4.0, "headline": "¥0起 · 3档方案", "tags": ["万相", "免费档", "阿里"], "asOf": "2026-08-01"},
    {"id": "video-runninghub", "category": "video", "name": "RunningHub", "type": "aggregator", "url": "https://www.runninghub.com/", "blurb": "云端 ComfyUI 工作流平台，10档方案，¥29/月起", "rating": 3.0, "headline": "¥29/月起 · 10档方案", "tags": ["ComfyUI", "工作流", "多档"], "asOf": "2026-08-01"},
    {"id": "video-hunyuan", "category": "video", "name": "腾讯混元", "type": "vendor", "url": "https://cloud.tencent.com/product/hunyuan", "blurb": "混元视频 API，四档方案", "rating": 3.0, "headline": "API 制 · 4档方案", "tags": ["混元", "API", "腾讯"], "asOf": "2026-08-01"},

    # ---- Image (6) ----
    {"id": "image-jimeng", "category": "image", "name": "即梦", "type": "vendor", "url": "https://jimeng.jianying.com/", "blurb": "Seedance 2.0，四档方案，¥69/月起，字节旗下", "rating": 5.0, "headline": "¥69/月起 · 4档方案", "tags": ["Seedance", "图片生成", "字节"], "asOf": "2026-08-01"},
    {"id": "image-midjourney", "category": "image", "name": "Midjourney", "type": "vendor", "url": "https://www.midjourney.com/", "blurb": "MJ V7，四档方案，$10/月起（≈¥70）", "rating": 5.0, "headline": "$10/月起 ≈¥70 · 4档", "tags": ["MJ V7", "美元", "图片生成"], "asOf": "2026-08-01"},
    {"id": "image-liblib", "category": "image", "name": "Liblib AI", "type": "aggregator", "url": "https://www.liblib.ai/", "blurb": "WebUI/ComfyUI/Kling/Seedream，六档方案，年付¥429/年起", "rating": 5.0, "headline": "¥429/年起(年付) · 6档", "tags": ["ComfyUI", "多模型", "年付"], "asOf": "2026-08-01"},
    {"id": "image-tongyi", "category": "image", "name": "通义万相", "type": "vendor", "url": "https://tongyi.aliyun.com/wanxiang/", "blurb": "万相 2.6，三档方案，¥72/月起", "rating": 4.0, "headline": "¥72/月起 · 3档方案", "tags": ["万相", "阿里"], "asOf": "2026-08-01"},
    {"id": "image-runninghub", "category": "image", "name": "RunningHub", "type": "aggregator", "url": "https://www.runninghub.com/", "blurb": "云端 ComfyUI 工作流平台，10档方案，¥29/月起", "rating": 3.0, "headline": "¥29/月起 · 10档方案", "tags": ["ComfyUI", "工作流"], "asOf": "2026-08-01"},
    {"id": "image-duiyou", "category": "image", "name": "堆友", "type": "vendor", "url": "https://www.duiyou.com/", "blurb": "国风/设计风格图片平台", "rating": 3.0, "headline": "¥399/年起 · 国风设计", "tags": ["国风", "设计"], "asOf": "2026-08-01"},

    # ---- Audio (4) ----
    {"id": "audio-suno", "category": "audio", "name": "Suno", "type": "vendor", "url": "https://suno.com/", "blurb": "v5.5 AI 音乐生成，三档方案含免费档", "rating": 5.0, "headline": "¥0起 · 3档方案", "tags": ["音乐生成", "免费档", "v5.5"], "asOf": "2026-08-01"},
    {"id": "audio-udio", "category": "audio", "name": "Udio", "type": "vendor", "url": "https://www.udio.com/", "blurb": "AI 音乐生成，三档方案含免费档", "rating": 4.0, "headline": "¥0起 · 3档方案", "tags": ["音乐生成", "免费档"], "asOf": "2026-08-01"},
    {"id": "audio-acestudio", "category": "audio", "name": "Ace Studio", "type": "vendor", "url": "https://www.acestudio.ai/", "blurb": "AI 歌声合成，年付制", "rating": 3.0, "headline": "年付制 · 歌声合成", "tags": ["歌声合成", "年付"], "asOf": "2026-08-01"},
    {"id": "audio-hailuo", "category": "audio", "name": "海螺AI", "type": "vendor", "url": "https://hailuo.ai/", "blurb": "Music 2.6 / Speech 2.8，五档方案含免费档", "rating": 3.0, "headline": "¥0起 · 5档方案", "tags": ["音乐", "语音", "免费档"], "asOf": "2026-08-01"},

    # ---- 中转站 (1) ----
    {"id": "relay-mirage", "category": "relay", "name": "幻境MirageAI", "type": "relay", "url": "https://pay.ldxp.cn/shop/mirage", "blurb": "gpt-5.4 / deepseek-v4-pro / gemini-2.5-flash / agnes-2.0-flash 等37款，按量充值的半公益中转站", "rating": 4.0, "headline": "按量充值 · 37款模型", "tags": ["中转站", "New API", "按量", "半公益"], "asOf": "2026-07-05"},
]

# ============ Plans ============
# 格式: providerId, planName, tier, billingMode, billingLabel, price, originalPrice, currency, periodDays, quotaAmount, quotaUnit, quotaWindow("5h"/"month"/"week"/None), models(list of dict), benefits(list), tags, highlight, subscribeUrl, badge, asOf
# Coding Plans -- 入门级 (月付 ≤ ¥50)
CODING_ENTRY = [
    ("coding-taotoken", "Lite", None, "CALL", "月度按次", 39, None, "CNY", 30, None, "call", None, [{"code":"glm-5.2"}], [], ["入门"], "", "https://taotoken.net/", "入门", "2026-07-31"),
    ("coding-supercomp", "Lite", None, "CALL", "月度按次", 20, None, "CNY", 30, 1200, "call", '5h', [{"code":"minimax-m2.5"},{"code":"qwen3-235b-a22b"}], [], ["入门"], "1200次/5h", "https://www.scnet.cn/ac/openapi/doc/2.0/moduleapi/codingplan/subscriptionnotice.html", "入门", "2026-07-31"),
    ("coding-ollama", "Free", None, "CALL", "免费", 0, None, "USD", None, None, "call", None, [{"code":"glm-5.1"},{"code":"deepseek-v4-flash"},{"code":"minimax-m2.7"}], ["免费使用"], ["免费"], "免费", "https://ollama.com/pricing", "免费", "2026-07-31"),
    ("coding-kuaishou", "Mini", None, "CALL", "月度按次", 29, None, "CNY", 30, 40, "prompt", 'month', [{"code":"kat-coder-pro-v2.5"}], ["40 Prompts/月"], [], "40 Prompts/月", "https://www.streamlake.com/marketing/coding-plan", "入门", "2026-07-31"),
    ("coding-iflytek", "高效版", None, "CALL", "月度按次", 199, None, "CNY", 30, 6000, "call", '5h', [{"code":"glm-5.2"},{"code":"spark-x2-agent"},{"code":"kimi-k2.7-code"}], ["6000次/5h"], [], "6000次/5h", "https://maas.xfyun.cn/packageSubscription", "", "2026-07-31"),
    ("coding-iflytek", "速通版", None, "CALL", "月度按次", 999, None, "CNY", 30, 30000, "call", 'month', [{"code":"glm-5.2"},{"code":"spark-x2-agent"},{"code":"kimi-k2.7-code"}], ["30000速通次数/月", "首购¥699"], [], "首购¥699", "https://maas.xfyun.cn/packageSubscription", "活动", "2026-07-31"),
    ("coding-baidu", "Mini", None, "TOKEN", "按 Token 计费", 4.9, None, "CNY", 30, 10000000, "token", None, [{"code":"glm"},{"code":"deepseek"},{"code":"kimi"}], ["1000万 Tokens/月"], [], "1000万 Tokens/月", "https://cloud.baidu.com/product/codingplan.html", "入门", "2026-07-31"),
    ("coding-baidu", "Lite", None, "TOKEN", "按 Token 计费", 19.9, None, "CNY", 30, 42000000, "token", None, [{"code":"glm"},{"code":"deepseek"},{"code":"kimi"}], ["4200万 Tokens/月"], [], "4200万 Tokens/月", "https://cloud.baidu.com/product/codingplan.html", "入门", "2026-07-31"),
    ("coding-liantong", "Lite", None, "CALL", "月度按次", 40, None, "CNY", 30, 1200, "call", '5h', [{"code":"deepseek-v4-pro"},{"code":"kimi-k2.6"},{"code":"qwen3.6-27b"}], ["1200次/5h"], [], "1200次/5h", "https://support.cucloud.cn/document/127/591/2357.html?id=2357&arcid=7015", "入门", "2026-07-31"),
    ("coding-tencent", "Lite", None, "CALL", "月度按次", 40, None, "CNY", 30, 1200, "call", '5h', [{"code":"glm-5"},{"code":"kimi-k2.5"},{"code":"minimax-m2.5"}], ["1200次/5h", "首月¥7.9"], [], "1200次/5h", "https://console.cloud.tencent.cn/tokenhub/codingplan?regionId=1", "入门", "2026-07-31"),
    ("coding-yidong", "Lite", None, "CALL", "月度按次", 40, None, "CNY", 30, 1200, "call", '5h', [{"code":"minimax-m2.5"}], ["1200次/5h", "首月¥7.9"], [], "1200次/5h", "https://ecloud.10086.cn/portal/act/codingplan", "入门", "2026-07-31"),
    ("coding-bytedance", "Lite", None, "CALL", "月度按次", 40, None, "CNY", 30, 1200, "call", '5h', [{"code":"glm-5.2"},{"code":"doubao-seed-2.1-turbo"},{"code":"kimi-k2.7"}], ["1200次/5h", "首月¥9.9"], [], "1200次/5h", "https://volcengine.com/L/RYnDeTYySYQ/", "入门", "2026-07-31"),
    ("coding-openstarry", "星痕版(免费)", None, "CALL", "免费", 0, None, "CNY", None, None, "call", None, [{"code":"glm-5.2"},{"code":"kimi-k3"},{"code":"deepseek-v4-pro"},{"code":"minimax-m3"},{"code":"kimi-k2.7-code"},{"code":"qwen3.7-max"}], ["免费", "赠200次", "不限制请求数"], ["免费"], "免费", "https://api.openstarry.com/auth?mode=register&aff=X6K8", "免费", "2026-07-31"),
    ("coding-openstarry", "星序版(周)", None, "CALL", "周付", 9.9, None, "CNY", 7, None, "call", None, [{"code":"glm-5.2"},{"code":"kimi-k3"},{"code":"deepseek-v4-pro"},{"code":"minimax-m3"}], ["赠200次", "周付"], [], "周付¥9.9", "https://api.openstarry.com/auth?mode=register&aff=X6K8", "入门", "2026-07-31"),
    ("coding-openstarry", "星创版", None, "CALL", "月度按次", 49.9, None, "CNY", 30, 1000, "call", '5h', [{"code":"glm-5.2"},{"code":"kimi-k3"},{"code":"deepseek-v4-pro"},{"code":"minimax-m3"}], ["1000次/5h"], [], "1000次/5h", "https://api.openstarry.com/auth?mode=register&aff=X6K8", "入门", "2026-07-31"),
    ("coding-lanyun", "入门版", None, "CALL", "月度按次", 49, None, "CNY", 30, 1200, "call", '5h', [{"code":"glm-5.1"}], ["1200次/5h"], [], "1200次/5h", "https://console.lanyun.net/#/register", "入门", "2026-07-31"),
    ("coding-zhipu", "Lite", None, "CALL", "月度按次", 49, None, "CNY", 30, 1200, "call", '5h', [{"code":"glm-5.2"}], ["1200次/5h"], [], "1200次/5h", "https://www.bigmodel.cn/invite?icode=naEahtDGpOp7hfCi6MPFVunfet45IvM%2BqDogImfeLyI%3D", "入门", "2026-07-31"),
    ("coding-youyun", "Mini", None, "CALL", "月度按次", 49, None, "CNY", 30, 200, "call", '5h', [{"code":"glm-5.2"},{"code":"deepseek-v4-pro"},{"code":"deepseek-v4-flash"},{"code":"qwen3.6-plus"},{"code":"minimax-m2.7"},{"code":"kimi-k2.6"}], ["200次/5h"], [], "200次/5h", "https://passport.compshare.cn/register", "入门", "2026-07-31"),
    ("coding-kimi", "Andante", None, "CALL", "月度按次", 49, None, "CNY", 30, None, "call", None, [{"code":"kimi-k3"},{"code":"kimi-k2.7-code"}], ["首月¥39"], [], "首月¥39", "https://kimi-bot.com/activities/zh-cn/invite/share?scenario=invite&from=share_poster&invitation_code=22K28A", "入门", "2026-07-31"),
    ("coding-jieyue", "Flash Mini", None, "CALL", "月度按次", 49, None, "CNY", 30, 1500, "call", '5h', [{"code":"step-3.5-flash"}], ["1500次/5h"], [], "1500次/5h", "https://platform.stepfun.com", "入门", "2026-07-31"),
    ("coding-meituan", "免费版", None, "CALL", "免费", 0, None, "CNY", None, None, "call", None, [], ["免费使用", "需下载客户端"], ["免费"], "免费", "https://catpaw.meituan.com/", "免费", "2026-07-31"),
    ("coding-charm", "Free", None, "CALL", "免费", 0, None, "USD", None, None, "call", None, [{"code":"deepseek-v4-flash"},{"code":"deepseek-v4-pro"},{"code":"glm-5.2"}], ["免费使用"], ["免费", "美元"], "$0免费", "https://hyper.charm.land/", "免费", "2026-07-31"),
    ("coding-minimax", "Plus", None, "CALL", "月度按次", 49, None, "CNY", 30, 1500, "call", '5h', [{"code":"minimax-m3"}], ["1500次/5h"], [], "1500次/5h", "https://platform.minimaxi.com/subscribe/token-plan", "入门", "2026-07-31"),
    ("coding-chatgpt", "Plus", None, "CALL", "月度按次", 20, None, "USD", 30, None, "call", 'month', [{"code":"gpt-5.4"},{"code":"gpt-image-2"},{"code":"gpt-5.3-codex"}], ["GPT-5.4 全功能"], [], "$20/月", "https://openai.com/chatgpt/pricing/", "入门", "2026-07-31"),
    ("coding-chatgpt", "Team", None, "CALL", "月度按次", 25, None, "USD", 30, None, "call", 'month', [{"code":"gpt-5.4"},{"code":"gpt-image-2"},{"code":"gpt-5.3-codex"}], ["团队协作"], [], "$25/用户/月", "https://openai.com/chatgpt/pricing/", "团队", "2026-07-31"),
    ("coding-sensenova", "Free · 公测", None, "CALL", "免费", 0, None, "CNY", None, 1500, "call", '5h', [{"code":"sensenova-6.7-flash-lite"},{"code":"sensenova-u1-fast"}], ["免费公测", "1500次/5h"], ["免费"], "免费公测", "https://www.sensenova.cn/token-plan", "免费", "2026-07-31"),
    ("coding-wenming", "Lite", "LITE", "CALL", "月度按次", 45, None, "CNY", 30, 1000, "call", 'month', [{"code":"glm-5.2", "isBonus": False}, {"code":"deepseek-v4-flash", "isBonus": True}], ["每月1000次 GLM-5.2", "赠送 DeepSeek-V4-Flash"], [], "新手尝鲜", "https://wenming7.cn/sales?ref=6FRFQW2D", "入门", "2026-07-31"),
    ("coding-wenming", "新用户活动套餐", None, "TOKEN", "按 Token 计费", 29.9, 99, "CNY", 7, 50000000, "token", None, [{"code":"glm-5.2"}], ["GLM-5.2 专属", "2500万token基础+加赠2500万", "有效期7天", "每人限购一次"], ["推荐", "热门"], "29.9元享5000万token", "https://wenming7.cn/sales?ref=6FRFQW2D", "活动", "2026-07-31"),
]

# Coding Plans -- 进阶级 (¥51-199)
CODING_MID = [
    ("coding-kuaishou", "Starter", None, "CALL", "月度按次", 70, None, "CNY", 30, 100, "prompt", 'month', [{"code":"kat-coder-pro-v2.5"}], ["100 Prompts/月"], [], "100 Prompts/月", "https://www.streamlake.com/marketing/coding-plan", "进阶", "2026-07-31"),
    ("coding-taotoken", "Pro", None, "CALL", "月度按次", 199, None, "CNY", 30, None, "call", None, [{"code":"glm-5.2"}], [], [], "", "https://taotoken.net/", "进阶", "2026-07-31"),
    ("coding-kimi", "Moderato", None, "CALL", "月度按次", 99, None, "CNY", 30, None, "call", None, [{"code":"kimi-k3"},{"code":"kimi-k2.7-code"}], ["首月¥79"], [], "首月¥79", "https://kimi-bot.com/activities/zh-cn/invite/share?scenario=invite&from=share_poster&invitation_code=22K28A", "进阶", "2026-07-31"),
    ("coding-supercomp", "Pro", None, "CALL", "月度按次", 100, None, "CNY", 30, 6000, "call", '5h', [{"code":"minimax-m2.5"},{"code":"qwen3-235b-a22b"}], ["6000次/5h"], [], "6000次/5h", "https://www.scnet.cn/ac/openapi/doc/2.0/moduleapi/codingplan/subscriptionnotice.html", "进阶", "2026-07-31"),
    ("coding-jieyue", "Flash Plus", None, "CALL", "月度按次", 99, None, "CNY", 30, 6000, "call", '5h', [{"code":"step-3.5-flash"}], ["6000次/5h"], [], "6000次/5h", "https://platform.stepfun.com", "进阶", "2026-07-31"),
    ("coding-kuaishou", "Pro", None, "CALL", "月度按次", 140, None, "CNY", 30, 300, "prompt", 'month', [{"code":"kat-coder-pro-v2.5"}], ["300 Prompts/月"], [], "300 Prompts/月", "https://www.streamlake.com/marketing/coding-plan", "进阶", "2026-07-31"),
    ("coding-charm", "Subscription", None, "CALL", "月度按次", 140, None, "CNY", 30, None, "call", 'month', [{"code":"deepseek-v4-flash"},{"code":"deepseek-v4-pro"},{"code":"glm-5.2"}], [], ["美元"], "$20/月", "https://hyper.charm.land/", "进阶", "2026-07-31"),
    ("coding-openstarry", "星途版", None, "CALL", "月度按次", 119, None, "CNY", 30, 2500, "call", '5h', [{"code":"glm-5.2"},{"code":"kimi-k3"},{"code":"deepseek-v4-pro"},{"code":"minimax-m3"}], ["2500次/5h"], [], "2500次/5h", "https://api.openstarry.com/auth?mode=register&aff=X6K8", "进阶", "2026-07-31"),
    ("coding-lanyun", "专业版", None, "CALL", "月度按次", 149, None, "CNY", 30, 6000, "call", '5h', [{"code":"glm-5.1"}], ["6000次/5h"], [], "6000次/5h", "https://console.lanyun.net/#/register", "进阶", "2026-07-31"),
    ("coding-zhipu", "Pro", None, "CALL", "月度按次", 149, None, "CNY", 30, 6000, "call", '5h', [{"code":"glm-5.2"}], ["6000次/5h"], [], "6000次/5h", "https://www.bigmodel.cn/invite?icode=naEahtDGpOp7hfCi6MPFVunfet45IvM%2BqDogImfeLyI%3D", "进阶", "2026-07-31"),
    # 高效版已在上方入门级记录，此处去重跳过
    ("coding-youyun", "Basic", None, "CALL", "月度按次", 199, None, "CNY", 30, 800, "call", '5h', [{"code":"glm-5.2"},{"code":"deepseek-v4-pro"},{"code":"deepseek-v4-flash"},{"code":"qwen3.6-plus"},{"code":"minimax-m2.7"},{"code":"kimi-k2.6"}], ["800次/5h"], [], "800次/5h", "https://passport.compshare.cn/register", "进阶", "2026-07-31"),
    ("coding-jieyue", "Flash Pro", None, "CALL", "月度按次", 199, None, "CNY", 30, 22500, "call", '5h', [{"code":"step-3.5-flash"}], ["22500次/5h"], [], "22500次/5h", "https://platform.stepfun.com", "进阶", "2026-07-31"),
    ("coding-minimax", "Max", None, "CALL", "月度按次", 119, None, "CNY", 30, 4500, "call", '5h', [{"code":"minimax-m3"}], ["4500次/5h"], [], "4500次/5h", "https://platform.minimaxi.com/subscribe/token-plan", "进阶", "2026-07-31"),
    ("coding-kimi", "Allegretto", None, "CALL", "月度按次", 199, None, "CNY", 30, None, "call", None, [{"code":"kimi-k3"},{"code":"kimi-k2.7-code"}], ["首月¥159"], [], "首月¥159", "https://kimi-bot.com/activities/zh-cn/invite/share?scenario=invite&from=share_poster&invitation_code=22K28A", "进阶", "2026-07-31"),
    ("coding-wenming", "Pro", "PRO", "CALL", "月度按次", 125, None, "CNY", 30, 5000, "call", 'month', [{"code":"glm-5.2", "isBonus": False}, {"code":"deepseek-v4-flash", "isBonus": True}], ["每月5000次", "赠送 DeepSeek-V4-Flash"], [], "高性价比", "https://wenming7.cn/sales?ref=6FRFQW2D", "性价比", "2026-07-31"),
    ("coding-wenming", "Plus", None, "CALL", "月度按次", 249, None, "CNY", 30, 15000, "call", 'month', [{"code":"glm-5.2", "isBonus": False}, {"code":"deepseek-v4-flash", "isBonus": True}], ["每月15000次", "赠送 DeepSeek-V4-Flash"], ["推荐"], "进阶高额度", "https://wenming7.cn/sales?ref=6FRFQW2D", "进阶", "2026-07-31"),
]

# Coding Plans -- 高阶级 (≥ ¥200)
CODING_HIGH = [
    ("coding-aliyun", "Pro", None, "CALL", "月度按次", 200, None, "CNY", 30, 45000, "call", 'week', [{"code":"qwen3.6-plus"}], ["每周 45,000 次请求", "Qwen3.6-Plus 专属"], [], "¥200/月", "https://bailian.console.aliyun.com/", "旗舰", "2026-07-31"),
    ("coding-taotoken", "Max", None, "CALL", "月度按次", 388, None, "CNY", 30, None, "call", None, [{"code":"glm-5.2"}], [], [], "", "https://taotoken.net/", "旗舰", "2026-07-31"),
    ("coding-baidu", "Pro", None, "TOKEN", "按 Token 计费", 99.9, None, "CNY", 30, 230000000, "token", None, [{"code":"glm"},{"code":"deepseek"},{"code":"kimi"}], ["2.3亿 Tokens/月"], [], "2.3亿 Tokens/月", "https://cloud.baidu.com/product/codingplan.html", "进阶", "2026-07-31"),
    ("coding-baidu", "Max", None, "TOKEN", "按 Token 计费", 299.9, None, "CNY", 30, 700000000, "token", None, [{"code":"glm"},{"code":"deepseek"},{"code":"kimi"}], ["7亿 Tokens/月"], [], "7亿 Tokens/月", "https://cloud.baidu.com/product/codingplan.html", "旗舰", "2026-07-31"),
    ("coding-liantong", "Pro", None, "CALL", "月度按次", 200, None, "CNY", 30, 6000, "call", '5h', [{"code":"deepseek-v4-pro"},{"code":"kimi-k2.6"},{"code":"qwen3.6-27b"}], ["6000次/5h"], [], "6000次/5h", "https://support.cucloud.cn/document/127/591/2357.html?id=2357&arcid=7015", "旗舰", "2026-07-31"),
    ("coding-tencent", "Pro", None, "CALL", "月度按次", 200, None, "CNY", 30, 6000, "call", '5h', [{"code":"glm-5"},{"code":"kimi-k2.5"},{"code":"minimax-m2.5"}], ["6000次/5h", "首月¥39.9"], [], "6000次/5h", "https://console.cloud.tencent.cn/tokenhub/codingplan?regionId=1", "旗舰", "2026-07-31"),
    ("coding-yidong", "Pro", None, "CALL", "月度按次", 200, None, "CNY", 30, 6000, "call", '5h', [{"code":"minimax-m2.5"}], ["6000次/5h", "首月¥39.9", "GLM-5.1 4x抵扣"], [], "6000次/5h", "https://ecloud.10086.cn/portal/act/codingplan", "旗舰", "2026-07-31"),
    ("coding-bytedance", "Pro", None, "CALL", "月度按次", 200, None, "CNY", 30, 6000, "call", '5h', [{"code":"glm-5.2"},{"code":"doubao-seed-2.1-turbo"},{"code":"kimi-k2.7"}], ["6000次/5h", "首月¥49.9", "注意:双层计费不透明"], [], "⚠计费不透明", "https://volcengine.com/L/RYnDeTYySYQ/", "旗舰", "2026-07-31"),
    ("coding-kuaishou", "Max", None, "CALL", "月度按次", 350, None, "CNY", 30, 1000, "prompt", 'month', [{"code":"kat-coder-pro-v2.5"}], ["1000 Prompts/月"], [], "1000 Prompts/月", "https://www.streamlake.com/marketing/coding-plan", "旗舰", "2026-07-31"),
    ("coding-minimax", "Ultra", None, "CALL", "月度按次", 469, None, "CNY", 30, 15000, "call", '5h', [{"code":"minimax-m3"}], ["15000次/5h"], [], "15000次/5h", "https://platform.minimaxi.com/subscribe/token-plan", "旗舰", "2026-07-31"),
    ("coding-wenming", "Max", "MAX", "CALL", "月度按次", 429, None, "CNY", 30, 40000, "call", 'month', [{"code":"glm-5.2", "isBonus": False}, {"code":"deepseek-v4-flash", "isBonus": True}], ["每月40000次", "赠送 DeepSeek-V4-Flash"], [], "高频AI开发", "https://wenming7.cn/sales?ref=6FRFQW2D", "旗舰", "2026-07-31"),
    ("coding-lanyun", "高级版", None, "CALL", "月度按次", 469, None, "CNY", 30, 24000, "call", '5h', [{"code":"glm-5.1"}], ["24000次/5h"], [], "24000次/5h", "https://console.lanyun.net/#/register", "旗舰", "2026-07-31"),
    ("coding-zhipu", "Max", None, "CALL", "月度按次", 469, None, "CNY", 30, 24000, "call", '5h', [{"code":"glm-5.2"}], ["24000次/5h", "积分制"], [], "24000次/5h", "https://www.bigmodel.cn/invite?icode=naEahtDGpOp7hfCi6MPFVunfet45IvM%2BqDogImfeLyI%3D", "旗舰", "2026-07-31"),
    ("coding-jieyue", "Flash Max", None, "CALL", "月度按次", 699, None, "CNY", 30, 75000, "call", '5h', [{"code":"step-3.5-flash"}], ["75000次/5h"], [], "75000次/5h", "https://platform.stepfun.com", "旗舰", "2026-07-31"),
    ("coding-kimi", "Allegro", None, "CALL", "月度按次", 699, None, "CNY", 30, None, "call", None, [{"code":"kimi-k3"},{"code":"kimi-k2.7-code"}], ["首月¥559"], [], "首月¥559", "https://kimi-bot.com/activities/zh-cn/invite/share?scenario=invite&from=share_poster&invitation_code=22K28A", "旗舰", "2026-07-31"),
]

# Coding Plans -- 海外/美元
CODING_OVERSEAS = [
    ("coding-opencode", "Go", None, "TOKEN", "按量计费", 10, None, "USD", 30, None, "call", '5h', [{"code":"grok-4.5"},{"code":"glm-5.2"},{"code":"gpt-5.6-luna"},{"code":"kimi-k3"},{"code":"hy3"},{"code":"deepseek-v4-pro"},{"code":"kimi-k2.6"},{"code":"deepseek-v4-flash"},{"code":"minimax-m2.7"},{"code":"gemini-2.5-flash"}], ["17款模型", "$12/5h", "$30/周", "$60/月", "首月$5"], [], "17款模型·首月$5", "https://opencode.ai/", "进阶", "2026-07-31"),
    ("coding-zai", "Lite", None, "CALL", "月度按次", 18, None, "USD", 30, 1200, "call", '5h', [{"code":"glm-5.1"}], ["1200次/5h"], [], "$18/月", "https://z.ai/subscribe", "入门", "2026-07-31"),
    ("coding-zai", "Pro", None, "CALL", "月度按次", 72, None, "USD", 30, 6000, "call", '5h', [{"code":"glm-5.1"}], ["6000次/5h"], [], "$72/月", "https://z.ai/subscribe", "进阶", "2026-07-31"),
    ("coding-zai", "Max", None, "CALL", "月度按次", 160, None, "USD", 30, 24000, "call", '5h', [{"code":"glm-5.1"}], ["24000次/5h"], [], "$160/月", "https://z.ai/subscribe", "旗舰", "2026-07-31"),
    ("coding-xkiro", "Free", None, "TOKEN", "月度订阅", 0, None, "USD", 30, None, "token", None, [{"code":"claude"},{"code":"gpt"},{"code":"gemini"},{"code":"deepseek"},{"code":"qwen"},{"code":"glm"}], ["免费永久", "100K tokens/天", "20+ 免费模型", "AI 图片生成（有限）", "文本转语音 · 148 种 AI 语音"], [], "永久免费", "https://xkiro.com/ref/3Y9VZSF", "免费", "2026-08-06"),
    ("coding-xkiro", "Pro", None, "TOKEN", "月度订阅", 5, None, "USD", 30, None, "token", None, [{"code":"claude"},{"code":"gpt"},{"code":"gemini"},{"code":"deepseek"},{"code":"qwen"},{"code":"glm"}], ["周预算 $67", "60+ 模型", "OpenAI & Anthropic SDK 兼容", "智能路由 + 自动故障转移", "AI 图片生成 · GPT Image", "文本转语音 · 148 种 AI 语音"], [], "入门 · $5/月", "https://xkiro.com/ref/3Y9VZSF", "入门", "2026-08-06"),
    ("coding-xkiro", "Pro+", None, "TOKEN", "月度订阅", 10, None, "USD", 30, None, "token", None, [{"code":"claude"},{"code":"gpt"},{"code":"gemini"},{"code":"deepseek"},{"code":"qwen"},{"code":"glm"}], ["周预算 $132", "60+ 模型", "双倍配额", "更多并发请求", "详细用量分析"], [], "性价比 · $10/月", "https://xkiro.com/ref/3Y9VZSF", "性价比", "2026-08-06"),
    ("coding-xkiro", "Max", None, "TOKEN", "月度订阅", 20, None, "USD", 30, None, "token", None, [{"code":"claude"},{"code":"gpt"},{"code":"gemini"},{"code":"deepseek"},{"code":"qwen"},{"code":"glm"}], ["周预算 $264", "60+ 模型", "4 倍配额", "更多并发请求", "开发者生产力工具"], [], "进阶 · $20/月", "https://xkiro.com/ref/3Y9VZSF", "进阶", "2026-08-06"),
    ("coding-xkiro", "Ultra", None, "TOKEN", "月度订阅", 100, None, "USD", 30, None, "token", None, [{"code":"claude"},{"code":"gpt"},{"code":"gemini"},{"code":"deepseek"},{"code":"qwen"},{"code":"glm"}], ["周预算 $1,320", "60+ 模型", "20 倍配额", "极高并发请求", "提前体验新功能", "高峰时段优先"], [], "旗舰 · $100/月", "https://xkiro.com/ref/3Y9VZSF", "旗舰", "2026-08-06"),
    ("coding-xkiro", "Power", None, "TOKEN", "月度订阅", 200, None, "USD", 30, None, "token", None, [{"code":"claude"},{"code":"gpt"},{"code":"gemini"},{"code":"deepseek"},{"code":"qwen"},{"code":"glm"}], ["周预算 $2,640", "60+ 模型", "40 倍配额", "最大并发请求", "最高输出限制", "最高优先级支持 · 12h"], [], "旗舰 · $200/月", "https://xkiro.com/ref/3Y9VZSF", "旗舰", "2026-08-06"),
]

# Token Plans
TOKEN_PLANS = [
    # Token 入门 (月付 ≤ ¥100)
    ("token-tencent", "Lite", None, "TOKEN", "按 Token 计费", 39, None, "CNY", 30, 35000000, "token", None, [{"code":"auto"},{"code":"deepseek-v4-flash"},{"code":"glm-5.1"},{"code":"kimi-k2.5"}], ["3500万 Tokens/月", "仅限AI工具使用"], [], "3500万/月", "https://console.cloud.tencent.cn/tokenhub/", "入门", "2026-08-01"),
    ("token-tianyi", "2500万", None, "TOKEN", "按 Token 计费", 29, None, "CNY", 30, 25000000, "token", None, [{"code":"glm-5"},{"code":"deepseek-v3.2"}], ["2500万 Tokens/月"], [], "2500万/月", "https://www.ctyun.cn/act/AI/zhuanxiang", "入门", "2026-08-01"),
    ("token-alaya", "入门版", None, "TOKEN", "按 Token 计费", 199, None, "CNY", 30, 32700000, "token", None, [{"code":"glm-5.2"},{"code":"glm-5.1"},{"code":"deepseek-v4-flash"}], ["3270万 Tokens/月"], [], "3270万/月", "https://codingplan.alayanew.com/docs/billing", "入门", "2026-08-01"),
    ("token-xiaomi", "Lite", None, "CREDITS", "Credit 计费", 39, None, "CNY", 30, 4100000000, "credit", 'month', [{"code":"mimo-v2.5-pro"},{"code":"mimo-v2.5"}], ["4.1B Credits/月", "Credit ≠ Token", "首月¥34.32"], [], "4.1B Credits", "https://platform.xiaomimimo.com/#/token-plan", "入门", "2026-08-01"),
    ("token-fangzhou", "Small", None, "CREDITS", "AFP 积分制", 40, None, "CNY", 30, 20000, "afp", 'month', [{"code":"deepseek-v4-pro"},{"code":"glm-5.1"},{"code":"kimi-k2.6"}], ["20,000 AFP/月"], [], "20,000 AFP/月", "https://www.volcengine.com/docs/82379/2366394?lang=zh", "入门", "2026-08-01"),
    ("token-opencode", "Go", None, "TOKEN", "按量计费", 10, None, "USD", 30, None, "call", '5h', [{"code":"glm-5.2"},{"code":"gpt-5.6-luna"},{"code":"deepseek-v4-pro"},{"code":"kimi-k2.6"},{"code":"grok-4.5"},{"code":"hy3"}], ["17款模型", "$12/5h", "$30/周", "$60/月", "首月$5"], [], "17款·首月$5", "https://opencode.ai/", "进阶", "2026-08-01"),
    ("token-chatgpt", "Token", None, "TOKEN", "按量计费", 100, None, "USD", 30, None, "call", None, [{"code":"gpt-5.4"},{"code":"gpt-image-2"},{"code":"gpt-5.3-codex"}], ["100 刀额度", "暂时售罄"], [], "$100·暂时售罄", "https://openai.com/chatgpt/pricing/", "售罄", "2026-08-01"),
    ("token-tencent", "Standard", None, "TOKEN", "按 Token 计费", 99, None, "CNY", 30, 100000000, "token", None, [{"code":"auto"},{"code":"deepseek-v4-flash"},{"code":"glm-5.1"},{"code":"kimi-k2.5"},{"code":"deepseek-v4-pro"},{"code":"hy3"}], ["1亿 Tokens/月", "仅限AI工具使用"], [], "1亿/月", "https://console.cloud.tencent.cn/tokenhub/", "进阶", "2026-08-01"),
    ("token-taotoken", "Lite", None, "CREDITS", "Credit 计费", 59, None, "CNY", 30, 5000, "credit", 'month', [{"code":"deepseek-v4-pro"},{"code":"kimi-k3"},{"code":"glm-5.2"}], ["5,000 Credits/月"], [], "5,000 Credits", "https://taotoken.net/", "入门", "2026-08-01"),
    ("token-taotoken", "加油包", None, "CREDITS", "Credit 计费", 99, None, "CNY", 30, 10000, "credit", 'month', [{"code":"deepseek-v4-pro"},{"code":"kimi-k3"},{"code":"glm-5.2"}], ["10,000 Credits/月", "附加购"], [], "附加购", "https://taotoken.net/", "", "2026-08-01"),
    ("token-tianyi", "8000万", None, "TOKEN", "按 Token 计费", 89, None, "CNY", 30, 80000000, "token", None, [{"code":"glm-5"},{"code":"deepseek-v3.2"}], ["8000万 Tokens/月"], [], "8000万/月", "https://www.ctyun.cn/act/AI/zhuanxiang", "进阶", "2026-08-01"),
    ("token-xiaomi", "Standard", None, "CREDITS", "Credit 计费", 99, None, "CNY", 30, 11000000000, "credit", 'month', [{"code":"mimo-v2.5-pro"},{"code":"mimo-v2.5"}], ["11B Credits/月", "Credit ≠ Token", "首月¥87.12"], [], "11B Credits", "https://platform.xiaomimimo.com/#/token-plan", "进阶", "2026-08-01"),
    # Token 进阶级 (¥101-500)
    ("token-tianyi", "1.8亿", None, "TOKEN", "按 Token 计费", 199, None, "CNY", 30, 180000000, "token", None, [{"code":"glm-5"},{"code":"deepseek-v3.2"}], ["1.8亿 Tokens/月"], [], "1.8亿/月", "https://www.ctyun.cn/act/AI/zhuanxiang", "进阶", "2026-08-01"),
    ("token-taotoken", "Pro", None, "CREDITS", "Credit 计费", 149, None, "CNY", 30, 14000, "credit", 'month', [{"code":"deepseek-v4-pro"},{"code":"kimi-k3"},{"code":"glm-5.2"}], ["14,000 Credits/月"], [], "14,000 Credits", "https://taotoken.net/", "进阶", "2026-08-01"),
    ("token-fangzhou", "Medium", None, "CREDITS", "AFP 积分制", 200, None, "CNY", 30, 100000, "afp", 'month', [{"code":"deepseek-v4-pro"},{"code":"glm-5.1"},{"code":"kimi-k2.6"}], ["100,000 AFP/月"], [], "100,000 AFP/月", "https://www.volcengine.com/docs/82379/2366394?lang=zh", "进阶", "2026-08-01"),
    ("token-xiaomi", "Pro", None, "CREDITS", "Credit 计费", 329, None, "CNY", 30, 38000000000, "credit", 'month', [{"code":"mimo-v2.5-pro"},{"code":"mimo-v2.5"}], ["38B Credits/月", "Credit ≠ Token", "首月¥289.52"], [], "38B Credits", "https://platform.xiaomimimo.com/#/token-plan", "进阶", "2026-08-01"),
    ("token-tianyi", "3.8亿", None, "TOKEN", "按 Token 计费", 399, None, "CNY", 30, 380000000, "token", None, [{"code":"glm-5"},{"code":"deepseek-v3.2"}], ["3.8亿 Tokens/月"], [], "3.8亿/月", "https://www.ctyun.cn/act/AI/zhuanxiang", "进阶", "2026-08-01"),
    # Token 高阶级 (≥ ¥500)
    ("token-aliyun", "标准坐席", None, "CREDITS", "坐席制", 150, None, "CNY", 30, 25000, "credit", 'month', [{"code":"qwen3.8-max-preview"},{"code":"qwen3.7-max"},{"code":"deepseek-v4-pro"},{"code":"glm-5.2"},{"code":"kimi-k2.6"}], ["25,000 Credits/月", "原价¥198·限时10倍加量"], ["推荐"], "限时10倍加量", "https://common-buy.aliyun.com/token-plan", "活动", "2026-08-01"),
    ("token-tencent", "Pro", None, "TOKEN", "按 Token 计费", 299, None, "CNY", 30, 320000000, "token", None, [{"code":"auto"},{"code":"deepseek-v4-flash"},{"code":"deepseek-v4-pro"},{"code":"glm-5.1"},{"code":"kimi-k2.5"},{"code":"hy3"}], ["3.2亿 Tokens/月", "仅限AI工具使用"], [], "3.2亿/月", "https://console.cloud.tencent.cn/tokenhub/", "旗舰", "2026-08-01"),
    ("token-fangzhou", "Large", None, "CREDITS", "AFP 积分制", 500, None, "CNY", 30, 250000, "afp", 'month', [{"code":"deepseek-v4-pro"},{"code":"glm-5.1"},{"code":"kimi-k2.6"}], ["250,000 AFP/月"], [], "250,000 AFP/月", "https://www.volcengine.com/docs/82379/2366394?lang=zh", "旗舰", "2026-08-01"),
    ("token-xiaomi", "Max", None, "CREDITS", "Credit 计费", 659, None, "CNY", 30, 82000000000, "credit", 'month', [{"code":"mimo-v2.5-pro"},{"code":"mimo-v2.5"}], ["82B Credits/月", "Credit ≠ Token", "首月¥579.92"], [], "82B Credits", "https://platform.xiaomimimo.com/#/token-plan", "旗舰", "2026-08-01"),
    ("token-tianyi", "6.8亿", None, "TOKEN", "按 Token 计费", 699, None, "CNY", 30, 680000000, "token", None, [{"code":"glm-5"},{"code":"deepseek-v3.2"}], ["6.8亿 Tokens/月"], [], "6.8亿/月", "https://www.ctyun.cn/act/AI/zhuanxiang", "旗舰", "2026-08-01"),
    ("token-tencent", "Max", None, "TOKEN", "按 Token 计费", 599, None, "CNY", 30, 650000000, "token", None, [{"code":"auto"},{"code":"deepseek-v4-flash"},{"code":"deepseek-v4-pro"},{"code":"glm-5.1"},{"code":"kimi-k2.5"},{"code":"hy3"},{"code":"hy3-preview"}], ["6.5亿 Tokens/月"], [], "6.5亿/月", "https://console.cloud.tencent.cn/tokenhub/", "旗舰", "2026-08-01"),
    ("token-aliyun", "高级坐席", None, "CREDITS", "坐席制", 550, None, "CNY", 30, 100000, "credit", 'month', [{"code":"qwen3.8-max-preview"},{"code":"qwen3.7-max"},{"code":"deepseek-v4-pro"},{"code":"glm-5.2"},{"code":"kimi-k2.6"}], ["100,000 Credits/月", "原价¥698·限时10倍加量"], [], "限时10倍加量", "https://common-buy.aliyun.com/token-plan", "旗舰", "2026-08-01"),
    ("token-aliyun", "尊享坐席", None, "CREDITS", "坐席制", 1398, None, "CNY", 30, 250000, "credit", 'month', [{"code":"qwen3.8-max-preview"},{"code":"qwen3.7-max"},{"code":"deepseek-v4-pro"},{"code":"glm-5.2"},{"code":"kimi-k2.6"}], ["250,000 Credits/月"], [], "250,000 Credits", "https://common-buy.aliyun.com/token-plan", "旗舰", "2026-08-01"),
    ("token-fangzhou", "Max", None, "CREDITS", "AFP 积分制", 1000, None, "CNY", 30, 500000, "afp", 'month', [{"code":"deepseek-v4-pro"},{"code":"glm-5.1"},{"code":"kimi-k2.6"}], ["500,000 AFP/月"], [], "500,000 AFP/月", "https://www.volcengine.com/docs/82379/2366394?lang=zh", "旗舰", "2026-08-01"),
]

def slugify(name):
    """生成稳定干净的 id slug：ASCII 转小写，连续非字母数字归一化为单个 '-'，首尾去除 '-'。
    中文等非 ASCII 字符会被剔除；若结果为空串，由外层构建循环用 'plan' + 序号兜底。"""
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

def build_billing_note(price, periodDays):
    """billingCycles.note：免费档显示"免费"；付费档按周期语义给说明。"""
    if price == 0:
        return "免费"
    if periodDays == 30:
        return "仅月付"
    if periodDays == 7:
        return "一次性"
    return "按量计费"

def build_usage_window(quotaAmount, quotaUnit, quotaWindow, highlight, benefits):
    """按配额语义生成 usageWindow，优先使用显式 quotaWindow 字段：
    - quotaWindow=="5h"   → fiveHour=quotaAmount
    - quotaWindow=="month" → monthly=quotaAmount
    - quotaWindow=="week"  → weekly=quotaAmount
    - quotaWindow==None    → 不再默认回填 fiveHour，保持 null（显示"待核实"）
    保留原有正则解析作为 fallback（当 quotaWindow 未提供时）。
    token/credit/afp 分支逻辑不变。"""
    text = " ".join(filter(None, [highlight] + list(benefits)))

    def num(m):
        return int(m.group(1).replace(",", ""))

    five, weekly, monthly, totalTokens = None, None, None, None

    # === 优先路径：显式 quotaWindow ===
    if quotaWindow is not None:
        if quotaUnit == "token":
            totalTokens = quotaAmount
        elif quotaUnit in ("credit", "afp"):
            monthly = quotaAmount
        elif quotaWindow == "5h":
            five = quotaAmount
        elif quotaWindow == "week":
            weekly = quotaAmount
        elif quotaWindow == "month":
            monthly = quotaAmount
        return {"fiveHour": five, "weekly": weekly, "monthly": monthly, "totalTokens": totalTokens}

    # === Fallback：正则解析（兼容旧数据或未标注 quotaWindow 的情况）===
    m = re.search(r'(\d[\d,]*)\s*次/5h', text)
    if m:
        five = num(m)
    m = re.search(r'(\d[\d,]*)\s*(?:次|Prompts?|请求)/周', text)
    if m:
        weekly = num(m)
    m = re.search(r'每周\s*(\d[\d,]*)\s*次', text)
    if m and weekly is None:
        weekly = num(m)
    m = re.search(r'(\d[\d,]*)\s*(?:次|Prompts?|请求)/月', text)
    if m:
        monthly = num(m)
    m = re.search(r'每月\s*(\d[\d,]*)\s*次', text)
    if m and monthly is None:
        monthly = num(m)

    if quotaUnit == "token":
        totalTokens = quotaAmount
        monthly = None
    elif quotaUnit in ("credit", "afp"):
        monthly = quotaAmount
    else:
        # Fallback: 无显式窗口标注时仍尝试回退到 5h（仅 fallback 路径）
        if five is None and weekly is None and monthly is None and quotaAmount is not None:
            five = quotaAmount
        elif five is None and quotaAmount is not None and "/5h" in text:
            five = quotaAmount
    return {"fiveHour": five, "weekly": weekly, "monthly": monthly, "totalTokens": totalTokens}

def build_plan(pid, name, tier, billingMode, billingLabel, price, originalPrice, currency, periodDays, quotaAmount, quotaUnit, quotaWindow, models_raw, benefits, tags, highlight, subUrl, badge, asOf):
    prov = next((p for p in PROVIDERS if p["id"] == pid), None)
    if not prov:
        return None
    models = []
    for m in models_raw:
        if isinstance(m, dict):
            models.append(m)
        else:
            models.append({"code": m, "isBonus": False})
    slug = slugify(name)
    plan = {
        "id": pid + (("-" + slug) if slug else ""),
        "providerId": pid,
        "provider": prov["name"],
        "providerType": prov["type"],
        "providerUrl": prov["url"],
        "planName": name,
        "tier": tier,
        "billingMode": billingMode,
        "billingLabel": billingLabel,
        "price": price,
        "originalPrice": originalPrice,
        "currency": currency,
        "periodDays": periodDays,
        "quotaAmount": quotaAmount,
        "quotaUnit": quotaUnit,
        "quotaWindow": quotaWindow,
        "billingCycles": {"monthly": price, "quarterly": None, "annual": None, "note": build_billing_note(price, periodDays)},
        "usageWindow": build_usage_window(quotaAmount, quotaUnit, quotaWindow, highlight, benefits),
        "models": models,
        "benefits": benefits,
        "tags": tags,
        "highlight": highlight,
        "subscribeUrl": subUrl or prov["url"],
        "source": subUrl or prov["url"],
        "sourceType": "manual",
        "asOf": asOf,
        "badge": badge or "",
        "isPlaceholder": False
    }
    return plan

# Build all plans
all_plan_tuples = CODING_ENTRY + CODING_MID + CODING_HIGH + CODING_OVERSEAS + TOKEN_PLANS
PLANS = []
seen_ids = set()
counter = {}
plan_fallback_counter = {}  # slug 为空（如中文档位名）时用 'plan' + 序号兜底
for t in all_plan_tuples:
    pid = t[0]
    name = t[1]
    prov = next((p for p in PROVIDERS if p["id"] == pid), None)
    if not prov: continue
    plan = build_plan(*t)
    if not plan: continue
    base = plan["id"]
    # slug 为空时 plan["id"] == pid，改用 'plan' + 序号兜底，避免尾随/双连字符 id
    if base == pid:
        plan_fallback_counter[pid] = plan_fallback_counter.get(pid, 0) + 1
        base = f"{pid}-plan{plan_fallback_counter[pid]}"
        plan["id"] = base
    # Make unique id（保持去重逻辑，但 base 已是干净 slug，不会再产生 --1 这类 id）
    if base in seen_ids:
        counter[base] = counter.get(base, 0) + 1
        plan["id"] = base + "-" + str(counter[base])
    seen_ids.add(plan["id"])
    PLANS.append(plan)

# ---- xKiro 后处理：修正 id（Pro+ 与 Pro 冲突）+ 季付-10% / 年付-20% ----
XKIRO_PLAN_IDS = {"Free": "free", "Pro": "pro", "Pro+": "proplus", "Max": "max", "Ultra": "ultra", "Power": "power"}
XKIRO_DISCOUNTS = {  # (quarterly 月均价, annual 月均价) = price*0.9 / price*0.8；免费档无季/年付，置 None 显示「免费」
    "free":    (None, None),
    "pro":     (4.5, 4),
    "proplus": (9, 8),
    "max":     (18, 16),
    "ultra":   (90, 80),
    "power":   (180, 160),
}
XKIRO_NOTES = {  # 保留周预算信息 + 折扣
    "free":    "100K tokens/天 · 无季/年付",
    "pro":     "周预算 $67 · 季付-10% 年付-20%",
    "proplus": "周预算 $132 · 季付-10% 年付-20%",
    "max":     "周预算 $264 · 季付-10% 年付-20%",
    "ultra":   "周预算 $1,320 · 季付-10% 年付-20%",
    "power":   "周预算 $2,640 · 季付-10% 年付-20%",
}
for plan in PLANS:
    if plan["providerId"] == "coding-xkiro":
        slug = XKIRO_PLAN_IDS.get(plan["planName"])
        if slug is None:
            # 未知档位：跳过价格/note 覆盖，保留默认值，避免 KeyError 中断整脚本
            print(f"⚠️ 跳过 xKiro 未知档位 {plan['planName']!r} 的后处理（id={plan['id']}）")
            continue
        plan["id"] = "coding-xkiro-" + slug
        q, a = XKIRO_DISCOUNTS.get(slug, (None, None))
        plan["billingCycles"]["quarterly"] = q
        plan["billingCycles"]["annual"] = a
        plan["billingCycles"]["note"] = XKIRO_NOTES.get(slug, plan["billingCycles"]["note"])
        plan["source"] = "https://xkiro.com/#pricing"

# 末步：注入编辑点评（REVIEWS 与 _add_reviews.py 共享同一份），单命令即可完整重建数据，
# 不再需要手动补跑第二步（此前漏跑曾导致全部点评丢失）
import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("_add_reviews", BASE_DIR / "_add_reviews.py")
_reviews_mod = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_reviews_mod)
_reviews_updated = _reviews_mod.apply_reviews(PROVIDERS)

# Write JSON files（基于脚本所在目录，显式 UTF-8）
with open(BASE_DIR / "providers.json", "w", encoding="utf-8") as f:
    json.dump(PROVIDERS, f, ensure_ascii=False, indent=2)

with open(BASE_DIR / "plans.json", "w", encoding="utf-8") as f:
    json.dump(PLANS, f, ensure_ascii=False, indent=2)

print(f"Generated {len(PROVIDERS)} providers (incl. { _reviews_updated } reviews) and {len(PLANS)} plans")
print(f"  Coding: {sum(1 for p in PROVIDERS if p['category']=='coding')} providers")
print(f"  Token: {sum(1 for p in PROVIDERS if p['category']=='token')} providers")
print(f"  Video: {sum(1 for p in PROVIDERS if p['category']=='video')} providers")
print(f"  Image: {sum(1 for p in PROVIDERS if p['category']=='image')} providers")
print(f"  Audio: {sum(1 for p in PROVIDERS if p['category']=='audio')} providers")
print(f"  Relay: {sum(1 for p in PROVIDERS if p['category']=='relay')} providers")
