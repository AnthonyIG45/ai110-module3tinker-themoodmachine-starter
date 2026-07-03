# mood_analyzer.py
"""
Rule based mood analyzer for short text snippets.

This class starts with very simple logic:
  - Preprocess the text
  - Look for positive and negative words
  - Compute a numeric score
  - Convert that score into a mood label
"""

import re
import string
from typing import List, Dict, Tuple, Optional

from dataset import POSITIVE_WORDS, NEGATIVE_WORDS, EMOTICON_MAP, WORD_WEIGHTS


class MoodAnalyzer:
    """
    A very simple, rule based mood classifier.
    """

    def __init__(
        self,
        positive_words: Optional[List[str]] = None,
        negative_words: Optional[List[str]] = None,
    ) -> None:
        # Use the default lists from dataset.py if none are provided.
        positive_words = positive_words if positive_words is not None else POSITIVE_WORDS
        negative_words = negative_words if negative_words is not None else NEGATIVE_WORDS

        # Store as sets for faster lookup.
        self.positive_words = set(w.lower() for w in positive_words)
        self.negative_words = set(w.lower() for w in negative_words)

        # Longest patterns first so ":-)" is matched before ":)" leaves a
        # dangling "-" behind.
        self.emoticon_map = dict(
            sorted(EMOTICON_MAP.items(), key=lambda item: len(item[0]), reverse=True)
        )

        # Look up how strongly each word should count. Words without an
        # explicit entry in WORD_WEIGHTS (e.g. custom words passed above)
        # fall back to a plain +1 / -1.
        self.word_weights: Dict[str, int] = {}
        for word in self.positive_words:
            self.word_weights[word] = WORD_WEIGHTS.get(word, 1)
        for word in self.negative_words:
            self.word_weights[word] = WORD_WEIGHTS.get(word, -1)

    # ---------------------------------------------------------------------
    # Preprocessing
    # ---------------------------------------------------------------------

    def preprocess(self, text: str) -> List[str]:
        """
        Convert raw text into a list of tokens the model can work with.

        TODO: Improve this method.

        Right now, it does the minimum:
          - Strips leading and trailing whitespace
          - Converts everything to lowercase
          - Splits on spaces

        Ideas to improve:
          - Remove punctuation - Complete
          - Handle simple emojis separately (":)", ":-(", "🥲", "😂") - Complete
          - Normalize repeated characters ("soooo" -> "soo") - Complete
        """
        cleaned = text.strip().lower()

        # Swap known emoticons/emoji for a canonical word (see dataset.EMOTICON_MAP)
        # before stripping punctuation, since ":)" is made entirely of punctuation
        # and would otherwise disappear in the next step.
        for pattern, canonical in self.emoticon_map.items():
            if pattern in cleaned:
                cleaned = cleaned.replace(pattern, f" {canonical} ")

        # Remove punctuation so "great!" and "great" match the same word.
        cleaned = cleaned.translate(str.maketrans("", "", string.punctuation))

        tokens = cleaned.split()

        # Normalize repeated characters so "soooo" and "soo" collapse to the
        # same token.
        tokens = [re.sub(r"(.)\1{2,}", r"\1\1", token) for token in tokens]

        return tokens

    # ---------------------------------------------------------------------
    # Scoring logic
    # ---------------------------------------------------------------------

    def score_text(self, text: str) -> int:
        """
        Compute a numeric "mood score" for the given text.

        Positive words increase the score.
        Negative words decrease the score.

        TODO: You must choose AT LEAST ONE modeling improvement to implement.
        For example:
          - Handle simple negation such as "not happy" or "not bad"
          - Count how many times each word appears instead of just presence
          - Give some words higher weights than others (for example "hate" < "annoyed")
          - Treat emojis or slang (":)", "lol", "💀") as strong signals
        """
        tokens = self.preprocess(text)

        score = 0
        for token in tokens:
            score += self.word_weights.get(token, 0)

        return score

    # ---------------------------------------------------------------------
    # Label prediction
    # ---------------------------------------------------------------------

    def predict_label(self, text: str) -> str:
        """
        Turn the numeric score for a piece of text into a mood label.

        The default mapping is:
          - score > 0  -> "positive"
          - score < 0  -> "negative"
          - score == 0 -> "neutral"

        TODO: You can adjust this mapping if it makes sense for your model.
        For example:
          - Use different thresholds (for example score >= 2 to be "positive")
          - Add a "mixed" label for scores close to zero
        Just remember that whatever labels you return should match the labels
        you use in TRUE_LABELS in dataset.py if you care about accuracy.
        """
        score = self.score_text(text)
        print(f"Predicted score: {score}")

        if score > 0:
            return "positive"
        if score < 0:
            return "negative"
        return "neutral"

    # ---------------------------------------------------------------------
    # Explanations (optional but recommended)
    # ---------------------------------------------------------------------

    def explain(self, text: str) -> str:
        """
        Return a short string explaining WHY the model chose its label.

        TODO:
          - Look at the tokens and identify which ones counted as positive
            and which ones counted as negative.
          - Show the final score.
          - Return a short human readable explanation.

        Example explanation (your exact wording can be different):
          'Score = 2 (positive words: ["love", "great"]; negative words: [])'

        The current implementation is a placeholder so the code runs even
        before you implement it.
        """
        tokens = self.preprocess(text)

        positive_hits: List[str] = []
        negative_hits: List[str] = []
        score = 0

        for token in tokens:
            if token in self.positive_words:
                positive_hits.append(token)
                score += 1
            if token in self.negative_words:
                negative_hits.append(token)
                score -= 1

        return (
            f"Score = {score} "
            f"(positive: {positive_hits or '[]'}, "
            f"negative: {negative_hits or '[]'})"
        )
