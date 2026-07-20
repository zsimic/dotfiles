# Bootstrap

Fresh-machine checklist:

1. On macOS, use an administrator account. Do not run the whole bootstrap with `sudo`.
2. Run:

   ```zsh
   zsh -c "$(curl -fsSL https://raw.githubusercontent.com/zsimic/dotfiles/main/bootstrap.sh)"
   ```

3. Let Homebrew and chezmoi finish, then reload the shell: `exec zsh -l`, verify with `cz`

On macOS, the script requests administrator authorization for the first Homebrew install. Homebrew
may ask again when adopting applications already in `/Applications`.

4. Manual additional steps on mac (can't be automated without privs)

- Accessibility
  - Zoom -> enable trackpad + scroll gesture modifier
