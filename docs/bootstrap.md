# Bootstrap

Fresh-machine checklist:

1. On macOS, use an administrator account. Do not run the whole bootstrap with `sudo`.
2. Run:

   ```zsh
   zsh -c "$(curl -fsSL https://raw.githubusercontent.com/zsimic/dotfiles/main/bootstrap.sh)"
   ```

3. Let Homebrew and chezmoi finish, then reload the shell:

   ```zsh
   exec zsh -l
   ```

4. Verify:

   ```zsh
   command -v brew chezmoi
   chezmoi status
   ```

On macOS, the script requests administrator authorization for the first Homebrew install. Homebrew
may ask again when adopting applications already in `/Applications`.

If an apply is interrupted:

```zsh
chezmoi apply
```

To retry only the package manifest:

```zsh
brew bundle install --file="$HOME/.config/homebrew/Brewfile"
```
