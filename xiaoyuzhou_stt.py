#!/usr/bin/env python3
import sys
import os
import requests
import json
import time
from bs4 import BeautifulSoup
import tempfile
from pathlib import Path
from http import HTTPStatus

import dashscope
from dashscope.audio.asr import Transcription

# 设置阿里的 API KEY
dashscope.api_key = os.environ.get("DASHSCOPE_API_KEY", "your-dashscope-api-key-here")

def print_status(msg):
    print(f"[Xiaoyuzhou STT] {msg}")

def process_podcast(url):
    print_status(f"Fetching URL: {url}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print_status(f"ERROR fetching URL: {e}")
        sys.exit(1)

    soup = BeautifulSoup(response.text, 'html.parser')

    title_tag = soup.find('meta', property='og:title')
    audio_tag = soup.find('meta', property='og:audio')

    if not title_tag or not audio_tag:
        print_status("ERROR: Could not find title or audio URL in the page.")
        sys.exit(1)

    title = title_tag['content']
    audio_url = audio_tag['content']

    print_status(f"Found Episode: {title}")
    print_status(f"Audio URL: {audio_url}")

    # 对于云端 API，我们可以直接把小宇宙 CDN 的音频 URL 传给阿里！
    # 这样连下载到本地 100MB 文件的过程都省了，速度快到飞起！
    print_status("Submitting audio URL to Alibaba Cloud DashScope (SenseVoice model)...")

    try:
        # 调用异步语音识别接口 (使用 qwen-asr-flash 替代已下线的 sensevoice-v1)
        task_response = Transcription.async_call(
            model='paraformer-v2',
            file_urls=[audio_url],
            language_hints=['zh'] # 提示主要语言是中文
        )

        if task_response.status_code != HTTPStatus.OK:
            print_status(f"ERROR: API Call Failed. Code: {task_response.status_code}, Message: {task_response.message}")
            sys.exit(1)

        task_id = task_response.output.task_id
        print_status(f"Task submitted successfully! Task ID: {task_id}")
        print_status("Waiting for transcription to complete (this usually takes a few minutes for a 1-hour podcast)...")

        # 轮询等待任务完成 (Fixing wait syntax)
        while True:
            result = Transcription.wait(task=task_id)
            if result.status_code == HTTPStatus.OK:
                if result.output.task_status == 'SUCCEEDED':
                    print_status("Transcription SUCCEEDED!")
                    break
                elif result.output.task_status == 'FAILED':
                    print_status(f"ERROR: Transcription FAILED. Message: {result.output.message}")
                    sys.exit(1)
                else:
                    # RUNNING or PENDING
                    print_status("Still processing... checking again in 10 seconds.")
                    time.sleep(10)
            else:
                print_status(f"ERROR checking status: {result.message}")
                sys.exit(1)

        # 任务成功后，获取识别结果的 URL
        # result.output.results is a list of dicts. We access it using bracket notation.
        result_url = result.output.results[0]['transcription_url']
        print_status("Downloading transcription result from cloud...")

        # 下载结果 JSON
        transcript_response = requests.get(result_url)
        transcript_data = transcript_response.json()

        # 阿里的返回格式是一个包含了每一句话信息的 JSON，我们需要把它们拼起来
        full_text = ""
        if 'transcripts' in transcript_data and len(transcript_data['transcripts']) > 0:
            sentences = transcript_data['transcripts'][0].get('sentences', [])
            for sentence in sentences:
                full_text += sentence.get('text', '') + "\n"

        if not full_text.strip():
            print_status("WARNING: Transcription result was empty!")
            full_text = "未能在音频中识别出有效的文字。"

        # 保存到本地临时文件供 Claude 读取
        temp_dir = Path("/tmp/xiaoyuzhou_stt")
        temp_dir.mkdir(parents=True, exist_ok=True)
        transcript_path = temp_dir / "transcript.txt"

        with open(transcript_path, 'w', encoding='utf-8') as f:
            f.write(full_text)

        print_status(f"Transcription complete! Saved to {transcript_path}")

        # 输出元数据供 Skill 流程使用
        metadata = {
            "title": title,
            "audio_url": audio_url,
            "transcript_path": str(transcript_path)
        }

        print(f"===METADATA_START===\n{json.dumps(metadata)}\n===METADATA_END===")

    except Exception as e:
        print_status(f"An error occurred during DashScope API call: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python xiaoyuzhou_stt.py <url>")
        sys.exit(1)

    process_podcast(sys.argv[1])
