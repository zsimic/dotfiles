# Claude Code

## Status line

[`shrinky claude_statusline`](../home/bin/gremlins/executable_shrinky) renders: 🫥 when thinking is off,
model (effort), ⚡ in fast mode, context size, 5h/7d usage limits left with their reset times, session cost and
duration. Not managed by chezmoi (work has its own status line): add it manually to `~/.claude/settings.json` on
personal machines:

```json
"statusLine": {"type": "command", "command": "/usr/bin/python3 ~/bin/gremlins/shrinky claude_statusline"}
```

Claude Code runs the command on events (new assistant message, `/compact`, permission or vim mode change, a
limit's `resets_at`…), debounced at 300ms, and cancels a still-running one when a new update comes in.
`refreshInterval` (seconds) also re-runs it on a timer, so the session duration keeps ticking while idle. See the
[status line docs][statusline].

Context is shown as a token count rather than a percentage (10% of a 1M window is already ~100k tokens re-read on
every turn): yellow from 150k, red from 300k, as a nudge to start a new session. 🧊 flags a cold prompt cache (it
expires 1h after the last request) on a big context: the next message re-sends all of it at full price, a good
moment to `/clear`. Thresholds are `ClaudeRenderer` class attributes.

Thinking can't be turned off on recent models (Opus/Sonnet/Haiku 5.5, Fable): `thinking.enabled` stays `true`
there, `/effort` is the knob that matters (see [model config][model-config]). Hence only "thinking off" is shown.

Try it, from the repo root:

```shell
/usr/bin/python3 home/bin/gremlins/executable_shrinky claude_statusline -itests/samples/claude-statusline.json
```

The sample is a [real capture], also used by the tests.

There's no `claude ...` invocation that prints this payload: Claude Code builds it in interactive sessions only.
To capture the real one, `tee` it, then replay with `-i`:

```json
"statusLine": {"type": "command",
  "command": "tee ~/.cache/claude-statusline.json | /usr/bin/python3 ~/bin/gremlins/shrinky claude_statusline"}
```

Payload received on stdin (as of Claude Code 2.1.330, see the [real capture]; `tee` one for newer versions):

| Key | Contents |
| --- | --- |
| `model` | `id`, `display_name` |
| `effort` | `level` |
| `thinking` | `enabled` |
| `fast_mode` | bool |
| `context_window` | `used_percentage`, `remaining_percentage`, `context_window_size`, `total_input_tokens`, |
| | `total_output_tokens`, `current_usage` (input, output, cache creation/read tokens) |
| `exceeds_200k_tokens` | bool |
| `rate_limits` | `five_hour` / `seven_day`: `used_percentage`, `resets_at` (epoch seconds) |
| `cost` | `total_cost_usd`, `total_duration_ms`, `total_api_duration_ms`, `total_lines_added`, |
| | `total_lines_removed` |
| `prompt_cache` | `warm`, `ttl`, `expires_at`, `hit_ratio`, `requests`, `misses`, miss causes, |
| | `recache_tokens_if_cold` |
| `workspace` | `current_dir`, `project_dir`, `added_dirs` |
| session info | `session_id`, `session_name`, `prompt_id`, `transcript_path`, `cwd`, `scratchpad_dir`, |
| | `version`, `output_style.name` |

## Managing a few keys of `settings.json` with chezmoi

Claude Code rewrites `~/.claude/settings.json` itself (`/config`, permission prompts…), so a regular managed
file would fight it. A chezmoi [`modify_` template][modify] gets the current content on stdin and outputs the new
one, setting only the listed keys. As `home/dot_claude/modify_settings.json`:

```
{{- /* chezmoi:modify-template */ -}}
{{- /* Claude Code rewrites settings.json itself (e.g. /config), so only the keys below are managed */ -}}
{{  fromJson (.chezmoi.stdin | default "{}")
    | setValueAtPath "statusLine" (dict
        "type" "command"
        "command" "/usr/bin/python3 ~/bin/gremlins/shrinky claude_statusline")
    | toPrettyJson "  " -}}
```

Caveats: keys come out sorted alphabetically (one-time reorder on first apply), and the `-}}` avoids a trailing
blank line. Not used here since it would also apply on work machines, which have their own status line.

[modify]: https://www.chezmoi.io/user-guide/manage-different-types-of-file/#handle-configuration-files-which-are-externally-modified
[model-config]: https://code.claude.com/docs/en/model-config.md
[real capture]: ../tests/samples/claude-statusline.json
[statusline]: https://code.claude.com/docs/en/statusline.md
