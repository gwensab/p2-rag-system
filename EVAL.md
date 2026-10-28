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

hybrid - Hybrid fuses bm25 and dense by reciprocal rank fusion over their full document ranking. The initial k value of 60 had poor performance of 0.471, yet lowering the k value to 5 improved score to 0.599 but resulted in the CI failing. Ultimately I am sticking to k=60 for hybrid.

rerank - Rerank uses the Sonnet model, cuts passages to 600 characters and a bad reply keeps the first stage order. The changes from lab 13 include the schema bounds and the first stage which is bm25 and dense fused with reciprocal rank fusion at its own k of 5. Its top 20 candidates go to claude.

---

### Practice queries (20)

Scores per system.

<!-- p2:begin shared-practice -->
| System | Recall@10 | MRR@10 | nDCG@10 |
| --- | ---: | ---: | ---: |
| bm25 | 0.625 | 0.507 | 0.518 |
| dense | 0.558 | 0.562 | 0.480 |
| hybrid | 0.592 | 0.471 | 0.444 |
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
| hybrid | Recall@10 | 0.500 | 0.405 | 0.917 |
| hybrid | MRR@10 | 0.514 | 0.154 | 0.792 |
| hybrid | nDCG@10 | 0.397 | 0.203 | 0.779 |
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
| hybrid minus bm25 | Recall@10 | -0.033 | [-0.250, +0.192] | 0.324 | not distinguishable |
| hybrid minus bm25 | MRR@10 | -0.036 | [-0.178, +0.084] | 0.193 | not distinguishable |
| hybrid minus bm25 | nDCG@10 | -0.075 | [-0.238, +0.075] | 0.228 | not distinguishable |
| hybrid minus dense | Recall@10 | +0.033 | [-0.125, +0.192] | 0.231 | not distinguishable |
| hybrid minus dense | MRR@10 | -0.091 | [-0.305, +0.110] | 0.300 | not distinguishable |
| hybrid minus dense | nDCG@10 | -0.036 | [-0.199, +0.113] | 0.227 | not distinguishable |
| rerank minus bm25 | Recall@10 | +0.208 | [+0.050, +0.383] | 0.242 | rerank higher |
| rerank minus bm25 | MRR@10 | +0.393 | [+0.200, +0.595] | 0.287 | rerank higher |
| rerank minus bm25 | nDCG@10 | +0.331 | [+0.167, +0.506] | 0.248 | rerank higher |
| rerank minus dense | Recall@10 | +0.275 | [+0.100, +0.450] | 0.259 | rerank higher |
| rerank minus dense | MRR@10 | +0.338 | [+0.150, +0.533] | 0.273 | rerank higher |
| rerank minus dense | nDCG@10 | +0.370 | [+0.205, +0.544] | 0.246 | rerank higher |
| rerank minus hybrid | Recall@10 | +0.242 | [+0.092, +0.417] | 0.236 | rerank higher |
| rerank minus hybrid | MRR@10 | +0.429 | [+0.246, +0.614] | 0.266 | rerank higher |
| rerank minus hybrid | nDCG@10 | +0.406 | [+0.256, +0.564] | 0.221 | rerank higher |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time.
<!-- p2:end shared-practice-pairs -->

The 40 test queries have no answer key in this repo.
Your test run files are scored by the course and the score comes back to you as feedback, so nothing goes here for them.

### What the intervals let you claim

Which differences are distinguishable from zero and which are not?
What is the minimum detectable difference at 20 queries, and what does that say about any gap smaller than it?
Which claim from lecture 12 or 13 did your numbers support, and which did they leave open?

The practice-query intervals let us claim that rerank performs the best overall. Its MRR@10 interval compared to hybrid is +0.246 to +0.614, compared to dense +0.150 to +0.533, and compared to bm25 +0.200 to +0.595, which all exclude zero. hybrid against dense and bm25 is not distinguishable on MRR@10 because the intervals include zero, and in Recall@10 hybrid abainst dense and bm25 are both not distinguishable since the interval includes zero. rerank against hybrid on Recall@10 though, is distinguishably higher (+0.092 to +0.417). The 20 query minimum detectable difference is 0.19 to 0.41 for MRR@10, so smaller gaps would be invisible if they exist. This supports the claim that no retiever wins everywhere. bm25 wins identifiers but loses paraphrase (0.810 vs 0.000), while dense demonstrates the reverse (0.333 vs 0.714). This claim doesnt cover everything though, since these numbers are practice scores. 

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

The corpus contains 498 files which contain a title and an abstract in each file of 2025 arXiv papers listed in both the robotics and computer vision topics. It contains 99,225 words, approximately 140,000 tokens, and has a size of 0.9 MB. 

