# Executable Prompt Engineering Paradigms

这个仓库收集了五个常见的提示词范式，并以可运行的方式展示它们如何落到工程实践中。重点不是“写得更像 prompt”，而是把模型调用过程整理成可验证、可调试、可控的一组示例。

## 目录结构

```text
Executable-Prompt-Paradigms/
├── 01-结构化输出范式/
├── 02-推理与任务拆解范式/
├── 03-工具与动作协同范式/
├── 04-反思与自愈范式/
└── 05-防御与安全范式/
```

## 运行方式

```bash
pip install -r requirements.txt
python 01-结构化输出范式/demo.py
python 02-推理与任务拆解范式/demo.py
python 03-工具与动作协同范式/demo.py
python 04-反思与自愈范式/demo.py
python 05-防御与安全范式/demo.py
```

## 说明

- 01-结构化输出范式：展示如何把输出约束到 schema 中。
- 02-推理与任务拆解范式：展示多样本推理与多数投票。
- 03-工具与动作协同范式：展示工具调用与 ReAct 风格循环。
- 04-反思与自愈范式：展示基于错误反馈的修复流程。
- 05-防御与安全范式：展示注入防御与基本安全边界。
