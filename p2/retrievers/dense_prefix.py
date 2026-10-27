"""dense_prefix: the ablation of dense with BGE's retrieval instruction in front of every query.

Everything else is dense's: the same model (bge-small-en-v1.5), the same 300-word chunks and the same
cached chunk vectors. Only [dense] query_prefix changes, from "" to the instruction BAAI recommends for
a short query searched against longer passages. The documents are not prefixed, so a difference from dense
on the own corpus comes from how the query is embedded.
"""

from __future__ import annotations

from p2.retrievers import dense

BASE = "dense"
NEEDS_CLAUDE = False

QUERY_PREFIX = "Represent this sentence for searching relevant passages: "


def build(corpus, cfg):
    tables = {**cfg.tables, "dense": {**cfg.table("dense"), "query_prefix": QUERY_PREFIX}}
    return dense.build(corpus, cfg.replace(tables=tables))
