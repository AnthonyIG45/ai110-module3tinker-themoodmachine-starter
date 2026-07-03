"""
Shared data for the Mood Machine lab.

This file defines:
  - POSITIVE_WORDS: starter list of positive words
  - NEGATIVE_WORDS: starter list of negative words
  - SAMPLE_POSTS: short example posts for evaluation and training
  - TRUE_LABELS: human labels for each post in SAMPLE_POSTS
"""

# ---------------------------------------------------------------------
# Starter word lists
# ---------------------------------------------------------------------

POSITIVE_WORDS = [
    "happy",
    "great",
    "good",
    "love",
    "excited",
    "awesome",
    "fun",
    "chill",
    "relaxed",
    "amazing",
    "emopositive",
]

NEGATIVE_WORDS = [
    "sad",
    "bad",
    "terrible",
    "awful",
    "angry",
    "upset",
    "tired",
    "stressed",
    "hate",
    "boring",
    "emonegative",
]

# ---------------------------------------------------------------------
# Word weights
# ---------------------------------------------------------------------

# How strongly each word should push the score toward positive/negative.
# Words not listed here fall back to a default of +1 / -1 in MoodAnalyzer.
# Emoji/emoticon tokens ("emopositive"/"emonegative") get a higher magnitude
# since an emoji is usually a stronger, more deliberate signal than a single
# word choice.
WORD_WEIGHTS = {
    "happy": 1,
    "great": 2,
    "good": 1,
    "love": 2,
    "excited": 2,
    "awesome": 2,
    "fun": 1,
    "chill": 1,
    "relaxed": 1,
    "amazing": 2,
    "emopositive": 3,
    "sick": 2,
    "stuck": -1,
    "sad": -1,
    "bad": -1,
    "terrible": -2,
    "awful": -2,
    "angry": -2,
    "upset": -1,
    "tired": -1,
    "stressed": -1,
    "hate": -2,
    "boring": -1,
    "emonegative": -3,
}

# ---------------------------------------------------------------------
# Emoticon / emoji handling
# ---------------------------------------------------------------------

# Maps simple emoticons and emoji to a canonical word that already exists
# in POSITIVE_WORDS / NEGATIVE_WORDS, so scoring logic doesn't need a
# separate code path for them. Longer patterns are matched before shorter
# ones (see MoodAnalyzer.preprocess) so ":-)" isn't left as a dangling "-".
EMOTICON_MAP = {
    ":-)": "emopositive",
    ":)": "emopositive",
    ":-d": "emopositive",
    ":d": "emopositive",
    "🙂": "emopositive",
    "😊": "emopositive",
    "😂": "emopositive",
    ":-(": "emonegative",
    ":(": "emonegative",
    ":'(": "emonegative",
    "🥲": "emonegative",
    "💀": "emonegative",
}

# ---------------------------------------------------------------------
# Starter labeled dataset
# ---------------------------------------------------------------------

# Short example posts written as if they were social media updates or messages.
SAMPLE_POSTS = [
    "I love this class so much",
    "Today was a terrible day",
    "Feeling tired but kind of hopeful",
    "This is fine",
    "So excited for the weekend",
    "I am not happy about this",
    "10/10", #Added
    "That is dope",
    "Feeling good",
    "I'm Dead",
    "k.",



]

# Human labels for each post above.
# Allowed labels in the starter:
#   - "positive"
#   - "negative"
#   - "neutral"
#   - "mixed"
TRUE_LABELS = [
    "positive",  # "I love this class so much"
    "negative",  # "Today was a terrible day"
    "mixed",     # "Feeling tired but kind of hopeful"
    "neutral",   # "This is fine"
    "positive",  # "So excited for the weekend"
    "negative",  # "I am not happy about this"
    "positive",  #Added
    "positive",
    "mixed",
    "mixed",
    "negative",



]

# TODO: Add 5-10 more posts and labels.
#
# Requirements:
#   - For every new post you add to SAMPLE_POSTS, you must add one
#     matching label to TRUE_LABELS.
#   - SAMPLE_POSTS and TRUE_LABELS must always have the same length.
#   - Include a variety of language styles, such as:
#       * Slang ("lowkey", "highkey", "no cap")
#       * Emojis (":)", ":(", "🥲", "😂", "💀")
#       * Sarcasm ("I absolutely love getting stuck in traffic")
#       * Ambiguous or mixed feelings
#
# Tips:
#   - Try to create some examples that are hard to label even for you.
#   - Make a note of any examples that you and a friend might disagree on.
#     Those "edge cases" are interesting to inspect for both the rule based
#     and ML models.
#
# Example of how you might extend the lists:
#
# SAMPLE_POSTS.append("Lowkey stressed but kind of proud of myself")
# TRUE_LABELS.append("mixed")
#
# Remember to keep them aligned:
#   len(SAMPLE_POSTS) == len(TRUE_LABELS)
