from groq import Groq

client = Groq(api_key="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")

MAX_TOKENS = 8000
MODEL = "llama-3.3-70b-versatile"


def trim_history(messages: list[dict], max_tokens: int = MAX_TOKENS) -> list[dict]:
    total_chars = sum(len(m.get("content", "")) for m in messages)
    estimated_tokens = total_chars // 4
    while estimated_tokens > max_tokens and len(messages) > 2:
        messages = messages[2:]
        total_chars = sum(len(m.get("content", "")) for m in messages)
        estimated_tokens = total_chars // 4
    return messages


def stream_chat(message: str, history: list[dict]):
    messages = [{"role": "system", "content": "You are a helpful, concise AI assistant."}]
    messages += history + [{"role": "user", "content": message}]
    messages = trim_history(messages)
    input_tokens = sum(len(m.get("content", "")) for m in messages) // 4

    stream = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=1024,
        stream=True,
    )

    output_tokens = 0
    for chunk in stream:
        text = chunk.choices[0].delta.content or ""
        if text:
            output_tokens += len(text) // 4 + 1
            yield f"data: {text}\n\n"

    total = input_tokens + output_tokens
    yield f"event: token_usage\ndata: {total}\n\n"
    yield "event: done\ndata: [DONE]\n\n"