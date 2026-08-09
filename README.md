# 面向研发的可执行提示词范式工程库

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE) [![Python: 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](#)

本仓库以工程化视角收集并实现若干可执行的提示词（prompt）范式，目标是把模型调用流程做成可验证、可调试、可复用的工程模块，便于在研发流程中复现与迭代。

**功能总览**

| 模块 | 现在可用能力 |
|---|---|
| Crawler | 多站点抓取、候选公告页发现、URL 去重 |
| Extractor | trafilatura + readability + 纯文本回退 |
| Structuring | LLM 优先抽取，规则引擎回退 |
| Database | 来源表、公告表、来源健康评分表 |
| API | /health /sources /announcements /sources/health |
| MCP | 提供工具接口骨架（Python 3.10+） |

**系统流程图**

```mermaid
flowchart LR
	A[来源配置 sources.yaml] --> B[多站点爬取/候选页发现]
	B --> C[抽取正文/清洗]
	C --> D[结构化抽取 (LLM/规则)]
	D --> E[入库: 来源/公告/元信息]
	E --> F[API 提供: /sources /announcements /health]
	style A fill:#f9f,stroke:#333,stroke-width:1px
```

**快速开始**

在项目根目录执行：

```bash
pip install -r requirements.txt
# 复制环境变量示例（Unix / macOS）
cp .env.example .env
# Windows PowerShell:
Copy-Item .env.example .env

# 初始化数据库（示例脚本，视项目实际路径调整）
python scripts/init_db.py

# 本地运行示例服务或定时任务
python scripts/run_daily.py
```

更多使用示例、配置项和设计思路请参见各子目录下的 `README.md`。

---

感谢使用与反馈，欢迎提交 issue 或 PR。 
