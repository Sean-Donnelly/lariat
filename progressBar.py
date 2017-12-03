import sys
import time

def update_prog(total, progress):
    barLength, status = 20, ""
    progress = float(progress) / float(total)
    if progress >= 1.:
        progress, status = 1, "\r\n"
    block = int(round(barLength * progress))
    text = "\033[94m\r[{}] {:.0f}% {}\033[0m".format(
        "#" * block + "-" * (barLength - block), round(progress * 100, 0),
        status)
    if progress < 1:
        sys.stdout.write(text)
    if progress >= 1:
	pass
    sys.stdout.flush()

