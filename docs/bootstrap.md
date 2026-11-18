# Bootstrap

1. On macOS, use an administrator account, without `sudo` for the whole run: the script asks for
   authorization for the first Homebrew install, and Homebrew may ask again when adopting apps already
   in `/Applications`.
2. Run [`bootstrap.sh`](../bootstrap.sh); it skips what is already installed, so rerun it after an
   interruption:

   ```zsh
   zsh -c "$(curl -fsSL https://raw.githubusercontent.com/zsimic/dotfiles/main/bootstrap.sh)"
   ```

3. Reload the shell with `exec zsh -l`, then check with `cz`.
4. On macOS, finish by hand (needs privileges chezmoi doesn't have):
   - Accessibility → Zoom: enable the trackpad and scroll-gesture modifier.

The final `chezmoi init --apply` only runs on personal machines; see [Reuse](./reuse/index.md) for
anyone else.
