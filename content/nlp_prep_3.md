Title: Preparing for an NLP interview - Day 3 and 4
Date: 2025-10-31 11:14
Category: Programming
Status: published

Another day has come. This one will be somewhat disjointed, I have an ~1.5 hrs in the morning and maybe some later in the evening.

Yesterday I remembered I watched [this](https://www.youtube.com/watch?v=FkHAYG8vASQ) youtube interview with a NLP data scientist and he listed the important stuff you kinda gotta know. I saved that list, had ChatGPT kind of expand on that. I think I'll try to spend the afternoon where I'm not by my computer having it tutor me on the different subjects.

Otherwise we have stuff to pick up from yesterday. But before that I thought maybe its a good opportunity to delve a bit deeper to tokenization. I've watched (and possibly implemented myself) the BPE tokenizer following Karpathy's lecture about a year ago, but it is known forgotten. Let's give a shot to the WordPiece tokenizer instead.

----

So yesterday I didn't have the opportunity to continue, so this is already day 4. I did get to do learn some more thru conversations with Claude and Gemini. We talked about perplexity, word2vec, and Sentence-BERT.

**Perplexity**: (per token) a measure of the uncertainty of the language model in predicting the next token. One interpretation for the value that it is as if the model has $PP$ options to choose from which are equally likely. Ie the perplexity for a uniformly random LM would be equal to $|V|$ There are two definitions:

- Vanilla: $PP=\sqrt[n]{1/P(w_1\dots w_n)}=\sqrt[n]{\prod_i 1/P(w_i|w_1\dots w_{i-1})}$
- Information Theoretic: $PP=2^{H(p_{real},p)}$
Since cross-entropy is used as loss on the dataset we can derive the perplexity from the loss. I wish I could say more but I've done Information Theory so long again I don't want to hand wave stuff.

**word2vec**: These are data-driven ways to generate decent embeddings for words. Not sure how much it is used today when there's embeddings from BERT etc, but the general notion is to train a simple linear embedding model that tries to predict a words context (surrounding words) from it or vice-versa.

Another method is GLoVe which factors the co-occurence matrix ($W_{ij} - how many times the word $i$ occurs in the context of $j$) to a multiplication of two lower rank matrices.

I'll get to sentence-bert perhaps tomorrow, maybe we'll try and implement it. For the rest of the day today, I'm gonna try to do [CS 224N Final Project](https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1234/project/default-final-project-bert-handout.pdf) which is to implement and train a kind of minBERT.

## Implementing minBERT

The first step is implementing the attention layer. The input is as follows:

- key - a tensor of all the keys along the batch, dim is (bs, num_attention_heads, seq_len, attention_head_size)
- same except for queries
- value - same except for values
- attention_mask - to exclude the padding tokens from the attention normalization

The first step is to calculate the score matrix
$$S=\frac{QK^T}{\sqrt{d_k}}$$
This is for the regular attention head, but now we have multihead attention with a batch, so this is a bit trickier. Let's figure it out mathematically

$$S_{b, i, j, k} = \sum_{h}\frac{Q_{bijh}K_{bikh}}{\sqrt{d_k}}$$

The easiest way for me is to just use einsum which exactly captures that
`S = torch.einsum("b i j h, b i k h -> b i j k", key, query)`

Now we need to mask the padded tokens. Basically if in batch `b` token `p` is padded then
`S[b,i,j,p]=S[b,i,p,j]=-inf`

We receive an attention mask of shape (bs, 1, 1, seq_len). Now, we  do 
`mask = mask & mask.transpose(2, 3)`
so we get a shape of (bs, 1, seq_len, seq_len) and now the mask is false if any of the last two indices belongs to a padded token. We then negate the mask and fill `-inf` where it's true and run softmax on the last dim. Finally to compute the weighted sum of values, we reuse einsum for clarity and get
`torch.einsum("b i j k, b i j h -> b i j h", P, v)`

Now for the BertLayer implementation. They ask us to implement to methods, `add_norm` and `forward`. Now there are some kind of silly subtleties about what is applied in what order, the dropout, the layer norm, the residual connection. The way they implemented it in the code is a little strange, but let's see if I got it right.

Fine. So we got to implement self-attention ourselves, fumbled around with the encoder block, now I'm finetuning on Stanford Sentiment Treebank dataset by taking the \[CLS\] token embedding and training a classifier on its embedding. What's next?

## What now?
I'm trying to decide where to go from here. Obviously there's an infinite amount of things to learn, but I'm trying to decide where to put my time. I found [this](https://trite-song-d6a.notion.site/Ace-your-NLP-Interview-1630af77bef380849679f1345339066d) question list and some stuff I should probably read on are

- BLEU/ROUGE metrics
- TF-IDF? dunno if its worth the time though
- Positional embeddings: learned, Sinusoidal, Relative, [RoPE](https://www.youtube.com/watch?v=Mn_9W1nCFLo)?
- Tokenizers - review, start with BPE
- [LDA](https://towardsdatascience.com/light-on-math-machine-learning-intuitive-guide-to-latent-dirichlet-allocation-437c81220158/)

In general it feels like most things are familiar but a bit hazy.

Okay, I have two more days. I think tomorrow I will speed run the NLP with transformers book, try to implement a couple of tasks. And also I'll review some of these things.