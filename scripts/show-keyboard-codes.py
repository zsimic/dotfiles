import os
import select
import sys
import termios
import tty

fd = sys.stdin.fileno()
old = termios.tcgetattr(fd)
data = b""
print("Press key combo...")

try:
    tty.setcbreak(fd)
    if select.select([fd], [], [], 5)[0]:
        data += os.read(fd, 1)
        while select.select([fd], [], [], 0.05)[0]:
            data += os.read(fd, 1)

finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old)

print(repr(data), [hex(b) for b in data])
