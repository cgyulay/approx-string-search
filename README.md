# approx-string-search
This class implements fast approximate string search in a large lexicon by
building an n-gram lookup table. Shared n-grams between a query word and
lexicon words can be used as a proxy for edit distance. For example, this might
be used by a spell checker to find close matches in a dictionary.

This system is based on the paper "Finding Approximate Matches in Large
Lexicons" (Zobel & Dart, 1995).

# Instructions

### Usage

```bash
from approx_lookup_table import ApproxLookupTable

# build table
lexicon = ["Elizabeth", "Eleanor", "Eliana", "Elane"]
lt = ApproxLookupTable(lexicon)

# query
print lt.query("Ellzabeth")
>> "Elizabeth"

# query k closest
print lt.query_k("Ellzabeth", 2)
>> ["Elizabeth", "Beth"]
```