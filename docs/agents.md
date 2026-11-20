# Agent instructions

A few lines every coding agent (claude, codex, opencode, pi) should know on these machines, kept as
small markdown fragments and rendered into each agent's global instructions file.

- **Fragments**: [`mix/agents/[0-9]*.md`](../mix/agents/), merged with the work overlay's (see
  [mix](./mix.md)): usually `00-dotfiles.md` here and `50-…` in the overlay.
- **Targets**: each agent's file (`~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`,
  `~/.config/opencode/AGENTS.md`, `~/.pi/agent/AGENTS.md`) is a one-line `.tmpl`, and
  [`.chezmoiignore`](../home/.chezmoiignore) skips agents that aren't installed (so after installing
  one, run `cz apply`).
- **On-demand docs**: un-numbered `mix/agents/*.md` are not rendered; reference them by path from a
  fragment in the same folder ("see `{here}/foo.md`") so agents read them only when relevant. `@` is
  avoided on purpose: claude would inline an `@path` reference into every session.

Keep it ruthlessly short: every line is loaded into every session of every agent.
