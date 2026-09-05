# 模块覆盖清单（终局）

| # | 模块 | 路径/范围 | 难度 | 命中 | 主工具 | 负责任务 | 依赖 | 状态 | 发现数 | 证据/测试 | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | index.html 全量（渲染状态机/价格折算/CSS 响应式/SEO/错误路径/主题持久化/esc 纪律） | index.html | 3 | 5 | 白盒读码 + browser-use 活体红绿测试 | R1-R8 主任务 | data JSON | 已覆盖 | 11 | index.html:1042 ::test_404_error_path | Bug2/3/4/5/9/11/12/13/15/16/18；含 375px 溢出、hash 双向、XSS 注入、404 降级活体验证 |
| 2 | 数据生成管线与一致性（含点评注入） | data | 2 | 4 | python3 白盒 + 探针脚本幂等复跑 | R1/R3/R5 主任务 | - | 已覆盖 | 5 | data/_generate_data.py:206 ::test_original_price_semantics | Bug1/6/10/14 相关、管线单命令化 |
| 3 | robots/sitemap/README/gitignore 契约 | README.md | 1 | 2 | 白盒逐句契约核对 | R2/R7/R9 主任务 | - | 已覆盖 | 2 | README.md:16 .gitignore:18 | Bug14/17 |
