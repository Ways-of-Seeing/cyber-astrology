# coding: utf-8
"""
ASCII art gallery for Cyber Astra.

Every run picks a random piece per context, so each execution feels
like a slightly different sky. Keep pieces ≤ ~62 columns wide so they
fit nicely inside 80-col terminals.
"""

from __future__ import annotations

import os
import random
import time

_rng = random.Random(time.time_ns() ^ os.getpid())

# ── Splashes de abertura (grandes) ───────────────────────────────────────────

SPLASH_ARTS: list[list[str]] = [
    # Lua cheia em blocos
    [
        "             ✦  .  *        .",
        "        .          ██████",
        "    *        ████░░░░████       ✦",
        "  .       ██░░░░░░░░░░░░██   .",
        "         ██░░░░░░░░░░░░░░██        *",
        "    ✦   ██░░░░░░░░░░░░░░░░██   .",
        "  .     ██░░░░░░░░░░░░░░░░██",
        "        ██░░░░░░░░░░░░░░██      ✦",
        "    *     ██░░░░░░░░░░██    .",
        "  .         ████░░████          *",
        "        ✦      ████      .",
    ],
    # Bola de cristal
    [
        "        .    *        ✦        .",
        "    *          .  .:::::::.  .     *",
        "   .        ✦  .:::::::::::::.   .",
        "        .     ::::   ✦   ::::      ✦",
        "    ✦    .   :::   ✧   *  :::   .",
        "   .         :::  *  ✦    :::  .",
        "        .    ::::  ✦     ::::     *",
        "    *     ✦   ':::::::::::::'   .",
        "   .      .     ':::::::'   .",
        "        *       __||__         ✦",
        "    .      ✦   (______)    .     .",
    ],
    # Roda do zodíaco
    [
        "    .       *        ✦        .     *",
        "        ✦       .-~~~~~~~~~-.   .",
        "   .       .  ~  ♈ ♉ ♊ ♋  ~   .",
        "    *      .  ~ ♓         ♌ ~   .",
        "   .     .  ~ ♒     ✦      ♍ ~     .",
        "        .  ~ ♒   ✧  ☾  ✧  ♎ ~   .",
        "   .     .  ~ ♑     ✦      ♏ ~   .",
        "    *      ~  ♑         ♐ ~      .",
        "   .       ~  ♑ ♐ ♏ ♐  ~    ✦",
        "        .     '-~~~~~~~~~-'    .",
        "    ✦    .        *      .        *",
    ],
    # Montanhas sob as estrelas
    [
        "    *        .        ✦         .",
        "  .      ✦      .        *",
        "        .         .  *       ✦      .",
        "    ✦      *            .        *",
        "   .          /\\            .       .",
        "      .      /  \\   /\\   ✦",
        "   *        /    \\ /  \\    .    *",
        "  .    ✦   /      v    \\  .",
        "   .      /            \\     .   ✦",
        "        * /______________\\       .",
        "   .  ✦    n  n  n  n       ✦",
    ],
    # Gato cósmico
    [
        "        .      *       ✦      .",
        "    *      /\\_____/\\       .       *",
        "   .      /  o   o  \\    .    ✦",
        "        .|    ▽     |  .         .",
        "    ✦     \\  ___  /    .    *",
        "   .    .  \\/   \\/   ✦     .",
        "        *  /|   |\\      .        ✦",
        "   .      / |   | \\   .      .",
        "    *    ✦  | ✧ |      .     *",
        "   .    .   |___|    ✦     .",
    ],
    # Telescópio
    [
        "        ✦        .        *        .",
        "   .        *        ✦        .",
        "              .  *      .          ✦",
        "                      ▄▄▄▄",
        "    ✦        .     ▄█▀▀▀▀█▄    .",
        "        .         █▌  ☾   ▐█",
        "    *      .      █▌      ▐█    .",
        "   .        ✦     █▌     ▄█▀      .",
        "        .      ▄▄▄█▌▄▄▄██▀   *",
        "    ✦         ▀▀▀▀█▌▀▀▀▀     .",
        "   .        .    █▌    .         ✦",
        "        *       ▄█▄        .",
        "   .           ▀▀▀     *      .",
    ],
]

# ── Artes de seção/funcionalidade (compactas) ────────────────────────────────

SECTION_ARTS: dict[str, list[list[str]]] = {
    "chart": [
        [
            "        ✦   .-~~~~~~~~~-.",
            "      .  ~  ♈   ☾   ♌  ~",
            "        ~ ♒   ✦      ♍ ~",
            "      .  ~  ♑   ♃   ♐  ~   .",
            "           '-~~~~~~~~~-'",
        ],
        [
            "      ☾        ✦        *",
            "         .        .",
            "    *     ┌─────────┐    .",
            "    .     │  ☉  ☽  │  ✦",
            "     ✦    │  ♀  ♂  │    .",
            "      .   └─────────┘       *",
        ],
    ],
    "synastry": [
        [
            "      .::::.   .::::.",
            "     :::::::. :::::::.",
            "     :::::::::::::::::",
            "     ':::::::::::::'",
            "       ':::::::::'",
            "         ':::'",
            "           '",
        ],
        [
            "     ✦        .        ✦",
            "    ☾    ✧  ~ ~ ~  ✧    ☽",
            "      .      ~ ~      .",
            "    *        \\/        *",
            "      .      \\/      .",
        ],
    ],
    "help": [
        [
            "        ✦     _____     *",
            "      .      /     \\   .",
            "    *       | (?)  |      ✦",
            "      .      \\___ _/   .",
            "        ✦       |/        .",
            "       .        ●    *",
        ],
    ],
    "exit": [
        [
            "      ✦        .        ☾",
            "    .      *        .       .",
            "        .      ✦       *",
            "   *     .        .       ✦",
            "      .       .      .     .",
        ],
    ],
    "wheel": [
        [
            "         .-~~~~~~~-.",
            "       ~  ♈  ☾  ♌  ~",
            "      ~ ♒   ✦    ♍ ~",
            "       ~  ♑  ♃  ♐  ~",
            "         '-~~~~~~~-'",
        ],
    ],
    "planets": [
        [
            "      ✦      ___",
            "     .     _/   \\_    .",
            "    *     | (•) |  *",
            "    .   _/|     |\\_  .",
            "    ✦  /__|_____|__\\",
            "   .      /     \\    .",
        ],
    ],
    "synthesis": [
        [
            "        ✦       *",
            "      .    \\  |  /    .",
            "    *    —  ✦✧✦  —      ✦",
            "      .    /  |  \\    .",
            "        *       ✦",
        ],
    ],
    "aspects": [
        [
            "    ✦        *",
            "     \\      /  \\",
            "      *----✦    ✦    .",
            "     /      \\  /  *",
            "    ✦        ✦      .",
        ],
    ],
    "houses": [
        [
            "          /\\",
            "         /  \\      ✦",
            "        /____\\",
            "       | []  |    .",
            "      _| []  |_  *",
        ],
    ],
}


def splash() -> list[str]:
    """Random splash art for CLI startup."""
    return _rng.choice(SPLASH_ARTS)


def section(key: str) -> list[str]:
    """Random art for a report section or menu feature."""
    arts = SECTION_ARTS.get(key)
    return _rng.choice(arts) if arts else []


def render(lines: list[str], style: str = "bright_magenta") -> str:
    """Art lines → Rich-markup string."""
    return f"[{style}]" + "\n".join(lines) + "[/]"
