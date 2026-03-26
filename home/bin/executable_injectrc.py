#!/usr/bin/env python3

import argparse
import os
import sys

PROGRAM_NAME = "injectrc.py"


class ShellRc:
    before_insertion = None  # type: list
    marked_contents = None  # type: list
    after_insertion = None  # type: list

    def __init__(self, target_path, snippet_contents, marker=None, comment=None, dryrun=False, verbose=False):
        """
        Args:
            target_path (str): Target file to modify (ex: ~/.bash_profile)
            snippet_contents (str): Example: "file:some-path" or "<some inlined content>"
            marker (str | None): Custom section marker to use in the file (by default: "injectrc.py")
            comment (str | None): Optional additional comment to add on the section marker line
            dryrun (bool): If True, no changes are done, a "Would update ..." is printed on stderr instead
            verbose (bool): If True, show all chatter on stderr
        """
        # All arguments are processed in some way, keep originally given values for logging and error reporting purposes
        self.given_target_path = target_path
        self.given_snippet_contents = snippet_contents
        self.given_marker = marker
        self.given_comment = comment
        self.dryrun = dryrun
        self.verbose = verbose
        self.target_path = os.path.expanduser(target_path)
        self.target_contents = self.file_contents(self.target_path)
        self.snippet_contents = self.resolved_snippet_contents(snippet_contents)
        self.marker_start = "## -- Added by %s --" % marker
        self.marker_end = "## -- end of addition by %s --" % marker
        if comment == "_default_":
            comment = "DO NOT MODIFY THIS SECTION"

        comment = self.splitlines(comment)
        if len(comment) > 1:
            line_count = len(comment)
            comment = "\n".join(comment)
            sys.exit("Provide maximum one line of comment, got %s lines:\n%s" % (line_count, comment))

        self.comment = comment[0] if comment else None

    def debug(self, message):
        if self.verbose:
            self.inform(message)

    def inform(self, message):
        """
        Args:
            message (str): Message to log on stderr
        """
        print(message, file=sys.stderr)

    def resolved_snippet_contents(self, snippet_contents):
        """
        Args:
            snippet_contents (str): Snippet to add, can be a "file:...", or "_empty_", or actual content

        Returns:
            (list[str]): Actual snippet contents
        """
        if not snippet_contents or snippet_contents == "_empty_":
            # "_empty_" can be used as a placeholder for asking to remove added snippet
            return []

        if snippet_contents.startswith("file:"):
            # Grab contents of stated file:
            return self.file_contents(snippet_contents[5:])

        if "\\n" in snippet_contents:
            snippet_contents = snippet_contents.replace("\\n", "\n")

        return self.splitlines(snippet_contents)

    @staticmethod
    def splitlines(text):
        """
        Args:
            text (str | list | None): Text to split

        Returns:
            (list): Meaningful/groomed lines from 'text'
        """
        return text.strip().splitlines() if text else []

    def file_contents(self, path):
        """
        Args:
            path (str): Path to file

        Returns:
            (list[str]): Contents of the file (list of lines)
        """
        path = os.path.expanduser(path)
        if not os.path.exists(path):
            return []

        with open(path) as fh:
            return self.splitlines(fh.read())

    def parse_target_contents(self):
        """Parse existing target file, recognize any already-existing section"""
        self.before_insertion = []
        self.marked_contents = []
        self.after_insertion = []
        accumulator = self.before_insertion
        for line in self.target_contents:
            if accumulator is self.after_insertion:
                accumulator.append(line)
                continue

            if line.startswith(self.marker_start):
                accumulator = self.marked_contents
                continue

            if line.startswith(self.marker_end):
                accumulator = self.after_insertion
                continue

            accumulator.append(line)

    def rendered_snippet(self, include_marker=True):
        """
        Args:
            include_marker (bool): Used for testing

        Returns:
            (list[str]): Rendered snippet, optionally with the section marker
        """
        result = []
        if self.snippet_contents:
            if include_marker:
                marker = self.marker_start
                if self.comment:
                    marker += " %s" % self.comment

                result.append(marker)

            result.extend(self.snippet_contents)
            if include_marker:
                result.append(self.marker_end)

        return result

    def rendered_target_contents(self):
        """
        Returns:
            (str): Rendered contents of target file (with snippet + its marker included)
        """
        result = []
        if self.before_insertion:
            result.extend(self.before_insertion)

        if self.snippet_contents and result and result[-1]:
            # Ensure an empty line is present before our insertion, for aeration
            result.append("")

        result.extend(self.rendered_snippet(include_marker=True))
        if self.after_insertion:
            if result and result[-1] and self.after_insertion and self.after_insertion[0]:
                # Ensure an empty line is present after our insertion, for aeration
                result.append("")

            result.extend(self.after_insertion)

        return "\n".join(result)

    def write_content(self, target_path, contents):
        """
        Args:
            target_path (str): Path to target file, example: ~/.bash_profile
            contents (str): Contents to write to the file
        """
        self.inform("Updating %s" % target_path)
        self.debug("Contents:\n%s" % contents)
        with open(target_path, "w") as fh:
            fh.write(contents)
            if contents and contents[-1] != "\n":
                fh.write("\n")

    def run_update(self, force=False):
        """
        Perform the actual update: inject snippet into the target file, in an idempotent manner

        Args:
            force (bool): If True, regenerate contents even if they didn't change

        Returns:
            (int): Exit code to report to calling shell
        """
        self.parse_target_contents()
        snippet_contents = self.rendered_snippet(include_marker=False)
        if not force and snippet_contents == self.marked_contents:
            self.inform("Section has not changed, not modifying '%s'" % self.given_target_path)
            return 0

        rendered_contents = self.rendered_target_contents()
        if self.dryrun:
            self.inform("[DRYRUN] Would update %s, contents:" % self.given_target_path)
            self.inform(rendered_contents)
            return 0

        # Write updated contents
        self.write_content(self.target_path, rendered_contents)
        return 0


def main(args=None):
    """Add a snippet to a bash/zsh/... shell rc file"""
    parser = argparse.ArgumentParser(prog=PROGRAM_NAME, description=main.__doc__)
    parser.add_argument("--dryrun", "-n", action="store_true", help="Perform a dryrun")
    parser.add_argument("--verbose", "-v", action="store_true", help="Be verbose")
    parser.add_argument("--force", "-f", action="store_true", help="Force update, even if not needed")
    parser.add_argument("--marker", "-m", default=PROGRAM_NAME, help="Marker to use to delimit our addition")
    parser.add_argument("--comment", "-c", default="_default_", help="Optional comment to add to the addition")
    parser.add_argument("target_path", help="Path to file to modify (ex: ~/.bash_profile)")
    parser.add_argument("snippet", help="Snippet to add to target file, or file:<path> (use contents of referred file:)")
    args = parser.parse_args(args)

    shell_rc = ShellRc(args.target_path, args.snippet, marker=args.marker, comment=args.comment, dryrun=args.dryrun, verbose=args.verbose)
    return shell_rc.run_update(force=args.force)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
