# 准备记录 — R1（2026-09-04）

## 项目识别
- 纯静态单文件站：index.html（HTML + 内联 CSS + 原生 JS，~1100 行）
- 数据：data/providers.json（56 平台）+ data/plans.json（95 套餐）
- 生成管线：data/_generate_data.py（含点评注入）+ data/_add_reviews.py（独立更新）
- 无后端/无数据库/无构建/无测试体系；本地 http.server 即可起服
- 技术栈：原生 JS（fetch + innerHTML 渲染）、Python3 stdlib

## 测试类型
- 白盒为主：通读 index.html 内联 JS + 两个数据脚本，追状态机/数据流/边界
- 黑盒 UI 面为辅：浏览器驱动打交互/断点/主题/几何断言
- 组合类型：白盒 + 黑盒(UI)；无 API/DB/TUI 接口面（项目不存在）

## 工具调研

验证日期：2026-09-04
- 本地知识库 .zcode/agent/tools-kb.md：45 条目，全部 ≤30 天有效
  （launch_bug_hunter.py pre 已校验通过，本地命中：browser-use 插件用于 UI 面，
  python3/node/git 系统工具用于白盒与自动化，均新鲜可用，无需重搜）
- 未走网络搜索：本地命中已覆盖本项目所需全部工具类型（本地优先原则）

## 工具选择
- 白盒：Read/Grep 读码 + node --check 语法 + python3 运行验证
- 黑盒 UI：browser-use:control-browser 插件（多断点/交互/主题/截图）
- 数据探针：python3 脚本校验 JSON 一致性
- 不选 postmcp/agent-tty/DB 工具：无对应接口面（因地制宜，不装用不到的）

## 工具就绪
- python3 / node / git：系统自带，本会话已多次使用验证 ✓
- browser-use:control-browser：本会话前轮回归测试已验证可用 ✓
- 可以开工：是

## 多工具协作
- 白盒读码发现可疑点 → browser-use 动态复现验证（上游喂下游）
- 数据探针脚本筛异常 → 白盒定位根因 → 浏览器 Live 复验修复
- 一模块一主工具：JS/数据脚本=白盒主攻，CSS 布局=浏览器主攻，互为辅助

## 准备结论
- 全部工具就绪且已验证，模块清单已建立（8 模块），可以开工：是
