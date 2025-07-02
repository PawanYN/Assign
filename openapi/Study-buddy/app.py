"""
Study‑Buddy assistant demo
--------------------------
Prerequisites:
  pip install openai python-dotenv
  # and put OPENAI_API_KEY=sk-... in your .env
"""


import os
from dotenv import load_dotenv
import openai
import requests
import json
import os

import time
import logging
from datetime import datetime
import streamlit as st

# ── Setup ──────────────────────────────────────────────────────────────────
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL_NAME = "gpt-4o-mini"          # adapt if you prefer "gpt-4-1106-preview"
PDF_PATH  = "cryptocurrency.pdf"    # make sure this path is correct
USER_MSG  = "What is mining?"       # initial question for the assistant



# ── 1. Upload file for retrieval ──────────────────────────────────────────
file_resp = client.files.create(
    file=open(PDF_PATH, "rb"),
    purpose="assistants"
)
file_id = file_resp.id
print("✅ Uploaded file:", file_id)

# ── 2. Create / reuse an assistant ────────────────────────────────────────
assistant = client.beta.assistants.create(
    name="Study Buddy",
    instructions="""You are a helpful study assistant who knows a lot about
    understanding research papers. Summarize, clarify terminology, extract key
    figures and data, and point out strengths and limitations. Your goal is to
    make complex scientific material accessible.""",
    tools=[{"type": "retrieval"}],
    model=MODEL_NAME,
    file_ids=[file_id],
)
assistant_id = assistant.id
print("✅ Assistant created:", assistant_id)

# ── 3. Create a thread and add the user’s first message ───────────────────
thread = client.beta.threads.create()
thread_id = thread.id

client.beta.threads.messages.create(
    thread_id=thread_id,
    role="user",
    content=USER_MSG
)
print("✅ Thread created:", thread_id)

# ── 4. Kick off a run ─────────────────────────────────────────────────────
run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assistant_id,
    instructions="Please address the user as Bruce."
)
run_id = run.id
print("▶️  Run started:", run_id)

# ── 5. Poll until the run is complete ─────────────────────────────────────
def wait_for_completion(client, thread_id, run_id, poll=2):
    while True:
        run_info = client.beta.threads.runs.retrieve(
            thread_id=thread_id, run_id=run_id
        )
        status = run_info.status
        if status == "completed":
            elapsed = run_info.completed_at - run_info.created_at
            print("✅ Run completed in", time.strftime("%H:%M:%S", time.gmtime(elapsed)))
            break
        elif status in {"failed", "cancelled"}:
            raise RuntimeError(f"Run finished with status: {status}")
        time.sleep(poll)

wait_for_completion(client, thread_id, run_id)

# ── 6. Fetch the assistant’s reply ────────────────────────────────────────
messages = client.beta.threads.messages.list(thread_id=thread_id)
assistant_reply = messages.data[0].content[0].text.value
print("\n🤖 Assistant says:", assistant_reply)