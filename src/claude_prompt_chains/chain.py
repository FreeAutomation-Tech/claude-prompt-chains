from claude_prompt_chains.parser import render_prompt
from claude_prompt_chains.llm import ClaudeClient


class ChainExecutor:

    def __init__(self, api_key=None, model=None, max_tokens=None):
        self.claude = ClaudeClient(
            api_key=api_key,
            model=model,
            max_tokens=max_tokens,
        )

    def run(self, chain, input_text=None):
        context = {}
        if input_text is not None:
            context["input"] = input_text

        results = {}
        for step in chain["steps"]:
            step_context = dict(context)
            step_context["steps"] = results
            rendered = render_prompt(step["prompt"], step_context)
            output = self.claude.send_prompt(rendered)
            results[step["name"]] = output

        return results
