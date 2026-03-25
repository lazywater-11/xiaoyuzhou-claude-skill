---
name: xiaoyuzhou
description: 下载小宇宙播客，进行语音转文字，提取总结并保存到 Obsidian。只需传入小宇宙播客链接。
---

# 小宇宙播客提取与总结 (Xiaoyuzhou to Obsidian)

当用户输入 `/xiaoyuzhou [小宇宙链接]` 时，你需要作为一个极其自律的知识沉淀助手，严格按照以下规范执行。

## 🎯 目标文件 (Target Files)
1. **执行脚本**：`~/.claude/scripts/xiaoyuzhou_stt.py`
2. **中间产物**：脚本生成的 `/tmp/xiaoyuzhou_stt/transcript.txt` 逐字稿文件
3. **最终输出**：`/Users/zhifengma/obsidian-lifeos/Podcasts/[播客标题].md`

## 📋 执行检查清单 (Execution Checklist)
- [ ] **步骤 1：触发转录**
      使用 `Bash` 运行命令：`python3 ~/.claude/scripts/xiaoyuzhou_stt.py "$ARGUMENTS"`。等待运行完毕并提取其输出的 JSON Metadata（包含 `title`, `audio_url`, `transcript_path`）。
- [ ] **步骤 2：读取逐字稿**
      使用 `Read` 工具读取 Metadata 指示的逐字稿路径。
- [ ] **步骤 3：执行提炼与总结**
      运用 LLM 能力，基于全文撰写高质量笔记（严格遵循下方的“文案规范”）。如果能区分不同嘉宾视角，请尽量保留。
- [ ] **步骤 4：格式化并写入 Obsidian**
      使用 `Write` 工具，将组装好的 Markdown 内容（包含 YAML 和正文）写入最终输出路径。如果文件名含特殊字符，请用短横线替换。
- [ ] **步骤 5：完成汇报**
      向用户反馈操作成功，并输出生成的 Obsidian 文件路径。

## ✍️ 代码/文案规范 (Standards & Formatting)

**最高原则：** 这不是为你自己写的摘要，而是为用户打造的、看一眼就能吸收核心价值的知识库沉淀。

最终写入的 Markdown 必须严格按照以下格式组织：

```yaml
---
tags: [播客, 小宇宙]
source: {原始播客链接}
audio: {Metadata中提取的 audio_url}
date: "{当前的 YYYY-MM-DD 日期}"
---
```

# 🎙️ {播客标题}

## 📖 前置导览 (Executive Summary)
用一段话作为摘要，介绍这期播客的核心背景、探讨了什么核心议题，以及读者（我）能从中获得什么样的启发或认知改变。

## 💡 核心观点与论据支撑 (Key Insights & Arguments)
提炼出这期播客中最有价值的 3-5 个核心观点（使用层级结构）。
**⚠️强制要求**：每个核心观点之下，**必须紧跟“论据支撑”**。不能只是一句干瘪的结论，必须用播客中讲到的具体例子、数据、逻辑推演或现实故事来支撑这个观点。我要看到他们是“为什么”得出这个结论的。

## 🗣️ 精彩语录 (Notable Quotes)
从逐字稿中提取 2-3 句最原汁原味、最能引发共鸣或最具洞察力的金句（保留原话的力度和温度），使用 `> ` 引用格式。

---

<details>
<summary>展开查看原始逐字稿位置</summary>
*原始逐字稿已由 Claude 自动提取并保存在本地临时目录：`/tmp/xiaoyuzhou_stt/transcript.txt`*
</details>
