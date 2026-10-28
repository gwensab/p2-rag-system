# Decision log

Your methods section, in your own words.
About one to two pages in total.

Answer these as you go, not the night before it is due.
Each answer is easier to write while the decision is still fresh, and prompt 1 only works if you write it before you see your own-corpus numbers.
Specifics beat polish: a short, honest answer with a number in it is worth more than a long vague one.

Each prompt ends with a marker line.
Replace that line with your answer.
`uv run p2 check` reports a marker as unfinished work, and `uv run p2 check --final` fails while any marker is left, so a finished log is part of being done.

Please do not let the agent write these for you.
These answers are about what you chose and what you knew, and the agent cannot know that.
Prompt 3 in particular only works in your own words.

---

## 1. Why this corpus, and what you expected

Why did you pick the corpus you used in stage 2, and why does it belong to a field or a question you care about?
Then say what you expected before you measured anything: which of `bm25`, `dense`, `hybrid` and `rerank` do you think will win on it, and which will do worst, and why?

Commit this answer before your first `uv run p2 score` on the own corpus.
Git history then shows that the expectation came first, which is what lets it be wrong in a way that teaches you something.
If you were surprised later, say so in prompt 4 or in EVAL.md; do not come back and rewrite this one.

I decided to use a collection of robot perception papers from arXiv which combines two topics I am extremely interested in, robotics and computer vision. This would be useful to research topics in my current courses and also apply in actual field work. This field is becoming even more relevant as robotics continues to progress and become increasingly prevalent. Additionally claude is able to extract documents from arXiv somewhat easily and it will create a managable set of relatively short documents. I expect rerank to perform the best on this data, which will stay consistent with its performance on the CFR, similar to in stage 1 but possibly by a smaller margin since there might be less for the reranker to fix if relevant abstracts are found quickly. I also think dense will perform fairly well due to its success in paraphrasing. I think bm25 will perform the worst because it is good with queries that contain a method or dataset name, but doesnt do well with more vauge topical questions and scored 0.000 on paraphrase queries on the CFR.

---

## 2. A fork in the road

Name one real design choice where you could have gone two ways: the chunk size, the embedding model, how the two systems are fused, how many documents the reranker sees, a sentence in `prompts/answer.txt`, how you cleaned the corpus.

Say which you picked, what the alternative was, and what you gave up by not taking it.
If you measured both, give both numbers.
If you rejected the alternative without measuring it, say why that was a fair call, and what it cost you in time, tokens or complexity.

"There was no alternative" is not an answer.
Find the fork.

While determining which approach to use for the embedding model, I had to choose between the 'bge-small' and 'potion' models. While potion is much faster (under 1 second), it becomes less effective when words aren't an exact match across documents and questions. Bge was the more logical choice despite its significantly longer run time (2.3 minutes) because it can match when different words with the same meaning may be used in questions and rules. I had claude run a quick comparison between the two on practice queries to see if bge would be the best choice and that data supported my decision. Paraphrase is where it really excels with bge scoring an MRR@10 of 0.714 and potion scoring only 0.300. By not using potion, I gave up a much higher score on identifier queries, with potion scoring 0.571 and bge getting only 0.333. Ultimately the paired interval for the difference between them includes zero, so the sample data doesnt definatively prove that bge is the better choice. However, I picked it because of the paraphrase class, which 'bm25' cannot handle.

--- 

## 3. Where you overruled the agent

One time Claude suggested, wrote or claimed something and you did not take it.
It might be a relevance judgment you disagreed with, a retriever it called finished when a run file showed otherwise, a number it summarized wrongly, or a license it said was fine.

What did it do?
How did you notice?
What did you do instead?

If it genuinely never happened, say so plainly, and then say what you would have had to check in order to notice.
Being honest here costs you far less than a story you cannot defend when you record your video.

When I built rerank, I decided to set passage_chars to 600 initially to reduce the amount of input. However, claude made the suggestion to increase this value to 1500, since the sections are a lot longer than the lab's articles. This would significantly increase the amount of tokens a run would use and on test data did not reduce the quality at all. This cannot be ensured without doing it on the full test set, but seemed like a valid risk to take. I noticed this while reading through its proposed plan and did not agree with the reasoning. Overruling this reduced computation and input tokens without losing too much quality. Later in the project I realized that 1500 words would actually worked significantly better for my own corpus so ended up going with claude's originally suggested answer.

---

## 4. A number you do not trust

Pick one number in `EVAL.md` that you do not fully trust, and say why.
It could be a mean over a small query class, a difference whose interval includes zero, a verified share of 100%, a score on a gold set you wrote yourself, or a result you got only once.

What would have to be true for you to trust it?
Did you do anything to test it, and what did that show?


One number I dont trust in my EVAL.md is the rerank MMR@10 score on hand queries. This was 0.467 compared to 0.873 on claude queries. I dont trust this because my gold set only contained one document per query and some of my hand queries were pretty vauge and could have applied to multiple documents. In order to trust this value I would have to reevaluate my hand queries and write some that are more curated to do well with rerank. To test this I looked at where rerank ranked the gold document for h06, h08, and h10. It placed them at 6, 6, and 9 respectively which definetly contributed to the lower scores. In the future I would reevaluate the bias in these queries to see if the rerank score could be improved.

---

## 5. What is still wrong

One thing in your system, your corpus or your gold set that is not right, not finished, or that you do not fully understand.

What would you do next, and how would you find out whether it matters?
Name the file, the query or the document where someone could look.


My gold set could use some improvement. I only added one document for each query which definitely influenced the results. In the future I would put more time into looking for documents for the gold set and ensuring that relevant documents are included. Having more documents for each query would make sense because a lot of the documents in this dataet discuss similar topics so many documents could answer the same question. However when I wrote some of the questions I had specific documents in mind for the gold set but then discovered that other documents also fit the same query.