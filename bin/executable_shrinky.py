#!/usr/bin/env python3
"""
Standalone script used to render PS1 parts and shortened folder names for tmux window names and shell prompts.
Must work fast, with system python, std libs only
"""

import os
import sys
from pathlib import Path


class Logger:
    log_location = "~/.cache/shrinky.log"
    logger = None

    @classmethod
    def enable_logging(cls):
        import logging

        logging.basicConfig(
            filename=os.path.expanduser(cls.log_location),
            datefmt="%m-%d %H:%M:%S",
            format="%(asctime)s [%(process)s] %(levelname)s %(message)s",
        )
        cls.logger = logging.getLogger(__name__)
        logging.root.setLevel(logging.DEBUG)
        cls.logger.setLevel(logging.DEBUG)

    @classmethod
    def debug(cls, message, *args):
        if cls.logger:
            cls.logger.debug(message, *args)

    @classmethod
    def fail(cls, msg, exit_code=1, exc_info=None):
        print(msg, file=sys.stderr)
        if cls.logger:
            cls.logger.error(msg, exc_info=exc_info)

        sys.exit(exit_code)


def run_program(*args: str):
    import subprocess

    Logger.debug("Running: %s", args)
    output = None
    try:
        p = subprocess.run(args, capture_output=True, shell=False, text=True)  # noqa: S603
        output = p.stdout and p.stdout.strip()
        Logger.debug("  stdout: %s", output)

    except Exception:
        return None

    else:
        return output


def get_path(path):
    if isinstance(path, Path):
        return path

    if path and path.startswith('"') and path.endswith('"'):
        path = path.strip('"')

    if path == "~":
        return Path(os.path.expanduser("~"))

    return Path(path or os.getcwd())


def get_py_venv_version(venv_path):
    """Fast Python Version detection without subprocess calls, looking for lib/pythonM.m"""
    lib_path = venv_path / "lib"
    if not lib_path.exists():
        return None

    py_dirs = [d.name for d in lib_path.iterdir() if d.name.startswith("python")]
    return (py_dirs and py_dirs[0].replace("python", "")) or None


def git_branch_name(folder):
    git_folder = git_root(folder)
    head_file = git_folder and git_folder / "HEAD"
    if not head_file or not head_file.exists():
        return None

    try:
        content = head_file.read_text().strip()
        if content.startswith("ref: "):
            return content.rpartition("/")[2]  # "ref: refs/heads/<branch-name>"

        return content[:5]  # Detached HEAD (SHA)

    except OSError:
        return None


def git_root(folder: Path):
    for parent in (folder, *folder.parents):
        folder = parent / ".git"
        if folder.is_dir():
            return folder


def scm_root(folder: Path):
    folder = git_root(folder)
    return folder and folder.parent


def capped_text(text: str, max_size: int):
    if max_size and text and len(text) > max_size:
        text = "𓈓%s" % text[-max_size:]

    return text


class ColorBit:
    def __init__(self, name, open_marker, close_marker, wrapper_fmt=None):
        self.name = name
        self.open_marker = open_marker
        self.close_marker = close_marker
        self.wrapper_fmt = wrapper_fmt

    def __repr__(self):
        return self.__call__(self.name)

    def wrapped(self, marker):
        if self.wrapper_fmt:
            marker = self.wrapper_fmt % marker

        return marker

    def __call__(self, text):
        open_marker = self.wrapped(self.open_marker)
        close_marker = self.wrapped(self.close_marker)
        return f"{open_marker}{text}{close_marker}"


class ColorSet:
    available = ("bold", "dim", "blue", "green", "yellow", "red", "cyan")  # magenta
    __ttyc = None  # type: ColorSet

    def __init__(self, name, bits):
        self.name = name
        self.bits = bits  # type: dict[str, ColorBit]
        self.bold = self.bits["bold"]
        self.dim = self.bits["dim"]
        self.blue = self.bits["blue"]
        self.green = self.bits["green"]
        self.yellow = self.bits["yellow"]
        self.red = self.bits["red"]
        self.cyan = self.bits["cyan"]

    @classmethod
    def ttyc(cls):
        if cls.__ttyc is None:
            cls.__ttyc = cls.tty_color_set()

        return cls.__ttyc

    @classmethod
    def tty_color_set(cls, name="tty-colors", wrapper_fmt=None):
        codes = {"bold": 1, "dim": 2, "blue": 34, "green": 32, "yellow": 33, "red": 31, "cyan": 36}
        code_format = "\x1b[%sm"
        bits = {}
        for color_name in cls.available:
            code = codes[color_name]
            clear = code_format % (39 if code > 9 else 22)
            bits[color_name] = ColorBit(color_name, code_format % code, clear, wrapper_fmt=wrapper_fmt)

        return cls(name, bits)

    @classmethod
    def color_set_by_name(cls, color_set_name):
        if color_set_name == "zsh":
            codes = {"bold": ("%B", "%b"), "dim": ("%{\x1b[2m%}", "%{\x1b[22m%}")}
            bits = {k: ColorBit(k, *codes.get(k, ("%%F{%s}" % k, "%f"))) for k in cls.available}
            return cls("zsh-ps1", bits)

        if color_set_name == "tty":
            return cls.ttyc()

        if color_set_name == "bash":
            return cls.tty_color_set(name="bash-ps1", wrapper_fmt="\\[%s\\]")

        if not color_set_name or color_set_name == "plain":
            return cls("plain", {k: ColorBit(k, "", "") for k in cls.available})

        Logger.fail("No color set for '%s'" % color_set_name)

    def __repr__(self):
        return self.name


