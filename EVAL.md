# Evaluation report

This is the report on what you built and what the numbers let you claim.
Two kinds of text live here.

The tables between a `p2:begin` comment line and its matching `p2:end` comment line are written by `uv run p2 score` from your committed run files and answers files.
Please do not edit anything between those two lines, because `uv run p2 check` recomputes them and fails when they differ.
A table that says no runs or answers exist yet is waiting for data; run `uv run p2 score` after you commit the files it needs.

Everything else is yours.
Each prompt ends with a marker line that you replace with your own writing; `uv run p2 check --final` fails while one is left.
Write what you measured, including what did not work.
What I read for is whether each claim matches its interval, not whether the result is good news.

Words used below: recall@10, MRR@10 and nDCG@10 are the three scores, each averaged over the queries of a set; step 7 of stage 1 in the README defines them, and lecture 14 goes deeper.
A paired interval is the 95% interval of the mean difference between two systems on the same queries, found by resampling the queries 10,000 times.
When an interval includes zero, the gold set cannot tell the two systems apart, and the right words are "not distinguishable on this gold set".
The minimum detectable difference is the smallest gap this many queries could reliably show, so a difference below it is invisible to this gold set, not absent.

---

## 1. Stage 1 - the shared corpus (30 CFR Chapter I)

### What you built

For each of `dense`, `hybrid` and `rerank`, one or two sentences: the embedding model, how documents were chunked, what was fused and how, how many candidates the reranker saw, and anything you changed from the 12 and 13 lab code.

dense - Dense embeds with the bge-small model and ranks chunks by cosine similarity to the query vector, looking at chunks rather than whole articles as in lab 12, and splits each document into chunks of 300 words with 50 overlap. Most sections fit in one chunk, and a document scores as its best chunk.

hybrid - Hybrid fuses bm25 and dense by reciprocal rank fusion over their full document ranking. The initial k value of 60 had poor performance, scoring 0.471 but reducing that k value to 30 improved it to 0.599 on practice queries.

rerank - Rerank uses the Sonnet model, cuts passages to 600 characters and a bad reply keeps the first stage order. The changes from lab 13 include the schema bounds and the first stage which is hybrid's top 20.

---

### Practice queries (20)

Scores per system.

<!-- p2:begin shared-practice -->
| System | Recall@10 | MRR@10 | nDCG@10 |
| --- | ---: | ---: | ---: |
| bm25 | 0.625 | 0.507 | 0.518 |
| dense | 0.558 | 0.562 | 0.480 |
| hybrid | 0.675 | 0.522 | 0.509 |
| rerank | 0.833 | 0.900 | 0.850 |

20 judged queries; nDCG uses binary labels; a random ranking of the 2,484 documents would get recall@10 near 0.004.
<!-- p2:end shared-practice -->

The same scores per query class.

<!-- p2:begin shared-practice-classes -->
| System | Metric | identifier (n=7) | paraphrase (n=7) | mixed (n=6) |
| --- | --- | ---: | ---: | ---: |
| bm25 | Recall@10 | 1.000 | 0.000 | 0.917 |
| bm25 | MRR@10 | 0.810 | 0.000 | 0.746 |
| bm25 | nDCG@10 | 0.857 | 0.000 | 0.728 |
| dense | Recall@10 | 0.214 | 0.595 | 0.917 |
| dense | MRR@10 | 0.333 | 0.714 | 0.653 |
| dense | nDCG@10 | 0.211 | 0.593 | 0.661 |
| hybrid | Recall@10 | 0.643 | 0.500 | 0.917 |
| hybrid | MRR@10 | 0.520 | 0.292 | 0.792 |
| hybrid | nDCG@10 | 0.456 | 0.331 | 0.779 |
| rerank | Recall@10 | 1.000 | 0.595 | 0.917 |
| rerank | MRR@10 | 1.000 | 0.714 | 1.000 |
| rerank | nDCG@10 | 1.000 | 0.626 | 0.936 |
<!-- p2:end shared-practice-classes -->

Differences between every pair of systems, each with its paired interval and the minimum detectable difference.

