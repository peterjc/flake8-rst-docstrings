# -*- coding: utf-8 -*-
u"""This module has an explicit UTF-8 encoding and unicode docstring.

The following text is a short sentence in Japanese:

日本語にはひらがな、カタカナ、æåがあります。

Japanese has hiragana, katakana, and kanji.
"""
from __future__ import print_function


def hello_jp():
    """Return 'Hello' in Japanese ('こんにちは')."""
    return u"こんにちは"


__all__ = ("hello_jp",)  # single entry tuple


if __name__ == "__main__":
    print(hello_jp())
