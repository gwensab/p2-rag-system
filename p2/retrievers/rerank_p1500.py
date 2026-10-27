"""rerank_p1500: the ablation of rerank with 1500-character passages instead of 600.

Everything else is rerank's: the same first stage (hybrid, first_stage_k = 5), the same 20 candidates, the
same prompt and model. Only [rerank] passage_chars changes, so a difference from rerank on the own corpus
comes from how much of each document the reranker reads. A document here (title lines plus abstract) has
a median of about 1,400 characters, and 60% of them are 1,500 or shorter, so 1500 shows most documents
whole while 600 cuts every one of them.
"""

from __future__ import annotations

from p2.retrievers import rerank

BASE = "rerank"
NEEDS_CLAUDE = True

PASSAGE_CHARS = 1500


def build(corpus, cfg):
    tables = {**cfg.tables, "rerank": {**cfg.table("rerank"), "passage_chars": PASSAGE_CHARS}}
    return rerank.build(corpus, cfg.replace(tables=tables))
