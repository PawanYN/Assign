import openai

openai.api_key  = "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"      # your key here
openai.api_base = "https://openrouter.ai/api/v1"

try:
    # free endpoint: just lists available models
    models = openai.Model.list()
    # If we get here, the key is valid
    print("✅ Key works! Example model IDs:", [m.id for m in models["data"][:5]])
except Exception as e:
    print("❌ Key failed:", e)
