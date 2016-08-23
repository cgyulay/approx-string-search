"""
This class implements fast approximate string search in a large lexicon by
building an n-gram lookup table. Shared n-grams between a query word and
lexicon words can be used as a proxy for edit distance. For example, this might
be used by a spell checker to find close matches in a dictionary.

This system is based on the paper "Finding Approximate Matches in Large
Lexicons" (Zobel & Dart, 1995).

- Colton Gyulay
"""

import time
EDGE_TOKEN = u"="


class ApproxLookupTable():
    """This class is responsible for building an n-gram lookup table for
    searching for approximate matches in a provided lexicon.
    """

    def __init__(self, words):
        """Build n-gram lookup table, and word->idx/idx->word tables for
        smaller memory footprint.

        Args:
            words: a list of words to search against.
        Returns:
            a queryable lookup object.
        """
        self.word2idx = {}
        self.idx2word = {}
        self.ngram_lookup = {}

        print "building n-gram lookup table..."
        start = time.clock()

        idx = 0
        for w in words:
            if w not in self.word2idx:
                self.word2idx[w] = idx
                self.idx2word[idx] = w
                idx += 1

            ngrams = self._extract_ngrams(w)
            for ngram in ngrams:
                if ngram not in self.ngram_lookup:
                    self.ngram_lookup[ngram] = []
                self.ngram_lookup[ngram].append(self.word2idx[w])

        print "completed table in %s s." % (time.clock() - start)

    def _extract_ngrams(self, word, ngram=3):
        """Extract all substrings of size n-gram from a word, using edge
        padding (e.g., "John" -> ["=jo", "joh", "ohn", "hn="]).

        Args:
            word: a string from which to extract n-grams.
            ngram: the n-gram length to use for matching.
        Returns:
            a list of n-grams contained in word.
        """
        w = EDGE_TOKEN + word.lower() + EDGE_TOKEN
        if len(w) < ngram + 1:
            return [w]

        subs = []
        for i in xrange(len(w) - ngram + 1):
            subs.append(w[i: i + ngram])
        return subs

    def query(self, word):
        """Find next closest word in lexicon based on shared n-grams.

        Args:
            word: a target string for which to find approximate matches.
        Returns:
            the closest word in the lexicon.
        """
        return self.query_k(word, 1)[0]

    def query_k(self, word, k=5):
        """Find k closest words in lexicon based on shared n-grams.

        Args:
            word: a target string for which to find approximate matches.
        Returns:
            the k closest words in the lexicon.
        """
        common = {}
        ngrams = self._extract_ngrams(word)
        for ngram in ngrams:
            shared = self.ngram_lookup.get(ngram) or []
            for idx in shared:
                if idx not in common:
                    common[idx] = 0
                common[idx] += 1
        if len(common) == 0:
            return [word]

        top_k = sorted(common.iteritems(), key=lambda x: -x[1])[:k]
        return [self.idx2word[i] for (i, v) in top_k]
