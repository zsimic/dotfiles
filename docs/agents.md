# Agent instructions

A few lines every coding agent (claude, codex, opencode, pi) should know on these machines, kept as
small markdown fragments and rendered into each agent's global instructions file.

- **Fragments** are `agents/[0-9]*.md` at the root of each dotfiles repo (this one, plus an optional
  overlay at `~/.local/share/chezmoi`, see [work overlay](./reuse/work-overlay.md)). They are not
  under `home/`, so chezmoi never deploys them individually.
- **Rendering**: [`agents.md`](../home/.chezmoitemplates/agents.md) concatenates all fragments
  from both repos, sorted by file name; a same-named overlay fragment replaces the base one. Each
  agent's file (`~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, `~/.config/opencode/AGENTS.md`,
  `~/.pi/agent/AGENTS.md`) is a one-line `.tmpl` including it, and
  [`.chezmoiignore`](../home/.chezmoiignore) skips agents that aren't installed (so after installing
  one, run `cz apply`).
- **Order**: the number only sets the merge order; usually one fragment per repo, `00-dotfiles.md`
  here and `50-…` in the overlay.
- **On-demand docs**: an un-numbered `agents/*.md` is not rendered; reference it by path from a
  fragment ("see `{dotfiles}/agents/foo.md`") so agents read it only when relevant. `{dotfiles}`
  renders as the absolute path of the fragment's own repo (`@` is avoided on purpose: claude would
  inline an `@path` reference into every session).
- **Removal needs nothing**: the output is derived, so deleting a fragment drops it on next apply.
  The personal templates read the overlay checkout directly, so apply order doesn't matter.

Keep it ruthlessly short: every line is loaded into every session of every agent.