def shortened_path(prefix, parts, max_parts=6):
    yield prefix
    if len(parts) > max_parts:
        yield "𓈓"
        parts = parts[-max_parts:]

    pivot = len(parts) - 2
    for i, part in enumerate(parts):
        if i < pivot:
            yield part[0] if part[0] != "." else part[0:2]

        else:
            yield part


def folder_parts(folder: Path):
    try:
        return "~", folder.relative_to(get_path("~")).parts

    except ValueError:
        return "", folder.parts[1:]


class CommandRenderer:
    flags = {}


class PathCleaner(CommandRenderer):
    flags = {"p": "path"}
    path = ""

    def cmd_clean_path(self):
        """Remove duplicates in PATH (but keep order)"""
        path = self.path or os.environ.get("PATH")
        seen = set()
        for folder in path.split(os.pathsep):
            folder = get_path(folder)
            if folder not in seen and folder.is_dir():
                yield str(folder)

            seen.add(folder)


class Ps1Renderer(CommandRenderer):
    dockerenv = "/.dockerenv"
    example = "ps1 -czsh -p.. -ozsimic,zoran -ufoo"
    flags = {"c": "color", "o": "owner", "p": "pwd", "u": "user", "v": "venv", "x": "exit_code"}

    color = ""
    exit_code = "0"
    owner = ""
    pwd = ""
    user = ""
    venv = ""

    def cmd_ps1(self):
        """
        PS1 minimalistic prompt
        """
        colors = ColorSet.color_set_by_name(self.color)
        if self.user == "root":
            yield "❕ "

        elif os.environ.get("CODER"):
            yield colors.cyan(" ")  #   

        elif os.environ.get("SSH_TTY"):
            yield colors.cyan(" ")  # 📡   󰑔  󰢹

        elif os.path.exists(self.dockerenv):
            yield "🐳 "

        if self.venv:
            venv = get_path(self.venv)
            activate = venv / "bin/activate"
            py_version = get_py_venv_version(venv)
            venv_name = None
            if activate.exists():
                import re

                regex = re.compile(r"""^\s*PS1="\(([\w-]+).+""")
                for line in activate.read_text().splitlines():
                    m = regex.match(line)
                    if m:
                        venv_name = m.group(1)

            if not venv_name:
                if venv.name == ".venv":
                    venv = venv.parent

                venv_name = venv.name

            venv_name = capped_text(venv_name, 24)
            py_version = capped_text(py_version, 5)
            yield "(%s %s) " % (colors.cyan(venv_name), colors.blue(py_version))

        if self.owner and self.user != "root":
            owners = self.owner.split(",")
            if self.user not in owners:
                yield "%s@" % colors.blue(self.user)

        if self.pwd:
            folder = get_path(self.pwd)
            prefix, parts = folder_parts(folder)
            short = "/".join(shortened_path(prefix, parts))
            dirname, _, basename = short.rpartition("/")
            if dirname:
                dirname += "/"

            yield colors.yellow(f"{colors.dim(dirname)}{basename}")

        if self.exit_code:
            color = colors.green if self.exit_code == "0" else colors.red
            char = color(" #" if self.user == "root" else ":")
            yield "%s " % char


class TmuxBranchSpec:
    def __init__(self, spec):
        self.spec = spec
        color, _, branches = spec.partition(":")
        self.icon = color and color[0]
        self.color = color and color[1:]
        self.branches = branches.split(",") if branches else None


class TmuxBranchSpecs:
    def __init__(self, specs):
        specs = specs or TmuxRenderer.branch_spec
        self.specs = specs.split("+")
        self.default = None
        self.by_branch = {}
        for spec in self.specs:
            spec = TmuxBranchSpec(spec)
            if spec.branches:
                for branch in spec.branches:
                    self.by_branch[branch] = spec

            else:
                self.default = spec

    def get_spec(self, branch):
        return self.by_branch.get(branch, self.default)


def rendered_uptime(stdout):
    i = stdout.index("up")
    stdout = stdout[i + 2 :].strip()
    up = list(uptime_bits(stdout))
    up = " ".join(up[:2])
    return "%s🔌" % tmux_colored(up or "-uptime?-", "default,dim", 10)  # 🕤⏳🪫🔋🔌


def tmux_colored(text, fg: str, max_size: int):
    text = capped_text(text, max_size)
    if fg:
        text = "#[fg=%s]%s#[default]" % (fg, text)

    return text