<!-- p2:begin shared-practice-pairs -->
| Comparison | Metric | Mean difference | 95% interval | MDD | Reading |
| --- | --- | ---: | ---: | ---: | --- |
| dense minus bm25 | Recall@10 | -0.067 | [-0.350, +0.225] | 0.415 | not distinguishable |
| dense minus bm25 | MRR@10 | +0.055 | [-0.225, +0.343] | 0.412 | not distinguishable |
| dense minus bm25 | nDCG@10 | -0.039 | [-0.302, +0.231] | 0.385 | not distinguishable |
| hybrid minus bm25 | Recall@10 | +0.050 | [-0.175, +0.267] | 0.322 | not distinguishable |
| hybrid minus bm25 | MRR@10 | +0.015 | [-0.153, +0.179] | 0.240 | not distinguishable |
| hybrid minus bm25 | nDCG@10 | -0.009 | [-0.188, +0.168] | 0.258 | not distinguishable |
| hybrid minus dense | Recall@10 | +0.117 | [-0.033, +0.275] | 0.235 | not distinguishable |
| hybrid minus dense | MRR@10 | -0.041 | [-0.233, +0.140] | 0.271 | not distinguishable |
| hybrid minus dense | nDCG@10 | +0.030 | [-0.121, +0.172] | 0.212 | not distinguishable |
| rerank minus bm25 | Recall@10 | +0.208 | [+0.050, +0.383] | 0.242 | rerank higher |
| rerank minus bm25 | MRR@10 | +0.393 | [+0.200, +0.595] | 0.287 | rerank higher |
| rerank minus bm25 | nDCG@10 | +0.331 | [+0.167, +0.506] | 0.248 | rerank higher |
| rerank minus dense | Recall@10 | +0.275 | [+0.100, +0.450] | 0.259 | rerank higher |
| rerank minus dense | MRR@10 | +0.338 | [+0.150, +0.533] | 0.273 | rerank higher |
| rerank minus dense | nDCG@10 | +0.370 | [+0.205, +0.544] | 0.246 | rerank higher |
| rerank minus hybrid | Recall@10 | +0.158 | [+0.025, +0.317] | 0.213 | rerank higher |
| rerank minus hybrid | MRR@10 | +0.378 | [+0.206, +0.560] | 0.257 | rerank higher |
| rerank minus hybrid | nDCG@10 | +0.340 | [+0.200, +0.494] | 0.213 | rerank higher |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time.
<!-- p2:end shared-practice-pairs -->

The 40 test queries have no answer key in this repo.
Your test run files are scored by the course and the score comes back to you as feedback, so nothing goes here for them.

### What the intervals let you claim

Which differences are distinguishable from zero and which are not?
What is the minimum detectable difference at 20 queries, and what does that say about any gap smaller than it?
Which claim from lecture 12 or 13 did your numbers support, and which did they leave open?

The practice-query intervals let us claim that rerank performs the best overall. Its MRR@10 interval compared to hybrid is +0.154 to +0.457, compared to dense +0.150 to +0.533, and compared to bm25 +0.200 to +0.595, which all exclude zero. hybrid against dense and bm25 is not distinguishable on MRR@10 because the intervals include zero, while in Recall@10 hybrid is higher than both of these. rerank against hybrid on Recall@10 though, is not distinguishable (+0.000 to +0.050). The 20 query minimum detectable difference is 0.22 to 0.29 for MRR@10, so smaller gaps would be invisible if they exist. This supports the claim that no retiever wins everywhere. bm25 wins identifiers but loses paraphrase (0.810 vs 0.000), while dense demonstrates the reverse (0.333 vs 0.714). This claim doesnt cover everything though, since these numbers are practice scores and hybrid's k and the reranker prompt were tuned on those queries. 

---

## 2. Stage 1 - cited answers on the 12 shared questions

<!-- p2:begin answers -->
| Label | System | Verified (in) | 95% interval | not_found (in) | Declined (out) | 95% interval | Quotes found |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| rerank | rerank | 8 of 8 (100%) | [0.676, 1.000] | 0 of 8 (0%) | 4 of 4 (100%) | [0.510, 1.000] | 13 of 13 |
<!-- p2:end answers -->

Which system answered, and why that one?
What did you change in `prompts/answer.txt`, if anything, and did the verified share or the declined share move?

