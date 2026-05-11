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

        joined_bigrams = {f"{tokens[i]} {tokens[i+1]}" for i in range(len(tokens) - 1)}

        for emotion, keywords in self.lexicon.items():
            if keywords.intersection(tokens) or keywords.intersection(joined_bigrams):
                found.add(emotion)

        if not found:
            found.add("neutral")
        return found


def build_default_model() -> EmotionModel:
    # Expanded lexicon for 28 emotion labels.
    lexicon = {
        "admiration": {"admire", "admired", "admirable", "respect", "impressed", "inspiring", "brilliant"},
        "amusement": {"funny", "hilarious", "amusing", "laugh", "laughed", "lol", "entertaining"},
        "anger": {"angry", "furious", "rage", "enraged", "outraged", "irate", "hate"},
        "annoyance": {"annoyed", "irritated", "bothered", "frustrated", "fed up", "tired of", "aggravating"},
        "approval": {"approve", "approved", "agree", "acceptable", "good job", "well done", "support"},
        "caring": {"care", "caring", "compassion", "kind", "gentle", "sympathetic", "concerned"},
        "confusion": {"confused", "puzzled", "unclear", "lost", "bewildered", "perplexed", "mixed up"},
        "curiosity": {"curious", "wonder", "wondering", "interested", "intrigued", "explore", "question"},
        "desire": {"want", "wish", "desire", "crave", "longing", "hope for", "need"},
        "disappointment": {"disappointed", "let down", "underwhelmed", "missed", "unmet", "dissatisfied"},
        "disapproval": {"disapprove", "disliked", "wrong", "unacceptable", "against", "object", "disagree"},
        "disgust": {"disgusted", "gross", "nasty", "revolting", "sickening", "repulsive", "ew"},
        "embarrassment": {"embarrassed", "awkward", "ashamed", "humiliated", "cringe", "self-conscious"},
        "excitement": {"excited", "thrilled", "pumped", "eager", "can't wait", "stoked"},
        "fear": {"afraid", "scared", "fear", "terrified", "frightened", "worried", "anxious"},
        "gratitude": {"grateful", "thankful", "thanks", "appreciate", "appreciated", "blessed"},
        "grief": {"grief", "mourning", "bereaved", "devastated", "heartbroken", "loss"},
        "joy": {"happy", "joy", "delighted", "glad", "cheerful", "pleased", "wonderful"},
        "love": {"love", "adore", "cherish", "beloved", "affection", "romantic", "fond"},
        "nervousness": {"nervous", "tense", "jittery", "uneasy", "on edge", "restless"},
        "optimism": {"optimistic", "hopeful", "positive", "confident", "bright", "promising"},
        "pride": {"proud", "accomplished", "achievement", "honored", "dignified", "self-respect"},
        "realization": {"realize", "realized", "aware", "it dawned", "figured out", "understood"},
        "relief": {"relieved", "finally", "at last", "thank goodness", "unburdened", "reassured"},
        "remorse": {"remorse", "regret", "sorry", "apologize", "guilty", "ashamed of"},
        "sadness": {"sad", "down", "depressed", "unhappy", "sorrow", "cry", "lonely"},
        "surprise": {"surprised", "shocked", "amazed", "astonished", "unexpected", "wow"},
        "neutral": set(),
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
    for emotion in model.lexicon.keys():
        print(f"{emotion}\t{counts.get(emotion, 0)}")


if __name__ == "__main__":
    main()
