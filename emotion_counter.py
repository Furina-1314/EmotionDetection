#!/usr/bin/env python3
"""Detect emotions from newline-separated English comments and count frequencies.

Usage:
  python emotion_counter.py --file comments.txt
  cat comments.txt | python emotion_counter.py
"""

from __future__ import annotations

import argparse
import re
from collections import Counter
from dataclasses import dataclass
from typing import Dict, Iterable, List, Set

WORD_RE = re.compile(r"[a-z']+")


@dataclass(frozen=True)
class EmotionModel:
    lexicon: Dict[str, Set[str]]

    def detect(self, text: str) -> Set[str]:
        tokens = WORD_RE.findall(text.lower())
        found: Set[str] = set()

        # Support simple two-word patterns first (e.g. "fed up").
        joined_bigrams = {f"{tokens[i]} {tokens[i+1]}" for i in range(len(tokens) - 1)}

        for emotion, keywords in self.lexicon.items():
            if keywords.intersection(tokens) or keywords.intersection(joined_bigrams):
                found.add(emotion)

        return found


def build_default_model() -> EmotionModel:
    # Small interpretable lexicon; one comment may map to multiple emotions.
    lexicon = {
        "joy": {"happy", "joy", "delighted", "great", "awesome", "love", "excited", "glad"},
        "sadness": {"sad", "depressed", "down", "heartbroken", "cry", "lonely", "upset"},
        "anger": {"angry", "mad", "furious", "annoyed", "hate", "outraged", "fed up"},
        "fear": {"afraid", "scared", "anxious", "nervous", "worried", "terrified"},
        "surprise": {"surprised", "shocked", "amazed", "unexpected", "wow"},
        "disgust": {"disgusted", "gross", "nasty", "revolting", "sickening"},
    }
    return EmotionModel(lexicon=lexicon)


def read_comments(path: str | None) -> List[str]:
    if path:
        with open(path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f]
    else:
        import sys

        lines = [line.strip() for line in sys.stdin]

    return [line for line in lines if line]


def analyze_comments(comments: Iterable[str], model: EmotionModel) -> Counter:
    counter: Counter = Counter()
    for comment in comments:
        emotions = model.detect(comment)
        for emotion in emotions:
            counter[emotion] += 1
    return counter


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Read newline-separated English comments, detect emotions per comment, and count frequencies."
    )
    parser.add_argument("--file", "-f", help="Input file path. If omitted, read from stdin.")
    args = parser.parse_args()

    comments = read_comments(args.file)
    model = build_default_model()
    counts = analyze_comments(comments, model)

    if not comments:
        print("No comments found.")
        return

    print("emotion\tcount")
    for emotion in sorted(model.lexicon.keys()):
        print(f"{emotion}\t{counts.get(emotion, 0)}")


if __name__ == "__main__":
    main()
