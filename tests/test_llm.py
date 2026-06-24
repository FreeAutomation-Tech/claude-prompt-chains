import json
import os
import urllib.error

import pytest

from claude_prompt_chains.llm import ClaudeClient, ClaudeAPIError


class FakeResponse:

    def __init__(self, data, code=200):
        self.data = json.dumps(data).encode("utf-8")
        self.code = code

    def read(self):
        return self.data

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


class TestClaudeClient:

    def test_init_without_key(self):
        if "ANTHROPIC_API_KEY" in os.environ:
            del os.environ["ANTHROPIC_API_KEY"]
        with pytest.raises(ValueError, match="API key"):
            ClaudeClient(api_key="")

    def test_init_with_key(self):
        client = ClaudeClient(api_key="sk-test")
        assert client.api_key == "sk-test"

    def test_send_prompt(self, mocker):
        client = ClaudeClient(api_key="sk-test")
        response_data = {
            "content": [{"type": "text", "text": "Hello!"}],
        }

        def fake_urlopen(*args, **kwargs):
            return FakeResponse(response_data)

        mocker.patch(
            "claude_prompt_chains.llm.urllib.request.urlopen",
            side_effect=fake_urlopen,
        )

        result = client.send_prompt("Say hello")
        assert result == "Hello!"

    def test_send_prompt_with_system(self, mocker):
        client = ClaudeClient(api_key="sk-test")
        response_data = {
            "content": [{"type": "text", "text": "Ok"}],
        }

        def fake_urlopen(*args, **kwargs):
            return FakeResponse(response_data)

        mocker.patch(
            "claude_prompt_chains.llm.urllib.request.urlopen",
            side_effect=fake_urlopen,
        )

        result = client.send_prompt("Do it", system="Be helpful")
        assert result == "Ok"

    def test_api_error(self, mocker):
        client = ClaudeClient(api_key="sk-test")

        mocker.patch(
            "claude_prompt_chains.llm.urllib.request.urlopen",
            side_effect=urllib.error.URLError("Connection refused"),
        )

        with pytest.raises(ClaudeAPIError, match="Connection refused"):
            client.send_prompt("test")

    def test_http_error(self, mocker):
        client = ClaudeClient(api_key="sk-test")

        class FakeHTTPError:
            def __init__(self):
                self.code = 429

            def read(self):
                return b"Rate limited"
            def close(self):
                pass

        mocker.patch(
            "claude_prompt_chains.llm.urllib.request.urlopen",
            side_effect=urllib.error.HTTPError(
                "url", 429, "Too Many", {}, FakeHTTPError()
            ),
        )

        with pytest.raises(ClaudeAPIError, match="429"):
            client.send_prompt("test")
