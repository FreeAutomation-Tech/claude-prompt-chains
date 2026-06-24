import argparse
import sys

from claude_prompt_chains.parser import parse_chain, ChainParseError
from claude_prompt_chains.chain import ChainExecutor


def main():
    parser = argparse.ArgumentParser(
        description="Run YAML-defined multi-step prompt chains with Claude"
    )
    parser.add_argument("chain_file", help="Path to YAML chain definition")
    parser.add_argument(
        "--input", "-i",
        help="Input text (or pipe via stdin)",
    )
    parser.add_argument(
        "--api-key",
        help="Anthropic API key (or set ANTHROPIC_API_KEY env var)",
    )
    parser.add_argument(
        "--model",
        default="claude-sonnet-4-20250514",
        help="Claude model to use",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=2048,
        help="Max tokens per step",
    )

    args = parser.parse_args()

    if args.input:
        input_text = args.input
    elif not sys.stdin.isatty():
        input_text = sys.stdin.read().strip()
    else:
        input_text = None

    try:
        chain = parse_chain(args.chain_file)
        executor = ChainExecutor(
            api_key=args.api_key,
            model=args.model,
            max_tokens=args.max_tokens,
        )
        results = executor.run(chain, input_text)
        for step_name, output in results.items():
            print(f"=== {step_name} ===")
            print(output)
            print()
    except (ChainParseError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
