#!/usr/bin/env python3
"""Detect emotions from newline-separated English comments and count frequencies."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from dataclasses import dataclass
from typing import Dict, Iterable, List, Set

WORD_RE = re.compile(r"[a-z']+")


COMMON_SUFFIXES = ("ing", "ed", "ly", "ness", "ment", "tion", "s")


def normalize_token(token: str) -> str:
    """Lightweight normalization to improve hit rate without extra dependencies."""
    t = token.lower().strip("'")
    if len(t) <= 3:
        return t

    # Handle common contractions.
    if t.endswith("n't"):
        t = t[:-3]

    # Simple suffix stripping.
    for suffix in COMMON_SUFFIXES:
        if len(t) > len(suffix) + 2 and t.endswith(suffix):
            t = t[: -len(suffix)]
            break
    return t


def expand_keywords(raw_keywords: Set[str]) -> Set[str]:
    expanded: Set[str] = set()
    for kw in raw_keywords:
        kw = kw.lower()
        expanded.add(kw)
        if " " not in kw:
            expanded.add(normalize_token(kw))
    return expanded


@dataclass(frozen=True)
class EmotionModel:
    lexicon: Dict[str, Set[str]]

    def detect(self, text: str) -> Set[str]:
        raw_tokens = WORD_RE.findall(text.lower())
        tokens = [normalize_token(tok) for tok in raw_tokens]
        found: Set[str] = set()

        raw_bigrams = {f"{raw_tokens[i]} {raw_tokens[i+1]}" for i in range(len(raw_tokens) - 1)}
        norm_bigrams = {f"{tokens[i]} {tokens[i+1]}" for i in range(len(tokens) - 1)}

        for emotion, keywords in self.lexicon.items():
            if keywords.intersection(raw_tokens) or keywords.intersection(tokens):
                found.add(emotion)
                continue
            if keywords.intersection(raw_bigrams) or keywords.intersection(norm_bigrams):
                found.add(emotion)

        if not found:
            found.add("neutral")
        return found


def build_default_model() -> EmotionModel:
    raw_lexicon = {
        "admiration": {"admire", "admirable", "respect", "impressed", "inspiring", "brilliant", "excellent"},
        "amusement": {"funny", "hilarious", "amusing", "laugh", "lol", "lmao", "entertaining", "joke"},
        "anger": {"angry", "furious", "rage", "enraged", "outraged", "irate", "hate", "fuming"},
        "annoyance": {"annoy", "irritat", "bother", "frustrat", "fed up", "tired of", "aggravat"},
        "approval": {"approve", "agree", "acceptable", "good job", "well done", "support", "solid"},
        "caring": {"care", "compassion", "kind", "gentle", "sympathetic", "concern", "thoughtful"},
        "confusion": {"confus", "puzzl", "unclear", "lost", "bewilder", "perplex", "mixed up"},
        "curiosity": {"curious", "wonder", "interest", "intrigu", "explore", "question"},
        "desire": {"want", "wish", "desire", "crave", "longing", "hope for", "need"},
        "disappointment": {"disappoint", "let down", "underwhelmed", "missed", "unmet", "dissatisf"},
        "disapproval": {"disapprove", "dislike", "wrong", "unacceptable", "against", "object", "disagree"},
        "disgust": {"disgust", "gross", "nasty", "revolting", "sickening", "repulsive", "ew"},
        "embarrassment": {"embarrass", "awkward", "ashamed", "humiliat", "cringe", "self conscious"},
        "excitement": {"excit", "thrill", "pumped", "eager", "can't wait", "stoked", "hyped"},
        "fear": {"afraid", "scared", "fear", "terrifi", "frighten", "worri", "anxious", "panic"},
        "gratitude": {"grateful", "thankful", "thanks", "appreciat", "blessed", "much appreciated"},
        "grief": {"grief", "mourning", "bereav", "devastat", "heartbroken", "loss"},
        "joy": {"happy", "joy", "delight", "glad", "cheerful", "pleased", "wonderful", "great"},
        "love": {"love", "adore", "cherish", "beloved", "affection", "romantic", "fond"},
        "nervousness": {"nervous", "tense", "jittery", "uneasy", "on edge", "restless", "stressed"},
        "optimism": {"optimistic", "hopeful", "positive", "confident", "bright", "promising"},
        "pride": {"proud", "accomplish", "achievement", "honored", "dignified", "self respect"},
        "realization": {"realize", "aware", "it dawned", "figured out", "understood", "i see"},
        "relief": {"relieved", "finally", "at last", "thank goodness", "unburden", "reassured"},
        "remorse": {"remorse", "regret", "sorry", "apologize", "guilty", "my bad"},
        "sadness": {"sad", "down", "depress", "unhappy", "sorrow", "cry", "lonely"},
        "surprise": {"surpris", "shocked", "amazed", "astonish", "unexpected", "wow"},
        "neutral": set(),
    }

    lexicon = {emotion: expand_keywords(words) for emotion, words in raw_lexicon.items()}
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
