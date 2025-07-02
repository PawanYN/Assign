#!/usr/bin/env python
"""
PromptEvaluator
===============
Batch‑evaluate document‑summary pairs using any LLM exposed through OpenRouter.
See README.md for usage.
"""
from __future__ import annotations
import argparse, json, time, os
from pathlib import Path
from typing import List, Dict, Any
import openai, dotenv, tqdm

# ---- helpers ---------------------------------------------------------------
def load_json(path: Path) -> Any:      return json.loads(path.read_text(encoding="utf-8"))
def read_text(path: Path) -> str:      return path.read_text(encoding="utf-8")
def build_prompt(tpl: str, doc: str, summ: str) -> str:
    return tpl.replace("{{Document}}", doc).replace("{{Summary}}", summ)

def query(prompt: str, *, model: str, n: int, max_toks: int, temp: float) -> List[str]:
    resp = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        n=n, temperature=temp, max_tokens=max_toks, top_p=1
    )
    return [c["message"]["content"] for c in resp["choices"]]

# ---- main ------------------------------------------------------------------
def main(a: argparse.Namespace) -> None:
    dotenv.load_dotenv(".env", override=False)
    key = a.key or os.getenv("OPENROUTER_API_KEY")
    if not key:
        raise SystemExit("No API key ‑‑ pass --key or set OPENROUTER_API_KEY in .env")

    openai.api_key, openai.api_base = key, "https://openrouter.ai/api/v1"
    data     = load_json(Path(a.summeval_fp))
    tpl      = read_text(Path(a.prompt_fp))
    results, skipped = [], 0

    for i, item in enumerate(tqdm.tqdm(data, desc="Eval", unit="doc"), 1):
        prompt = build_prompt(tpl, item["source"], item["system_output"])
        try:
            item["prompt"] = prompt
            item["responses"] = query(prompt, model=a.model, n=a.n, max_toks=a.max_t, temp=a.temp)
            results.append(item)
        except Exception as e:
            skipped += 1; print("skip", skipped, e); time.sleep(a.err_sleep); continue
        if i % a.save_every == 0: Path(a.save_fp).write_text(json.dumps(results, indent=2, ensure_ascii=False))

    Path(a.save_fp).write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"Done. saved→{a.save_fp}  ignored={skipped}")

def cli() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--prompt_fp", default="prompts/summeval/con_detailed.txt")
    p.add_argument("--summeval_fp", default="data/summeval.json")
    p.add_argument("--save_fp",    default="results/gpt4_con_detailed_openrouter.json")
    p.add_argument("--key")
    p.add_argument("--model", default="mistralai/mistral-small-3.2-24b-instruct:free")
    p.add_argument("--n",    type=int,   default=2,   help="completions per prompt")
    p.add_argument("--max_t",type=int,   default=5,    help="max_tokens")
    p.add_argument("--temp", type=float, default=2.0,  help="temperature")
    p.add_argument("--sleep",      type=float, default=0.5)
    p.add_argument("--err_sleep",  type=float, default=2.0)
    p.add_argument("--save_every", type=int,   default=50)
    return p.parse_args()

if __name__ == "__main__":
    main(cli())
