# Xiaoyuzhou to Obsidian (Claude Code Skill) 🎙️

A zero-friction, fully automated workflow for extracting, transcribing, and intelligently summarizing Chinese podcasts from Xiaoyuzhou (小宇宙) directly into your Obsidian knowledge base.

Powered by **Claude Code** and **Alibaba Cloud DashScope API**.

## 🚀 Features

- **Blazing Fast Transcription**: Instead of downloading hundreds of megabytes locally, this script extracts the raw audio CDN link from Xiaoyuzhou and submits it directly to Alibaba Cloud's asynchronous Speech-to-Text API (`paraformer-v2`). A 1-hour podcast is transcribed in just a few seconds/minutes!
- **AI-Powered Deep Summarization**: Claude Code reads the full transcript and uses advanced prompt engineering to generate:
  - 📖 **Executive Summary** (Core background and takeaways)
  - 💡 **Key Insights & Evidence** (3-5 structured insights, strictly backed by evidence/examples from the podcast)
  - 🗣️ **Notable Quotes** (Golden sentences extracted verbatim)
- **Seamless Obsidian Integration**: Automatically formats the output as a beautiful Markdown note with YAML Frontmatter (tags, source URL, audio link, date) and saves it directly to your local Obsidian vault. The raw transcript is preserved in a foldable `<details>` block at the bottom.
- **Native Claude Skill**: Runs entirely within your local Claude Code CLI environment. No heavy web servers or complex GUI apps required. Just type `/xiaoyuzhou [url]`.

## 🛠️ Prerequisites

1. [Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview) installed and authenticated.
2. Python 3.10+ installed locally.
3. An active **Alibaba Cloud DashScope API Key** (for SenseVoice/Paraformer transcription).
4. Local **Obsidian** vault.

## 📦 Installation

### 1. Set up the Python Script
Copy `xiaoyuzhou_stt.py` to your Claude scripts directory:
```bash
mkdir -p ~/.claude/scripts
cp xiaoyuzhou_stt.py ~/.claude/scripts/
```

Install the required Python packages:
```bash
pip install requests beautifulsoup4 dashscope
```

**Note:** Open `~/.claude/scripts/xiaoyuzhou_stt.py` and replace `dashscope.api_key` with your actual Alibaba Cloud API key, or export it in your environment:
```bash
export DASHSCOPE_API_KEY="sk-your-api-key"
```

### 2. Install the Claude Skill
Copy `SKILL.md` to your Claude Code skills directory:
```bash
mkdir -p ~/.claude/skills/xiaoyuzhou
cp SKILL.md ~/.claude/skills/xiaoyuzhou/
```

### 3. Configure Obsidian Path
Open `~/.claude/skills/xiaoyuzhou/SKILL.md` and edit the Obsidian destination path in Step 4 to match your personal vault's path (e.g., `/Users/yourname/Obsidian/Podcasts/`).

## 🎯 Usage

Whenever you find a great episode on Xiaoyuzhou, just open your terminal with Claude Code running and type:

```text
/xiaoyuzhou https://www.xiaoyuzhoufm.com/episode/xxxxxx
```

Claude will automatically:
1. Run the Python script to fetch the audio and transcribe it via Alibaba Cloud.
2. Read the resulting transcript.
3. Think, analyze, and write a structured, evidence-backed summary.
4. Save the final beautiful Markdown file to your Obsidian vault.

## 🧠 How it Works

This project demonstrates the power of the **Claude Code Skills Framework**. By offloading the "heavy lifting" (HTTP requests, STT API polling) to a simple Python helper script, we free up Claude Code to do what it does best: profound reading comprehension, summarization, and file system manipulation.

## 📜 License
MIT License.
