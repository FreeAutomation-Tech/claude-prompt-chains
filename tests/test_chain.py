from claude_prompt_chains.chain import ChainExecutor


SAMPLE_CHAIN = {
    "name": "test",
    "description": "",
    "steps": [
        {"name": "summarize", "prompt": "Summarize: {{input}}"},
        {"name": "analyze", "prompt": "Analyze: {{steps.summarize}}"},
    ],
}


class TestChainExecutor:

    def test_run_executes_steps(self, mocker):
        mock_client = mocker.patch(
            "claude_prompt_chains.chain.ClaudeClient"
        )
        instance = mock_client.return_value
        instance.send_prompt.side_effect = [
            "Summary output",
            "Analysis output",
        ]

        executor = ChainExecutor(api_key="sk-test")
        results = executor.run(SAMPLE_CHAIN, input_text="Some input")

        assert results["summarize"] == "Summary output"
        assert results["analyze"] == "Analysis output"
        assert instance.send_prompt.call_count == 2

    def test_run_without_input(self, mocker):
        mock_client = mocker.patch(
            "claude_prompt_chains.chain.ClaudeClient"
        )
        instance = mock_client.return_value
        instance.send_prompt.return_value = "output"

        chain = {
            "name": "simple",
            "description": "",
            "steps": [
                {"name": "step1", "prompt": "Do something"},
            ],
        }

        executor = ChainExecutor(api_key="sk-test")
        results = executor.run(chain)
        assert results["step1"] == "output"

    def test_prompt_rendering(self, mocker):
        mock_client = mocker.patch(
            "claude_prompt_chains.chain.ClaudeClient"
        )
        instance = mock_client.return_value
        instance.send_prompt.side_effect = [
            "First result",
            lambda prompt: (
                "good" if "First result" in prompt else "bad"
            ),
        ]

        executor = ChainExecutor(api_key="sk-test")
        results = executor.run(SAMPLE_CHAIN, input_text="test")
        assert results["summarize"] == "First result"
        assert "First result" in results.get("analyze", "")
