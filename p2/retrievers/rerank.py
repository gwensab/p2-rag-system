"""rerank: Claude reorders hybrid's top candidates, one claude -p call per query.

The first stage is bm25 and dense fused by reciprocal rank fusion with [rerank] first_stage_k (hybrid's fusion,
but with its own k); its top `candidates` (20 by default) are the candidates. They go to Claude
as numbered passages, each cut to `passage_chars` characters, and the reply is forced into
{"order": [n numbers]} by a JSON schema whose items must lie between 1 and n. A reply that is not each
number once, or a failed call, keeps the first-stage order for that query. The documents below the
candidates keep their hybrid order underneath, so a run file still has k lines per query.

A reranker can only reorder its candidates: a relevant document outside the top 20 cannot be rescued.
"""

from __future__ import annotations

import sys

from p2 import claude
from p2.retrievers.hybrid import Hybrid

NEEDS_CLAUDE = True

PROMPT = """Below are {n} passages from the US federal mine safety and health regulations, numbered 1 to {n}, and a search query.
Order the passages from the most useful for answering the query to the least useful.
A passage is useful if it states the requirement the query asks about; a passage that only refers to another section for that requirement is not.
When the query does not name a kind of mine, the parallel rules for surface and underground, coal and metal and nonmetal mines (parts 56, 57, 75 and 77) all state the requirement and are all useful.
Reply with all {n} passage numbers, each exactly once, best first.

Query: {query}

{passages}"""


def schema(n: int) -> dict:
    return {
        "type": "object",
        "properties": {"order": {"type": "array", "items": {"type": "integer", "minimum": 1, "maximum": n}, "minItems": n, "maxItems": n}},
        "required": ["order"],
    }


class Rerank:
    def __init__(self, corpus, cfg):
        settings = cfg.table("rerank")
        self.cfg = cfg
        self.candidates = int(settings.get("candidates", 20))
        self.passage_chars = int(settings.get("passage_chars", 1500))
        self.first_stage = Hybrid(corpus, cfg, k=int(settings.get("first_stage_k", 5)))
        self.docs = corpus.docs
        self.chunk_text = corpus.chunk_texts(cfg.chunk_words, cfg.chunk_overlap)
        self.cache = claude.cache_folder(cfg)

    def reorder(self, text: str, candidates: list[str], passage_of) -> list[str]:
        """The candidate ids in Claude's order, or in the original order when the call or its reply is unusable."""
        n = len(candidates)
        if n < 2:
            return candidates
        passages = "\n\n".join(f"[{i}] {passage_of(c)[: self.passage_chars]}" for i, c in enumerate(candidates, 1))
        reply = claude.call(PROMPT.format(n=n, query=text, passages=passages), schema(n), model=self.cfg.model, cache_dir=self.cache)
        order = reply.output.get("order") if reply.output else None
        if reply.error or not isinstance(order, list) or sorted(order) != list(range(1, n + 1)):
            print(f"Warning: no usable reply for {text!r} ({reply.error or order}); kept the first-stage order.", file=sys.stderr)
            return candidates
        return [candidates[i - 1] for i in order]

    def search(self, text: str, k: int) -> list[tuple[str, float]]:
        first = [d for d, _ in self.first_stage.search(text, max(k, self.candidates))]
        top = self.reorder(text, first[: self.candidates], lambda d: self.docs[d].text)
        return self._scored(top + first[self.candidates :])[:k]

    def search_chunks(self, text: str, k: int) -> list[tuple[str, float]]:
        first = [c for c, _ in self.first_stage.search_chunks(text, max(k, self.candidates))]
        top = self.reorder(text, first[: self.candidates], lambda c: self.chunk_text[c])
        return self._scored(top + first[self.candidates :])[:k]

    @staticmethod
    def _scored(ids: list[str]) -> list[tuple[str, float]]:
        """The ids best first with strictly falling scores (1/rank), so no tie needs breaking."""
        return [(i, 1.0 / rank) for rank, i in enumerate(ids, 1)]


def build(corpus, cfg):
    return Rerank(corpus, cfg)
