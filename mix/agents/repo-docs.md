# Repo docs

Repo docs live in `docs/`: a concise, interlinked map for the coding agent about to edit the repo and
for its maintainers. Architecture, cross-file flows, the "why", gotchas, where to start reading.
User-facing reference belongs in the `README.md` (the one a package index renders, so no links to repo
files there).

## Code is the authority

- A page says **where to look** and **what is surprising once there**; it never restates what one file
  already says plainly. Point at the source instead ("see `--help`", "in `pyproject.toml`").
- Cut any line that would go stale on a behavior-preserving refactor, or that a reader rebuilds in ten
  seconds from the file. Never paste generated output (`--help`, API dumps): it drifts like code.
- Keep what no single file tells: cross-file flows, why a weird thing is that way, footguns, entry
  points, findings that took an experiment to establish, and approaches tried and rejected (with why,
  so nobody retries them). A repo that holds domain state and will grow also gets an object-model
  page, see [`code-design.md`](./code-design.md).
- Verify every fact against the code; never trust existing docs. Don't describe unimplemented designs
  as behavior (a short "known gaps" page is fine).
- Reader-test before finishing: give a fresh subagent (no context) only the docs and 3-5 realistic
  questions; fix whatever it gets wrong, has to guess, or needs from outside the docs.

## Shape

- `docs/index.md`: strong overview, then relative links to the pages.
- One concept per file (`<concept>.md`), at most one level of subfolders, each with its own small
  `index.md`. A folder appears when it has real content, not before.
- Pages of 20-40 lines; past ~50 a page is usually carrying something the code should own. Cut
  trivial snippets, enumerations a tool already prints, headers that only introduce the next
  paragraph, and recaps of linked pages.
- Plain `# H1` title, no frontmatter. Relative links written to the `.md` file, never leading `/`.
- `docs/README.md`: two lines pointing to `index.md` (GitHub renders `README.md` when browsing a folder).
- Code blocks in `.md` must be lint-clean: formatters like `ruff format` reach into them.

## Around `docs/`

- `AGENTS.md` is a thin pointer: one or two sentences on what the repo is, a link to `docs/index.md`,
  then a few working notes that change what you'd write (language version, preferred libs, anything a
  linter won't catch). No preview of the docs, no duplicated facts.
- Word links agents should follow as triggers ("read `docs/x.md` before changing Y"): the wording, not
  the target, decides when they get read. State the wanted behavior rather than a prohibition.
- `CHANGELOG.md` stays at the repo root, [Keep a Changelog](https://keepachangelog.com) style
  (`## <version> - <date>`, then `### Added` / `### Changed` / `### Fixed`); docs link up to it.
- Spec, plan or notes files: give each fact one home in `docs/`, delete the originals, fix the links.
- Every fact lives in one place. Almost every edit that removes something makes the docs better.
