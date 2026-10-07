# coding: utf-8
"""ASCII animations for a friendly, magical CLI experience."""

from __future__ import annotations

import random
import time
from contextlib import contextmanager

from rich.console import Console
from rich.live import Live
from rich.text import Text

_STARS = ["✦", "✧", "⋆", "*", "·", ".", "+"]
_COLORS = ["bright_white", "yellow", "cyan", "magenta", "white", "bright_blue"]

_BANNER = [
    "   ✨  C Y B E R   A S T R A  ✨   ",
    "  🌙  seu mapa astral em poucos  ⭐ ",
    "         passos, sem mistério       ",
]


def _starfield_frame(width: int, height: int, tick: int) -> Text:
    """One frame of a twinkling starfield with the banner in the middle."""
    rng = random.Random(tick * 7919)  # deterministic-ish per tick
    text = Text()
    banner_start = (height - len(_BANNER)) // 2

    for row in range(height):
        for col in range(width):
            bi = row - banner_start
            if 0 <= bi < len(_BANNER):
                line = _BANNER[bi]
                pad = (width - len(line)) // 2
                if col == pad:
                    text.append(line, style="bold bright_magenta")
                    col += len(line) - 1  # skip banner chars
                    continue
                if pad < col < pad + len(line):
                    continue
            # star density ~7%, twinkle by regenerating per tick
            if rng.random() < 0.07:
                star = rng.choice(_STARS)
                color = rng.choice(_COLORS)
                text.append(star, style=color)
            else:
                text.append(" ")
        text.append("\n")
    return text


def twinkle_banner(console: Console, seconds: float = 1.8,
                   width: int = 68, height: int = 11) -> None:
    """Animated starfield banner. Skipped silently when not a TTY."""
    if not console.is_terminal:
        console.print("[bold magenta]" + "\n".join(_BANNER) + "[/]")
        return
    frames = int(seconds * 12)
    with Live(console=console, refresh_per_second=12,
              transient=True) as live:
        for tick in range(frames):
            live.update(_starfield_frame(width, height, tick))
            time.sleep(1 / 12)


@contextmanager
def stargazing(console: Console, message: str):
    """Spinner context with a cosmic flavor while something computes."""
    if console.is_terminal:
        with console.status(f"[cyan]{message}[/]", spinner="moon",
                            spinner_style="bright_magenta"):
            yield
    else:
        console.print(f"[dim]{message}[/]")
        yield


def reveal_lines(console: Console, text: str, delay: float = 0.012) -> None:
    """Print text line by line, like the chart drawing itself."""
    if console.is_terminal:
        for line in text.splitlines():
            console.print(line, highlight=False)
            time.sleep(delay)
    else:
        console.print(text, highlight=False)
