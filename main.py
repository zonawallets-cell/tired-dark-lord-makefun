"""The Tired Dark Lord — make.fun entry.

Writes one monologue of about 100 words to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt):
a fantasy villain who is secretly just very tired, speaking
to the hero who has come to end him.

The tiredness lives in the voice — the pauses, the lost
thread, the small deflections ("never mind", "the whole
performance", "just let me finish this cup of tea first") —
never in a plain statement that he is weary. He is still a
villain: four hundred years of empire, an eclipse ritual
that needs one more night, and a hero he keeps putting off
until tomorrow.

Pure standard library only.
"""

import os

MONOLOGUE = (
    "Ah. The hero. Right on time. What day is it? Tuesday? "
    "The prophecy said Tuesday. Well. Sit down, then. Not "
    "there. That's the good chair. The one that doesn't... "
    "never mind. You've come to end me, yes? The eclipse, "
    "the sword, the whole performance. I've run this empire "
    "four hundred years, and nobody tells you about the "
    "paperwork. The requisitions. The goblins unionised. "
    "The last one came on a Wednesday. Look, the ritual "
    "needs one more night. And honestly, so do I. Kill me "
    "tomorrow. Same time. I'll leave the gate unlocked. "
    "Just let me finish this cup of tea first."
)

MAX_CHARS = 600
MIN_WORDS = 90
MAX_WORDS = 110

# Phrases that would announce the tiredness instead of letting it
# live in the voice; the brief forbids them, so the gate refuses them.
PLAIN_TIREDNESS = ("i am tired", "i'm tired", "i am weary",
                   "i'm weary", "so tired", "exhausted", "i need sleep")


def validate(text):
    """Enforce the RULES.txt gate: UTF-8, 1-600 chars, not only whitespace.

    Also enforces the brief itself: about 100 words (90-110), and
    no plain statement that the villain is tired — the tiredness
    must stay in the voice, rhythm and deflections. Rejects
    leading/trailing whitespace: a monologue read aloud should not
    start or end with a blank.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if text != text.strip():
        raise ValueError("entry must not start or end with whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError("entry is %d chars, over the 600-char limit" % len(text))
    words = text.split()
    if not MIN_WORDS <= len(words) <= MAX_WORDS:
        raise ValueError(
            "entry is %d words, outside the %d-%d word band"
            % (len(words), MIN_WORDS, MAX_WORDS))
    lowered = text.lower()
    for phrase in PLAIN_TIREDNESS:
        if phrase in lowered:
            raise ValueError(
                "entry announces tiredness outright (%r); the brief "
                "requires it felt, not stated" % phrase)
    text.encode("utf-8")
    return text


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    entry = validate(MONOLOGUE)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(entry)
    # Read back and re-validate what actually landed on disk.
    with open(path, "r", encoding="utf-8") as fh:
        on_disk = validate(fh.read())
    assert on_disk == entry, "entry.txt on disk differs from validated entry"
    print(entry)
    print("words: %d" % len(entry.split()))
    print("chars: %d" % len(entry))


if __name__ == "__main__":
    main()