According to arXiv's API terms page, "you are free to use descriptive metadata about arXiv e-prints under the terms of the Creative Commons Universal (CC0 1.0) Public Domain Declaration." Metadata includes "title, abstract, authors, identifiers, and classification terms" which works for out purposes here. Therefore the license basis allows us to only access the title, and abstracts.

I was not unsure about any of the documents, the p2 license run flagged nothing and I ensured that we are only using titles and abstract which lie under the cc0-1.0 license for public use as detailed.

### The gold set

How many queries, how many with origin `hand` and how many with origin `claude`, and which query classes did you use and why?
How did you decide that a document is relevant: write your relevance rule in two or three sentences, the way the brief does for the shared corpus.
How did you find candidates (the systems' top 10, a keyword search, reading), and did you read every document before you labeled it?
Your labels are binary (`rel` 1) unless you say otherwise: if you use graded labels, declare the scale here, for example 2 means the document answers the query fully and 1 means it helps.

I have 30 total queries, 12 with the origin hand and 18 with the origin claude. Both the queries I wrote and those by claude cover a variety of identifier, paraphrase, and mixed classes to test performance on different classes.  Identifiers test exact name matching, paraphrases test meaning without entirely shared words, and mixed queries test both. Claude queries were drafted from abstracts so they may share more words with the papers.

Relevance rule: The abstract must give information that helps answer the question for paraphrase and mixed. Identifiers must be named explicitly in either the title or the abstract. For topic queries and paraphrase, the abstracts main contribution should include the query's subject, not just a mention.

To find candidates come from the top 10 of the three systems, the keyword scan, and my own reading. I read most of the abstracts before labeling.

---

## 4. Stage 2 - results on your corpus

Scores per system on your gold set.

<!-- p2:begin own -->
| System | Recall@10 | MRR@10 | nDCG@10 |
| --- | ---: | ---: | ---: |
| bm25 | 0.900 | 0.878 | 0.883 |
| dense | 0.883 | 0.751 | 0.780 |
| hybrid | 0.950 | 0.844 | 0.869 |
| rerank | 0.950 | 0.719 | 0.763 |
| ablation/dense_prefix | 0.850 | 0.746 | 0.768 |
| ablation/rerank_p1500 | 0.917 | 0.793 | 0.813 |

30 judged queries; nDCG uses binary labels; a random ranking of the 498 documents would get recall@10 near 0.020.
<!-- p2:end own -->

The same scores per query class.

<!-- p2:begin own-classes -->
| System | Metric | identifier (n=10) | paraphrase (n=11) | mixed (n=9) |
| --- | --- | ---: | ---: | ---: |
| bm25 | Recall@10 | 1.000 | 0.818 | 0.889 |
| bm25 | MRR@10 | 1.000 | 0.818 | 0.815 |
| bm25 | nDCG@10 | 1.000 | 0.818 | 0.833 |
| dense | Recall@10 | 0.900 | 0.773 | 1.000 |
| dense | MRR@10 | 0.850 | 0.609 | 0.816 |
| dense | nDCG@10 | 0.863 | 0.640 | 0.858 |
| hybrid | Recall@10 | 0.900 | 0.955 | 1.000 |
| hybrid | MRR@10 | 0.900 | 0.725 | 0.926 |
| hybrid | nDCG@10 | 0.900 | 0.779 | 0.944 |
| rerank | Recall@10 | 0.900 | 0.955 | 1.000 |
| rerank | MRR@10 | 0.900 | 0.513 | 0.769 |
| rerank | nDCG@10 | 0.900 | 0.588 | 0.824 |
| ablation/dense_prefix | Recall@10 | 0.900 | 0.773 | 0.889 |
| ablation/dense_prefix | MRR@10 | 0.850 | 0.606 | 0.800 |
| ablation/dense_prefix | nDCG@10 | 0.863 | 0.638 | 0.821 |
| ablation/rerank_p1500 | Recall@10 | 1.000 | 0.773 | 1.000 |
| ablation/rerank_p1500 | MRR@10 | 1.000 | 0.616 | 0.778 |
| ablation/rerank_p1500 | nDCG@10 | 1.000 | 0.627 | 0.832 |
<!-- p2:end own-classes -->

The same scores for the queries you wrote yourself (`hand`) and the ones a model drafted (`claude`), with the difference between the two groups and its interval.
Once both groups have queries, the table also says whether `bm25`'s lead over `dense` differs between them, and what share of each query's content words its best relevant document contains, which is stretch option 6.

<!-- p2:begin own-origins -->
| System | Metric | hand (n=12) | claude (n=18) | hand minus claude | 95% interval | Reading |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| bm25 | Recall@10 | 0.917 | 0.889 | +0.028 | [-0.194, +0.222] | not distinguishable |
| bm25 | MRR@10 | 0.861 | 0.889 | -0.028 | [-0.250, +0.194] | not distinguishable |
| bm25 | nDCG@10 | 0.875 | 0.889 | -0.014 | [-0.250, +0.194] | not distinguishable |
| dense | Recall@10 | 0.917 | 0.861 | +0.056 | [-0.167, +0.278] | not distinguishable |
| dense | MRR@10 | 0.670 | 0.806 | -0.135 | [-0.415, +0.142] | not distinguishable |
| dense | nDCG@10 | 0.728 | 0.814 | -0.086 | [-0.342, +0.165] | not distinguishable |
| hybrid | Recall@10 | 0.917 | 0.972 | -0.056 | [-0.250, +0.083] | not distinguishable |
| hybrid | MRR@10 | 0.861 | 0.832 | +0.029 | [-0.215, +0.253] | not distinguishable |
| hybrid | nDCG@10 | 0.875 | 0.865 | +0.010 | [-0.211, +0.206] | not distinguishable |
| rerank | Recall@10 | 0.917 | 0.972 | -0.056 | [-0.250, +0.083] | not distinguishable |
| rerank | MRR@10 | 0.486 | 0.873 | -0.387 | [-0.639, -0.119] | claude higher |
| rerank | nDCG@10 | 0.587 | 0.880 | -0.294 | [-0.509, -0.073] | claude higher |
| ablation/dense_prefix | Recall@10 | 0.833 | 0.861 | -0.028 | [-0.306, +0.222] | not distinguishable |
| ablation/dense_prefix | MRR@10 | 0.711 | 0.769 | -0.057 | [-0.348, +0.231] | not distinguishable |
| ablation/dense_prefix | nDCG@10 | 0.741 | 0.786 | -0.045 | [-0.321, +0.224] | not distinguishable |
| ablation/rerank_p1500 | Recall@10 | 0.917 | 0.917 | +0.000 | [-0.222, +0.167] | not distinguishable |
| ablation/rerank_p1500 | MRR@10 | 0.708 | 0.849 | -0.140 | [-0.404, +0.122] | not distinguishable |
| ablation/rerank_p1500 | nDCG@10 | 0.760 | 0.848 | -0.089 | [-0.328, +0.141] | not distinguishable |

The hand and claude queries are different queries, so the interval of hand minus claude comes from resampling the queries within each group (10,000 times), not from pairing them.

Do model-written queries favor keyword search? bm25's lead over dense (bm25 minus dense, per query) on the claude queries and on the hand queries, and claude minus hand:

| Metric | Lead on claude | Lead on hand | Claude minus hand | 95% interval | Reading |
| --- | ---: | ---: | ---: | ---: | --- |
| Recall@10 | +0.028 | +0.000 | +0.028 | [-0.278, +0.333] | not distinguishable |
| MRR@10 | +0.083 | +0.191 | -0.108 | [-0.460, +0.267] | not distinguishable |
| nDCG@10 | +0.075 | +0.147 | -0.072 | [-0.400, +0.281] | not distinguishable |

Mean content-word overlap, the share of a query's content words found in its best relevant document: hand 0.76 (12 queries), claude 0.73 (18 queries).

Stretch option 6 asks for at least 20 judged queries of each origin; here there are 12 hand and 18 claude.
<!-- p2:end own-origins -->

Differences between every pair of systems.

<!-- p2:begin own-pairs -->
| Comparison | Metric | Mean difference | 95% interval | MDD | Reading |
| --- | --- | ---: | ---: | ---: | --- |
| dense minus bm25 | Recall@10 | -0.017 | [-0.167, +0.133] | 0.217 | not distinguishable |
| dense minus bm25 | MRR@10 | -0.126 | [-0.296, +0.046] | 0.250 | not distinguishable |
| dense minus bm25 | nDCG@10 | -0.104 | [-0.264, +0.056] | 0.234 | not distinguishable |
| hybrid minus bm25 | Recall@10 | +0.050 | [-0.067, +0.167] | 0.169 | not distinguishable |
| hybrid minus bm25 | MRR@10 | -0.034 | [-0.155, +0.074] | 0.168 | not distinguishable |
| hybrid minus bm25 | nDCG@10 | -0.014 | [-0.128, +0.088] | 0.158 | not distinguishable |
| hybrid minus dense | Recall@10 | +0.067 | [+0.000, +0.167] | 0.130 | not distinguishable |
| hybrid minus dense | MRR@10 | +0.092 | [-0.025, +0.218] | 0.176 | not distinguishable |
| hybrid minus dense | nDCG@10 | +0.089 | [-0.001, +0.186] | 0.136 | not distinguishable |
| rerank minus bm25 | Recall@10 | +0.050 | [-0.067, +0.167] | 0.169 | not distinguishable |
| rerank minus bm25 | MRR@10 | -0.159 | [-0.332, +0.020] | 0.260 | not distinguishable |
| rerank minus bm25 | nDCG@10 | -0.120 | [-0.267, +0.033] | 0.220 | not distinguishable |
| rerank minus dense | Recall@10 | +0.067 | [+0.000, +0.167] | 0.130 | not distinguishable |
| rerank minus dense | MRR@10 | -0.033 | [-0.125, +0.052] | 0.128 | not distinguishable |
| rerank minus dense | nDCG@10 | -0.017 | [-0.091, +0.050] | 0.102 | not distinguishable |
| rerank minus hybrid | Recall@10 | +0.000 | [+0.000, +0.000] | - | identical on every query |
| rerank minus hybrid | MRR@10 | -0.125 | [-0.267, +0.013] | 0.204 | not distinguishable |
| rerank minus hybrid | nDCG@10 | -0.106 | [-0.210, -0.012] | 0.146 | hybrid higher |
| ablation/dense_prefix minus bm25 | Recall@10 | -0.050 | [-0.217, +0.117] | 0.236 | not distinguishable |
| ablation/dense_prefix minus bm25 | MRR@10 | -0.132 | [-0.304, +0.040] | 0.254 | not distinguishable |
| ablation/dense_prefix minus bm25 | nDCG@10 | -0.115 | [-0.282, +0.051] | 0.243 | not distinguishable |
| ablation/dense_prefix minus dense | Recall@10 | -0.033 | [-0.100, +0.000] | 0.093 | not distinguishable |
| ablation/dense_prefix minus dense | MRR@10 | -0.006 | [-0.056, +0.044] | 0.071 | not distinguishable |
| ablation/dense_prefix minus dense | nDCG@10 | -0.012 | [-0.055, +0.029] | 0.061 | not distinguishable |
| ablation/dense_prefix minus hybrid | Recall@10 | -0.100 | [-0.233, +0.000] | 0.156 | not distinguishable |
| ablation/dense_prefix minus hybrid | MRR@10 | -0.098 | [-0.227, +0.022] | 0.182 | not distinguishable |
| ablation/dense_prefix minus hybrid | nDCG@10 | -0.101 | [-0.209, -0.002] | 0.151 | hybrid higher |
| ablation/dense_prefix minus rerank | Recall@10 | -0.100 | [-0.233, +0.000] | 0.156 | not distinguishable |
| ablation/dense_prefix minus rerank | MRR@10 | +0.027 | [-0.076, +0.141] | 0.159 | not distinguishable |
| ablation/dense_prefix minus rerank | nDCG@10 | +0.005 | [-0.079, +0.097] | 0.128 | not distinguishable |
| ablation/rerank_p1500 minus bm25 | Recall@10 | +0.017 | [-0.117, +0.150] | 0.196 | not distinguishable |
| ablation/rerank_p1500 minus bm25 | MRR@10 | -0.085 | [-0.252, +0.083] | 0.241 | not distinguishable |
| ablation/rerank_p1500 minus bm25 | nDCG@10 | -0.070 | [-0.220, +0.075] | 0.214 | not distinguishable |
| ablation/rerank_p1500 minus dense | Recall@10 | +0.033 | [-0.067, +0.133] | 0.164 | not distinguishable |
| ablation/rerank_p1500 minus dense | MRR@10 | +0.041 | [-0.039, +0.139] | 0.130 | not distinguishable |
| ablation/rerank_p1500 minus dense | nDCG@10 | +0.033 | [-0.040, +0.125] | 0.121 | not distinguishable |
| ablation/rerank_p1500 minus hybrid | Recall@10 | -0.033 | [-0.133, +0.067] | 0.164 | not distinguishable |
| ablation/rerank_p1500 minus hybrid | MRR@10 | -0.051 | [-0.201, +0.096] | 0.215 | not distinguishable |
| ablation/rerank_p1500 minus hybrid | nDCG@10 | -0.056 | [-0.180, +0.068] | 0.179 | not distinguishable |
| ablation/rerank_p1500 minus rerank | Recall@10 | -0.033 | [-0.133, +0.067] | 0.164 | not distinguishable |
| ablation/rerank_p1500 minus rerank | MRR@10 | +0.074 | [-0.009, +0.177] | 0.136 | not distinguishable |
| ablation/rerank_p1500 minus rerank | nDCG@10 | +0.050 | [-0.028, +0.147] | 0.128 | not distinguishable |
| ablation/rerank_p1500 minus ablation/dense_prefix | Recall@10 | +0.067 | [-0.067, +0.200] | 0.187 | not distinguishable |
| ablation/rerank_p1500 minus ablation/dense_prefix | MRR@10 | +0.047 | [-0.046, +0.153] | 0.147 | not distinguishable |
| ablation/rerank_p1500 minus ablation/dense_prefix | nDCG@10 | +0.045 | [-0.043, +0.142] | 0.136 | not distinguishable |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time. Two systems that score the same on every query have no interval to speak of, so their MDD is shown as -.
<!-- p2:end own-pairs -->

Which differences are distinguishable and which are not, at your gold-set size?
Do the `hand` queries and the `claude` queries tell the same story?
Did your prediction in `DECISIONS.md` prompt 1 hold?


At my gold-set size, no pair of the four systems overall is distinguishable from another. The widest gaps are rerank minus bm25 at -0.159 [-0.332, +0.020] and rerank minus hybrid at -0.125 [-0.267, +0.013] which both include zero. The one pair that is distinguishable for one system is rerank minus hybrid on nDCG@10  which is -0.106 [-0.210, -0.012] with hybrid being higher. These two are identical on recall@10 for every query. 
The minimum detectable difference for MRR@10 is between 0.128 (rerank vs dense) and 0.260 (rerank vs bm25). Although estimates point towards bm25 beating rerank, we cannot claim that because a gap smaller than the existing one is invisible for my gold-set size of 30. 
For bm25, dense, and hybrid both hand and claude results are indistingushable. But rerank has a distingishable gap of -0.387 [-0.639, -0.119] with claude higher. Claude and hand written queries were indistinguishable when looking at if they favor keyword search,since the interval includes zero but leans towards hand queries having more. Content-word overlap is also similar (hand 0.76, claude 0.73) so that also doesnt explain the rerank gap. A likely contributer to claude queries scoring higher is that my hand queries included broader topical questions that could have been answered by many papers but only had one in the gold set.
My prediction from the decisions prompt 1 did not hold. I expected rerank to perform best, dense to be fairly good and bm25 to be the worst. On MRR@10 and nDCG@10, bm25 is best, and rerank is the lowest with dense in third. On recall@10 rerank and hybrid are tied for best at 0.950, followed by bm25 and dense. This almost entirely opposes my initial prediction. This is likely due to the structure of my queries. My corpus had more overlap between queries and texts than the CFR for every class which largely explains why bm25 performed well. Rerank does not perform well because the reranker often selects the right paper in its top 5 on the first stage so the reranker just adds noise. 

---

## 5. The ablation

Change one thing and keep everything else the same.
Write your hypothesis here before you run it, in one sentence with a direction: "I expect X to raise MRR@10 on my corpus because Y."
The run file for it lives in `runs/own/ablation/`.

<!-- p2:begin own-ablation -->
| Comparison | Metric | Mean difference | 95% interval | MDD | Reading |
| --- | --- | ---: | ---: | ---: | --- |
| ablation/dense_prefix minus bm25 | Recall@10 | -0.050 | [-0.217, +0.117] | 0.236 | not distinguishable |
| ablation/dense_prefix minus bm25 | MRR@10 | -0.132 | [-0.304, +0.040] | 0.254 | not distinguishable |
| ablation/dense_prefix minus bm25 | nDCG@10 | -0.115 | [-0.282, +0.051] | 0.243 | not distinguishable |
| ablation/dense_prefix minus dense | Recall@10 | -0.033 | [-0.100, +0.000] | 0.093 | not distinguishable |
| ablation/dense_prefix minus dense | MRR@10 | -0.006 | [-0.056, +0.044] | 0.071 | not distinguishable |
| ablation/dense_prefix minus dense | nDCG@10 | -0.012 | [-0.055, +0.029] | 0.061 | not distinguishable |
| ablation/dense_prefix minus hybrid | Recall@10 | -0.100 | [-0.233, +0.000] | 0.156 | not distinguishable |
| ablation/dense_prefix minus hybrid | MRR@10 | -0.098 | [-0.227, +0.022] | 0.182 | not distinguishable |
| ablation/dense_prefix minus hybrid | nDCG@10 | -0.101 | [-0.209, -0.002] | 0.151 | hybrid higher |
| ablation/dense_prefix minus rerank | Recall@10 | -0.100 | [-0.233, +0.000] | 0.156 | not distinguishable |
| ablation/dense_prefix minus rerank | MRR@10 | +0.027 | [-0.076, +0.141] | 0.159 | not distinguishable |
| ablation/dense_prefix minus rerank | nDCG@10 | +0.005 | [-0.079, +0.097] | 0.128 | not distinguishable |
| ablation/rerank_p1500 minus bm25 | Recall@10 | +0.017 | [-0.117, +0.150] | 0.196 | not distinguishable |
| ablation/rerank_p1500 minus bm25 | MRR@10 | -0.085 | [-0.252, +0.083] | 0.241 | not distinguishable |
| ablation/rerank_p1500 minus bm25 | nDCG@10 | -0.070 | [-0.220, +0.075] | 0.214 | not distinguishable |
| ablation/rerank_p1500 minus dense | Recall@10 | +0.033 | [-0.067, +0.133] | 0.164 | not distinguishable |
| ablation/rerank_p1500 minus dense | MRR@10 | +0.041 | [-0.039, +0.139] | 0.130 | not distinguishable |
| ablation/rerank_p1500 minus dense | nDCG@10 | +0.033 | [-0.040, +0.125] | 0.121 | not distinguishable |
| ablation/rerank_p1500 minus hybrid | Recall@10 | -0.033 | [-0.133, +0.067] | 0.164 | not distinguishable |
| ablation/rerank_p1500 minus hybrid | MRR@10 | -0.051 | [-0.201, +0.096] | 0.215 | not distinguishable |
| ablation/rerank_p1500 minus hybrid | nDCG@10 | -0.056 | [-0.180, +0.068] | 0.179 | not distinguishable |
| ablation/rerank_p1500 minus rerank | Recall@10 | -0.033 | [-0.133, +0.067] | 0.164 | not distinguishable |
| ablation/rerank_p1500 minus rerank | MRR@10 | +0.074 | [-0.009, +0.177] | 0.136 | not distinguishable |
| ablation/rerank_p1500 minus rerank | nDCG@10 | +0.050 | [-0.028, +0.147] | 0.128 | not distinguishable |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time.
<!-- p2:end own-ablation -->

The queries your ablation helped and hurt, against the system it varies, by reciprocal rank.
`p2 score` finds that system from a line such as `BASE = "bm25"` in your variant's file, or else from its name: `bm25_lab` varies `bm25`.

<!-- p2:begin own-ablation-queries -->
ablation/dense_prefix against dense (BASE = "dense" in p2/retrievers/dense_prefix.py): it helped 2 queries, hurt 3 and left 25 unchanged.

| Query | Class | Origin | dense RR | ablation/dense_prefix RR | Change | Effect |
| --- | --- | --- | ---: | ---: | ---: | --- |
| h07 | paraphrase | hand | 0.500 | 1.000 | +0.500 | helped |
| h10 | paraphrase | hand | 0.200 | 0.333 | +0.133 | helped |
| c07 | paraphrase | claude | 1.000 | 0.500 | -0.500 | hurt |
| c09 | paraphrase | claude | 0.500 | 0.333 | -0.167 | hurt |
| h06 | mixed | hand | 0.143 | 0.000 | -0.143 | hurt |

ablation/rerank_p1500 against rerank (BASE = "rerank" in p2/retrievers/rerank_p1500.py): it helped 5 queries, hurt 3 and left 22 unchanged.

| Query | Class | Origin | rerank RR | ablation/rerank_p1500 RR | Change | Effect |
| --- | --- | --- | ---: | ---: | ---: | --- |
| h02 | identifier | hand | 0.000 | 1.000 | +1.000 | helped |
| h08 | paraphrase | hand | 0.167 | 1.000 | +0.833 | helped |
| h09 | paraphrase | hand | 0.500 | 1.000 | +0.500 | helped |
| h07 | paraphrase | hand | 0.143 | 0.500 | +0.357 | helped |
| h05 | mixed | hand | 0.250 | 0.333 | +0.083 | helped |
| c09 | paraphrase | claude | 0.500 | 0.167 | -0.333 | hurt |
| c12 | paraphrase | claude | 0.111 | 0.000 | -0.111 | hurt |
| h10 | paraphrase | hand | 0.111 | 0.000 | -0.111 | hurt |

RR is the reciprocal rank of the first relevant document in the top 10 (0 when none is there), the per-query value behind MRR@10; the queries at the top of each list are the ones to read.
<!-- p2:end own-ablation-queries -->

What did you change, what happened, and does the interval support the claim you want to make?
If the result is not distinguishable, say what size of effect your gold set could have seen.
Read the queries at the top of each list in the second table, and say whether your change explains them.


Hypothesis: I plan to change the character limit from 600 to 1500. I believe that this will increase the MRR@10 for rerank on my corpus because it will allow an entire abstract to fit in a chunk, rather than just the first part of one. This is supported by the fact that the rerank score is low on paraphrase queries because the important information is usually later in the abstract. The median abstract length is 1,400 characters so 1,500 should cover most of them.

Results: The rerank MRR@10 score at 1,500 characters is 0.793 conpared to 0.719 at 600 characters. This is a difference of +0.074 with an interval of [-0.009, +0.177] which makes it undistinguishable. However, the direction still matches my hypothesis. The minimum detectable difference is 0.136 so the direction fits but the 30 queries cannot confirm it. nDCG@10 behaved simillarly while recall@10 slipped slightly. Claude generated a table demonstrating the scores on identifier, paraphrase, and mixed for each number of characters. Overall 1500 characters performed better on average. Paraphrase gained +0.103 which supports my earlier reasoning. The identifier class also rose by 0.100 which i did not anticipate. h02 underwent the biggest gain, (0.000 to 1.000) since the identifier "SATA" first appears at character 935. Additionally, h08 focuses on older VLN models which is mentioned at character 672 of the abstract. Both of these were helped by increasing the character limit. h10 and c09 were both hurt by this, since their original answers appeared at characters 354 and 1705. Rank dropped for both of these but cannot necessarily be explained by the locations of relevant info. From the cost table, rerank at 1,500 chars uses about 12.904 inputs per query and 6.1 seconds compared to 9,652 and 4.7 seconds for 600 chars. I think this is a fair tradeoff for the obtained results. The interval ultimately supports that the direction matches my hypothesis and the effect on paraphrase queries is potentially real, but indistinguishable from zero on only 30 queries. We cannot, therefore, claim that 1,500 characters is better in general since the interval includes zero. More paraprase queries would solidify the outcome.

---

## 6. Failure analysis

Pick the queries where your best system on your own corpus failed: the relevant document is missing from the top 10, or sits far below the top.
Take at least five, and read what the system returned next to what was relevant.
Then sort the failures by cause, for example a vocabulary mismatch, near-duplicate documents, a chunk that cut the answer in half, a query that is ambiguous, or a label that was wrong, because sometimes the gold set is what failed.

| qid | what the best system returned | what was relevant | cause | what you would try |
|---|---|---|---|---|
| c08 | bm25: OpenLKA (2501.03287) | "Robust sensor fusion against on-vehicle sensor staleness" (2506.05780) | vocabulary mismatch | rewrite the query or use dense or hybrid |
| c11 | bm25: "Motion Synthesis with Sparse and Flexible Keyjoint Control" (2503.15557) | "Universal Online Temporal Calibration..." (2501.01788) | vocabulary mismatch | rewrite the query or use dense |
| h04 | bm25: "Mixture of Horizons in Action Chunking" (2511.19433) | Cosmos World Foundation Model Platform (2501.03575) | filler words | remove question words from query |
| h05 | bm25: DiWA (2508.03645) | "Multimodal Spatial Language Maps..." (2506.06862) | broad query, narrow gold set | judge more papers for broad queries |
| h02 | rerank: 2501.01704 (satellite fiducial paper) | 2512.23162 | character limit | show the reranker more characters |
| h08 | rerank returned 2512.00027 (the VLN survey) | 2508.02917 | character limit | show the reranker more characters |



---

## 7. Cross-corpus comparison

The two tables to compare are the shared-corpus scores in section 1 and your own-corpus scores in section 4, with their intervals.
If you want them side by side, copy the rows you need into a table here and say that you copied them.

Did the winner change between the shared corpus and yours?
Why, or why not: what is different about the two collections (document length, vocabulary, identifiers, near-duplicates, how the queries were written), and which of your explanations did you test and which are guesses?
Say what 20 queries on one side and your gold-set size on the other cannot support.


Yes the winner did change between the shared corpus and my own. On the shared practice set, rerank performed the best by a significant margin, distinguishably from the other three. On my corpus, bm25 is best by point estimate but no two pair is actually distinguishable since all intervals include zero.
One key difference was the query wording overlap. On my corpus, paraphrase queries shared 0.49 of the words with the paper, while the CFR was only 0.11 shared. This is partially due to claudes queries which mostly pulled from the documents and my own which were also mostly derived directly from documents. Document length also varied between the corpuses, with CFR being approximately 300 words and my own being 1400 characters long.
Since the CFR has 20 queries and my gold-set contains 30, we have a fairly small minimum detectable difference for both (0.19 to 0.41 for CFR and 0.13 to 0.26 for mine). Differences smaller than these are invisible which gives us a small range. Also its harder to see concrete winners with such small query sets. Also rerank and hybrids settings were tuned using the practice data so the performance is biased there. 

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

1. I selected option 4, a second ablation of a different kind. 
Hypothesis: I expect that adding BGE's retrieval instruction to the front of each query will raise dense MMR@10 scores on the paraphrase queries for my corpus, since the model was trained with that prefix on short queries searched against longer passages and paraphrase queries are the ones that share the fewest words with the abstracts that answer them.

2. The BGE retrieval instruction was added in front of every query and nothing else was changed. This included editing and running the variant which wrote to p2/retrievers/dense_prefix.py (the variant) and runs/own/ablation/dense_prefix.trec (the run). This changed how the first-stage query is embedded.

3. The tables are own-ablation and own-ablation-queries are in section 5 where rerank_p1500 appears. 

4. The MRR@10 changed by -0.006 with an interval of [-0.056, +0.044]. This interval includes zero and the minimum detectable difference in 0.071. With 30 queries the prefix did not make a substatial difference in results. Therefore my hypothesis was not supported by the results. The paraphrase score is indistingushable from the previous, going from 0.609 to 0.606 We cannot claim though, that the prefix would never help. A bigger effect is rulled out but a smaller one is not. The four queries I read were h07, h10, c07, and c09. In each of these queries, the judged paper stayed in the top 10 and every move was only 1 or two places. Since my gold set only has one paper per query, a swap with an equally good paper is considered a loss which helps to explain the results. Since two queries went up and two went down, they essenstially cancel each other out and result in very little change.

5. One thing I would do next would be to try again with a bigger gold set to allow a smaller effect to be detected on the MRR@10 score. Ideally the result that would show this worked would be an interval excluding zero to demonstrate an actual difference. The other good outcome would be an interval that narrows tightly around zero, like +-0.03 for example which would solidify that the prefix does nothing.

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
| traces/own-own-ablation-rerank_p1500.jsonl | rerank_p1500 | 30 | 30 | 2 | 387,117 | 2,730 | 181.7 | 12,904 | 91 | 6.1 |
| traces/own-own-rerank.jsonl | rerank | 30 | 30 | 18 | 289,572 | 2,730 | 140.2 | 9,652 | 91 | 4.7 |
| traces/shared-practice-rerank.jsonl | rerank | 20 | 20 | 2 | 227,379 | 2,513 | 77.6 | 11,369 | 126 | 3.9 |
| traces/shared-test-rerank.jsonl | rerank | 40 | 40 | 0 | 453,460 | 4,492 | 156.7 | 11,336 | 112 | 3.9 |

A span is one query of a run, one question of an answers file, or one claim of a judged file. A saved reply costs nothing now, so it counts the tokens and the seconds of the call that made it.

Every pair of systems on the same queries where at least one calls Claude, the one with fewer Claude input tokens per query first:

| Cheaper minus dearer | Queries | MRR@10 difference | 95% interval | Input tokens saved per query | Seconds saved per query | Reading |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| shared practice: bm25 minus rerank | 20 | -0.393 | [-0.595, -0.200] | 11,369 | 3.9 | rerank higher |
| shared practice: dense minus rerank | 20 | -0.338 | [-0.533, -0.150] | 11,369 | 3.9 | rerank higher |
| shared practice: hybrid minus rerank | 20 | -0.429 | [-0.614, -0.246] | 11,369 | 3.9 | rerank higher |
| own: bm25 minus rerank | 30 | +0.159 | [-0.020, +0.332] | 9,652 | 4.7 | not distinguishable |
| own: dense minus rerank | 30 | +0.033 | [-0.052, +0.125] | 9,652 | 4.7 | not distinguishable |
| own: hybrid minus rerank | 30 | +0.125 | [-0.013, +0.267] | 9,652 | 4.7 | not distinguishable |

The difference is the cheaper system's score minus the dearer one's, with its paired interval; the savings count Claude calls only, so a system that makes none saves all of the other's.

Systems that do not call Claude, from traces/retrieval/ on the machine that last ran `p2 score` (git ignores that folder, so `p2 check` does not compare this part):

| Trace | System | Queries | Seconds | Milliseconds per query |
| --- | --- | ---: | ---: | ---: |
| traces/retrieval/own-own-ablation-dense_prefix.jsonl | dense_prefix | 30 | 0.49 | 16.3 |
| traces/retrieval/own-own-bm25.jsonl | bm25 | 30 | 0.03 | 0.9 |
| traces/retrieval/own-own-dense.jsonl | dense | 30 | 0.25 | 8.3 |
| traces/retrieval/own-own-hybrid.jsonl | hybrid | 30 | 0.36 | 11.9 |
| traces/retrieval/shared-practice-bm25.jsonl | bm25 | 20 | 0.06 | 2.9 |
| traces/retrieval/shared-practice-dense.jsonl | dense | 20 | 0.25 | 12.7 |
| traces/retrieval/shared-practice-hybrid.jsonl | hybrid | 20 | 0.43 | 21.4 |
| traces/retrieval/shared-test-bm25.jsonl | bm25 | 40 | 0.18 | 4.5 |
| traces/retrieval/shared-test-dense.jsonl | dense | 40 | 0.58 | 14.4 |
| traces/retrieval/shared-test-hybrid.jsonl | hybrid | 40 | 0.70 | 17.5 |
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