Then read three in-corpus answers that `uv run p2 verify` passed.
For each one, open the cited chunk and say whether the quote really supports the claim next to it.
The check proves a quote is a real piece of the chunk and cannot prove that it supports the claim, so this reading is the part only you can do.


The rerank system answered, since it scored the highest. I did not change anything in prompts/answer.txt so the verified share and declined share did not move. 

For the question "Within how many minutes must a mine operator call MSHA after an accident that kills a miner?", the gold section id is cfr30-50.10 which is used for both claims of the answer. This chunk contains both quotes that support the claims.
The claim "The operator must contact MSHA immediately, without delay and within 15 minutes, at the toll-free number once the operator knows or should know of an accident." quotes "The operator shall immediately contact MSHA at once without delay and within 15 minutes at the toll-free number, 1-800-746-1553, once the operator knows or should know that an accident has occurred involving:" which removes the actual phone number and changes some wording slightly for sentence flow. Then, "This notification requirement covers an accident involving a death of an individual at the mine." quotes "(a) A death of an individual at the mine;" which adds some words for context and clarity.

For the question "How long must the self-rescue device given to each underground coal miner be able to protect that person?", the gold section ids are cfr30-75.1714 and cfr30-75.1714-1 which are both retrieved and the first is cited. This chunk contains the quote that supports the claim. The claim is "Each operator must make available to each miner going underground an approved self-rescue device adequate to protect that person for 1 hour or longer." comes from the quote "an approved self-rescue device or devices which is adequate to protect such person for 1 hour or longer." This removes the 'or devices' from the original yet maintains meaning.

For the question "What is the permissible exposure level for noise at a mine, as an 8-hour average?", the gold section id is crf 30-62.101 which is retrieved and cited. This chunk contains the quote and supports the claim. The claim is "The permissible exposure level is an 8-hour time-weighted average of 90 dBA, equivalent to a 100% dose." from the quote "Permissible exposure level. A TWA8 of 90 dBA or equivalently a dose of 100% of that permitted by the standard, integrating all sound levels from 90 dBA to at least 140 dBA." This restrucures the quote and phrasing by removing unnecessary words without losing meaning and replaces TWA8 with its meaning.

---

## 3. Stage 2 - your corpus and your gold set

### The corpus

What is it, where did it come from, how many documents and how many megabytes, and what is the license basis for publishing it?
Name the one or two documents you were least sure about and what you decided.
Say which of the allowed sources in the brief it comes from.

TODO: describe your corpus and its license basis.

### The gold set

