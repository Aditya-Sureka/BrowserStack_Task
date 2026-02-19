from collections import Counter
import re

def analyze_words(titles):
    text = " ".join(titles).lower()
    words = re.findall(r'\b[a-z]+\b', text)

    counter = Counter(words)

    print("\nRepeated Words (>2 times):")
    for word, count in counter.items():
        if count > 2:
            print(f"{word}: {count}")
