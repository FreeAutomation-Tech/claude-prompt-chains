import tempfile
import os

import pytest

from claude_prompt_chains.parser import parse_chain, render_prompt, ChainParseError


SAMPLE_CHAIN = """
name: test-chain
description: A test chain
steps:
  - name: summarize
    prompt: "Summarize: {{input}}"
  - name: analyze
    prompt: "Analyze: {{steps.summarize}}"
"""


class TestParseChain:

    def test_parse_valid_yaml(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yml", delete=False
        ) as f:
            f.write(SAMPLE_CHAIN)
            path = f.name
        try:
            chain = parse_chain(path)
            assert chain["name"] == "test-chain"
            assert len(chain["steps"]) == 2
            assert chain["steps"][0]["name"] == "summarize"
        finally:
            os.unlink(path)

    def test_parse_empty_file(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yml", delete=False
        ) as f:
            f.write("")
            path = f.name
        try:
            with pytest.raises(ChainParseError, match="mapping"):
                parse_chain(path)
        finally:
            os.unlink(path)

    def test_parse_no_steps(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yml", delete=False
        ) as f:
            f.write("name: empty")
            path = f.name
        try:
            with pytest.raises(ChainParseError, match="at least one step"):
                parse_chain(path)
        finally:
            os.unlink(path)

    def test_parse_step_no_prompt(self):
        yaml = """
steps:
  - name: broken
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yml", delete=False
        ) as f:
            f.write(yaml)
            path = f.name
        try:
            with pytest.raises(ChainParseError, match="no prompt"):
                parse_chain(path)
        finally:
            os.unlink(path)

    def test_parse_invalid_step_type(self):
        yaml = """
steps:
  - "just a string"
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yml", delete=False
        ) as f:
            f.write(yaml)
            path = f.name
        try:
            with pytest.raises(ChainParseError, match="mapping"):
                parse_chain(path)
        finally:
            os.unlink(path)


class TestRenderPrompt:

    def test_simple_variable(self):
        result = render_prompt("Hello {{name}}", {"name": "World"})
        assert result == "Hello World"

    def test_nested_variable(self):
        context = {"steps": {"summary": "Some text"}}
        result = render_prompt("Result: {{steps.summary}}", context)
        assert result == "Result: Some text"

    def test_missing_variable(self):
        result = render_prompt("Hello {{unknown}}", {})
        assert result == "Hello "

    def test_no_variables(self):
        result = render_prompt("Static text", {})
        assert result == "Static text"

    def test_multiple_variables(self):
        context = {"a": "1", "b": "2"}
        result = render_prompt("{{a}} + {{b}}", context)
        assert result == "1 + 2"
