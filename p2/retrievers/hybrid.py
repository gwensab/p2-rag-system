"""hybrid: reciprocal rank fusion of bm25 and dense.

Each document scores the sum of 1 / (k + rank) over the two full rankings (k = 60 by default, from
[hybrid] in p2.toml). Fusing full rankings, not top-10 lists, lets a document that is 11th in both
lists reach the fused top 10. The same fusion over chunk rankings gives search_chunks for `p2 answer`.

k is 30 here because CI runs this system again on another machine, where near-tied dense scores can swap
places; with a small k the fused score then moves by more than p2 check's tolerance. rerank builds this
class with its own k (see [rerank] first_stage_k in p2.toml), because CI never runs rerank again.
"""

from __future__ import annotations

from p2 import retrievers
from p2.runfile import order

NEEDS_CLAUDE = False


def rrf(rankings, k: int = 60) -> list[tuple[str, float]]:
    """Fuse rankings (lists of ids, best first); an id scores the sum of 1 / (k + rank) over the lists."""
    scores: dict[str, float] = {}
    for ranking in rankings:
        for rank, item in enumerate(ranking, 1):
            scores[item] = scores.get(item, 0.0) + 1.0 / (k + rank)
    return order(scores.items())


class Hybrid:
    def __init__(self, corpus, cfg, k: int | None = None):
        self.k = int(k if k is not None else cfg.table("hybrid").get("rrf_k", 60))
        self.bm25 = retrievers.build("bm25", corpus, cfg)
        self.dense = retrievers.build("dense", corpus, cfg)
        self.n_docs = len(corpus.docs)
        self.n_chunks = len(self.dense.chunks)

    def search(self, text: str, k: int) -> list[tuple[str, float]]:
        rankings = [[d for d, _ in system.search(text, self.n_docs)] for system in (self.bm25, self.dense)]
        return rrf(rankings, self.k)[:k]

    def search_chunks(self, text: str, k: int) -> list[tuple[str, float]]:
        rankings = [[c for c, _ in system.search_chunks(text, self.n_chunks)] for system in (self.bm25, self.dense)]
        return rrf(rankings, self.k)[:k]


def build(corpus, cfg):
    return Hybrid(corpus, cfg)
