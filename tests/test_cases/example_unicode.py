# -*- coding: utf-8 -*-
u"""This module has an explicit URF-8 encoding and unicode docstring.

The following text is a short sentence in Japanese:

日本語にはひらがな、カタカナ、æåがあります。

Japanese has hiragana, katakana, and kanji.
"""

from __future__ import print_function


def hello_jp():
    """Return 'Hello' in Japanese ('こんにちは')."""
    return u"こんにちは"


if __name__ == "__main__":
    print(hello_jp())
