from setuptools import setup, find_packages

setup(
    name="claude-prompt-chains",
    version="0.1.0",
    packages=find_packages("src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "claude-prompt-chains=claude_prompt_chains.cli:main",
        ],
    },
    python_requires=">=3.9",
    install_requires=["pyyaml"],
)