def uptime_bits(text):
    for bit in text.split(","):
        bit = bit.strip()
        if bit:
            if "user" in bit or "session" in bit or "load" in bit:
                return

            if ":" in bit:
                h, _, m = bit.partition(":")
                yield "%sh" % int(h)
                yield "%sm" % int(m)
                continue

            n, _, unit = bit.partition(" ")
            if n and unit:
                yield "%s%s" % (int(n), unit[0])


class TmuxRenderer(CommandRenderer):
    # Other icons: 🔀🧐🚨🚧📌🔧📄💡🍻🏷️💫🩹🎨
    branch_spec = "🔧magenta+✨cyan:main+🚨green:release,publish"
    path = ""
    flags = {"b": "branch_spec", "p": "path"}

    def rendered_branch(self, folder):
        branch_name = git_branch_name(folder)
        if not branch_name:
            return None

        specs = TmuxBranchSpecs(self.branch_spec)
        spec = specs.get_spec(branch_name)
        return spec and "%s%s" % (tmux_colored(branch_name, spec.color, 24), spec.icon)

    def cmd_tmux_status(self):
        """
        Status for tmux status-right part

        Example:
          set -g status-right '#(/usr/bin/python3 shrinky.py tmux_status -p"#{pane_current_path}")'
        """
        folder = get_path(self.path)
        if folder:
            yield self.rendered_branch(folder)

        uptime = run_program("uptime")
        if uptime and "up" in uptime:
            yield rendered_uptime(uptime)

    def cmd_tmux_short(self):
        """
        Short name to show for a given tmux window

        Example:
          setw -g automatic-rename-format '#(/usr/bin/python3 shrinky.py tmux_short -b📌yellow+✨blue,master,main -p"#{pane_current_path}")'
        """
        folder = get_path(self.path)
        if folder == get_path("~"):
            yield "~"
            return

        root = scm_root(folder)
        folder = folder.name if not root or folder == root else "%s/%s" % (root.name, folder.relative_to(root).name)
        yield capped_text(folder, max_size=20)


class CommandDef:
    def __init__(self, base_cls, name, delimiter):
        self.name = name
        self.base_cls = base_cls
        self.delimiter = delimiter

    def __repr__(self):
        return self.name

    def get_func(self, instance=None):
        func = getattr(instance or self.base_cls, "cmd_%s" % self.name)
        return func

    def get_doc(self):
        func = self.get_func()
        doc = func.__doc__ or "?"
        return doc

    def summary(self):
        return self.get_doc().strip().splitlines()[0]

    def run_with_args(self, args):
        instance = self.base_cls()
        for arg in args:
            if not arg or len(arg) <= 1 or not arg.startswith("-"):
                Logger.fail("Unrecognized argument '%s'" % arg)

            key = arg[1]
            value = arg[2:]
            flag = self.base_cls.flags.get(key)
            if not flag:
                Logger.fail("Unknown flag '%s'" % key)

            setattr(instance, flag, value)

        func = self.get_func(instance=instance)
        bits = list(func())
        response = self.delimiter.join(x for x in bits if x)
        Logger.debug("%s %s -> %s", self, args, response)
        print(response)

    def show_help(self):
        from textwrap import dedent

        doc = self.get_doc()
        doc = dedent(doc).strip()
        print("%s\n" % doc, file=sys.stderr)
        sys.exit(0)


class CommandParser:
    def __init__(self):
        self.available_commands = {}

    def add_command(self, cmd, delimiter=""):
        for k in dir(cmd):
            if k.startswith("cmd_"):
                name = k[4:]
                cmd_def = CommandDef(cmd, name, delimiter)
                self.available_commands[name] = cmd_def

    def get_command(self, name, fatal=True):
        cmd = self.available_commands.get(name)
        if cmd is None and fatal:
            Logger.fail("Unknown command '%s'" % name)

        return cmd

    def show_help(self, msg=None, exit_code=0):
        if msg:
            print(msg, file=sys.stderr)

        print("Usage: COMMAND [ARGS]...", file=sys.stderr)
        print(__doc__, file=sys.stderr)
        print("\nCommands:", file=sys.stderr)
        for name, cmd in sorted(self.available_commands.items()):
            print("  %s%s" % (ColorSet.ttyc().bold("%-18s" % name), cmd.summary()), file=sys.stderr)

        if exit_code is not None:
            sys.exit(exit_code)

    def run_args(self, args):
        if not args:
            self.show_help("No command provided", exit_code=1)

        cmd = args[0]
        args = args[1:]
        if cmd == "--help":
            self.show_help()

        if cmd in ("-v", "--debug"):
            cmd = args[0]
            args = args[1:]
            Logger.enable_logging()

        cmd = self.get_command(cmd)
        if "--help" in args:
            cmd.show_help()

        try:
            cmd.run_with_args(args)

        except Exception as e:
            Logger.fail("'%s()' crashed: %s" % (cmd.name, e), exc_info=e)


def main(args=None):
    parser = CommandParser()
    parser.add_command(PathCleaner, delimiter=os.pathsep)
    parser.add_command(Ps1Renderer)
    parser.add_command(TmuxRenderer, delimiter="┆")
    parser.run_args(args or sys.argv[1:])


if __name__ == "__main__":  # pragma: no cover
    main()
