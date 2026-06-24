import pytest


class TestCli:

    def test_chain_file_required(self, mocker):
        mocker.patch("sys.argv", ["claude-prompt-chains"])
        from claude_prompt_chains.cli import main
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code != 0

    def test_nonexistent_file(self, mocker):
        mocker.patch(
            "sys.argv",
            ["claude-prompt-chains", "nonexistent.yml"],
        )
        from claude_prompt_chains.cli import main
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code != 0
