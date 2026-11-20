# Mix

[`mix`](../home/.chezmoitemplates/mix) renders one target from numbered fragments kept in both dotfiles
repos, so the work overlay can extend a file this repo owns (chezmoi can't merge two sources on its own,
see [reuse](./reuse/index.md)).

- **Fragments**: `mix/<name>/[0-9]*` at the root of this repo and, optionally, of the work overlay at
  `~/.local/share/chezmoi`. Usually `00-…` here and `50-…` there. Other files in `mix/<name>/` are not
  rendered, they can be referenced from fragments (e.g. [agents](./agents.md)' on-demand docs).
- **Target**: a one-line `.tmpl`: `{{ template "mix" "<name>" }}`.
- **Rendering**: fragments sorted by file name, each trimmed, separated by a blank line; a same-named
  overlay fragment replaces the base one. `{here}` renders as the absolute path of the fragment's folder.
- **Apply order doesn't matter**: the template reads the overlay checkout directly. Deleting a fragment
  drops it on the next apply.
- `mix/` is outside the chezmoi source root (`.chezmoiroot` is `home`), so chezmoi never deploys or
  parses it: fragments are included verbatim.

| `<name>` | Target |
| --- | --- |
| `agents` | Every coding agent's global instructions, see [agent instructions](./agents.md) |
| `gh-hosts` | `~/.config/gh/hosts.yml`: `github.com` here, the work hosts in the overlay |
