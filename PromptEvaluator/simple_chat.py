#!/usr/bin/env python
from pathlib import Path
import argparse, os, openai, dotenv

dotenv.load_dotenv(".env", override=False)

def query(msg: str, key: str, model: str) -> str:
    openai.api_key, openai.api_base = key, "https://openrouter.ai/api/v1"
    r = openai.ChatCompletion.create(model=model, messages=[{"role":"user","content":msg}], max_tokens=200)
    return r["choices"][0]["message"]["content"]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ask",  help="prompt to send (if omitted, interactive)")
    ap.add_argument("--model",default="openai/gpt-3.5-turbo")
    ap.add_argument("--key")
    a = ap.parse_args()
    key = a.key or os.getenv("OPENROUTER_API_KEY") or exit("No key provided")
    prompt = a.ask or input("↪︎  Enter your prompt: ")
    print("\n🧠", query(prompt, key, a.model))

if __name__ == "__main__": main()
