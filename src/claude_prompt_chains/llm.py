import json
import os
import urllib.request
import urllib.error


ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
DEFAULT_MODEL = "claude-sonnet-4-20250514"
DEFAULT_MAX_TOKENS = 2048


class ClaudeAPIError(Exception):
    pass


class ClaudeClient:

    def __init__(self, api_key=None, model=DEFAULT_MODEL,
                 max_tokens=DEFAULT_MAX_TOKENS):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        if not self.api_key:
            raise ValueError(
                "Anthropic API key required. Set ANTHROPIC_API_KEY "
                "env var or pass --api-key"
            )
        self.model = model
        self.max_tokens = max_tokens

    def send_prompt(self, prompt, system=None):
        messages = [{"role": "user", "content": prompt}]
        payload = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "messages": messages,
        }
        if system:
            payload["system"] = system

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            ANTHROPIC_API_URL,
            data=data,
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
        )
        try:
            resp = urllib.request.urlopen(req)
            body = resp.read().decode("utf-8")
            result = json.loads(body)
            blocks = result.get("content", [])
            texts = [
                b["text"] for b in blocks if b.get("type") == "text"
            ]
            return "\n".join(texts)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            raise ClaudeAPIError(
                f"Anthropic API error {e.code}: {body}"
            ) from e
        except urllib.error.URLError as e:
            raise ClaudeAPIError(f"Request failed: {e.reason}") from e
