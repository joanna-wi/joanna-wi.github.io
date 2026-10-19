# -*- coding: utf-8 -*-

!pip -q install keybert sentence-transformers
import pandas as pd, numpy as np
from google.colab import files

files.upload()   # add review file

# create a column for reviews
COL = "full_review"
df = pd.read_csv("reviews.csv")
# convert to text and trim whitespaces
df[COL] = df[COL].astype("string").str.strip()
# drop empty reviews and keep the original row number
df = df[df[COL].notna() & (df[COL] != "")].reset_index(names="orig_row")
print(len(df), "non-empty reviews")

from transformers import pipeline

# load a pretrained roberta sentiment model; top_k=None returns scores for all three labels,
# truncation cuts long reviews at 256 tokens, device=0 uses the gpu, batch_size=64 to speed up processing
sent = pipeline("text-classification",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                top_k=None, truncation=True, max_length=256,
                device=0, batch_size=64)

# helper: for each text, return (winning label, positive score minus negative score)
def run_sent(texts):
    rows = []
    for out in sent(texts):
        # turn the model output into {label: score}
        d = {x["label"].lower(): x["score"] for x in out}
        # label with the highest probability, plus a single score from -1 to 1
        rows.append((max(d, key=d.get), d["positive"] - d["negative"]))
    return rows

# score all reviews and store label and numeric score as new columns
res = run_sent(df[COL].tolist())
df["sentiment"] = [r[0] for r in res]
df["score"] = [r[1] for r in res]      # -1 to 1
df.to_csv("reviews_scored.csv", index=False)   # safety copy in case the session dies
# count of how many reviews fall in each sentiment label
df["sentiment"].value_counts()

from keybert import KeyBERT
from sentence_transformers import SentenceTransformer

# load a small, fast embedding model on the gpu and plug it into keybert
emb = SentenceTransformer("all-MiniLM-L6-v2", device="cuda")
kb = KeyBERT(model=emb)

texts = df[COL].tolist()
kws = []
# process reviews in chunks of 2000
for s in range(0, len(texts), 2000):
    # extract the top 5 keyphrases of 2-3 words per review; mmr adds diversity so phrases aren't near-duplicates
    kws += kb.extract_keywords(texts[s:s+2000], keyphrase_ngram_range=(2, 3),
                               stop_words="english", use_mmr=True,
                               diversity=0.5, top_n=5)
    print(s + 2000, "done")

# flatten into one row per phrase, keeping the review id and that review's sentiment
phrases = pd.DataFrame(
    [{"orig_row": df.loc[i, "orig_row"], "review_sentiment": df.loc[i, "sentiment"],
      "phrase": p.lower()}
     for i, lst in enumerate(kws) for p, _ in lst])
print(len(phrases), "phrases,", phrases.phrase.nunique(), "unique")

from collections import Counter
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS as SW

# count individual words across all phrases, skipping stop words and very short words
# (used to see what themes show up, which helped build the concept regexes below)
c = Counter(w for p in phrases.phrase for w in p.split() if w not in SW and len(w) > 2)
c.most_common(60)

import re


# common phrases grouped into concepts
CONCEPTS = {
    "delivery":  r"deliver|delivered|shipping|shipped|ship|arrive|courier|parcel|package|dispatch|days|post|waiting|missing|date|deadline",
    "quality":   r"quality|broke|broken|defect|faulty|different|condition|correct|right",
    "service":   r"service|support|staff|customer care|rude|helpful|replacement|response|website|office",
    "price":     r"price|cost|expensive|value|money|afford|overpriced|cheap",
    "packaging": r"packaging|box\b|wrapp|sealed",
    "size":      r"size|too (big|small)|fit",
    "experience": r"excellent|great|perfect|good|recommend|like|satisfied|loved|super|cancel|return"
}

# 1. find the sentences that mention each concept
rows = []
for _, r in df.iterrows():
    # split each review into sentences (at . ! ? or line breaks)
    for s in re.split(r"(?<=[.!?])\s+|\n+", r[COL]):
        s = s.strip()
        # skip fragments that are too short to be meaningful
        if len(s) < 4:
            continue
        # record the sentence once for every concept whose pattern it matches
        for c, pat in CONCEPTS.items():
            if re.search(pat, s, re.I):
m = pd.DataFrame(rows, columns=["orig_row", "concept", "sentence"])
print(len(m), "concept mentions in", m.orig_row.nunique(), "reviews")

# 2. sentiment of those sentences only (each unique sentence scored once)
uniq_s = m.sentence.unique().tolist()
sc = dict(zip(uniq_s, [x[1] for x in run_sent(uniq_s)]))
# map the scores back onto every concept mention
m["score"] = m.sentence.map(sc)

# 3. one row per review and concept: average if mentioned several times
rc = (m.groupby(["orig_row", "concept"], as_index=False)["score"].mean())
# bucket the average score into negative (below -0.25), neutral, or positive (above 0.25)
rc["sentiment"] = pd.cut(rc.score, [-1.01, -0.25, 0.25, 1.01],
                         labels=["negative", "neutral", "positive"])

# 4. overall: % of reviews mentioning each concept that are pos/neu/neg
overall = pd.crosstab(rc.concept, rc.sentiment) # counts per concept and sentiment
n = overall.sum(axis=1)                         # total reviews per concept
overall_pct = (overall.div(n, axis=0) * 100).round(1)
overall_pct["n_reviews"] = n
print(overall_pct)

# save results
overall_pct.to_csv("concept_overall.csv")
m.to_csv("concept_sentences.csv", index=False)
# download
for f in ["concept_overall.csv", "concept_by_product.csv", "concept_sentences.csv"]:
    files.download(f)