How many queries, how many with origin `hand` and how many with origin `claude`, and which query classes did you use and why?
How did you decide that a document is relevant: write your relevance rule in two or three sentences, the way the brief does for the shared corpus.
How did you find candidates (the systems' top 10, a keyword search, reading), and did you read every document before you labeled it?
Your labels are binary (`rel` 1) unless you say otherwise: if you use graded labels, declare the scale here, for example 2 means the document answers the query fully and 1 means it helps.

TODO: describe your gold set and your relevance rule.

---

## 4. Stage 2 - results on your corpus

Scores per system on your gold set.

<!-- p2:begin own -->
_No scored runs here yet: run `uv run p2 run --corpus own --system bm25` (or `--all`), then `uv run p2 score`._
<!-- p2:end own -->

The same scores per query class.

<!-- p2:begin own-classes -->
_No scored runs here yet: run `uv run p2 run --corpus own --system bm25` (or `--all`), then `uv run p2 score`._
<!-- p2:end own-classes -->

The same scores for the queries you wrote yourself (`hand`) and the ones a model drafted (`claude`), with the difference between the two groups and its interval.
Once both groups have queries, the table also says whether `bm25`'s lead over `dense` differs between them, and what share of each query's content words its best relevant document contains, which is stretch option 6.

<!-- p2:begin own-origins -->
_No scored runs here yet: run `uv run p2 run --corpus own --system bm25` (or `--all`), then `uv run p2 score`._
<!-- p2:end own-origins -->

Differences between every pair of systems.

<!-- p2:begin own-pairs -->
_No scored runs here yet: run `uv run p2 run --corpus own --system bm25` (or `--all`), then `uv run p2 score`._
<!-- p2:end own-pairs -->

Which differences are distinguishable and which are not, at your gold-set size?
Do the `hand` queries and the `claude` queries tell the same story?
Did your prediction in `DECISIONS.md` prompt 1 hold?

TODO: write what your own-corpus intervals let you claim.

---

## 5. The ablation

Change one thing and keep everything else the same.
Write your hypothesis here before you run it, in one sentence with a direction: "I expect X to raise MRR@10 on my corpus because Y."
The run file for it lives in `runs/own/ablation/`.

<!-- p2:begin own-ablation -->
_No ablation runs yet: `uv run p2 run --corpus own --system NAME --ablation` writes one to runs/own/ablation/, then `uv run p2 score` fills this table._
<!-- p2:end own-ablation -->

The queries your ablation helped and hurt, against the system it varies, by reciprocal rank.
`p2 score` finds that system from a line such as `BASE = "bm25"` in your variant's file, or else from its name: `bm25_lab` varies `bm25`.

<!-- p2:begin own-ablation-queries -->
_No ablation runs yet: `uv run p2 run --corpus own --system NAME --ablation` writes one to runs/own/ablation/, then `uv run p2 score` fills this table._
<!-- p2:end own-ablation-queries -->

What did you change, what happened, and does the interval support the claim you want to make?
If the result is not distinguishable, say what size of effect your gold set could have seen.
Read the queries at the top of each list in the second table, and say whether your change explains them.

TODO: write the ablation: the one change, the hypothesis, the result and the claim.

---

## 6. Failure analysis

Pick the queries where your best system on your own corpus failed: the relevant document is missing from the top 10, or sits far below the top.
Take at least five, and read what the system returned next to what was relevant.
Then sort the failures by cause, for example a vocabulary mismatch, near-duplicate documents, a chunk that cut the answer in half, a query that is ambiguous, or a label that was wrong, because sometimes the gold set is what failed.

| qid | what the best system returned | what was relevant | cause | what you would try |
|---|---|---|---|---|

TODO: add one row for each failure you analyzed, and write two or three sentences on the pattern you see across them.

---

## 7. Cross-corpus comparison

The two tables to compare are the shared-corpus scores in section 1 and your own-corpus scores in section 4, with their intervals.
If you want them side by side, copy the rows you need into a table here and say that you copied them.

Did the winner change between the shared corpus and yours?
Why, or why not: what is different about the two collections (document length, vocabulary, identifiers, near-duplicates, how the queries were written), and which of your explanations did you test and which are guesses?
Say what 20 queries on one side and your gold-set size on the other cannot support.

TODO: write the cross-corpus comparison.

---

## 8. Stretch

498E: the stretch is one of the six options in the brief's "One stretch" section, and that section says what earns the 25 points for each.
It is optional, so `uv run p2 check --final` never waits on this section.
598E: the rider is your stretch, so write "rider" below and put its results in section 9; the other options add no points, because the project is capped at 150.

Whichever option you chose, write these five things:

1. The option's name.
2. What you did, and the files that hold it.
3. The table `p2 score` wrote for it, by name: one of the three below, `own-ablation` and `own-ablation-queries` in section 5 for a second ablation, `own-origins` in section 4 for the hand and claude queries, or `repeats` in section 9 for the rider.
4. What its interval lets you claim, and what it does not.
5. One thing you would do next, and what result would tell you it worked.

For a second ablation, write its hypothesis here before you run it, and commit it, so your history shows that it came first.
For the hand and claude queries, do the same with your prediction before you score.

### Claim-level faithfulness check (option 2)

Claude's verdicts from `p2 judge` against your own verdicts in the calibration file.

<!-- p2:begin stretch-judge -->
_No judged answers yet (stretch option 2): `uv run p2 judge answers/shared/LABEL.json` writes them, your own verdicts go in answers/shared/LABEL.calibration.tsv, and then `uv run p2 score` fills this table._
<!-- p2:end stretch-judge -->

### Cost and latency (option 3)

The Claude calls, tokens and seconds in every trace you committed, and what a cheaper system or answers file saves against what it loses.

<!-- p2:begin stretch-cost -->
Every trace in traces/ that records a Claude call:

| Trace | System | Spans | Claude calls | Saved | Input tokens | Output tokens | Seconds | Input per span | Output per span | Seconds per span |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| traces/answers-rerank.jsonl | rerank | 12 | 24 | 4 | 210,780 | 4,442 | 94.8 | 17,565 | 370 | 7.9 |
| traces/shared-practice-rerank.jsonl | rerank | 20 | 20 | 2 | 227,379 | 2,513 | 77.6 | 11,369 | 126 | 3.9 |
| traces/shared-test-rerank.jsonl | rerank | 40 | 40 | 0 | 453,460 | 4,492 | 156.7 | 11,336 | 112 | 3.9 |

A span is one query of a run, one question of an answers file, or one claim of a judged file. A saved reply costs nothing now, so it counts the tokens and the seconds of the call that made it.

Every pair of systems on the same queries where at least one calls Claude, the one with fewer Claude input tokens per query first:

| Cheaper minus dearer | Queries | MRR@10 difference | 95% interval | Input tokens saved per query | Seconds saved per query | Reading |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| shared practice: bm25 minus rerank | 20 | -0.393 | [-0.595, -0.200] | 11,369 | 3.9 | rerank higher |
| shared practice: dense minus rerank | 20 | -0.338 | [-0.533, -0.150] | 11,369 | 3.9 | rerank higher |
| shared practice: hybrid minus rerank | 20 | -0.378 | [-0.560, -0.206] | 11,369 | 3.9 | rerank higher |

The difference is the cheaper system's score minus the dearer one's, with its paired interval; the savings count Claude calls only, so a system that makes none saves all of the other's.

Systems that do not call Claude, from traces/retrieval/ on the machine that last ran `p2 score` (git ignores that folder, so `p2 check` does not compare this part):

| Trace | System | Queries | Seconds | Milliseconds per query |
| --- | --- | ---: | ---: | ---: |
| traces/retrieval/shared-practice-bm25.jsonl | bm25 | 20 | 0.04 | 2.0 |
| traces/retrieval/shared-practice-dense.jsonl | dense | 20 | 0.28 | 14.1 |
| traces/retrieval/shared-practice-hybrid.jsonl | hybrid | 20 | 0.25 | 12.7 |
| traces/retrieval/shared-test-bm25.jsonl | bm25 | 40 | 0.09 | 2.3 |
| traces/retrieval/shared-test-dense.jsonl | dense | 40 | 0.39 | 9.7 |
| traces/retrieval/shared-test-hybrid.jsonl | hybrid | 40 | 0.50 | 12.5 |
<!-- p2:end stretch-cost -->

### The grep agent (option 5)

Your stretch run on some of your own queries against the four systems on the same queries.

<!-- p2:begin stretch-agent -->
_No stretch runs yet (stretch option 5): `uv run p2 run --corpus own --queries eval/own/agent.queries.tsv --system agent --stretch` writes one to runs/own/stretch/, then `uv run p2 score` fills this table._
<!-- p2:end stretch-agent -->

### Your stretch

Write the five things here.

---

## 9. 598E only - repeats and the pre-registered claim

498E students can leave this section as it is; nothing checks it.
598E students replace each line that starts with "598E: write", and `uv run p2 check --final` counts those lines as work still to do until they are gone.

### Repeats on the shared corpus

Three runs of the reranker on the practice queries, and three answers files, with their run-to-run spread and Wilson intervals.

<!-- p2:begin repeats -->
_No repeated runs or answers files yet (598E: `p2 run ... --repeat 3` and `p2 answer ... --repeat 3`)._
<!-- p2:end repeats -->

Does the reranker's gain over its first stage survive the run-to-run variation?
Write what the spread is, how it compares with the gain, and what the Wilson intervals on the verified share and the declined share say about 8 and 4 questions.

598E: write the repeats result here.

### The pre-registered claim

The claim, the smallest effect, the gold-set size and the test are in `PREREG.md`, committed before your own gold-set judgments.
Here, say whether you followed the plan, what the interval turned out to be, and what that means.
The outcome section of `PREREG.md` holds the short version.

598E: write the claim and its outcome here.
