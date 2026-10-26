"""dense: embed every chunk once, embed the query, and rank chunks by cosine similarity.

The model comes from the [dense] table of p2.toml (bge-small-en-v1.5 by default). Chunk vectors are
cached in .cache/vectors/ by p2.embed, so only the first run encodes the corpus. Vectors have length 1,
so one matrix product gives the cosine similarity of the query with every chunk, and ChunkScorer lifts
the chunk scores to documents (a document scores its best chunk).
"""

from __future__ import annotations

from p2 import embed
from p2.retrievers import ChunkScorer

NEEDS_CLAUDE = False


class Dense(ChunkScorer):
    def __init__(self, corpus, cfg):
        super().__init__(corpus, cfg)
        settings = cfg.table("dense")
        self.model = settings.get("model", embed.BGE)
        self.query_prefix = settings.get("query_prefix", "")
        self.embedder = embed.load(self.model)
        self.vectors = embed.doc_vectors(self.embedder, [c.text for c in self.chunks], cfg.root)

    def score_chunks(self, text: str) -> list[float]:
        if not len(self.vectors):
            return []
        query = self.embedder.encode([self.query_prefix + text])[0]
        return (self.vectors @ query).tolist()


def build(corpus, cfg):
    return Dense(corpus, cfg)
