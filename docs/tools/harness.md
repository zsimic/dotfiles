# Agent CLI harnesses

| Harness | Lang | License | GH Stars | Brew formula | Wins |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [opencode] 🪪 | TS | MIT | ~227k | opencode | Closest open-source spiritual successor to Claude Code, with Plan/Build modes and built-in LSP support. |
| [codex] 🪪 | Rust | Apache 2.0 | ~136k | codex 🛢️ | Best-in-class native sandboxing, git worktree isolation, and direct parity with your ChatGPT plan. |
| [pi] 🪪 | TS | MIT | ~113k | pi-coding-agent | Ultra-minimalist core (~1k token prompt) designed for radical customization via TypeScript extensions. |
| [cline] 🪪 | TS | Apache 2.0 | ~64k | cline-ai/tap/cline-cli | Granular human-in-the-loop governance with workspace checkpoints and `/undo` rollbacks. |
| [goose] | Rust | Apache 2.0 | ~56k | block-goose-cli | Fast, zero-dependency Rust binary backed by the Linux Foundation with deep MCP extension support. |
| [aider] | Python | Apache 2.0 | ~49k | aider | Unmatched Git workflow with AST repo-mapping and automatic atomic commits after every edit. |
| [antigravity] | TS / Go | Proprietary | ~3k | antigravity-cli 🛢️ | Official Google harness with native AI Pro OAuth, `/agents` subagent orchestration, and GUI session export. |

- 🪪 = Native ChatGPT subscription OAuth (no proxy)
- 🛢️ = brew cask

[opencode]: https://github.com/anomalyco/opencode
[codex]: https://github.com/openai/codex
[pi]: https://github.com/earendil-works/pi
[cline]: https://github.com/cline/cline
[goose]: https://github.com/aaif-goose/goose
[aider]: https://github.com/aider-ai/aider
[antigravity]: https://github.com/google-antigravity/antigravity-cli

## Token usage

[toktally] sums [ccusage] reports per model over a period (default: last 30 days) for every agent ccusage reports.
Rows are sorted by cost by default. Use `toktally -m` to sort by model name, or `toktally -mgpt` to also filter
to names containing `gpt`. Combine either with `-a codex,claude` to select agents. See `toktally --help` for options.
Token counts are shown with units (`146M`), cost in USD as ccusage computes it, colored green under $100,
yellow up to $200, red above (only on a terminal, `--color`/`--no-color` to force).

[toktally]: ../../home/bin/gremlins/executable_toktally
[ccusage]: https://github.com/ryoppippi/ccusage
