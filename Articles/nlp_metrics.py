# nlp_metrics.py
import re
from dataclasses import dataclass
from typing import List

@dataclass
class Metrics:
    url_id: str
    url: str
    positive_score: int
    negative_score: int
    polarity_score: float
    subjectivity_score: float
    avg_sentence_length: float
    percent_complex_words: float
    fog_index: float
    avg_words_per_sentence: float
    complex_word_count: int
    word_count: int
    syllables_per_word: float
    personal_pronouns: int
    avg_word_length: float

class NLP:

    VALID_WORD_RE = re.compile(r"[a-zA-Z]+(?:'[a-z]+)?")
    SENT_SPLIT_RE = re.compile(r"[.!?]+[\s]+")

    @staticmethod
    def count_syllables(word: str) -> int:
        w = re.sub(r"[^a-z]", "", word.lower())
        if not w: return 0
        if len(w) > 2 and w.endswith("e") and re.search(r"[aeiouy]", w[:-1]):
            w = w[:-1]
        groups = re.findall(r"[aeiouy]+", w)
        return max(1, len(groups))

    @staticmethod
    def tokenize_sentences(text: str) -> List[str]:
        return [s.strip() for s in re.split(NLP.SENT_SPLIT_RE, text) if s.strip()]

    @staticmethod
    def tokenize_words(text: str) -> List[str]:
        return [m.group(0).lower() for m in NLP.VALID_WORD_RE.finditer(text)]

    @staticmethod
    def clean_and_remove_stopwords(words: List[str], stopwords: set) -> List[str]:
        return [w for w in words if w not in stopwords]

    @staticmethod
    def count_personal_pronouns(text: str) -> int:
        pattern = re.compile(r"\b(I|we|my|ours|us)\b", re.IGNORECASE)
        return sum(1 for m in pattern.findall(text) if m != "US")

    @staticmethod
    def compute_metrics(title: str, body: str, stopwords: set, pos_words: set, neg_words: set, url_id: str, url: str) -> Metrics:
        full_text = f"{title.strip()}. {body.strip()}".strip()
        sentences = NLP.tokenize_sentences(full_text)
        words_all = NLP.tokenize_words(full_text)
        words_clean = [w for w in words_all if w not in stopwords and not w.isdigit()]

        total_words = len(words_clean)
        total_sentences = max(1, len(sentences))

        pos_score = sum(1 for w in words_clean if w in pos_words)
        neg_score = sum(1 for w in words_clean if w in neg_words)

        polarity = (pos_score - neg_score) / (pos_score + neg_score + 1e-6)
        subjectivity = (pos_score + neg_score) / (total_words + 1e-6) if total_words > 0 else 0.0

        syll_counts = [NLP.count_syllables(w) for w in words_clean]
        complex_words = sum(1 for s in syll_counts if s >= 3)
        total_syllables = sum(syll_counts)

        avg_sentence_len = len(words_all) / total_sentences
        pct_complex = complex_words / total_words if total_words > 0 else 0.0
        fog = 0.4 * (avg_sentence_len + pct_complex * 100)
        pronouns = NLP.count_personal_pronouns(full_text)
        avg_word_len = sum(len(w) for w in words_clean) / total_words if total_words > 0 else 0.0

        return Metrics(url_id, url, pos_score, neg_score, polarity, subjectivity, avg_sentence_len,
                       pct_complex, fog, avg_sentence_len, complex_words, total_words,
                       total_syllables / total_words if total_words > 0 else 0.0,
                       pronouns, avg_word_len)
