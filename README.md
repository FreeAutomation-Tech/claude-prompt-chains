# claude-prompt-chains

YAML-defined multi-step prompt pipelines for Claude. Output of one step feeds into the next.

## Installation

```bash
pip install claude-prompt-chains
```

## Usage

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
claude-prompt-chains chain.yml --input "Some text to process"
```

### Chain file format

```yaml
name: analyze-document
description: Analyze and summarize text
steps:
  - name: summarize
    prompt: "Summarize the following:\n\n{{input}}"

  - name: key_points
    prompt: "Extract key points from:\n\n{{steps.summarize}}"

  - name: final
    prompt: "Write a conclusion based on:\n\n{{steps.key_points}}"
```

### Variables

| Variable | Description |
|----------|-------------|
| `{{input}}` | The initial input text |
| `{{steps.step_name}}` | Output from a previous step |
| `{{env.VAR}}` | Environment variable |

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--input`, `-i` | stdin | Input text |
| `--api-key` | `ANTHROPIC_API_KEY` env var | Anthropic API key |
| `--model` | `claude-sonnet-4-20250514` | Claude model |
| `--max-tokens` | 2048 | Max tokens per step |

## Disclaimer

Provided for educational and research purposes.
